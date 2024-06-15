from django.urls import include, path

urlpatterns = [
    path("auth/", include(("authentication.urls", "authentication"))),
    path("users/", include(("user.urls", "users"))),
    path("errors/", include(("errors.urls", "errors"))),
    path("files/", include(("files.urls", "files"))),
    path(
        "google-oauth2/", include(("blog_examples.google_login_server_flow.urls", "google-oauth2"))
    ),
]
