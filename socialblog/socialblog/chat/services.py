from common.services import model_update
from users.models import BaseUser
from chat.models import ChatRoom, ChatMessage, UnreadUnreadChatRoomMessages




def room_create(
    *, user1: BaseUser, user2: BaseUser
) -> ChatRoom:

    return ChatRoom.objects.create(user1=user1, user2=user2)


def message_create(
    *, sender: BaseUser, room: ChatRoom, content: str
) -> ChatMessage:

    return ChatMessage.objects.create(sender=sender, room=room, content=content)
