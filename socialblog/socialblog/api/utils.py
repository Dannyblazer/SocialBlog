from rest_framework import serializers
from rest_framework.response import Response
from rest_framework.views import APIView

def create_serializer_class(name, fields):
    return type(name, (serializers.Serializer,), fields)


def inline_serializer(*, fields, data=None, **kwargs):
    # Important note if you are using `drf-spectacular`
    # Please refer to the following issue:
    # https://github.com/HackSoftware/Django-Styleguide/issues/105#issuecomment-1669468898
    # Since you might need to use unique names (uuids) for each inline serializer
    serializer_class = create_serializer_class(name="inline_serializer", fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)

class AllEndpointsApi(APIView):
    def get(self, request):
        data = {
            # authentication endpoints
            "register": "api/users/register",
            "login": "api/account/login",
            "logout": "api/user/logout/",
            "token-refresh": "api/token/refresh/",

            # user endpoints
            "users_list": "api/users/list",
            "user_update": "api/users/update",
            "user_profile": "api/users/profile/<int:user_id>/",
            "profile_update": "api/users/profile_update/<int:user_id>/",
            "follow_user": "api/users/follow/<int:user_id>/",
            "unfollow_user": "api/users/unfollow/<int:user_id>/",
            "user_followers_requests": "api/users/requests",
            "user_followers": "api/users/followers", #it needs query params eg. "?username=username"
            "accept_request": "api/users/request/accept/<int:request_id>/",
            "decline_request": "api/users/request/decline/<int:request_id>/",
            "following_users": "api/users/following/<int:user_id>/",

            # blog endpoints
            "blogs": "/api/blogs/",
            "blog-create": "/api/blogs/create/",
            "blog-update": "/api/blogs/update/<int:blog_id>/",
            "blog-delete": "/api/blogs/delete/<int:blog_id>/",
            "like-blog": "/api/blogs/like/<int:blog_id>/",
            "comment-list": "/api/blogs/comments/list/<int:blog_id>/",
            "comment-blog": "/api/blogs/comment/<int:blog_id>/",
            "comment-delete": "api/blogs/comment/delete/<int:comment_id>/",
            
        }

        return Response(data)
