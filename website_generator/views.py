from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from .models import GeneratedPage
from .serializers import GeneratePageSerializer, PageSerializer, EditPageSerializer
from .utils import generate_page_content, create_html_page
from django.http import HttpResponse

class GeneratePageView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = GeneratePageSerializer(data=request.data)
        if serializer.is_valid():
            industry = serializer.validated_data['industry']
            try:
                content = generate_page_content(industry)
                html_content = create_html_page(content)
                page = GeneratedPage.objects.create(
                    user=request.user,
                    industry=industry,
                    html_content=html_content
                )
                return Response({
                    'message': 'Page generated successfully',
                    'page': PageSerializer(page).data
                }, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PreviewPageView(APIView):
    def get(self, request, preview_url):
        page = get_object_or_404(GeneratedPage, preview_url=preview_url)
        return HttpResponse(page.html_content, content_type='text/html')

class EditPageView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, preview_url):
        page = get_object_or_404(GeneratedPage, preview_url=preview_url, user=request.user)
        serializer = EditPageSerializer(page, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Page updated successfully',
                'page': PageSerializer(page).data
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ListPagesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        pages = GeneratedPage.objects.filter(user=request.user)
        serializer = PageSerializer(pages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)