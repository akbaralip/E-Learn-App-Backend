from rest_framework import serializers
from .models import Message
from users.serializers import * 

class MessageSerializers(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'message_content', 'timestamp', 'room_name']

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['sender', 'message_content', 'timestamp']