from rest_framework import serializers
from .models import UserManager

class UserSignupSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100, write_only=True)

    def validate_email(self, value):
        user_manager = UserManager()
        if user_manager.find_user_by_email(value):
            raise serializers.ValidationError("Email already exists")
        return value
    
class UserLoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(max_length=100)


class UserDetailsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    email = serializers.EmailField()