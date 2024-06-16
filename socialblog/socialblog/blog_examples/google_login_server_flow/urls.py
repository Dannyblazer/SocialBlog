from django.urls import include, path

login_urlpatterns = [
    path(
        "raw/",
        include(("blog_examples.google_login_server_flow.raw.urls", "login-raw")),
    ),
    path(
        "sdk/",
        include(("blog_examples.google_login_server_flow.sdk.urls", "login-sdk")),
    ),
]

urlpatterns = [
    path("login/", include(login_urlpatterns)),
]
