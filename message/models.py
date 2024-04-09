from django.db import models
from django.conf import settings


class Message(models.Model):
    sender = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender} -> {self.receiver}: {self.content}"

# class Message(models.Model):
#     sender_id = models.IntegerField(verbose_name="id Отправителя", null=True, blank=True)
#     receiver_id = models.IntegerField(verbose_name="id Получателя", null=True, blank=True)
#     content = models.TextField(verbose_name="Сообщение", null=True, blank=True)
#     timestamp = models.DateTimeField(verbose_name="Дата и время", auto_now_add=True)
#
#     def __str__(self):
#         return 'Сообщения всех пользователей'
