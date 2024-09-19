from ast import Dict
from django.db.models import Q, Prefetch
from django.db.models.query import QuerySet
from channels.db import database_sync_to_async
#from user.models import BaseUser
from .models import ChatMessage, ChatRoom, UnreadChatRoomMessages
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



# Consumers Selectors

@database_sync_to_async
def get_room_or_error(room_id, user):
    """
    Tries to fetch a room for the user, checking permissions along the way
    """
    try:
        room = ChatRoom.objects.select_related('user1', 'user2').prefetch_related(
            Prefetch('room', queryset=UnreadChatRoomMessages.objects.filter(user=user))
        ).get(pk=room_id)
    except ChatRoom.DoesNotExist:
        print("Get room or error exception!")
        raise Exception("Invalid Room.")
    
    # Is this user allowed into this room?
    if user != room.user1 and user != room.user2:
        print("Not your chat bro!")
        raise Exception("You do not have permission to join this room.")
    
    return room


@database_sync_to_async
def connected_users(room):
    return room.connected_users.all()

