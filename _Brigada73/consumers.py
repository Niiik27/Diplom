import time

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
import json

from django.db.models import Q


def get_channel_name(user_id):
    return f"chanel_{user_id}"


class ChatConsumer(AsyncWebsocketConsumer):
    roomGroupName = None

    async def connect(self):
        user = self.scope['user']
        self.roomGroupName = get_channel_name(user.id)
        print("sender id on connect in consumers:", self.roomGroupName)
        await self.channel_layer.group_add(
            self.roomGroupName,
            self.channel_name
        )
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)

        content = text_data_json['message']
        receiver_id = text_data_json['channel_name']
        channel_name = get_channel_name(receiver_id)
        receiver_name = text_data_json['receiver_name']
        sender_name = text_data_json['sender_name']
        sender_id = text_data_json['sender_id']
        message_type = text_data_json['type']

        user = await self.get_user_by_id(receiver_id)
        print('Пользователь полученный из базы', user.username)
        sender = await self.get_user_by_id(sender_id)
        receiver = await self.get_user_by_id(receiver_id)
        await self.save_message(sender, receiver, content)
        if sender_name!=receiver_name:
            await self.send(text_data=json.dumps({
                'type': 'from_me',
                'message': content,
                'sender_name': sender_name,
            }))
        await self.send_message(sender_name, receiver_name, channel_name, content, message_type)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        CustomUser = apps.get_model(app_label='profile', model_name='CustomUser')
        return CustomUser.objects.get(pk=user_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        Message = apps.get_model(app_label='message', model_name='Message')
        msg = Message(sender=sender, receiver=receiver, content=content)
        msg.save()

    async def send_message(self, sender_name, receiver_name, channel_name, message, message_type):
        print('channel_name', channel_name)
        print('receiver_name', receiver_name)
        print('sender_name', sender_name)
        print('message', message)
        print('message_type', message_type)

        await self.channel_layer.group_send(channel_name, {
            "type": message_type,
            'message': message,
            'sender_name': sender_name,
            'receiver_name': receiver_name,
        })
        print('метод полностью отработал')

    async def chat_message(self, event):  # не удалять!!! это нужно для "type": message_type, имя метода = значению type
        await self.send(text_data=json.dumps({"message": event["message"], "sender_name": event["sender_name"],
                                              'receiver_name': event['receiver_name'], 'type': 'to_me'}))

class HistoryConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()
        await self.send(text_data=json.dumps({
            'type': 'to_me',
            'message': "Ты должен это увидеть. ты подключился",
            'sender_name': "Историк",
            'receiver_name': "Получатель",
        }))

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        receiver_id = text_data_json['channel_name']
        sender_id = text_data_json['sender_id']
        sender = await self.get_user_by_id(sender_id)
        receiver = await self.get_user_by_id(receiver_id)

        messages = await self.get_messages(sender, receiver)
        print("История сообщений получена")

        await self.send_history(messages)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        CustomUser = apps.get_model(app_label='profile', model_name='CustomUser')
        return CustomUser.objects.get(pk=user_id)

    @database_sync_to_async
    def get_messages(self, sender, receiver):
        print("История начала запрашиваться")
        Message = apps.get_model(app_label='message', model_name='Message')
        messages = Message.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))).order_by('timestamp')
        messages_data = []
        for message in messages:
            message_data = {
                'content': message.content,
                'sender_name': message.sender.username,
                'receiver_name': message.receiver.username,
            }
            messages_data.append(message_data)
        return messages_data

    # @sync_to_async
    async def send_history(self, messages):
        print("Отправляется тестовое сообщение")
        await self.send(text_data=json.dumps({
            'type': 'to_me',
            'message': "Ты должен это увидеть, тебе должна отправится история переписки",
            'sender_name': "Историк",
            'receiver_name': "Получатель",
        }))
        print("Тестовое сообщение отправилось")

        print("История сообщений отправляется")
        if messages:
            for message in messages:
                # await self.send_message(message['sender_name'], message['receiver_name'], message['content'])
                await self.send(text_data=json.dumps({
                    'type': 'from_me' if message['sender_name'] == self.scope['user'] else 'to_me',
                    'message': message['content'],
                    'sender_name': message['sender_name'],
                    'receiver_name': message['receiver_name'],
                }))
                print("История сообщений была отправлена", message['content'])
        else:
            print("История сообщений пуста")
        print("Отправка истории завершена")
