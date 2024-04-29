from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer
from django.apps import apps
import json


from django.db.models import Count
from django.db import models
from django.db.models import Q

from Print import Print


chat_users = set()
online_users = set()


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


def get_chat_channel_name(user_id):
    return f"chanel_{user_id}"


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
        group_name = get_chat_channel_name(user.id)
        await self.channel_layer.group_add(
            group_name,
            self.channel_name
        )
        chat_users.add(group_name)
        await self.accept()

    async def disconnect(self, close_code):
        group_name = get_chat_channel_name(self.scope['user'].id)
        chat_users.discard(group_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print("self.scope", self.scope)
        message_type = text_data_json['type']

        content = text_data_json['message']
        receiver_id = text_data_json['channel_name']
        channel_name = get_chat_channel_name(receiver_id)
        receiver_name = text_data_json['receiver_name']
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
            if channel_name in chat_users:
                await self.send_message(sender_name, receiver_name, channel_name, content, message_type, message_id)
            if channel_name in online_users:
                await self.send_notify_about_new_message(channel_name)

        elif message_type == 'history':
            messages = await self.get_messages(sender, receiver)
            await self.send_history(messages)

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

    async def send_message(self, sender_name, receiver_name, channel_name, message, message_type, msg_id):
        await self.channel_layer.group_send(channel_name, {
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
        message_model = apps.get_model(app_label='message', model_name='Message')
        unread_messages = message_model.objects.filter(receiver=me, status=False)
        unread_messages_count = unread_messages.count()
        return unread_messages_count

    async def send_notify_about_new_message(self, channel_name):
        await self.channel_layer.group_send(channel_name, { "type": 'send_notify','notify_type': 'new_msg','num': 1,})
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
            Print.purpur("Подключился пользователь из браузера",await self.get_status_name())
            user_status = await self.get_status_name()
            if user_status == "Мастер":# Еще нужны оповещения для простых строителей. это все статусы до мастера.
                # Мастерам и доступна инфа о заказах но недоступна о бригадах.
                # То есть они не могут наняться в бригаду в качестве работника. Они сами должжны создавать бригаду
                Print.purpur("Мастер подключлся из браузера")
                group_name = await get_order_channel_name(self.user)
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
                online_users.add(group_name)
                num = await self.get_total_orders()
                await self.send_total_orders(group_name,num)
            elif user_status not in ("Мастер", "Прораб", "Заказ"):#Все кроме этих должны узнать есть ли новые бригады
                Print.purpur("Строитель подключлся из браузера")
                group_name = await get_team_channel_name(self.user)
                await self.channel_layer.group_add(
                    group_name,
                    self.channel_name
                )
                online_users.add(group_name)
                num = await self.get_total_orders()
                await self.send_total_orders(group_name, num)

            #Сообщения будут доступны всем статусам
            group_name = get_chat_channel_name(self.user.id)
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
            online_users.add(group_name)

            num = await self.get_total_unread_num()
            Print.yellow(num)
            await self.send_total_messages_notify(num)
            await self.accept()


        else:#Анонимный пользователь получается из за питоновского клиента. его можно лишь подключить
            Print.purpur("Подключился питонский клиент. Для того что бы разослать оповещение об обновлении модели")
            await self.accept()#это выполнимо для обоих исходов  но так понятнее для кого подключениие

    async def disconnect(self, close_code):
        group_name = get_chat_channel_name(self.scope['user'].id)
        online_users.discard(group_name)
        await self.close()

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        Print.green("text_data_jsontext_data_jsontext_data_json", text_data_json)
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
        elif notify_type == 'from_server_notify_new_order':#Это приходит строго из питон клиента, это иммитация коннекта
            Print.purpur("Питонский клиент после подключения выслал свой id что бы авторизоваться рассылки ордеров")
            user_id = text_data_json['user_id']
            self.user = await self.get_user_by_id(user_id)
            Print.purpurs("Теперь он", self.user)
            group_name = await get_order_channel_name(self.user)
            Print.purpur("И он находится в групппе", group_name)
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
            # num = await self.get_total_orders()
            Print.blue("Питонский клиент отправляет инфо о том что он увеличил количество заказов на 1")
            # await self.send_total_orders(group_name,num)
            await self.send_notify_about_new_order(group_name)# Пусть клиент сам считает количество воходящих
        elif notify_type == 'from_server_notify_new_team':#Это приходит строго из питон клиента, это иммитация коннекта
            Print.purpur("Питонский клиент после подключения выслал свой id что бы авторизоваться рассылки бригад")
            user_id = text_data_json['user_id']
            self.user = await self.get_user_by_id(user_id)
            Print.purpurs("Теперь он", self.user)
            group_name = await get_team_channel_name(self.user)
            Print.purpur("И он находится в групппе", group_name)
            await self.channel_layer.group_add(
                group_name,
                self.channel_name
            )
            num = await self.get_total_teams()
            Print.blue("Питонский клиент отправляет инфо о том что он увеличил количество бригад на 1")
            # await self.send_total_orders(group_name,num)
            # await self.send_notify_about_new_team(group_name)# Пусть клиент сам считает количество воходящих

    @database_sync_to_async
    def get_status_name(self):
        # status_model = apps.get_model(app_label='profile', model_name='Status')
        return self.user.status.name
    @database_sync_to_async
    def get_user_by_id(self, user_id):
        custom_user_model = apps.get_model(app_label='profile', model_name='CustomUser')
        return custom_user_model.objects.get(pk=user_id)

    @database_sync_to_async
    def get_total_orders(self):

        order_model = apps.get_model(app_label='orders', model_name='Order')
        new_orders = order_model.objects.filter(confirmed=False)
        customer_ids = []
        for order in new_orders:
            customer = order.customer
            if customer.address.city == self.user.address.city:
                customer_ids.append(customer)
        num_orders = len(customer_ids)
        return num_orders

    @database_sync_to_async
    def get_total_teams(self):#Это вызовется когда я создам бригаду или отредактирую ее

        #brigadir, coworker, specialisation, status, qualify, city, allow, confirmed
        custom_user_model = apps.get_model(app_label='profile', model_name='CustomUser')
        team_model = apps.get_model(app_label='team', model_name='Team')#нахожу свою бригаду, она может быть только одна, для новой бригады требуется новый аккаунт
        my_new_team = team_model.objects.filter(brigadir=self.user, coworker=None)
        # brigade_city = my_new_team.first().city

        for specialist in my_new_team:
            specialisation = specialist.specialisation
            # allow_filter = Q(allow__id__in=specialisation.allow)
            candidate = custom_user_model.objects.filter(
                # allow_filter,
                address__city=specialist.city,
                status = specialist.status,
                qualify = specialist.qualify,
                specialisation__in=[specialisation],
                )

            for allow in specialist.allow.all():
                candidate &= candidate.filter(allow=allow)


            print("my_new_team", candidate)







        # my_new_team = team_model.objects.filter(brigadir=self.user, coworker=None).first()
        # specialisation = my_new_team.specialisation.specialisation


        # Получаем бригаду бригадира


        #     specialisations = my_new_team.specialisation
        #     Print.green("Удалось отфильтровать пользователей", specialisations.specialisation)
        #     candidate = custom_user_model.objects.filter(city=my_new_team.city, specialisation__in=my_new_team.specialisation.all())
        #
        #
        #
        # # new_teams = team_model.objects.filter(city=self.user.address.city, coworker=None,#Обязательные требования
        # #                                       specialisation__in=self.user.specialisation.all(), status=self.user.status,
        # #                                       qualify=self.user.qualify)
        #
        # # matching_users = self.user_model.objects.filter(
        # #     Q(allow__in=brigade_allowances) &
        # #     Q(other_criteria_here)
        # # ).distinct()
        #

        #
        # if not new_teams:#Смягчаем условия выборки - убираем статус, потому что это лишь самооценка.
        #     Print.red("Не нашлось пользователей со строгим соответствием. Смягчили поиск - исключили статус")
        #     new_teams = team_model.objects.filter(city=self.user.address.city, coworker=None,  # Обязательные требования
        #                                           specialisation=self.user.specialisation,
        #                                           qualify=self.user.qualify, allow=self.user.allow)
        #
        #     if not new_teams:#Смягчаем условия выборки - убираем квалификацию, это предмет для торга и ответственности
        #         Print.red("Не нашлось пользователей без статуса Смягчили поиск - исключили квалификацию")
        #         new_teams = team_model.objects.filter(city=self.user.address.city, coworker=None,  # Обязательные требования
        #                                               specialisation=self.user.specialisation, allow=self.user.allow)
        #         # brigade_allowances = team_model.allow.all()
        #         # matching_users = self.user.objects.annotate(
        #         #     matching_allowances=Count('profile__allow', filter=models.Q(profile__allow__in=brigade_allowances))
        #         # ).filter(matching_allowances=len(brigade_allowances))
        #         # Print.greens("matching_users",matching_users)
        #
        #
        #
        #
        #         if not new_teams:  # Дальше видимо нельзя смягчать
        #             # потому что под эти требования нельзя подстрроиться, но для удобств разработки придется смягчить
        #             #Исключаю разрешения
        #             Print.purpur("Не нашлось пользователей без квалификации Смягчили поиск - исключили разрешения")
        #             new_teams = team_model.objects.filter(city=self.user.address.city, coworker=None,  # Обязательные требования
        #                                                   specialisation=self.user.specialisation)
        #             if not new_teams:  # Это смягчение очень глупое, но так удобней
        #                 Print.purpur("Не нашлось пользователей без разрешений Смягчили поиск - исключили специализацию")
        #                 new_teams = team_model.objects.filter(city=self.user.address.city, coworker=None)
        #                 if not new_teams:  # Еще более идиотское смягчение
        #                     Print.purpur("Не нашлось пользователей без специализации Смягчили поиск - исключили разрешения")
        #                     new_teams = team_model.objects.filter(coworker=None)
        #                     if not new_teams:  # Наивысшая степень дибилизма, зато наверняка я что то увижу браузере
        #                         Print.purpur("Вообше исключили все фильтры")
        #                         new_teams = team_model.objects.all()


        # customer_ids = []
        # for team in new_teams:
        #     customer = team.customer
        #     if customer.address.city == self.user.address.city:
        #         customer_ids.append(customer)
        # num_orders = len(customer_ids)
        return 1

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

    async def send_total_messages_notify(self, num):
        await self.channel_layer.group_send(get_chat_channel_name(self.scope['user'].id), {
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
        await self.channel_layer.group_send(group_name, {"type": 'send_notify','notify_type': 'new_order','num': 1})

    async def send_total_teams(self, group_name, num):

        await self.channel_layer.group_send(group_name, {
            "type": 'send_notify',
            'notify_type': 'total_teams',
            'num': num,
        })
    async def send_notify_about_new_team(self, group_name):
        await self.channel_layer.group_send(group_name, {"type": 'send_notify','notify_type': 'new_team','num': 1})
    async def send_notify(self, event):
        Print.purpur(event)
        await self.send(text_data=json.dumps({"num": event['num'], "type": event["notify_type"]}))

