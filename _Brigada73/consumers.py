from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
import json
from unidecode import unidecode

from django.db.models import Q


chat_users = set()
online_users = set()
async def redis_disconnect(self, *args):
    pass
    # Handle disconnect

def get_channel_name(user_id):
    return f"chanel_{user_id}"


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        print("chatconnected",self.scope)
        group_name = get_channel_name(user.id)
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
        print("self.scope", self.scope)

        content = text_data_json['message']
        receiver_id = text_data_json['channel_name']
        channel_name = get_channel_name(receiver_id)
        receiver_name = text_data_json['receiver_name']
        sender_name = text_data_json['sender_name']
        sender_id = text_data_json['sender_id']
        message_type = text_data_json['type']
        # user = await self.get_user_by_id(receiver_id)
        sender = await self.get_user_by_id(sender_id)
        receiver = await self.get_user_by_id(receiver_id)
        message_id = await self.save_message(sender, receiver, content)
        if sender_name != receiver_name:
            await self.send(text_data=json.dumps({
                'type': 'from_me',
                'status': 'true',
                'id': -1,
                'message': content,
                'sender_name': sender_name,
                'receiver_name': receiver_name,
            }))
        if channel_name in chat_users:
            await self.send_message(sender_name, receiver_name, channel_name, content, message_type, message_id)
        if channel_name in online_users:
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
                                            {
                                                "type": 'total_num_notify_message'})  # Как побочный эффект выполнения этого метода

    async def chat_message(self, event):  # не удалять!!! это нужно для "type": message_type, имя метода = значению type
        await self.send(text_data=json.dumps({"message": event["message"], 'status': event["status"],
                                              "sender_name": event["sender_name"], 'id': event["id"],
                                              'receiver_name': event['receiver_name'], 'type': 'to_me'}))

    async def total_num_notify_message(self, event):
        print("Активируется отправка оповещения")
        pass

    async def send_total_orders(self, event):
        print("Вызвалось оповещение о заказе в чате")
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
            messages_data.append({
                'type': 'to_me',
                'content': message.content,
                'status': message.status,
                'id': message.id,
                'sender_name': message.sender.username,
                'receiver_name': message.receiver.username,
            })
        return messages_data

    # @sync_to_async
    async def send_history(self, messages):
        await self.send(text_data=json.dumps({
            'type': 'to_me',
            'status': 'true',
            'id': -1,
            'message': "Добро пожаловать в чат",
            'sender_name': "Историк",
            'receiver_name': self.scope['user'].username,
        }))
        if messages:
            for message in messages:
                await self.send(text_data=json.dumps({
                    'type': 'from_me' if message['sender_name'] == self.scope['user'].username else 'to_me',
                    'status': bool(message['status']),
                    'id': message['id'],
                    'message': message['content'],
                    'sender_name': message['sender_name'],
                    'receiver_name': message['receiver_name'],
                }))


class NotifyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        user = self.scope['user']
        group_name = get_channel_name(user.id)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        online_users.add(group_name)
        await self.accept()
        num = await self.get_total_unread_num()
        await self.send_message(num)

    async def disconnect(self, close_code):
        group_name = get_channel_name(self.scope['user'].id)
        online_users.discard(group_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print("text_data_jsontext_data_jsontext_data_json",text_data_json)
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

    @database_sync_to_async
    def set_status(self, read_ids):
        try:
            message_model = apps.get_model(app_label='message', model_name='Message')
            message_model.objects.filter(id__in=read_ids).update(status=True)
            return True
        except Exception as e:
            return False

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
        # num = await self.get_total_unread_num()
        await self.send(text_data=json.dumps({"num": event['num'], "type": "total"}))

    async def chat_message(self, event):  # не удалять!!! это нужно для "type": message_type, имя метода = значению type
        pass

    async def send_total_orders(self, event):
        print("Вызвалось оповещение о заказе в оповещениях")
        pass


translit_dict = {
    'а': 'a', 'б': 'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z',
    'и': 'i', 'й': 'y', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
    'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'kh', 'ц': 'ts', 'ч': 'ch', 'ш': 'sh', 'щ': 'shch',
    'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'yu', 'я': 'ya',
    'А': 'A', 'Б': 'B', 'В': 'V', 'Г': 'G', 'Д': 'D', 'Е': 'E', 'Ё': 'E', 'Ж': 'Zh', 'З': 'Z',
    'И': 'I', 'Й': 'Y', 'К': 'K', 'Л': 'L', 'М': 'M', 'Н': 'N', 'О': 'O', 'П': 'P', 'Р': 'R',
    'С': 'S', 'Т': 'T', 'У': 'U', 'Ф': 'F', 'Х': 'Kh', 'Ц': 'Ts', 'Ч': 'Ch', 'Ш': 'Sh', 'Щ': 'Shch',
    'Ъ': '', 'Ы': 'Y', 'Ь': '', 'Э': 'E', 'Ю': 'Yu', 'Я': 'Ya'
}
@sync_to_async
def get_order_channel_name(user):
    city = user.address.city.name
    city_translit = ''.join(translit_dict.get(c, c) for c in city)
    return f"orders_{city_translit}"
    # return "orders_"
class OrderConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_anonymous:
            group_name = await get_order_channel_name(self.user)
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
            online_users.add(group_name)
            num = await self.get_total_orders()
            await self.send_message(num,self.user)
        await self.accept()



    async def disconnect(self, close_code):
        group_name = get_channel_name(self.scope['user'].id)
        online_users.discard(group_name)
        await self.close()
        print("Заказы отключены:", group_name)

    async def receive(self, text_data=None, bytes_data=None):
        print("Что то пришло")
        text_data_json = json.loads(text_data)
        print("text_data_json",text_data_json)

        notify_type = text_data_json['type']
        if notify_type == 'user_id':
            user_id = text_data_json['user_id']
            self.user = await self.get_user_by_id(user_id)
            print("Получили пользователя отправителя",self.user.username)
            num = await self.get_total_orders()
            await self.send_message(num, self.user)
        elif notify_type == 'new_order':
            print("Получили тестовое сообщение")
            print("Получили тестовое сообщение от", self.user.username,text_data_json['message'])

            num = await self.get_total_orders()
            # user_id = text_data_json['user_id']
            # user = await self.get_user_by_id(user_id)
            await self.send_message(num,self.user)

    @database_sync_to_async
    def get_total_orders(self):

        order_model = apps.get_model(app_label='profile', model_name='Order')
        new_orders = order_model.objects.filter(confirmed=False)
        customer_ids = []
        for order in new_orders:
            customer = order.customer
            if customer.address.city == self.user.address.city:
                customer_ids.append(customer)
        num_orders = len(customer_ids)
        return num_orders

    @database_sync_to_async
    def get_orders(self):
        me = self.scope['user']
        order_model = apps.get_model(app_label='profile', model_name='Order')
        new_orders = order_model.objects.filter(confirmed=False)
        customer_ids = []
        for order in new_orders:
            customer = order.customer
            if customer.address.city == me.address.city:
                customer_ids.append(customer)
        return customer_ids

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        custom_user_model = apps.get_model(app_label='profile', model_name='CustomUser')
        return custom_user_model.objects.get(pk=user_id)


    async def send_message(self, num, user):
        print('Sending отправляем количество новых ордеров')
        group_name = await get_order_channel_name(user)
        print('group_name',group_name)

        await self.channel_layer.group_send(group_name, {
            "type": 'send_total_orders',
            'num': num,
        })

    async def send_total_orders(self, event):
        print("Вызвалось оповещение о заказе в заказе")
        await self.send(text_data=json.dumps({"num": event['num'], "type": "total_orders"}))

    async def total_num_notify_message(self, event):
        pass
    async def chat_message(self, event):  # не удалять!!! это нужно для "type": message_type, имя метода = значению type
        pass
