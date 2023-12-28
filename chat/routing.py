from django.urls import re_path
from .consumers import ChatConsumer, OneToOneChatConsumer

websocket_urlpatterns = [
    re_path(r'ws/chat/(?P<room_name>\w+)/$', ChatConsumer.as_asgi()),
    re_path(r'ws/one_to_one_chat/(?P<user_id>\w+)/$', OneToOneChatConsumer.as_asgi()),
]
