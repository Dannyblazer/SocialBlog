from django.conf import settings
from rest_framework.views import APIView
from rest_framework import serializers, status
from rest_framework.response import Response

from .models import Blog
from .services import blog_create, blog_update



class BlogCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        author = serializers.SlugRelatedField(
            slug_field='email',
            queryset=settings.AUTH_USER_MODEL.objects.all()
        )
        title = serializers.CharField(max_length=50)
        body = serializers.CharField()
        like = serializers.IntegerField(required=False, allow_null=True)

        def create(self, validated_data):
            return Blog.objects.create(**validated_data)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        author = serializers.CharField(source='author.email')
        title = serializers.CharField()
        body = serializers.CharField()
        like = serializers.IntegerField(required=False, allow_null=True)

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        blog = input_serializer.save()

        output_serializer = self.OutputSerializer(blog)
        return Response(output_serializer.data, status=status.HTTP_201_CREATED)


