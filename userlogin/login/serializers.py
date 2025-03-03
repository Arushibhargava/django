from django.contrib.auth.models import User
from rest_framework import serializers

class RegisterSerializer(serializers.Serializer):
    username=serializers.CharField()
    email=serializers.EmailField()
    password=serializers.CharField()
    
    def validate(self,data):
        if data['username']:
            if User.objects.filter(username=data['username']).exists():
                raise serializers.ValidationError('username already exist') 
            
        if data['email']:
            if User.objects.filter(email=data['email']).exists():
                raise serializers.ValidationError('email already exist')
                
        return data  
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']