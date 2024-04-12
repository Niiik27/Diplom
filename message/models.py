from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='Отправитель',  on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL,verbose_name='Получатель',  on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField(verbose_name='Текст', blank=True, null=True )
    status = models.BooleanField(verbose_name='Статус прочтения', default=False, help_text='Статус прочтения')
    timestamp = models.DateTimeField(verbose_name='Время', auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"
