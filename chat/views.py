from rest_framework.response import Response
from users.models import User
from .serializers import *
from rest_framework.views import APIView
from rest_framework import status
from .models import Message, OneToOneChatMessage
from .serializers import MessageSerializers

from django.shortcuts import get_object_or_404
from django.db.models import Q

class GetMessages(APIView):
    def get(self, request, room_name):
        messages = Message.objects.filter(room_name=room_name)
        serializer = MessageSerializers(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class OneToOneChatMessagesView(APIView):
    def get(self, request, user_id):
        user = get_object_or_404(User, id=user_id)

        messages = OneToOneChatMessage.objects.filter(Q(sender=user) | Q(receiver=user))

        serializer = MessageSerializer(messages, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

