# website_generator/views.py
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WebsiteManager
from .serializers import WebsiteGenerationSerializer, WebsiteSerializer, WebsiteUpdateSerializer
import requests
from django.http import HttpResponse
from django.conf import settings
from django.core.cache import cache
import json
from datetime import datetime, timedelta
from bleach import clean

class WebsiteGenerationView(APIView):
    throttle_scope = 'website_generation'

    def post(self, request):
        serializer = WebsiteGenerationSerializer(data=request.data)
        if serializer.is_valid():
            business_type = clean(serializer.validated_data['business_type'])
            industry = clean(serializer.validated_data['industry'])
            
            prompt = f"""
            Generate a basic website structure with content for a {business_type} in the {industry} industry.
            Return the response in JSON format with sections: home, about, services, contact.
            Each section should have a title and content.
            """
            
            headers = {
                "Authorization": f"Bearer {settings.OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            }
            
            payload = {
                "model": "mistralai/mistral-7b-instruct:free",
                "messages": [{"role": "user", "content": prompt}]
            }
            
            try:
                response = requests.post(
                    "https://openrouter.ai/api/v1/chat/completions",
                    headers=headers,
                    json=payload,
                    timeout=30
                )
                response.raise_for_status()
                ai_response = response.json()
                structure = json.loads(ai_response['choices'][0]['message']['content'])
            except requests.RequestException as e:
                return Response({'error': f'AI generation failed: {str(e)}'}, 
                              status=status.HTTP_503_SERVICE_UNAVAILABLE)
            except json.JSONDecodeError:
                return Response({'error': 'Invalid AI response format'}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            website_manager = WebsiteManager()
            website_id = website_manager.create_website(
                user_id=request.user,
                business_type=business_type,
                industry=industry,
                structure=structure
            )
            
            # Invalidate website list cache for this user
            cache.delete(f"website_list_{request.user}")
            
            return Response({
                'website_id': website_id,
                'structure': structure
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WebsiteListView(APIView):
    throttle_scope = 'website_management'

    def get(self, request):
        cache_key = f"website_list_{request.user}"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            print("data from cache")
            return Response(cached_data)
        
        print("data from database")
        website_manager = WebsiteManager()
        websites = website_manager.get_user_websites(request.user)
        serializer = WebsiteSerializer(websites, many=True)
        response_data = serializer.data
        
        # Cache for 5 minutes
        cache.set(cache_key, response_data, timeout=300)
        return Response(response_data)

class WebsiteDetailView(APIView):
    throttle_scope = 'website_management'

    def get(self, request, website_id):
        cache_key = f"website_detail_{website_id}"
        cached_data = cache.get(cache_key)
        
        if cached_data is not None:
            print("data from cache")
            return Response(cached_data)
        
        print("data from database")
        website_manager = WebsiteManager()
        website = website_manager.get_website(website_id)
        if not website or website['user_id'] != request.user:
            return Response({'error': 'Website not found or unauthorized'}, 
                          status=status.HTTP_404_NOT_FOUND)
        serializer = WebsiteSerializer(website)
        response_data = serializer.data
        
        # Cache for 5 minutes
        cache.set(cache_key, response_data, timeout=300)
        return Response(response_data)

    def put(self, request, website_id):
        website_manager = WebsiteManager()
        website = website_manager.get_website(website_id)
        if not website or website['user_id'] != request.user:
            return Response({'error': 'Website not found or unauthorized'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        serializer = WebsiteUpdateSerializer(data=request.data)
        if serializer.is_valid():
            sanitized_structure = {
                key: clean(str(value)) for key, value in serializer.validated_data['structure'].items()
            }
            website_manager.update_website(website_id, {'structure': sanitized_structure})
            
            # Invalidate caches
            cache.delete(f"website_detail_{website_id}")
            cache.delete(f"website_list_{request.user}")
            
            return Response({'message': 'Website updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, website_id):
        website_manager = WebsiteManager()
        website = website_manager.get_website(website_id)
        if not website or website['user_id'] != request.user:
            return Response({'error': 'Website not found or unauthorized'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        website_manager.delete_website(website_id)
        
        # Invalidate caches
        cache.delete(f"website_detail_{website_id}")
        cache.delete(f"website_list_{request.user}")
        
        return Response({'message': 'Website deleted successfully'})

class GeneratePreviewView(APIView):
    throttle_scope = 'preview'

    def post(self, request, website_id):
        website_manager = WebsiteManager()
        website = website_manager.get_website(website_id)
        if not website or website['user_id'] != request.user:
            return Response({'error': 'Website not found or unauthorized'}, 
                          status=status.HTTP_404_NOT_FOUND)
        
        url_token = website_manager.generate_preview(website_id)
        preview_url = f"{request.scheme}://{request.get_host()}/website/preview/{url_token}/"
        
        return Response({
            'preview_url': preview_url,
            'expires_at': datetime.now() + timedelta(hours=24)
        })

class PreviewWebsiteView(APIView):
    authentication_classes = []
    permission_classes = []
    throttle_scope = 'anon'

    def get(self, request, url_token):
        cache_key = f"preview_{url_token}"
        cached_html = cache.get(cache_key)
        
        if cached_html is not None:
            print("data from cache")
            response = HttpResponse(cached_html)
            response['X-Frame-Options'] = 'DENY'
            response['Content-Security-Policy'] = "default-src 'self'"
            return response
        
        print("data from database")
        
        website_manager = WebsiteManager()
        website = website_manager.get_website_by_token(url_token)
        
        if not website:
            return HttpResponse("Preview not found or expired", status=404)
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <title>Website Preview</title>
            <meta charset="UTF-8">
            <style>
                body { font-family: Arial, sans-serif; margin: 20px; }
                section { margin-bottom: 30px; }
                h1 { color: #333; }
            </style>
        </head>
        <body>
        """
        
        for section, content in website['structure'].items():
            html_content += f"""
            <section>
                <h1>{clean(content['title'])}</h1>
                <p>{clean(content['content'])}</p>
            </section>
            """
        
        html_content += """
        </body>
        </html>
        """
        
        # Cache for 1 hour (or until preview expires, whichever is shorter)
        cache.set(cache_key, html_content, timeout=3600)
        
        response = HttpResponse(html_content)
        response['X-Frame-Options'] = 'DENY'
        response['Content-Security-Policy'] = "default-src 'self'"
        return response
