from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Max
from django.db.models.signals import post_save
from django.dispatch import receiver

from main.models import Competition

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Dogs(models.Model):
    """Модель собаки привязка к юзеру pk"""

    RKF = 'RKF'
    PED1 = 'SKOR'

    PEDIGREE = (
        (RKF, 'РКФ'),
        (PED1, 'СКОР'),
    )

    SUKA ='Сука'
    KOBEL ='Кобель'

    FEMALE = (
        (SUKA, 'Сука'),
        (KOBEL, 'Кобель')
    )

    id_dog = models.CharField(max_length=7, verbose_name='Id собаки', unique=True)

    dog_name = models.CharField(max_length=20, verbose_name='Кличка по родословной*', **NULLABLE)
    dog_avatar = models.ImageField(upload_to='dogs_photo', verbose_name='Аватар собаки (не более 1мб, 600х600px)', **NULLABLE)
    home_name = models.CharField(max_length=20, verbose_name='Домашняя кличка*', **NULLABLE)

    date_borne = models.DateField(verbose_name='Дата рождения', **NULLABLE)
    breed_dog = models.CharField(max_length=20, verbose_name='Порода собаки*')
    pedigree_dog = models.CharField(max_length=20, choices=PEDIGREE, verbose_name='Родословная', **NULLABLE)

    other_federation = models.CharField(max_length=20, verbose_name='Другая федерация', **NULLABLE)
    pedigree_file = models.FileField(verbose_name='Родословная - файл', **NULLABLE)
    number_chip = models.CharField(max_length=20, verbose_name='Номер чипа', **NULLABLE)

    brand_dog = models.CharField(max_length=20, verbose_name='Клеймо', **NULLABLE)  # уточнить тип поля

    female_dog = models.CharField(max_length=20, choices=FEMALE, verbose_name='Пол собаки*', **NULLABLE)
    number_bookwork = models.IntegerField(verbose_name='№ Рабочей книжки', **NULLABLE)

    # Зависимость от создателя
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Владелец Собаки',
                              **NULLABLE)
    father_name = models.CharField(max_length=50, verbose_name='Имя отца по родословной', **NULLABLE)
    father_pedigree_number = models.CharField(max_length=50, verbose_name='Номер родословной отца', **NULLABLE)
    father_titles = models.TextField(verbose_name='Титулы отца', **NULLABLE)
    mother_name = models.CharField(max_length=50, verbose_name='Имя матери по родословной', **NULLABLE)
    mother_pedigree_number = models.CharField(max_length=50, verbose_name='Номер родословной матери', **NULLABLE)
    mother_titles = models.TextField(verbose_name='Титулы матери', **NULLABLE)
    ex_count_ro_dety = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-дети', **NULLABLE)
    ex_count_ro_shenki = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-щенки', **NULLABLE)
    ex_count_ro_debut = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-дебют', **NULLABLE)
    ex_count_ro_veterany = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-ветераны', **NULLABLE)
    ex_count_ro_1 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-1', **NULLABLE)
    ex_count_ro_2 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-2', **NULLABLE)
    ex_count_ro_3 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-3', **NULLABLE)
    ex_count_ro_4 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-4(мастера)', **NULLABLE)

    def save(self, *args, **kwargs):
        if not self.id_dog:
            last_dog = Dogs.objects.aggregate(Max('id_dog'))['id_dog__max']
            if last_dog is None:
                self.id_dog = "DG00001"
            else:
                last_number = int(last_dog[2:])
                new_number = last_number + 1
                self.id_dog = f"DG{new_number:05}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.dog_name} (ID: {self.id_dog})"

    class Meta:
        verbose_name = 'Собака'
        verbose_name_plural = 'Собаки'


# Модель юзера с расширяющими полями
class User(AbstractUser):
    """Модель юзера"""
    username = models.CharField(max_length=150, unique=True, verbose_name='Ваш ник нейм', **NULLABLE)
    email = models.EmailField(unique=True, verbose_name='почта')
    middle_name = models.CharField(max_length=100, verbose_name='Отчество', blank=True, null=True)
    phone = models.CharField(max_length=11, verbose_name='телефон (обяз)')
    avatar = models.ImageField(upload_to='users', verbose_name='аватар', **NULLABLE)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    # дополнительные поля Юзера, доступны только после авторизации
    user_tegram = models.CharField(max_length=20, verbose_name='Телеграм', **NULLABLE)
    user_whatsup = models.CharField(max_length=20, verbose_name='Ватсап', **NULLABLE)
    user_vk = models.CharField(max_length=20, verbose_name='ВК', **NULLABLE)

    user_other = models.CharField(max_length=20, verbose_name='Другие данные', **NULLABLE)
    # user_avatar = models.ImageField(verbose_name='Аватар', **NULLABLE)
    user_town = models.CharField(max_length=20, verbose_name='Город', **NULLABLE)

    user_club = models.CharField(max_length=20, verbose_name='Клуб', **NULLABLE)
    user_trainer = models.CharField(max_length=20, verbose_name='Тренер', **NULLABLE)
    user_about = models.TextField(max_length=500, verbose_name='О себе', **NULLABLE)

    user_hide_info = models.BooleanField(default=False, verbose_name='Скрыть инфо, по умол.открыто')

    check_info = models.BooleanField(default=False, verbose_name='Проверка инфо админом')
    is_active = models.BooleanField(default=False, verbose_name='Пользователь активен')
    email_confirm_key = models.CharField(max_length=20, verbose_name='Ключ верификации', **NULLABLE)

    org_status = models.BooleanField(default=False, verbose_name='Статус организатора')
    get_check = models.BooleanField(default=False,
                                    verbose_name='Запрос на организатора отправлен')  # запрос на подтверждение адмионм (письмо)
    ex_count_ro_dety = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-дети', **NULLABLE)
    ex_count_ro_shenki = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-щенки', **NULLABLE)
    ex_count_ro_debut = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-дебют', **NULLABLE)
    ex_count_ro_veterany = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-ветераны', **NULLABLE)
    ex_count_ro_1 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-1', **NULLABLE)
    ex_count_ro_2 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-2', **NULLABLE)
    ex_count_ro_3 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-3', **NULLABLE)
    ex_count_ro_4 = models.IntegerField(default=0, verbose_name='Количество "отлично" в РО-4(мастера)', **NULLABLE)

    class Meta:
        verbose_name = 'Юзер'
        verbose_name_plural = 'Юзеры'

