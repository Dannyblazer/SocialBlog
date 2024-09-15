# myapp/middleware.py
from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import get_user_model

User = get_user_model()

class JWTAuthMiddleware(BaseMiddleware):
    async def __call__(self, scope, receive, send):
        # Get the token from headers (Authorization: Bearer <token>)
        headers = dict(scope["headers"])
        token = None

        if b"authorization" in headers:
            auth_header = headers[b"authorization"].decode("utf-8")
            if auth_header.startswith("Bearer "):
                token = auth_header.split()[1]

        # Authenticate the user using the JWT token
        scope["user"] = await self.get_user(token)

        return await super().__call__(scope, receive, send)

    @database_sync_to_async
    def get_user(self, token):

        try:
            # Decode the JWT token to get the user ID
            access_token = AccessToken(token)
            user_id = access_token["user_id"]
            return User.objects.get(id=user_id)
        except Exception:
            return None
