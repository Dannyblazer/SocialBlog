
from tokenize import Comment
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response

from api.mixins import ApiAuthMixin
from user.models import BaseUser
from .selectors import blog_list, blog_get, comment_list
from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from .models import Blog
from .services import blog_create, blog_update, comment_create, blog_like, blog_delete



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
            
            new_blog = blog_update(blog=blog, data=input_serializer.validated_data)
            output = self.OutputSerializer(new_blog)
            # Remove the update response later
            return Response({"data": output.data}, status=status.HTTP_202_ACCEPTED)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class BlogListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 3

    class InputSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        author = serializers.SlugRelatedField(
            slug_field='email',
            queryset=BaseUser.objects.all(),
            required=False
        )
        title = serializers.CharField(max_length=100, required=False)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        author = serializers.SlugRelatedField(
            slug_field='email',
            queryset = BaseUser.objects.all()
        )
        title = serializers.CharField()
        body = serializers.CharField()
        like = serializers.IntegerField()
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()


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


class BlogDeleteApi(ApiAuthMixin, APIView):
    def post(self, request, blog_id):
        blog = blog_get(blog_id)
        if request.user == blog.author:
            blog_delete(blog)
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_401_UNAUTHORIZED)



class BlogLikeApi(ApiAuthMixin, APIView):
    def post(self, request, blog_id):
        blog = blog_get(blog_id)
        user = request.user
        likeable = blog_like(user, blog)
        if likeable:
            return Response(status=status.HTTP_200_OK)
        return Response(status=status.HTTP_400_BAD_REQUEST)


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
    

class CommentListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 3

    class OutputSerializer(serializers.Serializer):
        owner = serializers.SlugRelatedField(
            slug_field='email',
            queryset=BaseUser.objects.all()
            )
        body = serializers.CharField()
        created_at = serializers.DateTimeField()
        
    def get(self, request, blog_id):
        comments = comment_list(blog_id)
        
        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=comments,
            request=request,
            view=self,
        )


