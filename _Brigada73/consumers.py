import time

from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
import json

from django.db.models import Q

chat_users = set()
online_users = set()


def get_channel_name(user_id):
    return f"chanel_{user_id}"


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        group_name = get_channel_name(user.id)
        print("sender id on connect in consumers:", group_name)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        chat_users.add(group_name)
        await self.accept()

    async def disconnect(self, close_code):
        group_name = get_channel_name(self.scope['user'].id)
        chat_users.discard(group_name)
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
        message_id = await self.save_message(sender, receiver, content)

        print("В чате:", chat_users)
        if channel_name in chat_users:
            print("Пользователь в чате")
            await self.send_message(sender_name, receiver_name, channel_name, content, message_type, message_id)
        print("В чате:", chat_users)
        if channel_name in online_users:
            print("Пользователь в сети")
            await self.send_notify(channel_name)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        custom_user_model = apps.get_model(app_label='profile', model_name='CustomUser')
        return custom_user_model.objects.get(pk=user_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        message_model = apps.get_model(app_label='message', model_name='Message')
        msg = message_model(sender=sender, receiver=receiver, content=content)
        msg.save()
        print("Получили id сообщения", msg.id)
        return msg.id

    async def send_message(self, sender_name, receiver_name, channel_name, message, message_type, msg_id):
        await self.channel_layer.group_send(channel_name, {
            "type": message_type,
            'status': 'false',
            'id': msg_id,
            'message': message,
            'sender_name': sender_name,
            'receiver_name': receiver_name,  # пока не нужный параметр
        })

    async def send_notify(self, channel_name):  # Вызовется в Notify
        await self.channel_layer.group_send(channel_name,
                                            {"type": 'total_num_notify_message'})  # Как побочный эффект выполнения этого метода

    async def chat_message(self, event):  # не удалять!!! это нужно для "type": message_type, имя метода = значению type
        await self.send(text_data=json.dumps({"message": event["message"], 'status': event["status"],
                                              "sender_name": event["sender_name"], 'id': event["id"],
                                              'receiver_name': event['receiver_name'], 'type': 'to_me'}))

    async def total_num_notify_message(self, event):
        print("Активируется отправка оповещения")
        pass


class HistoryConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        receiver_id = text_data_json['channel_name']
        sender_id = text_data_json['sender_id']
        sender = await self.get_user_by_id(sender_id)
        receiver = await self.get_user_by_id(receiver_id)
        messages = await self.get_messages(sender, receiver)
        await self.send_history(messages)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        custom_user_model = apps.get_model(app_label='profile', model_name='CustomUser')
        return custom_user_model.objects.get(pk=user_id)

    @database_sync_to_async
    def get_messages(self, sender, receiver):
        message_model = apps.get_model(app_label='message', model_name='Message')
        messages = message_model.objects.filter(
            (Q(sender=sender) & Q(receiver=receiver)) | (Q(sender=receiver) & Q(receiver=sender))).order_by('timestamp')
        messages_data = []
        for message in messages:
            message_data = {
                'type': 'to_me',
                'content': message.content,
                'status': message.status,
                'id': message.id,
                'sender_name': message.sender.username,
                'receiver_name': message.receiver.username,
            }
            messages_data.append(message_data)
        return messages_data

    # @sync_to_async
    async def send_history(self, messages):
        await self.send(text_data=json.dumps({
            'type': 'to_me',
            'status': 'true',
            'id': -1,
            'message': "Доброо пожаловать в чат",
            'sender_name': "Историк",
            'receiver_name': self.scope['user'].username,
        }))
        if messages:
            for message in messages:
                # await self.send_message(message['sender_name'], message['receiver_name'], message['content'])
                await self.send(text_data=json.dumps({
                    'type': 'from_me' if message['sender_name'] == self.scope['user'] else 'to_me',
                    'status': message['status'],
                    'id': message['id'],
                    'message': message['content'],
                    'sender_name': message['sender_name'],
                    'receiver_name': message['receiver_name'],
                }))


class NotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        group_name = get_channel_name(user.id)
        print("Оповещения подключены:", group_name)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        online_users.add(group_name)
        print("Оповещения подключены, в чате", online_users)
        await self.accept()
        num = await self.get_total_unread_num()
        await self.send_message(num)

    async def disconnect(self, close_code):
        group_name = get_channel_name(self.scope['user'].id)
        online_users.discard(group_name)
        await self.close()
        print("Оповещения отключены:", group_name)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        notify_type = text_data_json['type']
        if notify_type == 'read_report':
            read_ids = text_data_json['read_ids']
            status = await self.set_status(read_ids)
            if status:
                await self.send(text_data=json.dumps({
                    'type': 'set_statuses',
                    'statuses': read_ids
                }))
                num = await self.get_total_unread_num()
                await self.send_message(num)
                # await self.total_num_notify_message()
        # type_num_request = text_data_json['type']
        # if type_num_request == 'total':
        #     num = await self.get_total_unread_num()
        #     await self.send_message(num)
        # await self.send(text_data=json.dumps({'num': num}))

    # @database_sync_to_async
    # def get_user_by_id(self, user_id):
    #     CustomUser = apps.get_model(app_label='profile', model_name='CustomUser')
    #     return CustomUser.objects.get(pk=user_id)

    # @database_sync_to_async
    # def get_num_unread_messages(self, sender):
    #     me = self.scope['user']
    #     print("История начала запрашиваться")
    #     Message = apps.get_model(app_label='message', model_name='Message')
    #     unread_messages = Message.objects.filter(receiver=me, new=True)
    #     unread_messages_count = unread_messages.count()
    #     return unread_messages_count

    @database_sync_to_async
    def set_status(self, read_ids):
        print('Обновление id',read_ids)
        read_ids_int = list(map(int, read_ids))
        try:
            message_model = apps.get_model(app_label='message', model_name='Message')
            # message_model.objects.filter(id__in=read_ids_int).update(status=True)
            for message_id in read_ids:
                message = message_model.objects.get(id=message_id)
                message.status = True
                message.save()
            print('Обновление id получилось', read_ids_int)
            return True
        except Exception as e:
            print(f"An error occurred: {e}")
            print('Обновление id не получилось', read_ids_int)
            return False

    # @database_sync_to_async
    # def get_read_ids(self):
    #     me = self.scope['user']
    #     message_model = apps.get_model(app_label='message', model_name='Message')
    #     unread_messages = message_model.objects.filter(receiver=me, status=True).values_list('id', flat=True)
    #     return list(unread_messages)
    @database_sync_to_async
    def get_total_unread_num(self):
        me = self.scope['user']
        message_model = apps.get_model(app_label='message', model_name='Message')
        unread_messages = message_model.objects.filter(receiver=me, status=False)
        unread_messages_count = unread_messages.count()
        return unread_messages_count

    async def send_message(self, num):
        await self.channel_layer.group_send(get_channel_name(self.scope['user'].id), {
            "type": 'total_num_notify_message',
            'num': num,
        })

    async def total_num_notify_message(self, event):
        print("Отправка уведомления")
        num = await self.get_total_unread_num()
        await self.send(text_data=json.dumps({"num": num,"type": "total"}))
        print("Отправка уведомления произошла")

    async def chat_message(self, event):  # не удалять!!! это нужно для "type": message_type, имя метода = значению type
        pass
