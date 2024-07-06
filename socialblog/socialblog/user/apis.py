#import email
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.mixins import ApiAuthMixin

from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from user.models import BaseUser, Follow
from user.selectors import (user_list, user_get, get_followers,
                            get_following, follow_user, unfollow_user,
                            get_pending_follow_requests, accept_follow_request, decline_follow_request)
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
        #output_serializer = self.OutputSerializer(user)

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



class UserFollowApi(ApiAuthMixin, APIView):

    def post(self, request, user_id):
        followed = user_get(user_id)
        follower = request.user

        following = follow_user(follower, followed)
        return Response(status=status.HTTP_202_ACCEPTED if following else status.HTTP_409_CONFLICT)



class UserUnFollowApi(ApiAuthMixin, APIView):

    def post(self, request, user_id):
        followed = user_get(user_id)
        follower = request.user

        following = unfollow_user(follower, followed)
        return Response(status=status.HTTP_202_ACCEPTED if following else status.HTTP_404_NOT_FOUND)



class UserFollowerListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class InputSerializer(serializers.Serializer):
        username = serializers.SlugRelatedField(
            slug_field='username',
            queryset=BaseUser.objects.all()
        )

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        follower = serializers.SlugRelatedField(
            slug_field='username',
            queryset=Follow.objects.all()
        )

    def get(self, request):
        inputserializer = self.InputSerializer(data=request.query_params)
        inputserializer.is_valid(raise_exception=True)

        followers = get_followers(user=inputserializer.validated_data['username'])

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=followers,
            request=request,
            view=self,
        )
        


class UserFollowingListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        followed = serializers.CharField()

    def get(self, request, user_id):
        user = user_get(user_id)

        followers = get_following(user=user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=followers,
            request=request,
            view=self,
        )
       


class UserFollowRequestListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 5

    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        follower = serializers.CharField()
        created_at = serializers.DateTimeField()


    def get(self, request):
        user = request.user
        follow_requests = get_pending_follow_requests(user)

        return get_paginated_response(
            pagination_class=self.Pagination,
            serializer_class=self.OutputSerializer,
            queryset=follow_requests,
            request=request,
            view=self,
        )
    

class UserRequestAcceptApi(ApiAuthMixin, APIView):
    def post(self, request, request_id):
        request_status = accept_follow_request(request_id)
        return Response(status=status.HTTP_202_ACCEPTED if request_status else status.HTTP_409_CONFLICT)

class UserRequestDeclineApi(ApiAuthMixin, APIView):
    def post(self, request, request_id):
        decline_follow_request(request_id)
        return Response(status=status.HTTP_202_ACCEPTED)
    
