import json
import os

from django.apps import apps
from django.db.models.signals import post_migrate, post_save, pre_init
from django.contrib import admin
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.templatetags.static import static

import APP_NAMES
from _Brigada73 import settings
from message.models import Message
from .models import *
from django.contrib.admin import StackedInline, TabularInline


class AddressInline(StackedInline):
    model = Address
    extra = 0
    max_num = 1
    can_delete = False


class UserSocialInline(StackedInline):
    model = UserSocial
    extra = 0
    # max_num = 5
    fields = 'link',


# class AllowanceInline(StackedInline):
#     model = Allowance
#     extra = 0
#     # max_num = 5
#     fields = 'allow',


# class SkillsInline(StackedInline):
#     model = Skills
#     extra = 0
#     # max_num = 5
#     fields = 'skill',

# class SpecialisationsInline(StackedInline):
#     model = Specialisations
#     extra = 0
#     # max_num = 5
#     fields = 'specialisation',


class FineInline(StackedInline):
    model = Fine
    extra = 0
    # max_num = 5
    fields = 'fine',


class CardInline(StackedInline):
    model = Card
    extra = 0
    # max_num = 5
    fields = 'number', 'date', 'cvs'


class ContactsInline(TabularInline):
    model = Contacts
    extra = 0
    max_num = 1
    fields = 'phone', 'messenger',


class NotificationsInline(StackedInline):
    model = Notifications
    extra = 0
    # max_num = 1
    fields = 'notification', 'new',


class PortfolioInline(StackedInline):
    model = Portfolio
    extra = 0
    # max_num = 1
    fields = 'portfolio',


@admin.register(CustomUser, site=admin.site)
class CustomUserAdmin(admin.ModelAdmin):
    # list_display = ('username', 'first_name', 'last_name', 'birth','status',)
    # search_fields = ('username', 'first_name', 'last_name', 'birth','status',)
    inlines = [CardInline, AddressInline, ContactsInline, UserSocialInline,
               FineInline, NotificationsInline, PortfolioInline]
    fieldsets = (
        ('Основное', {'fields': ('username',)}),
        ('Персональная информация',
         {'fields': ('first_name', 'last_name', 'email', 'status', 'qualify', 'specialisation')}),
        ('Важные даты', {'fields': ('last_login', 'date_joined')}),
    )


@admin.register(SocialList, site=admin.site)
class SocialListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(MessengerList, site=admin.site)
class MessengerListAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Qualify, site=admin.site)
class QualifyAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)

@admin.register(Status, site=admin.site)
class StatusAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Allowance, site=admin.site)
class AllowanceAdmin(admin.ModelAdmin):
    list_display = ('allow',)
    search_fields = ('allow',)


@admin.register(Specialisations, site=admin.site)
class SpecialisationsAdmin(admin.ModelAdmin):
    list_display = ('specialisation',)
    search_fields = ('specialisation',)


# @admin.register(Notifications, site=admin.site)
# class NotificationsAdmin(admin.ModelAdmin):
#     list_display = ('notification', 'new')
#     search_fields = ('notification', 'new')

def parse_social_list(social_name:str):
    data = social_name.split("-")
    res={}
    res['name'] = data[0]
    domains = data[1].split('.')
    domain_names = domains.pop(0).split('_')
    res['domain_names'] = domain_names
    res['domains'] = domains
    return res

@receiver(post_migrate)
def create_external_lists(sender, **kwargs):
    """
    Функция, которая будет вызываться после миграции приложения.
    Создает объекты SocialList с названиями социальных сетей.
    """

    SocialList = apps.get_model(APP_NAMES.PROFILE[APP_NAMES.NAME], 'SocialList')
    if kwargs.get('app_config').name == APP_NAMES.PROFILE[APP_NAMES.NAME]:

        messenger_image_dir = 'static/messengers_ico'
        messenger_image_files = [f for f in os.listdir(messenger_image_dir) if os.path.isfile(os.path.join(messenger_image_dir, f))]
        messenger_image_names = [os.path.splitext(f)[0] for f in messenger_image_files]
        for messenger_name in messenger_image_names:
            MessengerList.objects.get_or_create(name=messenger_name.capitalize(), icon_path=f'messengers_ico/{messenger_name}.png')

        # MessengerList.objects.get_or_create(name='WhatsApp')
        # MessengerList.objects.get_or_create(name='Telegram')
        # MessengerList.objects.get_or_create(name='Viber')

        social_image_dir = 'static/social_ico'
        social_image_files = [f for f in os.listdir(social_image_dir) if os.path.isfile(os.path.join(social_image_dir, f))]
        social_image_names = [os.path.splitext(f)[0] for f in social_image_files]

        for social_name in social_image_names:
            params = parse_social_list(social_name)
            SocialList.objects.get_or_create(name=params.pop('name').capitalize(), icon_path=f'social_ico/{social_name}.png',template_string=json.dumps(params, ensure_ascii=False))

        # SocialList.objects.get_or_create(name='Вконтакте', icon_path=static(f'social_ico/vk.png'))
        # SocialList.objects.get_or_create(name='Одноклассники')
        # SocialList.objects.get_or_create(name='Инстаграмм')
        # SocialList.objects.get_or_create(name='Фасебук')

        City.objects.get_or_create(name='Ульяновск')
        City.objects.get_or_create(name='Димитровград')
        City.objects.get_or_create(name='Казань')
        City.objects.get_or_create(name='Самара')
        City.objects.get_or_create(name='Самара')
        City.objects.get_or_create(name='Тольяти')
        City.objects.get_or_create(name='Сызрань')
        City.objects.get_or_create(name='Оренбург')
        City.objects.get_or_create(name='Москва')
        City.objects.get_or_create(name='Питер')

        Status.objects.get_or_create(name='Новичок')
        Status.objects.get_or_create(name='Строитель')
        Status.objects.get_or_create(name='Прораб')
        Status.objects.get_or_create(name='Заказчик')

        Qualify.objects.get_or_create(name='Дешево')
        Qualify.objects.get_or_create(name='Средне')
        Qualify.objects.get_or_create(name='Дорого')
        Qualify.objects.get_or_create(name='Очень дорого')

        Specialisations.objects.get_or_create(specialisation='Плиточник')
        Specialisations.objects.get_or_create(specialisation='Каменщик')
        Specialisations.objects.get_or_create(specialisation='Монтажник')
        Specialisations.objects.get_or_create(specialisation='Отделочник')
        Specialisations.objects.get_or_create(specialisation='Электрик')
        Specialisations.objects.get_or_create(specialisation='Сантехник')
        Specialisations.objects.get_or_create(specialisation='Грузчик')

        Allowance.objects.get_or_create(allow ='Права категории Б')
        Allowance.objects.get_or_create(allow ='Права категории Ц')
        Allowance.objects.get_or_create(allow ='Права категории Д')
        Allowance.objects.get_or_create(allow ='Сертификат промышленного альпиниста')
        Allowance.objects.get_or_create(allow ='Сертификат электрика')
        Allowance.objects.get_or_create(allow ='Сертификат сантехника')
        Allowance.objects.get_or_create(allow ='Права на управление краном')


@receiver(post_save, sender=CustomUser)
def create_additional_models(sender, instance, created, **kwargs):
    if created:
        Address.objects.create(user=instance)
        Contacts.objects.create(user=instance)
        Card.objects.create(user=instance)

        # initial_message = Message.objects.create(sender_id=instance, receiver_id=instance, content="Welcome to our platform!")