from django.urls import path

from .apis import (UserListApi, UserCreateApi, UserUpdateApi, UserFollowApi,
                   UserUnFollowApi, UserFollowerListApi, UserFollowingListApi)

urlpatterns = [
        path("", UserCreateApi.as_view(), name="create"),
        path("follow/<int:user_id>", UserFollowApi.as_view(), name="follow"),
        path("followers", UserFollowerListApi.as_view(), name="followers"),
        path("following/<int:user_id>", UserFollowingListApi.as_view(), name="following"),
        path("list", UserListApi.as_view(), name="list"),
        path("unfollow/<int:user_id>", UserUnFollowApi.as_view(), name="unfollow"),
        path("update", UserUpdateApi.as_view(), name="update"),
        
            ]
