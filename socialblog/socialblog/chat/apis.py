from rest_framework import serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from api.mixins import ApiAuthMixin


"""from api.pagination import (
    LimitOffsetPagination,
    get_paginated_response,
)"""
from user.selectors import user_get
from .selectors import get_or_return_room, chat_room_list


class CreateOrReturnRoomApi(ApiAuthMixin, APIView):
    class OutputSerializer(serializers.Serializer):
        id = serializers.IntegerField()

    def post(self, request, user2_id):
        user1 = request.user
        user2 = user_get(user2_id)
        if user1 == user2:
            return Response(status=status.HTTP_400_BAD_REQUEST)
        room = get_or_return_room(user1, user2)

        output = self.OutputSerializer(room)

        return Response({"data": output.data}, status=status.HTTP_202_ACCEPTED)


# Create the Chat Room List & Decide wether to use sockets or normal api to query chat messages
class GetChatListApi(ApiAuthMixin, APIView):
    def get(self, request):
        user = request.user

        room_list = chat_room_list(user)
        return Response({"data": room_list}, status=status.HTTP_202_ACCEPTED)
    
