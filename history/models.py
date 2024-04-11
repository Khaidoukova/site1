from datetime import timedelta

from django.conf import settings
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator

from django.db import models


# Create your models here.
class History(models.Model):
    """ Модель истории выступлений (в соответствие с рабочей книжкой)"""
    CLASSES = (
        ('ro_dety', 'РО-Дети'),
        ('ro_shenki', 'РО-Щенки'),
        ('ro_debut', 'РО-Дебют'),
        ('ro_veterany', 'РО-Ветераны'),
        ('ro_1', 'РО-1'),
        ('ro_2', 'РО-2'),
        ('ro_3', 'РО-3'),
        ('ro_4', 'РО-4 (мастер)')
    )

    GRADES = (
        ('excellent', 'Отлично'),
        ('very_good', 'Очень хорошо'),
        ('good', 'Хорошо'),
        ('not_enough', 'Недостаточно'),
    )
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                             verbose_name='Владелец собаки', null=True, blank=True)
    class_dog = models.CharField(max_length=20, choices=CLASSES, verbose_name='Класс собаки', null=True, blank=True)
    # first_name = models.ForeignKey(User.first_name, on_delete=models.CASCADE, verbose_name='Имя')
    competition = models.CharField(max_length=20, verbose_name='Название соревнования', null=True, blank=True)
    date_competition = models.DateField(verbose_name='Дата соревнования', null=True, blank=True)
    track1_points = models.IntegerField(verbose_name='Количество очков, трасса 1', null=True, blank=True)
    track1_grade = models.CharField(max_length=20, choices=GRADES,verbose_name='Оценка собаки, трасса 1', null=True, blank=True)
    track1_time = models.DurationField(validators=[MaxValueValidator(timedelta(minutes=60))],
                                       verbose_name='Время на трассе 1', null=True, blank=True)
    track1_place = models.IntegerField(verbose_name='Место, трасса 1', null=True, blank=True)

    track2_points = models.IntegerField(verbose_name='Количество очков, трасса 2', null=True, blank=True)
    track2_grade = models.CharField(max_length=20, choices=GRADES, verbose_name='Оценка собаки, трасса 2', null=True, blank=True)
    track2_time = models.DurationField(validators=[MaxValueValidator(timedelta(minutes=60))],
                                       verbose_name='Время на трассе 2', null=True, blank=True)
    track2_place = models.IntegerField(verbose_name='Место, трасса 2', null=True, blank=True)

    def __str__(self):
        return self.user.email
    class Meta:
        verbose_name = 'История соревнования'
        verbose_name_plural = 'История соревнований'
