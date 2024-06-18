from pyexpat import model
from tokenize import Comment
from django.conf import settings
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from rest_framework import serializers, status
from rest_framework.response import Response

from api.mixins import ApiAuthMixin
from user.models import BaseUser
from .selectors import blog_list, blog_get
from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from .models import Blog
from .services import blog_create, blog_update, comment_create



class BlogCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        
        title = serializers.CharField(max_length=255)
        body = serializers.CharField()
        
    def post(self, request):
        user = request.user
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        blog_create(
                author=user,
                title=input_serializer.validated_data['title'],
                body=input_serializer.validated_data['body']
                )

        return Response(status=status.HTTP_201_CREATED)



class BlogUpdateApi(ApiAuthMixin, APIView):

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=50)
        body = serializers.CharField()
        like = serializers.IntegerField(required=False, allow_null=True)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Blog
            fields = ("id", "author", "title", "body", "like")
    
    def patch(self, request, blog_id):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        blog = blog_get(blog_id)

        if request.user == blog.author:
            
            new_blog, update_status = blog_update(blog=blog, data=input_serializer.validated_data)
            output = self.OutputSerializer(new_blog)
            # Remove the update response later
            return Response({"update_status": update_status, "data": output.data}, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class BlogListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 3

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        author = serializers.SlugRelatedField(
            slug_field='author',
            queryset=BaseUser.objects.all(),
            required=False
        )
        title = serializers.CharField(max_length=100, required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Blog
            fields = "__all__"

    def get(self, request):
        input_serializer = self.InputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        blogs = blog_list(filters=input_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=blogs,
            request=request,
            view=self,
        )



class CommentCreateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        body = serializers.CharField()

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Comment
            fields = "__all__"

    def post(self, request, blog_id):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        
        blog = blog_get(blog_id)
        comment_create(owner=request.user, post=blog, body=input_serializer.validated_data['body'])

        return Response(status=status.HTTP_201_CREATED)
    