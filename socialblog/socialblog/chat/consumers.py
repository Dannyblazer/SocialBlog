import asyncio
from email.mime import base
import json
import traceback
from django.conf import settings
from django.utils import timezone
#from django.db.models import Prefetch
#from django.core.paginator import Paginator
from channels.generic.websocket import AsyncJsonWebsocketConsumer
from .selectors import (get_room_or_error, connected_users,
                        get_room_chat_messages)
from .services import (create_room_chat_message, disconnect_user,
                       connect_user, on_user_connected,
                       append_unread_msg_if_not_connected)
from .utils import calculate_timestamp
from .exception import apply_wrappers
from .constants import BASE_URL


@apply_wrappers
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
            elif command == "get_room_chat_messages":
                room = await get_room_or_error(content['room'], self.scope['user'])
                payload = await get_room_chat_messages(room, content['page_number'])
                if payload != None:
                    payload = json.loads(payload)
                    await self.send_messages_payload(payload['messages'], payload['new_page_number'])
                else:
                    raise Exception("Something went wrong retrieving the chat messages.")
        
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
        
        await connect_user(room, self.scope["user"])

        if not self.channel_layer:
            print("Helpoo")
    
        self.room_id = room.id

        await on_user_connected(room, self.scope["user"])

        await self.channel_layer.group_add(
            room.group_name,
            self.channel_name
        )
        
        await self.send_json({
            "join": str(room.id)
        })

    async def leave_room(self, room_id):
        print("ChatConsumer: leave_room")

        room = await get_room_or_error(room_id, self.scope["user"])

        await disconnect_user(room, self.scope["user"])

        self.room_id = None
        
        await self.channel_layer.group_discard(
            room.group_name,
            self.channel_name
        )

    async def send_room(self, room_id, message):
        print("Consumer: send_room")
        if self.room_id != None:
            if str(room_id) != str(self.room_id):
                print("ClientError for send_room")
        else:
            print("ClientError room-id is none")
        
        room = await get_room_or_error(room_id, self.scope["user"])

        # Create the message in the database
        msg = await create_room_chat_message(room, self.scope["user"], message)


        await self.channel_layer.group_send(
            room.group_name,
            {
                "type": "chat_message",
                #"username": self.scope["user"].username,
                "user_id": self.scope["user"].pk,
                "message": message,
            }
        )

        try:
            connected_user_s = await connected_users(room)
        except Exception as e:
            print(f"Connected: {e}")
        
        async def handle_async_tasks():
            try:
                await asyncio.gather(
                    append_unread_msg_if_not_connected(room, room.user1, connected_user_s, message),
                    append_unread_msg_if_not_connected(room, room.user2, connected_user_s, message)
                )
            except Exception as e:
                traceback.print_exc()
        await handle_async_tasks()

    async def chat_message(self, event):
        """ Called when someone messaged our chat"""
        timestamp = calculate_timestamp(timezone.now())

        await self.send_json({
            #"username": event["username"],
            "user_id": event["user_id"],
            "message": event["message"],
            "natural_timestamp": timestamp,
        })

    async def send_messages_payload(self, messages, new_page_number):
        # Send a payload of message(s) to client socket
        print("Consumer: send messages payload")
        await self.send_json({
            "messages_payload": "messages_payload",
            "messages": messages,
            "new_page_number": new_page_number,
        })



