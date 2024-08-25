from django.urls import path
from .apis import CreateOrReturnRoomApi, GetChatListApi


urlpatterns = [
    path("chat_list", GetChatListApi.as_view(), name="get-rooms"),
    path("get_room/<int:user2_id>", CreateOrReturnRoomApi.as_view(), name="get-room")
]
