from django.db.models.query import QuerySet
from .models import ChatRoom, ChatMessage, UnreadChatRoomMessages
from .filters import ChatFilter



def chat_message_list(*, filters=None) -> QuerySet[ChatMessage]:
    filters = filters or {}
    qs = ChatMessage.objects.select_related('author')
    return ChatFilter(filters, qs).qs

