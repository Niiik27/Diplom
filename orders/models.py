from django.db import models
from profile.models import CustomUser


class Order(models.Model):
    customer = models.ForeignKey(CustomUser, verbose_name="Заказ", on_delete=models.CASCADE, related_name='order_customer', null=True,blank=True)
    master = models.ForeignKey(CustomUser, verbose_name="Мастер", on_delete=models.CASCADE, related_name='order_master', null=True,blank=True)
    confirmed = models.BooleanField(verbose_name="Подтверждение сотрудничества",default=False)
    has_brigade = models.BooleanField(verbose_name="Бригада укомплектована",default=False)
    timestamp = models.DateTimeField(verbose_name='Время', auto_now_add=True)


