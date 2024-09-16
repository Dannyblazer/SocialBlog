import json
from django.conf import settings
from django.utils import timezone
from django.db.models import Prefetch
from django.core.paginator import Paginator
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatRoom, UnreadChatRoomMessages



class ChatConsumer(AsyncJsonWebsocketConsumer):
    async def connect(self):
        print("ChatConusmer: connect: " + str(self.scope["user"].username))
        await self.accept()
        self.room_id = None


    async def receive_json(self, content):
        print("ChatConsumer: receive_json")
        command = content.get("command", None)
        try:
            if command == "join":
                await self.join_room(content['room'])
            elif command == "leave":
                await self.leave_room(content['room'])
            elif command == "send":
                if len(content['message'].lstrip()) != 0:
                    await self.send_room(content['room'], content['message'])
            """elif command == "get_room_chat_messages":
                room = await get_room_or_error(content['room'], self.scope['user'])
                payload = await get_room_chat_messages(room, content['page_number'])""" 
        except Exception as e:
            pass

    
    async def disconnect(self, code):
        print("ChatConsumer: disconnect")
        try:
            if self.room_id != None:
                await self.leave_room(self.room_id)
        except Exception as e:
            pass
        return await super().disconnect(code)
    

    async def join_room(self, room_id):
        print("ChatConsumer: join_room: " + str(room_id))
        try:
            room = await get_room_or_error(room_id, self.scope['user'])
        except Exception as e:
            return e
        
        #await connect_user



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
