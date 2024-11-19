
from tokenize import Comment
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response
from django.db.models import Count
from django.http import Http404

from api.mixins import ApiAuthMixin
from user.models import BaseUser
from .selectors import blog_list, blog_get, comment_list, comment_get
from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from .models import Blog
from .services import blog_create, blog_update, comment_create, blog_like, blog_delete, comment_delete



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

        return Response({"created" : True},status=status.HTTP_201_CREATED)



class BlogUpdateApi(ApiAuthMixin, APIView):

    class InputSerializer(serializers.Serializer):
        title = serializers.CharField(max_length=50)
        body = serializers.CharField()   

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Blog
            fields = ("id", "author", "title", "body")
    
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
            queryset=BaseUser.objects.all()
        )
        title = serializers.CharField()
        body = serializers.CharField()
        likes = serializers.IntegerField(source='likes_count')
        comments = serializers.IntegerField(source='comments_count')
        created_at = serializers.DateTimeField()
        updated_at = serializers.DateTimeField()

    def get(self, request):
        input_serializer = self.InputSerializer(data=request.query_params)
        input_serializer.is_valid(raise_exception=True)

        blogs = blog_list(filters=input_serializer.validated_data).annotate(likes_count=Count('likes__users'), comments_count=Count('comments'))

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=blogs,
            request=request,
            view=self,
        )



class BlogDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, blog_id):
        blog = blog_get(blog_id)
        if request.user == blog.author:
            blog_delete(blog)
            return Response(
                {
                    "delete_status" : True,
                    "message" : "Blog deleted successfully"
                },
                status=status.HTTP_204_NO_CONTENT)

        return Response(
            {
                "delete_status" : False,
                "message" : "You are not authorized to delete this blog, You can only delete your own blogs"
            },
            status=status.HTTP_401_UNAUTHORIZED)



class BlogLikeApi(ApiAuthMixin, APIView):
    def post(self, request, blog_id):
        blog = blog_get(blog_id)
        user = request.user
        likeable = blog_like(user, blog)
        if likeable:
            return Response(
                {
                    "liked" : True,
                    "message" : "Blog liked successfully"
                },
                status=status.HTTP_200_OK
                )

        return Response(
            {
                "liked" : False,
                "message" : "You have already liked this blog"
            },
            status=status.HTTP_400_BAD_REQUEST
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

        return Response(
            {
                "created" : True,
                "message" : "Comment created successfully"
            },
            status=status.HTTP_201_CREATED
            )
    


class CommentListApi(APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
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



class CommentDeleteApi(ApiAuthMixin, APIView):
    def delete(self, request, comment_id):
        try:
            comment = comment_get(comment_id)
            if request.user == comment.owner:
                comment_delete(comment)
                return Response(
                    {
                        "delete_status" : True,
                        "message" : "Comment deleted successfully"
                    },
                    status=status.HTTP_204_NO_CONTENT
                    )
            return Response(
                {
                    "delete_status" : False,
                    "message" : "You are not authorized to delete this comment, You can only delete your own comments"
                },
                status=status.HTTP_401_UNAUTHORIZED
                )

        except Http404:
            return Response(
                {
                    "delete_status" : False,
                    "message" : "Comment not found"
                },
                status=status.HTTP_404_NOT_FOUND
                )