from django.db import models
from users.models import *
from course.models import *

# Create your models here.
class Message(models.Model):
    sender = models.TextField()
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    room_name = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"From: {self.sender}  - {self.timestamp}"


class OneToOneChatMessage(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sender')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receiver')
    message_content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OneToOneChatMessage from {self.sender} to {self.receiver} at {self.timestamp}"
