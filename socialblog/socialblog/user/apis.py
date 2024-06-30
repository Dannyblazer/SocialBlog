#import email
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.mixins import ApiAuthMixin

from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from user.models import BaseUser
from user.selectors import user_list
from user.services import user_create, user_update



class UserCreateApi(APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        username = serializers.CharField()
        password = serializers.CharField(write_only=True)

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        email = serializers.EmailField()
        username = serializers.CharField()
        is_admin = serializers.BooleanField()

    def post(self, request):
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)
        user = user_create(
                email=input_serializer.validated_data['email'],
                username=input_serializer.validated_data['username'],
                password=input_serializer.validated_data['password']
            )
        output_serializer = self.OutputSerializer(user)

        return Response(status=status.HTTP_201_CREATED)



class UserUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        email = serializers.EmailField()
        username = serializers.CharField()

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        email = serializers.EmailField()
        username = serializers.CharField()

    def patch(self, request):
        # Get authentication fixed
        user = request.user
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        new_user = user_update(user=user, data=input_serializer.validated_data)
        output_serializer = self.OutputSerializer(new_user)
        return Response({"detail" : output_serializer.data}, status=status.HTTP_200_OK) 



class UserListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 3

    class FilterSerializer(serializers.Serializer):
        id = serializers.IntegerField(required=False)
        is_admin = serializers.BooleanField(required=False, allow_null=True, default=None)
        email = serializers.EmailField(required=False)
        username = serializers.CharField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = BaseUser
            fields = ("id", "email", "username", "is_admin")

    def get(self, request):
        # Make sure the filters are valid, if passed
        filters_serializer = self.FilterSerializer(data=request.query_params)
        filters_serializer.is_valid(raise_exception=True)

        users = user_list(filters=filters_serializer.validated_data)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=users,
            request=request,
            view=self,
        )
