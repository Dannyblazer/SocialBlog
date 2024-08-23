from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.contenttypes.fields import GenericRelation
from django.contrib.contenttypes.models import ContentType
from common.models import BaseModel
#from user.models import BaseUser
# Create your models here.


class ChatRoom(BaseModel):
# A Private chat room between to users
    user1       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user1')
    user2       = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='user2')
    is_active   		= models.BooleanField(default=True)
    connected_users     = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True, related_name="connected_users")

    def __str__(self):
        return f"A chat between {self.user1.username} and {self.user2.username}"

    def connect_user(self, user):
        """
        return true if user is added to the connected_users list
        """
        is_user_added = False
        if user in [self.user1, self.user2] and not user in self.connected_users.all():
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
        
        return f"Room-{self.pk}"


class ChatMessageManager(models.Manager):
    def by_room(self, room):
        qs = ChatMessage.objects.filter(room=room).order_by("-created_at")
        return qs
    

class ChatMessage(BaseModel):
    sender          = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    room            = models.ForeignKey(ChatRoom, on_delete=models.CASCADE)
    content         = models.TextField(unique=False, blank=False)

    objects = ChatMessageManager()

    def __str__(self):
        return self.content


class UnreadChatRoomMessages(models.Model):
	"""
	Keep track of the number of unread messages by a specific user in a specific private chat.
	When the user connects the chat room, the messages will be considered "read" and 'count' will be set to 0.
	"""
	room                = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name="room")

	user                = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

	count               = models.IntegerField(default=0)

	most_recent_message = models.CharField(max_length=500, blank=True, null=True)

	# last time msgs were read by the user
	reset_timestamp     = models.DateTimeField()

	#notifications       = GenericRelation(Notification)


	def __str__(self):
		return f"Messages that {str(self.user.username)} has not read yet."

	def save(self, *args, **kwargs):
		if not self.id: # if just created, add a timestamp. Otherwise do not automatically change it ever.
			self.reset_timestamp = timezone.now()
		return super(UnreadChatRoomMessages, self).save(*args, **kwargs)

	@property
	def get_cname(self):
		"""
		For determining what kind of object is associated with a Notification
		"""
		return "UnreadChatRoomMessages"

	@property
	def get_other_user(self):
		"""
		Get the other user in the chat room
		"""
		if self.user == self.room.user1:
			return self.room.user2
		else:
			return self.room.user1
