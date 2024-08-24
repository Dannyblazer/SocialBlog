import django_filters
from .models import ChatMessage


class ChatFilter(django_filters.FilterSet):
    class Meta:
        model = ChatMessage
        fields = ("id", "room", "sender", "content", "created_at")
        