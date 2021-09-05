from django.urls import path

from .views import chat_index, chat_room

urlpatterns = [
    path('', chat_index, name='chat'),
    path('<str:username>', chat_room, name='chat_room'),
]
