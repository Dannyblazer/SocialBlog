from ast import Dict
from django.db.models import Q
from django.db.models.query import QuerySet
from .models import ChatMessage, ChatRoom
from .filters import ChatFilter, RoomEncoder



def chat_message_list(*, filters=None) -> QuerySet[ChatMessage]:
    filters = filters or {}
    qs = ChatMessage.objects.select_related('author')
    return ChatFilter(filters, qs).qs


def chat_room_list(request) -> Dict:
    user = request.user
    encoder = RoomEncoder(context={'user': user})
    serialized_data = encoder.to_representation()
    return serialized_data


def get_or_return_room(user1, user2) -> ChatRoom:
    chat, created = ChatRoom.objects.get_or_create(
        Q(user1=user1, user2=user2) | Q(user1=user2, user2=user1),
        defaults={'user1': user1, 'user2': user2}
    )
    return chat

