from django.urls import path

from .apis import (UserListApi, UserCreateApi, UserUpdateApi, UserFollowApi,
                   UserUnFollowApi, UserFollowerListApi, UserFollowingListApi,
                   UserFollowRequestListApi, UserRequestAcceptApi, UserRequestDeclineApi,
                   ProfileViewApi, ProfileUpdateApi)

urlpatterns = [
        path("register", UserCreateApi.as_view(), name="create"), #-----> Done
        path("update", UserUpdateApi.as_view(), name="update"), # ----> Done
        path("list", UserListApi.as_view(), name="list"), # ----> Done
        path("request/accept/<int:request_id>", UserRequestAcceptApi.as_view(), name="accept-request"),  # ----> Done
        path("request/decline/<int:request_id>", UserRequestDeclineApi.as_view(), name="decline-request"), # ----> Done
        path("follow/<int:user_id>", UserFollowApi.as_view(), name="follow"), # ----> Done
        path("unfollow/<int:user_id>", UserUnFollowApi.as_view(), name="unfollow"),
        path("followers", UserFollowerListApi.as_view(), name="followers"), # ----> Done
        path("following/<int:user_id>", UserFollowingListApi.as_view(), name="following"),
        path("profile/<int:user_id>", ProfileViewApi.as_view(), name="profile"), # ----> Done
        path("profile_update/<int:user_id>", ProfileUpdateApi.as_view(), name="profile-update"),
        path("requests", UserFollowRequestListApi.as_view(), name="requests"), # ----> Done
            ]
