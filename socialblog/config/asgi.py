# ruff: noqa
"""
ASGI config for SocialBlog project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/dev/howto/deployment/asgi/

"""

import os
import sys
from pathlib import Path

from django.core.asgi import get_asgi_application
from channels.routing import URLRouter, ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator  # new
from django.core.asgi import get_asgi_application

from django.urls import re_path
from chat.consumers import ChatConsumer
#from notification.consumers import NotificationConsumer
from .tokenauth_middleware import JWTAuthMiddleware  # new

# This allows easy placement of apps within the interior
# socialblog directory.
BASE_DIR = Path(__file__).resolve(strict=True).parent.parent
sys.path.append(str(BASE_DIR / "socialblog"))

# If DJANGO_SETTINGS_MODULE is unset, default to the local settings
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AllowedHostsOriginValidator(  
        JWTAuthMiddleware(
            URLRouter([
                    re_path(r"ws/chat/$", ChatConsumer.as_asgi()),
            ])
        )
    )
})

                    #re_path(r"ws/notification/$", NotificationConsumer.as_asgi()),
