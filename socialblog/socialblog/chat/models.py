from django.db import models
from django.conf import settings
from common.models import BaseModel
#from user.models import BaseUser
# Create your models here.


class Room(BaseModel):
# A Private chat between to users
    user1       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1')
    user2       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2')
    is_active   		= models.BooleanField(default=True)
    connected_users     = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="connected_users")

    def __str__(self):
        return f"A chat between {self.user1} and {self.user2}"

    def connect_user(self, user):
        """
        return true if user is added to the connected_users list
        """
        is_user_added = False
        if not user in self.connected_users.all():
            self.connected_users.add(user)
            is_user_added = True
        return is_user_added
    
    def disconnect_user(self, user):
        """
        return true if user is removed from connected_users list
        """
        is_user_removed = False
        if user in self.connected_users.all():
            self.connected_users.remove(user)
            is_user_removed = True
        return is_user_removed

    @property
    def group_name(self):
        """ Return the channels group name that sockets should subscribe to receive private chat messages (pair-wise) """
        
        return f"PrivateChatRoom-{self.pk}"


class ChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = ChatMessage.objects.filter(room=room).order_by("-created_at")
        return qs
    

class ChatMessage(BaseModel):
    sender          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room            = models.ForeignKey(Room, on_delete=models.CASCADE)
    content         = models.TextField(unique=False, blank=False)

    objects = ChatMessageManager()

    def __str__(self):
        return self.content
