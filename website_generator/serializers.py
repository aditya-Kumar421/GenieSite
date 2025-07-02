from rest_framework import serializers
from .models import GeneratedPage

class GeneratePageSerializer(serializers.ModelSerializer):
    industry = serializers.CharField(required=True)

    class Meta:
        model = GeneratedPage
        fields = ['industry']

class PageSerializer(serializers.ModelSerializer):
    class Meta:
        model = GeneratedPage
        fields = ['id', 'industry', 'html_content', 'preview_url', 'created_at', 'updated_at']

class EditPageSerializer(serializers.ModelSerializer):
    html_content = serializers.CharField(required=True)

    class Meta:
        model = GeneratedPage
        fields = ['html_content']