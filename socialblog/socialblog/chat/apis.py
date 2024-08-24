from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.mixins import ApiAuthMixin


from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)
from .models import ChatRoom, ChatMessage, UnreadChatRoomMessages
from user.selectors import user_get
from .selectors import get_or_return_room
from .services import *


class CreateOrReturnRoom(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        room_id = serializers.IntegerField()

    def post(self, request, user2_id):
        user1 = request.user
        user2 = user_get(user2_id)
        room = get_or_return_room(user1, user2)

        output = self.OutputSerializer(room)

        return Response({"data": output.data}, status=status.HTTP_202_ACCEPTED)


# Create the Chat Room List & Decide wether to use sockets or normal api to query chat messages