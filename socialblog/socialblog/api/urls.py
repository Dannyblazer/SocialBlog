from django.urls import include, path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("blogs/", include(("blog.urls", "blogs"))),
    path("chat/", include(("chat.urls", "chats"))),
    path("users/", include(("user.urls", "users"))),
    path("errors/", include(("errors.urls", "errors"))),
    path("files/", include(("files.urls", "files"))),
    
]
"""path(
        "google-oauth2/", include(("blog_examples.google_login_server_flow.urls", "google-oauth2"))
    ),"""