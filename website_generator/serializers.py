# website_generator/serializers.py
from rest_framework import serializers

class WebsiteGenerationSerializer(serializers.Serializer):
    business_type = serializers.CharField(max_length=100)
    industry = serializers.CharField(max_length=100)

class WebsiteSerializer(serializers.Serializer):
    id = serializers.CharField(source='_id', read_only=True)
    user_id = serializers.CharField(read_only=True)
    business_type = serializers.CharField(max_length=100)
    industry = serializers.CharField(max_length=100)
    structure = serializers.DictField()
    preview = serializers.SerializerMethodField()

    def get_preview(self, obj):
        if obj.get('preview', {}).get('url_token'):
            return {
                'url_token': obj['preview']['url_token'],
                'expires_at': obj['preview']['expires_at']
            }
        return None

class WebsiteUpdateSerializer(serializers.Serializer):
    structure = serializers.DictField()