from asgiref.sync import sync_to_async, async_to_sync
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

from django.apps import apps
import json

from django.db.models import Count, QuerySet
from django.db import models
from django.db.models import Q

import APP_NAMES
from Print import Print

chat_users = set()
online_users = {}


async def redis_disconnect(self, *args):
    pass
    # Handle disconnect


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


def get_chat_channel_name(user):
    user_translit = ''.join(translit_dict.get(c, c) for c in user.username)
    return f"{user_translit}_{user.id}"
def build_chat_channel_name(username, user_id):
    user_translit = ''.join(translit_dict.get(c, c) for c in username)
    return f"{user_translit}_{user_id}"


def get_spec_channel_name(spec):
    return f"spec_{spec.id}"


@sync_to_async
def get_order_channel_name(user):
    city = user.address.city.name
    city_translit = ''.join(translit_dict.get(c, c) for c in city)
    return f"orders_{city_translit}"


@sync_to_async
def get_team_channel_name(user):
    city = user.address.city.name
    city_translit = ''.join(translit_dict.get(c, c) for c in city)
    return f"team_{city_translit}"


class ChatConsumer(AsyncWebsocketConsumer):

    async def connect(self):
        user = self.scope['user']
        group_name = get_chat_channel_name(user)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        chat_users.add(group_name)
        await self.accept()

    async def disconnect(self, close_code):
        group_name = get_chat_channel_name(self.scope['user'])
        chat_users.discard(group_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message_type = text_data_json['type']

        content = text_data_json['message']
        receiver_id = text_data_json['channel_name']
        receiver_name = text_data_json['receiver_name']
        group_name = build_chat_channel_name(receiver_name, receiver_id)
        sender_name = text_data_json['sender_name']
        sender_id = text_data_json['sender_id']
        sender = await self.get_user_by_id(sender_id)
        receiver = await self.get_user_by_id(receiver_id)
        if message_type == 'message':

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
            if group_name in chat_users:
                await self.send_message(sender_name, receiver_name, group_name, content, message_type, message_id)
            if receiver_id in online_users:
                await self.send_notify_about_new_message(group_name)

        elif message_type == 'history':
            messages = await self.get_messages(sender, receiver)
            await self.send_history(messages)

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        custom_user_model = apps.get_model(app_label=APP_NAMES.PROFILE[APP_NAMES.NAME], model_name='CustomUser')
        return custom_user_model.objects.get(pk=user_id)

    @database_sync_to_async
    def save_message(self, sender, receiver, content):
        message_model = apps.get_model(app_label=APP_NAMES.MESSAGE[APP_NAMES.NAME], model_name='Message')
        msg = message_model(sender=sender, receiver=receiver, content=content)
        msg.save()
        return msg.id

    @database_sync_to_async
    def get_messages(self, sender, receiver):
        message_model = apps.get_model(app_label=APP_NAMES.MESSAGE[APP_NAMES.NAME], model_name='Message')
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

    async def send_message(self, sender_name, receiver_name, group_name, message, message_type, msg_id):
        await self.channel_layer.group_send(group_name, {
            "type": message_type,
            'status': 'false',
            'id': msg_id,
            'message': message,
            'sender_name': sender_name,
            'receiver_name': receiver_name,  # пока не нужный параметр
        })

    @database_sync_to_async
    def get_total_unread_num(self):
        me = self.scope['user']
        message_model = apps.get_model(app_label=APP_NAMES.MESSAGE[APP_NAMES.NAME], model_name='Message')
        unread_messages = message_model.objects.filter(receiver=me, status=False)
        unread_messages_count = unread_messages.count()
        return unread_messages_count

    async def send_notify_about_new_message(self, group_name):
        await self.channel_layer.group_send(group_name, {"type": 'send_notify', 'notify_type': 'new_msg', 'num': 1, })

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({"message": event["message"], 'status': event["status"],
                                              "sender_name": event["sender_name"], 'id': event["id"],
                                              'receiver_name': event['receiver_name'], 'type': 'to_me'}))


class NotifyConsumer(AsyncWebsocketConsumer):
    def __init__(self, *args, **kwargs):
        super().__init__(args, kwargs)
        self.user = None

    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_anonymous:

            user_status = await self.get_status_name()
            channel_name = self.channel_name
            online_users[self.user.id] = channel_name

            if user_status == "Мастер":
                group_name = await get_order_channel_name(self.user)
                await self.channel_layer.group_add(
                    group_name,
                    channel_name
                )

                num = await self.get_total_orders()
                await self.send_total_orders(group_name, num)
            elif user_status not in ("Мастер", "Прораб", "Заказ"):  # Все кроме этих должны узнать есть ли новые бригады
                group_name = await get_team_channel_name(self.user)
                await self.channel_layer.group_add(
                    group_name,
                    channel_name
                )
                num = await self.get_total_teams()
                await self.send_total_teams(group_name, num)

            # Сообщения будут доступны всем статусам
            group_name = get_chat_channel_name(self.user)
            await self.channel_layer.group_add(
                group_name,
                channel_name
            )
            num = await self.get_total_unread_num()
            await self.send_total_messages_notify(num)

        await self.accept()  # это выполнимо для обоих исходов  но так понятнее для кого подключениие

    async def disconnect(self, close_code):
        if not self.user.is_anonymous:
            online_users.pop(self.user.id, None)
            await self.close()

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
                await self.send_total_messages_notify(num)
        elif notify_type == 'from_server_notify_new_order':  # Это приходит строго из питон клиента, это иммитация коннекта
            user_id = text_data_json['user_id']
            self.user = await self.get_user_by_id(user_id)
            group_name = await get_order_channel_name(self.user)
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
            # num = await self.get_total_orders()
            # await self.send_total_orders(group_name,num)
            await self.send_notify_about_new_order(group_name)  # Пусть клиент сам считает количество воходящих
        elif notify_type == 'from_server_notify_new_team':  # Это приходит строго из питон клиента, это иммитация коннекта
            user_id = text_data_json['user_id']
            self.user = await self.get_user_by_id(user_id)
            # group_name = get_spec_channel_name(self.user)
            # Print.purpur("И он находится в групппе", group_name)
            # await self.channel_layer.group_add(
            #     group_name,
            #     self.channel_name
            # )
            num = await self.filter_teams()
            # await self.send_notify_about_new_team(group_name)
            # await self.send_total_orders(group_name,num)
            # await self.send_notify_about_new_team(group_name)# Пусть клиент сам считает количество воходящих

    @database_sync_to_async
    def get_status_name(self):
        # status_model = apps.get_model(app_label='profile', model_name='Status')
        return self.user.status.name

    @database_sync_to_async
    def get_user_by_id(self, user_id):
        custom_user_model = apps.get_model(app_label=APP_NAMES.PROFILE[APP_NAMES.NAME], model_name='CustomUser')
        return custom_user_model.objects.get(pk=user_id)

    @database_sync_to_async
    def get_total_orders(self):

        order_model = apps.get_model(app_label=APP_NAMES.ORDERS[APP_NAMES.NAME], model_name='Order')
        new_orders = order_model.objects.filter(confirmed=False)
        customer_ids = []
        for order in new_orders:
            customer = order.customer
            if customer.address.city == self.user.address.city:
                customer_ids.append(customer)
        num_orders = len(customer_ids)
        return num_orders

    @database_sync_to_async
    def get_total_teams(self):  # Это вызовется когда я создам бригаду или отредактирую ее
        team_model = apps.get_model(app_label=APP_NAMES.TEAMS[APP_NAMES.NAME], model_name='Team')
        # brigadir, coworker, specialisation, status, qualify, city, allow, confirmed
        my_new_team = team_model.objects.filter(
            city=self.user.address.city,
            specialisation__id__in=[spec.id for spec in self.user.specialisation.all()],
            coworker=None
        )
        return my_new_team.count()

    @database_sync_to_async
    def filter_teams(self):
        candidates = None
        team_model = apps.get_model(app_label=APP_NAMES.TEAMS[APP_NAMES.NAME], model_name='Team')
        my_new_team = team_model.objects.filter(brigadir=self.user, coworker=None)

        for specialist in my_new_team:
            group_name = get_spec_channel_name(specialist)
            candidates = self.filter_specialist(specialist)
            # async_to_sync(self.channel_layer.group_add)(group_name, self.channel_name)

            for member in candidates:
                channel_name = online_users.get(member.id)
                if channel_name is not None:
                    async_to_sync(self.channel_layer.group_add)(group_name, channel_name)

            # async_to_sync(self.send_notify_about_new_team)(group_name)
            # async_to_sync(channel_layer.group_send)(group_name, {"type": "send_notify", 'notify_type': 'new_team', 'num': 1})
            async_to_sync(self.send_notify_about_new_team)(group_name)
        return candidates

    # @database_sync_to_async
    def filter_specialist(self, specialist, qualify=True, status=True, spec=True, allow=True, address=True):
        custom_user_model = apps.get_model(app_label=APP_NAMES.PROFILE[APP_NAMES.NAME], model_name='CustomUser')
        candidates = custom_user_model.objects.none()
        specialisations = specialist.specialisation
        if address: required_filter = Q(address__city=specialist.city)
        if status:
            required_filter &= Q(status=specialist.status)
        else:
            required_filter &= ~Q(status__name__in=["Заказ", "Прораб"])
        if qualify: required_filter &= Q(qualify=specialist.qualify)
        if spec: required_filter &= Q(specialisation__in=[specialisations])
        if allow:
            allowed_permissions = specialist.allow.all()
            allowed_permission_ids = [permission.id for permission in allowed_permissions]
            filtered_candidates = custom_user_model.objects.filter(required_filter)
            for allow_id in allowed_permission_ids:
                filtered_candidates = filtered_candidates.filter(allow__id=allow_id)
            candidates |= filtered_candidates
        candidates |= custom_user_model.objects.filter(required_filter)

        if candidates.count() == 0:  # Понижаем строгость фильтра, удобно для тестов, правила понижения мои субъективные,
            # по этому могу здесь это сделать без универсальной логики
            if qualify:
                return self.filter_specialist(specialist, qualify=False)
            elif status:
                return self.filter_specialist(specialist, qualify=False, status=False)
            elif allow:
                return self.filter_specialist(specialist, qualify=False, status=False, allow=False)
            elif spec:
                return self.filter_specialist(specialist, qualify=False, status=False, allow=False, spec=False)
            elif address:
                return self.filter_specialist(specialist, qualify=False, status=False, allow=False, spec=False,
                                              address=False)
        return candidates

    @database_sync_to_async
    def set_status(self, read_ids):
        try:
            message_model = apps.get_model(app_label=APP_NAMES.MESSAGE[APP_NAMES.NAME], model_name='Message')
            message_model.objects.filter(id__in=read_ids).update(status=True)
            return True
        except Exception as e:
            return False

    @database_sync_to_async
    def get_total_unread_num(self):
        me = self.scope['user']
        message_model = apps.get_model(app_label=APP_NAMES.MESSAGE[APP_NAMES.NAME], model_name='Message')
        unread_messages = message_model.objects.filter(receiver=me, status=False)
        unread_messages_count = unread_messages.count()
        return unread_messages_count

    async def send_total_messages_notify(self, num):
        await self.channel_layer.group_send(get_chat_channel_name(self.scope['user']), {
            "type": 'send_notify',
            'notify_type': 'total_messages',
            'num': num,
        })

    async def chat_message(self, event):  # не удалять!!! это нужно для "type": message_type, имя метода = значению type
        pass

    async def send_total_orders(self, group_name, num):

        await self.channel_layer.group_send(group_name, {
            "type": 'send_notify',
            'notify_type': 'total_orders',
            'num': num,
        })

    async def send_notify_about_new_order(self, group_name):
        await self.channel_layer.group_send(group_name, {"type": 'send_notify', 'notify_type': 'new_order', 'num': 1})

    async def send_total_teams(self, group_name, num):

        await self.channel_layer.group_send(group_name, {
            "type": 'send_notify',
            'notify_type': 'total_teams',
            'num': num,
        })

    async def send_notify_about_new_team(self, group_name):
        # async_to_sync(self.channel_layer.group_send)(group_name, {"type": "send_notify", 'notify_type': 'new_team', 'num': 1})

        await self.channel_layer.group_send(group_name, {"type": 'send_notify', 'notify_type': 'new_team', 'num': 1})

    async def send_notify(self, event):
        await self.send(text_data=json.dumps({"num": event['num'], "type": event["notify_type"]}))


