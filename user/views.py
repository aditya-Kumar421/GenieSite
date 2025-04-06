from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSignupSerializer, UserLoginSerializer, UserDetailsSerializer
from .models import UserManager
import jwt
from datetime import datetime, timedelta
from django.conf import settings
import bcrypt

class SignupView(APIView):
    def post(self, request):
        serializer = UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            user_manager = UserManager()
            user_id = user_manager.create_user(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                password=serializer.validated_data['password']
            )
            
            # Generate JWT token
            payload = {
                'user_id': user_id,
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            
            return Response({
                'token': token,
                'user_id': user_id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            user_manager = UserManager()
            user = user_manager.find_user_by_email(serializer.validated_data['email'])
            
            if not user:
                return Response({'error': 'Invalid credentials'}, 
                              status=status.HTTP_401_UNAUTHORIZED)
            
            # Verify password
            if not bcrypt.checkpw(
                serializer.validated_data['password'].encode('utf-8'),
                user['password']
            ):
                return Response({'error': 'Invalid credentials'}, 
                              status=status.HTTP_401_UNAUTHORIZED)
            
            # Generate JWT token
            payload = {
                'user_id': str(user['_id']),
                'exp': datetime.utcnow() + timedelta(days=1),
                'iat': datetime.utcnow()
            }
            token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
            
            return Response({
                'token': token,
                'user_id': str(user['_id'])
            })
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailsView(APIView):
    def get(self, request):
        user_manager = UserManager()
        user = user_manager.find_user_by_id(request.user)  # request.user is user_id from JWT
        
        if not user:
            return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)
        
        serializer = UserDetailsSerializer({
            'username': user['username'],
            'email': user['email']
        })
        return Response(serializer.data)