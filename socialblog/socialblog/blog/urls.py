from django.urls import path
from .apis import (
            BlogCreateApi, BlogUpdateApi, BlogListApi,
            BlogDeleteApi, CommentCreateApi, CommentListApi, BlogLikeApi)


urlpatterns = [
    path("", BlogListApi.as_view(), name="create-list"),
    path("comment/<int:blog_id>", CommentCreateApi.as_view(), name="comment"),
    path("comment/list/<int:blog_id>", CommentListApi.as_view(), name="comment-list"),
    path("create", BlogCreateApi.as_view(), name="create-blog"),
    path("delete/<int:blog_id>", BlogDeleteApi.as_view(), name="delete-blog"),
    path("like/<int:blog_id>", BlogLikeApi.as_view(), name="like-blog"),
    path("update/<int:blog_id>", BlogUpdateApi.as_view(), name="update-blog"),
]
