#from common.services import model_update
from channels.db import database_sync_to_async
from user.models import BaseUser
from chat.models import ChatRoom, ChatMessage, UnreadChatRoomMessages




def room_create(
    *, user1: BaseUser, user2: BaseUser
) -> ChatRoom:

    return ChatRoom.objects.create(user1=user1, user2=user2)


def message_create(
    *, sender: BaseUser, room: ChatRoom, content: str
) -> ChatMessage:

    return ChatMessage.objects.create(sender=sender, room=room, content=content)


# Consumer Services

@database_sync_to_async
def create_room_chat_message(room, user, message):
	return ChatMessage.objects.create(sender=user, room=room, content=message)


@database_sync_to_async
def disconnect_user(room, user):
	# remove from connected_users list
	account = BaseUser.objects.get(pk=user.pk)
	return room.disconnect_user(account)


@database_sync_to_async
def connect_user(room, user):
	# add user to connected_users list
	account = BaseUser.objects.get(pk=user.pk)
	return room.connect_user(account)



@database_sync_to_async
def append_unread_msg_if_not_connected(room, user, connected_user_s, message):
	if not user in connected_user_s: 
		try:
			unread_msgs = UnreadChatRoomMessages.objects.get(room=room, user=user)
			unread_msgs.most_recent_message = message
			unread_msgs.count += 1
			unread_msgs.save()
		except UnreadChatRoomMessages.DoesNotExist:
			UnreadChatRoomMessages(room=room, user=user, count=1).save()
			pass
	return


@database_sync_to_async
def on_user_connected(room, user):

    connected_users = room.connected_users.all()
    if user in connected_users:
        try:
            # Celerize this!
            unread_msgs = UnreadChatRoomMessages.objects.get(room=room, user=user)
            unread_msgs.count = 0
            unread_msgs.save()
        except UnreadChatRoomMessages.DoesNotExist:
            UnreadChatRoomMessages(room=room, user=user).save()
            pass
    return
