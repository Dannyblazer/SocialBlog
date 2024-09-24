import json
from ast import Dict
from django.db.models import Q, Prefetch
from django.db.models.query import QuerySet
from channels.db import database_sync_to_async
from django.core.paginator import Paginator
from .constants import DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE
from .models import ChatMessage, ChatRoom, UnreadChatRoomMessages
from .filters import ChatFilter, RoomEncoder
from .utils import calculate_timestamp, LaxyRoomChatMessageEncoder
from user.utils import LazyAccountEncoder


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

@database_sync_to_async
def get_room_chat_messages(room, page_number):
    try:
        qs = ChatMessage.objects.by_room(room)
        p = Paginator(qs, DEFAULT_ROOM_CHAT_MESSAGE_PAGE_SIZE)

        payload = {}
        new_page_number = int(page_number)
        if new_page_number <= p.num_pages:
            new_page_number = new_page_number + 1
            s = LaxyRoomChatMessageEncoder()
            payload['messages'] = s.serialize(p.page)
        else:
            payload['messages'] = None
        payload['new_page_number'] = new_page_number
        payload['messages'] = payload['messages'][::-1]
        return json.dumps(payload)
    except Exception as e:
        print("EXCEPTION last: " + str(e))
    return None


@database_sync_to_async
def get_user_info(room, user):
    try:
        other_user = room.user1 if room.user1 != user else room.user2
        s = LazyAccountEncoder()
        final = s.serialize([other_user])[0]
        payload = {'user_info': final}
        return json.dumps(payload, indent=4, sort_keys=True, default=str)
    
    except Exception as e:
        print("EXCEPTiON: " + str(e))
        return None


