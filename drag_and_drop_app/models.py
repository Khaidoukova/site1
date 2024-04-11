from django.db import models

from main.models import Competition
from users.models import User

NULLABLE = {'blank': True, 'null': True}

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


class Image(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь с юзером

    file_link = models.CharField(max_length=200, verbose_name='Ссылка на трассу', **NULLABLE)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    image_class_com = models.CharField(max_length=20, choices=CLASSES, verbose_name='Класс участия', **NULLABLE)

    competition = models.ForeignKey(Competition, on_delete=models.CASCADE, **NULLABLE, verbose_name='Соревнование')  # связь с соревнованиями

    image_list = models.TextField(max_length=500, verbose_name='Список знаков')

    image_data = models.TextField(**NULLABLE)  # данные изображения в формате base64
    image_name = models.CharField(max_length=255, **NULLABLE)  # имя изображения

    def __str__(self):
        return self.image_name

    class Meta:
        verbose_name = 'Трасса'
        verbose_name_plural = 'Трассы'
