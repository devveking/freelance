# chat/consumers.py

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import Chat, Message
from accounting.models import CustomUser  # Используем CustomUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.chat_id = self.scope['url_route']['kwargs']['chat_id']
        self.chat_group_name = f'chat_{self.chat_id}'

        await self.channel_layer.group_add(
            self.chat_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.chat_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        sender_id = self.scope['user'].id  # Получаем кастомного пользователя
        print(f"Scope user: {self.scope['user']}, ID: {self.scope['user'].id}")

        # Сохраняем сообщение в базе данных
        message_obj = await self.save_message(sender_id, message)

        # Отправляем сообщение всем участникам чата
        await self.channel_layer.group_send(
            self.chat_group_name,
            {
                'type': 'chat_message',
                'message': message_obj.content,  # Отправляем текст сообщения
                'sender_id': sender_id
            }
        )


    async def chat_message(self, event):
        user = await self.get_user(event['sender_id'])
        message_data = {
            'sender': user.username,
        }

        # добавляем поля, если они есть
        if 'message' in event:
            message_data['message'] = event['message']
        if 'image_url' in event:
            message_data['image_url'] = event['image_url']
        if 'file_url' in event:
            message_data['file_url'] = event['file_url']

        await self.send(text_data=json.dumps(message_data))

    @database_sync_to_async
    def save_message(self, sender_id, message):
        try:
            chat = Chat.objects.get(id=self.chat_id)
            sender = CustomUser.objects.get(id=sender_id)
            return Message.objects.create(chat=chat, sender=sender, content=message)
            print(f"Saving message from {sender_id} in chat {self.chat_id}: {message}")

        except Chat.DoesNotExist:
            print(f"Chat with ID {self.chat_id} not found")
            return None

    @database_sync_to_async
    def get_user(self, user_id):
        return CustomUser.objects.get(id=user_id)  # Используем CustomUser
