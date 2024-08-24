from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.mixins import ApiAuthMixin


from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from .models import ChatRoom, ChatMessage, UnreadChatRoomMessages

