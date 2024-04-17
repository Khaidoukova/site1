from django.db import models

from users.models import User
NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Trainer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    trainer_title = models.CharField(max_length=50, verbose_name='Заголовок сообщения', **NULLABLE)
    trainer_text = models.CharField(max_length=250, verbose_name='Текст сообщения', **NULLABLE)
    trainer_banner = models.ImageField(upload_to='trainer_banner', verbose_name='Картинка баннер', **NULLABLE)

    def __str__(self):
        return f'{self.trainer_title}, опубликовал {self.user}'

    class Meta:
        verbose_name = "Сообщение тренера"
        verbose_name_plural = "Сообщение тренера"
