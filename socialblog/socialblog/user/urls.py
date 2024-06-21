from django.urls import path

from .apis import UserListApi, UserCreateApi, UserUpdateApi

urlpatterns = [
        path("", UserCreateApi.as_view(), name="create"),
        path("list", UserListApi.as_view(), name="list"),
        path("update", UserUpdateApi.as_view(), name="update"),
        
            ]
