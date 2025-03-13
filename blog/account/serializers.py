from rest_framework import serializers
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
class RegisterSerializer(serializers.Serializer):
    first_name=serializers.CharField()
    last_name=serializers.CharField()
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self,data):
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('username is already taken')
        
        return data
    
    def create(self,validate_data):
        user=User.objects.create(first_name=validate_data['first_name'],last_name=validate_data['last_name'],username=validate_data['username'].lower())
        user.set_password(validate_data['password'])
        user.save()
        return user
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
    
    def validate(self,data):
        if not User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError('acoount not found')
        
        return data
    
    def get_jwt_token(self,data):
        user=authenticate(username=data['username'],password=data['password'])
        if user is None:
            return {'message': 'Invalid credentials', 'data': {}}
        
        print(data)
        refresh=RefreshToken.for_user(user)
        
        return {'message':'login success','data':{'token': {  'refresh': str(refresh), 'access': str(refresh.access_token)}}}