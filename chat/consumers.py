import json

from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from .models import Chat, MessageBody
from network.models import User


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat = await self.get_chat()
        self.chat_id = self.chat.unique_id
        self.chat_name = 'chat_%s' % self.chat_id

        await self.channel_layer.group_add(
            self.chat_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.chat_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        new_message = await self.create_new_message(message)

        data = {
            'sender': new_message.sender.username,
            'receiver': new_message.receiver.username,
            'time_send': new_message.time_send.strftime('%Y-%m-%d %H:%m'),
            'content': new_message.content
        }

        print(data)

        await self.channel_layer.group_send(
            self.chat_name,
            {
                'type': 'chat_message',
                'message': data
            }
        )

    async def chat_message(self, event):
        message = event['message']

        await self.send(text_data=json.dumps({
            'message': message
        }))

    @database_sync_to_async
    def get_chat(self):
        other_user = User.objects.get(slug=self.scope['url_route']['kwargs']['username'])
        chat = Chat.objects.get_or_create_chat(self.scope['user'], other_user)
        return chat

    @database_sync_to_async
    def create_new_message(self, message):
        other_user = User.objects.get(slug=self.scope['url_route']['kwargs']['username'])
        message = MessageBody.objects.create(
            chat_fk=self.chat,
            sender=self.scope['user'],
            receiver=other_user,
            content=message
        )
        self.chat.messages.add(message)
        return message
