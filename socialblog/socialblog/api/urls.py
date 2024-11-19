from django.urls import include, path

from user.apis import (
    CustomObtainTokenPairView, 
    CustomTokenRefreshView, 
    UserLogoutApi
                       )

from .utils import AllEndpointsApi


urlpatterns = [
    # authentication urls
    path('account/login/', CustomObtainTokenPairView.as_view(), name='token_obtain_pair'), #----> Done
    path('token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'), #----> Done
    path('user/logout/', UserLogoutApi.as_view(), name='auth_logout'), #----> Done

    # app urls
    path("blogs/", include(("blog.urls", "blogs"))), #----> Done
    path("chat/", include(("chat.urls", "chats"))),
    path("users/", include(("user.urls", "users"))), #----> Done
    path("errors/", include(("errors.urls", "errors"))),
    path("files/", include(("files.urls", "files"))),

    # utils(accessible only by superuser) ---> see all endpoints
    path("endpoints/", AllEndpointsApi.as_view(), name="all-endpoints"),
    
]
"""path(
        "google-oauth2/", include(("blog_examples.google_login_server_flow.urls", "google-oauth2"))
    ),"""