#import email
from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from django.http import Http404
from api.mixins import ApiAuthMixin

from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from user.models import BaseUser, Follow, Profile
from user.selectors import (user_list, user_get, get_followers,
                            get_following, follow_user, unfollow_user,
                            get_pending_follow_requests, accept_follow_request, decline_follow_request)
from user.services import user_create, user_update, profile_update


class CustomObtainTokenPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        try:
            # Call the parent class to get the token response
            response = super().post(request, *args, **kwargs)

            # Extract tokens
            tokens = response.data
            access_token = tokens.get('access')
            refresh_token = tokens.get('refresh')

            if not access_token or not refresh_token:
                raise ValueError("Tokens not generated.")

            # Create a new response
            res = Response(
                {'login_status': True},
                status=response.status_code
            )

            # Set cookies for tokens
            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite='Strict'
            )
            res.set_cookie(
                key='refresh_token',
                value=refresh_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite='Strict'
            )

            return res

        except Exception as e:
            # Return error response
            return Response({"error": str(e)}, status=400)

class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get('refresh_token')

            request.data['refresh'] = refresh_token
            response = super().post(request, *args, **kwargs)

            tokens = response.data

            access_token = tokens.get('access')

            res = Response()

            res.data = {
                'refreshed': True,
                'access': access_token
            }

            res.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
                secure=False,  # Set to True in production with HTTPS
                samesite='Strict'
            )

            return res
  
        except Exception as e:
            # Return error response
            return Response(
                {
                    "error": str(e),
                    "refreshed": False
                }, 
                status=400)

class UserLogoutApi(APIView):
    def post(self, request):
        try:
            res = Response()
            res.delete_cookie('access_token')
            res.delete_cookie('refresh_token')
            res.data = {
                'logout_status': True
            }
            return res
        except Exception as e:
            return Response(
                {
                    "error": str(e),
                    "logout_status": False
                }, 
                status=400)

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

        return Response(
            {
                "created" : True,
                "message" : "Account created successfully"
            },
            status=status.HTTP_201_CREATED
            )

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
        return Response({"data" : output_serializer.data}, status=status.HTTP_200_OK) 

class UserListApi(ApiAuthMixin, APIView):
    class Pagination(LimitOffsetPagination):
        default_limit = 10

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

class ProfileViewApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ("id", "user", "image", "bio", "location", "birth_date")
            
        # modified representation to hide "birth_date" field from other users besides profile owner
        def to_representation(self, instance):
            representation = super().to_representation(instance)
            request = self.context.get('request', None)
            
            if request and request.user != instance.user:
                representation.pop('birth_date', None)
            
            return representation
        
    def get(self, request, user_id):
        user = user_get(user_id)
        profile = Profile.objects.get(user=user)

        output_serializer = self.OutputSerializer(profile, context={'request': request})

        return Response({"data":output_serializer.data}, status=status.HTTP_200_OK)

class ProfileUpdateApi(ApiAuthMixin, APIView):
    class InputSerializer(serializers.Serializer):
        image = serializers.ImageField(required=False)
        bio = serializers.CharField(required=False)
        location = serializers.CharField(required=False)
        birth_date = serializers.DateField(required=False)

    class OutputSerializer(serializers.ModelSerializer):
        class Meta:
            model = Profile
            fields = ("id", "user", "image", "bio", "location", "birth_date")
    
    def patch(self, request, user_id):
        user = user_get(user_id)
        
        if user != request.user:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        
        input_serializer = self.InputSerializer(data=request.data)
        input_serializer.is_valid(raise_exception=True)

        profile = Profile.objects.get(user=user)
        new_profile = profile_update(profile=profile, data=input_serializer.validated_data)
        output_serializer = self.OutputSerializer(new_profile)

        return Response({"data": output_serializer.data}, status=status.HTTP_200_OK)
     
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
        try:
            # Call the utility function to accept the follow request
            user = request.user
            request_status = accept_follow_request(user, request_id)
            if request_status:
                return Response(
                    {
                        "accept_status": True,
                        "message": "Request accepted successfully",
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    {
                        "accept_status": False,
                        "message": "Request already accepted",
                    },
                    status=status.HTTP_409_CONFLICT,
                )
        
        except Http404:
            return Response(
                {
                    "accept_status": False,
                    "message": "Request not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

class UserRequestDeclineApi(ApiAuthMixin, APIView):
    def post(self, request, request_id):
        try:
            # Call the utility function to decline the follow request
            user = request.user
            decline_follow_request(user, request_id)
            return Response(
                {
                    "decline_status": True,
                    "message": "Request declined successfully",
                },
                status=status.HTTP_202_ACCEPTED,
            )
        except Http404:
            return Response(
                {
                    "decline_status": False,
                    "message": "Request not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    

