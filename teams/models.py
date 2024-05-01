from django.db import models
from profile.models import CustomUser,Allowance,City,Qualify,Specialisations,Status



class Team(models.Model):
    brigadir = models.ForeignKey(CustomUser, verbose_name="Мастер", on_delete=models.CASCADE, related_name='team_master',
                               null=True, blank=True)
    coworker = models.ForeignKey(CustomUser, verbose_name="Заказ", on_delete=models.CASCADE,
                                 related_name='team_user', null=True, blank=True)
    specialisation = models.ForeignKey(Specialisations, on_delete=models.DO_NOTHING, verbose_name='Специализация', null=True, blank=True)
    status = models.ForeignKey(Status, verbose_name='Статус', on_delete=models.DO_NOTHING, null=True, blank=True)
    qualify = models.ForeignKey(Qualify, verbose_name="Квалификация", on_delete=models.DO_NOTHING, null=True,
                                blank=True, )
    city = models.ForeignKey(City, verbose_name="Город", on_delete=models.DO_NOTHING, null=True, blank=True,)
    allow = models.ManyToManyField(Allowance, verbose_name='Разрешения', blank=True)
    timestamp = models.DateTimeField(verbose_name='Время', auto_now_add=True)


    def __str__(self):
        return self.brigadir.username
    class Meta:
        verbose_name = 'Бригада'
        verbose_name_plural = 'Бригада'


