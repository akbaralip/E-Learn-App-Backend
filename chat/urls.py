from django.urls import path
from .views import *

urlpatterns = [
    path('community_all_messages/<str:room_name>/', GetMessages.as_view(), name='get_messages'),
    path('one_to_one_chat_messages/<int:user_id>/', OneToOneChatMessagesView.as_view(), name='one_to_one_chat_messages'),

]

