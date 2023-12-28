from channels.generic.websocket import AsyncWebsocketConsumer
import json
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from .models import Message, OneToOneChatMessage
from datetime import datetime

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f"chat_{self.room_name}"

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def create_message(self, user, message_content, room_name):
        return Message.objects.create(
            sender=user,
            message_content=message_content,
            timestamp=datetime.now(),
            room_name=room_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        username = text_data_json['user']

        user = await database_sync_to_async(User.objects.get)(username=username)

        message = await self.create_message(user, message_content, self.room_name)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat.message',
                'message_content': message_content,
                'user': username
            }
        )

    async def chat_message(self, event):
        message = event['message_content']
        username = event['user']
        timestamp = datetime.now().isoformat()

        await self.send(text_data=json.dumps({
            'message_content': message,
            'sender': username,
            'timestamp': timestamp
        }))


class OneToOneChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user_id = self.scope['url_route']['kwargs']['user_id']
        self.room_name = f"one_to_one_{self.user_id}"

        await self.channel_layer.group_add(
            self.room_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_name,
            self.channel_name
        )

    @database_sync_to_async
    def create_one_to_one_message(self, sender, receiver, message_content):
        return OneToOneChatMessage.objects.create(
            sender=sender,
            receiver=receiver,
            message_content=message_content
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_content = text_data_json['message']
        username = text_data_json['user']

        sender = await database_sync_to_async(User.objects.get)(username=username)
        receiver = await database_sync_to_async(User.objects.get)(id=self.user_id)

        message = await self.create_one_to_one_message(sender, receiver, message_content)

        await self.channel_layer.group_send(
            self.room_name,
            {
                'type': 'chat.message',
                'message_content': message_content,
                'user': username
            }
        )

    async def chat_message(self, event):
        message = event['message_content']
        username = event['user']
        timestamp = datetime.now().isoformat()

        await self.send(text_data=json.dumps({
            'message_content': message,
            'sender': username,
            'timestamp': timestamp
        }))