from django.urls import path

from .apis import (UserListApi, UserCreateApi, UserUpdateApi, UserFollowApi,
                   UserUnFollowApi, UserFollowerListApi, UserFollowingListApi,
                   UserFollowRequestListApi, UserRequestAcceptApi, UserRequestDeclineApi,
                   ProfileViewApi, ProfileUpdateApi)

urlpatterns = [
        path("", UserCreateApi.as_view(), name="create"),
        path("accept/<int:request_id>", UserRequestAcceptApi.as_view(), name="accept-request"),
        path("decline/<int:request_id>", UserRequestDeclineApi.as_view(), name="decline-request"),
        path("follow/<int:user_id>", UserFollowApi.as_view(), name="follow"),
        path("followers", UserFollowerListApi.as_view(), name="followers"),
        path("following/<int:user_id>", UserFollowingListApi.as_view(), name="following"),
        path("list", UserListApi.as_view(), name="list"),
        path("profile/<int:user_id>", ProfileViewApi.as_view(), name="profile"),
        path("profile_update/<int:user_id>", ProfileUpdateApi.as_view(), name="profile-update"),
        path("requests", UserFollowRequestListApi.as_view(), name="requests"),
        path("unfollow/<int:user_id>", UserUnFollowApi.as_view(), name="unfollow"),
        path("update", UserUpdateApi.as_view(), name="update"),
        
            ]
