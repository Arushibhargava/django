from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import BlogSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
# Create your views here.
from django.db.models import Q
from .models import Blog
from django.core.paginator import Paginator
class PublicBlog(APIView):
    def get(self,request):
        try:
            blogs=Blog.objects.all().order_by('?')
            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains=search)| Q(blog_text__icontains=search))
           
            page_number=request.GET.get('page',1)
            pagination=Paginator(blogs,5)
            serializer=BlogSerializer(pagination.page(page_number),many=True)
            return Response({
               'data':serializer.data,
               'message':'blog fetched successfully'
           },status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'data':serializer.data,
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
    
    
class BlogView(APIView):
    permission_classes=[IsAuthenticated]
    authentication_classes=[JWTAuthentication]
    def get(self,request):
        try:
            blogs=Blog.objects.filter(user=request.user)
            
            if request.GET.get('search'):
                search=request.GET.get('search')
                blogs=blogs.filter(Q(title__icontains=search)| Q(blog_text__icontains=search))
            serializer=BlogSerializer(blogs,many=True)
            return Response({
               'data':serializer.data,
               'message':'blog fetched successfully'
           },status=status.HTTP_201_CREATED)
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
    
            
    def post(self,request):
        try:
           data=request.data
           data['user']=request.user.id
           serializer=BlogSerializer(data=data)
           if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
                
           serializer.save()
           
           
           
           return Response({
               'data':serializer.data,
               'message':'blog created successfully'
           },status=status.HTTP_201_CREATED)
       
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
            
    def patch(self,request):
        try:
            data=request.data
            blog=Blog.objects.filter(uid=data.get('uid'))
            print(data.get('uid'))
            if not blog.exists():
                return Response({
                'data':{},
                'message':'invalid uid'
            },status=status.HTTP_400_BAD_REQUEST)
                
            if request.user!=blog[0].user:
                return Response({
                'data':{},
                'message':'you are not authorized to this'
            },status=status.HTTP_400_BAD_REQUEST)
                
            serializer=BlogSerializer(blog[0],data=data,partial=True)
            if not serializer.is_valid():
                return Response({
                    'data':serializer.errors,
                    'message':'something went wrong'
                },status=status.HTTP_400_BAD_REQUEST)
                
            serializer.save()
           
           
           
            return Response({
               'data':serializer.data,
               'message':'blog updated successfully'
           },status=status.HTTP_201_CREATED)   
            
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
            
            
    def delete(self,request):
        try:
            data=request.data
            blog=Blog.objects.filter(uid=data.get('uid'))
            
            if not blog.exists():
                return Response({
                'data':{},
                'message':'invalid uid'
            },status=status.HTTP_400_BAD_REQUEST)
                
            if request.user!=blog[0].user:
                return Response({
                'data':{},
                'message':'you are not authorized to this'
            },status=status.HTTP_400_BAD_REQUEST)
              
            blog[0].delete()
            return Response({
               'data':{},
               'message':'blog deleted successfully'
           },status=status.HTTP_201_CREATED) 
            
        except Exception as e:
            print(e)
            return Response({
                'data':{},
                'message':'something went wrong'
            },status=status.HTTP_400_BAD_REQUEST)
            
    