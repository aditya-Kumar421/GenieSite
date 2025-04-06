from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import WebsiteManager
from .serializers import WebsiteGenerationSerializer, WebsiteSerializer, WebsiteUpdateSerializer
import requests
from django.conf import settings
import json
from decouple import config
  # Add this to your .env file
OPENROUTER_API_KEY = config('OPENROUTER_API_KEY')

class WebsiteGenerationView(APIView):
    def post(self, request):
        serializer = WebsiteGenerationSerializer(data=request.data)
        if serializer.is_valid():
            business_type = serializer.validated_data['business_type']
            industry = serializer.validated_data['industry']
            
            # Generate website structure using Mistral AI
            prompt = f"""
            Generate a basic website structure with content for a {business_type} in the {industry} industry.
            Return the response in JSON format with sections: home, about, services, contact.
            Each section should have a title and content.
            """
            
            headers = {
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
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
                    json=payload
                )
                response.raise_for_status()
                ai_response = response.json()
                structure = json.loads(ai_response['choices'][0]['message']['content'])
            except Exception as e:
                return Response({'error': f'AI generation failed: {str(e)}'}, 
                              status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
            # Save to MongoDB
            website_manager = WebsiteManager()
            website_id = website_manager.create_website(
                user_id=request.user,
                business_type=business_type,
                industry=industry,
                structure=structure
            )
            
            return Response({
                'website_id': website_id,
                'structure': structure
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class WebsiteListView(APIView):
    def get(self, request):
        website_manager = WebsiteManager()
        websites = website_manager.get_user_websites(request.user)
        serializer = WebsiteSerializer(websites, many=True)
        return Response(serializer.data)

class WebsiteDetailView(APIView):
    def get(self, request, website_id):
        website_manager = WebsiteManager()
        website = website_manager.get_website(website_id)
        if not website:
            return Response({'error': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        if website['user_id'] != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        serializer = WebsiteSerializer(website)
        return Response(serializer.data)

    def put(self, request, website_id):
        website_manager = WebsiteManager()
        website = website_manager.get_website(website_id)
        if not website:
            return Response({'error': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        if website['user_id'] != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = WebsiteUpdateSerializer(data=request.data)
        if serializer.is_valid():
            website_manager.update_website(website_id, serializer.validated_data)
            return Response({'message': 'Website updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, website_id):
        website_manager = WebsiteManager()
        website = website_manager.get_website(website_id)
        if not website:
            return Response({'error': 'Website not found'}, status=status.HTTP_404_NOT_FOUND)
        if website['user_id'] != request.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_403_FORBIDDEN)
        
        website_manager.delete_website(website_id)
        return Response({'message': 'Website deleted successfully'})