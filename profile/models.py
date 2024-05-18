from django.db import models
from django.contrib.auth.models import AbstractUser

import APP_NAMES


class CustomUser(AbstractUser):
    photo_url = models.CharField('Ссылка на фото', max_length=256, null=True, blank=True)
    image = models.ImageField('Изображение', upload_to=f'{APP_NAMES.PROFILE[APP_NAMES.NAME]}/image', null=True, blank=True)
    first_name = models.CharField(verbose_name='Имя', max_length=250, blank=True, null=True)
    last_name = models.CharField(verbose_name='Фамилия', max_length=250, blank=True, null=True)
    email = models.CharField(verbose_name="Почта", max_length=254, null=True, blank=True)
    birth = models.DateField(verbose_name="Дата рождения", blank=True, null=True)
    about = models.TextField(verbose_name="О себе", blank=True, null=True)
    specialisation = models.ManyToManyField('Specialisations', verbose_name='Специализация', blank=True)
    social_list = models.ManyToManyField('SocialList', verbose_name='Соцсети',blank=True)
    status = models.ForeignKey('Status', verbose_name='Статус', on_delete=models.DO_NOTHING, null=True, blank=True)
    qualify = models.ForeignKey('Qualify',verbose_name="Квалификация", on_delete=models.DO_NOTHING, null=True,
                                blank=True, )
    allow = models.ManyToManyField('Allowance', verbose_name='Разрешения',blank = True)


    def __str__(self):
        return f'{self.username}'

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

class City(models.Model):
    name = models.CharField(verbose_name="Город", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Город'
        verbose_name_plural = 'Города'


class Address(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='address')
    city = models.ForeignKey(City, verbose_name='Город', on_delete=models.DO_NOTHING, null=True, blank=True)
    district = models.CharField(verbose_name="Район", max_length=100, null=True, blank=True)
    street = models.CharField(verbose_name="Улица", max_length=100, null=True, blank=True)
    house_number = models.CharField(verbose_name="Номер дома", max_length=100, null=True, blank=True)
    apartment = models.IntegerField(verbose_name="Квартира", null=True, blank=True)
    postal_code = models.IntegerField(verbose_name="Индекс", null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Адрес'
        verbose_name_plural = 'Адреса'


class UserSocial(models.Model):
    user = models.ForeignKey('CustomUser', on_delete=models.CASCADE, related_name='social_user', null=True, blank=True)
    link = models.URLField(verbose_name="Профиль в соцсети", null=True, blank=True)
    social_id = models.IntegerField(verbose_name="id соцсети", null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Социальная сеть'
        verbose_name_plural = 'Ссылки на социальные сети'


class SocialList(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название соцсети")
    icon_path = models.CharField('Путь к иконке', max_length=255, blank=True)
    template_string = models.CharField('Домен соцсети', max_length=255, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список всех соцсетей'
        verbose_name_plural = 'Список всех соцсетей'


class MessengerList(models.Model):
    name = models.CharField(max_length=100, verbose_name="Название мессенджера")
    icon_path = models.CharField('Путь к иконке', max_length=255, blank=True)
    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список всех мессенджеров'
        verbose_name_plural = 'Список всех мессенджеров'


class Contacts(models.Model):
    user = models.OneToOneField(CustomUser, verbose_name="Пользователь", on_delete=models.CASCADE,
                                related_name='user_contacts')
    phone = models.CharField(verbose_name="Телефон", max_length=254, null=True, blank=True)
    messenger = models.ManyToManyField('MessengerList', verbose_name="Мессенджеры", related_name='user_messenger',
                                       blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Контактная информация'
        verbose_name_plural = 'Контакты'


class Allowance(models.Model):
    # user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='allowance')
    allow = models.CharField(verbose_name="Разрешение", max_length=254, null=True, blank=True)

    def __str__(self):
        return self.allow

    class Meta:
        verbose_name = 'Разрешение'
        verbose_name_plural = 'Разрешения'


class Specialisations(models.Model):
    specialisation = models.CharField(verbose_name="Специализация", max_length=254, null=True, blank=True)

    def __str__(self):
        return self.specialisation

    class Meta:
        verbose_name = 'Специализация'
        verbose_name_plural = 'Специализация'


class Fine(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='fine')
    fine = models.CharField(verbose_name="Штрафы", max_length=254, null=True, blank=True)

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Штраф'
        verbose_name_plural = 'Штрафы'


class Status(models.Model):
    name = models.CharField(verbose_name="Статус", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список статусов'
        verbose_name_plural = 'Список статусов'


class Qualify(models.Model):
    name = models.CharField(verbose_name="Квалификация", max_length=200)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Список квалификаций'
        verbose_name_plural = 'Список квалификаций'


# class Skills(models.Model):
#     user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='skills')
#     skill = models.CharField(verbose_name="Навык", max_length=254, null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         verbose_name = 'Навык'
#         verbose_name_plural = 'Навыки'



# class Card(models.Model):
#     user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='card')
#
#     number = models.CharField(verbose_name="Номер", max_length=20, null=True, blank=True)
#     date = models.DateField(verbose_name="Действительна до", max_length=5, null=True, blank=True)
#     cvs = models.CharField(verbose_name="Код с обратной стороны карты", max_length=3, null=True, blank=True)
#
#     def __str__(self):
#         return self.user.username
#
#     class Meta:
#         verbose_name = 'Карта'
#         verbose_name_plural = 'Данные банковской карты'





