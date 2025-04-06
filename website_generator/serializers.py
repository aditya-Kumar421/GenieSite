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

class WebsiteUpdateSerializer(serializers.Serializer):
    structure = serializers.DictField()