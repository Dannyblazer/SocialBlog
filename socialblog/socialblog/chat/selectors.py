from ast import Dict
from django.db.models import Q
from django.db.models.query import QuerySet
from .models import ChatMessage, ChatRoom
from .filters import ChatFilter, RoomEncoder



def chat_message_list(*, filters=None) -> QuerySet[ChatMessage]:
    filters = filters or {}
    qs = ChatMessage.objects.select_related('author')
    return ChatFilter(filters, qs).qs


def chat_room_list(user) -> Dict:
    encoder = RoomEncoder(context={'user': user})
    serialized_data = encoder.to_representation()
    return serialized_data


def get_or_return_room(user1, user2) -> ChatRoom:
    try:
        # Attempt to retrieve the chat room with either user1/user2 or user2/user1
        chat = ChatRoom.objects.get(Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1))
    except ChatRoom.DoesNotExist:
        # If the chat room doesn't exist, create it
        chat = ChatRoom.objects.create(user1=user1, user2=user2)
    return chat

