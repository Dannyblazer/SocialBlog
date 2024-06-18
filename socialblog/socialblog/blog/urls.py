from django.urls import path
from .apis import BlogCreateApi, BlogUpdateApi, BlogListApi


urlpatterns = [
    path("", BlogListApi.as_view(), name="create-list"),
    path("create", BlogCreateApi.as_view(), name="create-blog"),
    path("update/<int:blog_id>", BlogUpdateApi.as_view(), name="update-blog"),
]
