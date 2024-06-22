from django.urls import path
from .apis import (
            BlogCreateApi, BlogUpdateApi, BlogListApi, CommentDeleteApi,
            BlogDeleteApi, CommentCreateApi, CommentListApi, BlogLikeApi)


urlpatterns = [
    path("", BlogListApi.as_view(), name="create-list"),
    path("comment/<int:blog_id>", CommentCreateApi.as_view(), name="comment-create"),
    path("comment/list/<int:blog_id>", CommentListApi.as_view(), name="comment-list"),
    path("comment/delete/<int:comment_id>", CommentDeleteApi.as_view(), name="delete-comment"),
    path("create", BlogCreateApi.as_view(), name="create-blog"),
    path("delete/<int:blog_id>", BlogDeleteApi.as_view(), name="delete-blog"),
    path("like/<int:blog_id>", BlogLikeApi.as_view(), name="like-blog"),
    path("<int:blog_id>", BlogUpdateApi.as_view(), name="update-blog"),
]
