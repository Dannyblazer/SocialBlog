import django_filters
from django.db.models import Q
from django.utils import timezone
from rest_framework import serializers
from .models import ChatMessage, ChatRoom


class ChatFilter(django_filters.FilterSet):
    class Meta:
        model = ChatMessage
        fields = ("id", "room", "sender", "content", "created_at") 


class RoomEncoder(serializers.BaseSerializer):
    def to_representation(self):
        user = self.context['user']
        rooms = ChatRoom.objects.filter(
            Q(user1=user) | Q(user2=user), 
            is_active=True
        ).prefetch_related('user1', 'user2')
        #base_url = 'https://taskitly.com'

        room_data = []
        for room in rooms:
            if room.user1 == user:
                friend = room.user2
            else:
                friend = room.user1

            try:
                message = ChatMessage.objects.filter(room=room).select_related('user').latest('timestamp') # Remember to prefetch here
            except ChatMessage.DoesNotExist:
                message = ChatMessage(
                    user=friend,
                    room=room,
                    timestamp=timezone.now(),
                    content="",
                )
            if message.user == user:

                room_data.append({
                    #'room_id': str(room.id),
                    'friend_id': str(friend.pk),
                    'user': str(friend.username),
                    'first_name': str(friend.first_name),
                    'last_name': str(friend.last_name),
                    'profile_image': str(friend.profile_image.ur),
                    'last_message': {
                        'room': str(message.room.id),
                        'timestamp': message.timestamp.isoformat(),
                        'content': message.content,
                    }
                })
            else:
                room_data.append({
                    #'room_id': str(room.id),
                    'friend_id': str(friend.pk),
                    'user': str(message.user.username),
                    'first_name': str(message.user.first_name),
                    'last_name': str(message.user.last_name),
                    'profile_image': str(message.user.profile_image.url),
                    'last_message': {
                        'room': str(message.room.id),
                        'timestamp': message.timestamp.isoformat(),
                        'content': message.content,
                    }
                })

        return room_data

