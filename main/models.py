from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator

NULLABLE = {'blank': True, 'null': True}


def validate_image_size(image):
    # Проверяем размер изображения (в байтах)
    max_size = 1024 * 1024  # 1MB
    if image.size > max_size:
        raise ValidationError("Слишком большой файл. Максимальный размер файла - 1МБ.")


# Create your models here.
class Competition(models.Model):
    """Модель соревнования"""

    RULES = (
        ('Mankovoi', 'СПб, А. Маньковой, 2024'),
        ('FCI', 'FCI, 2024'),
        ('Over', 'СПб (А. Маньковой), 2018')
    )

    PLAY_GROUND = (
        ('Open', 'Открытая'),
        ('Close', 'Закрытая'),
        ('Weather', 'По погоде')
    )

    name_competition = models.CharField(max_length=20, verbose_name='Название соревнования')
    image_competition = models.ImageField(upload_to='banner_competition', verbose_name='Баннер соревнования (<1мб, 600х600 px)',
                                          validators=[validate_image_size, FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png'])], **NULLABLE)
    date_competition = models.DateField(verbose_name='Дата соревнования', **NULLABLE)

    pre_date_competition = models.CharField(max_length=40, verbose_name='Предполагаемый период соревновний', **NULLABLE)
    start_date_competition = models.DateField(verbose_name='Дата начала регистрации', **NULLABLE)
    end_date_competition = models.DateField(verbose_name='Дата окончания регистарции', **NULLABLE)

    send_message_start_competition = models.BooleanField(default=False, verbose_name='Уведомление о начале регистрации (организатору)')
    invitation_competition = models.BooleanField(default=False, verbose_name='Разослать приглашения')

    rules_competition = models.CharField(max_length=20, choices=RULES, verbose_name='Правила')  #радио кнопка выбор из 3-х

    # Статусы соревнования
    status_not_official = models.BooleanField(default=False, verbose_name='Неофициальные (не в графике ркф)')
    status_RKF = models.BooleanField(default=False, verbose_name='В графике РКФ')
    status_open = models.BooleanField(default=False, verbose_name='Открытое')
    status_Tests = models.BooleanField(default=False, verbose_name='Испытания')
    status_Quality = models.BooleanField(default=False, verbose_name='Квалификационные соревнования')
    status_Certificate = models.BooleanField(default=False, verbose_name='Сертификатные CACROb и CACIROb')
    status_Training = models.BooleanField(default=False, verbose_name='Тренировочное')
    status_other = models.CharField(max_length=200, verbose_name='Другой статус (заполнить)', **NULLABLE)

    place_competition = models.CharField(max_length=50, verbose_name='Город соревнования')
    play_ground_competition = models.CharField(max_length=20, choices=PLAY_GROUND, verbose_name='Тип площадки')
    place_on_map = models.CharField(max_length=150, verbose_name='Карта-точка на яндекс карте ')

    contact_organization = models.CharField(max_length=20, verbose_name='Контакт организатора', )
    club_organization = models.CharField(max_length=20, verbose_name='Клуб-организатор', **NULLABLE)
    logo_club_organization = models.ImageField(upload_to='logo_clubs', verbose_name='Логотип клуба организатора', **NULLABLE)
    judge_competition = models.CharField(max_length=20, verbose_name='Основной судья соревнований')

    # Классы соревнований
    class_ro_dety = models.BooleanField(default=False, verbose_name='РО-дети')
    class_ro_shenki = models.BooleanField(default=False, verbose_name='РО-щенки')
    class_ro_debut = models.BooleanField(default=False, verbose_name='РО-дебют')
    class_ro_veterany = models.BooleanField(default=False, verbose_name='РО-ветераны')
    class_ro_1 = models.BooleanField(default=False, verbose_name='РО-1')
    class_ro_2 = models.BooleanField(default=False, verbose_name='РО-2')
    class_ro_3 = models.BooleanField(default=False, verbose_name='РО-3')
    class_ro_4 = models.BooleanField(default=False, verbose_name='РО-4(мастера)')

    # ПРЕДВАРИТЕЛЬНО СКРЫТЫЕ ПОЛЯ
    # Судьи для отдельных классов
    judge_class_ro_dety = models.CharField(max_length=25, verbose_name='Судья РО-дети', **NULLABLE)
    judge_class_ro_shenki = models.CharField(max_length=25, verbose_name='Судья РО-щенки', **NULLABLE)
    judge_class_ro_debut = models.CharField(max_length=25, verbose_name='Судья РО-дебют', **NULLABLE)
    judge_class_ro_veterany = models.CharField(max_length=25, verbose_name='Судья РО-ветераны', **NULLABLE)
    judge_class_ro_1 = models.CharField(max_length=25, verbose_name='Судья РО-1', **NULLABLE)
    judge_class_ro_2 = models.CharField(max_length=25, verbose_name='Судья РО-2', **NULLABLE)
    judge_class_ro_3 = models.CharField(max_length=25, verbose_name='Судья РО-3', **NULLABLE)
    judge_class_ro_4 = models.CharField(max_length=25, verbose_name='Судья РО-4(мастера)', **NULLABLE)

    # максимальное количество участников в классе
    count_class_ro_dety = models.IntegerField(verbose_name='Максимум участников РО-дети', **NULLABLE)
    count_class_ro_shenki = models.IntegerField(verbose_name='Максимум участников РО-щенки', **NULLABLE)
    count_class_ro_debut = models.IntegerField(verbose_name='Максимум участников РО-дебют', **NULLABLE)
    count_class_ro_veterany = models.IntegerField(verbose_name='Максимум участников РО-ветераны', **NULLABLE)
    count_class_ro_1 = models.IntegerField(verbose_name='Максимум участников РО-1', **NULLABLE)
    count_class_ro_2 = models.IntegerField(verbose_name='Максимум участников РО-2', **NULLABLE)
    count_class_ro_3 = models.IntegerField(verbose_name='Максимум участников РО-3', **NULLABLE)
    count_class_ro_4 = models.IntegerField(verbose_name='Максимум участников РО-4(мастера)', **NULLABLE)

    # Возможность участия в резерв
    reserve_class_ro_dety = models.IntegerField(default=False, verbose_name='Возможность резерва РО-дети', **NULLABLE)
    reserve_class_ro_shenki = models.IntegerField(default=False, verbose_name='Возможность резерва РО-щенки', **NULLABLE)
    reserve_class_ro_debut = models.IntegerField(default=False, verbose_name='Возможность резерва РО-дебют', **NULLABLE)
    reserve_class_ro_veterany = models.IntegerField(default=False, verbose_name='Возможность резерва РО-ветераны', **NULLABLE)
    reserve_class_ro_1 = models.IntegerField(default=False, verbose_name='Возможность резерва РО-1', **NULLABLE)
    reserve_class_ro_2 = models.IntegerField(default=False, verbose_name='Возможность резерва РО-2', **NULLABLE)
    reserve_class_ro_3 = models.IntegerField(default=False, verbose_name='Возможность резерва РО-3', **NULLABLE)
    reserve_class_ro_4 = models.IntegerField(default=False, verbose_name='Возможность резерва РО-4(мастера)', **NULLABLE)

    # кол-во возможных регистраций в резерв
    count_reserve_class_ro_dety = models.IntegerField(verbose_name='Максимум участников в резерве РО-дети', **NULLABLE)
    count_reserve_class_ro_shenki = models.IntegerField(verbose_name='Максимум участников в резерве РО-щенки', **NULLABLE)
    count_reserve_class_ro_debut = models.IntegerField(verbose_name='Максимум участников в резерве РО-дебют', **NULLABLE)
    count_reserve_class_ro_veterany = models.IntegerField(verbose_name='Максимум участников в резерве РО-ветераны', **NULLABLE)
    count_reserve_class_ro_1 = models.IntegerField(verbose_name='Максимум участников в резерве РО-1', **NULLABLE)
    count_reserve_class_ro_2 = models.IntegerField(verbose_name='Максимум участников в резерве РО-2', **NULLABLE)
    count_reserve_class_ro_3 = models.IntegerField(verbose_name='Максимум участников в резерве РО-3', **NULLABLE)
    count_reserve_class_ro_4 = models.IntegerField(verbose_name='Максимум участников в резерве РО-4(мастера)', **NULLABLE)

    # возможность участие вне зачета по классам
    vnezachet_class_ro_dety = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-дети')
    vnezachet_class_ro_shenki = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-щенки')
    vnezachet_class_ro_debut = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-дебют')
    vnezachet_class_ro_veterany = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-ветераны')
    vnezachet_class_ro_1 = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-1')
    vnezachet_class_ro_2 = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-2')
    vnezachet_class_ro_3 = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-3')
    vnezachet_class_ro_4 = models.BooleanField(default=False, verbose_name='Возможность участия внезачет РО-4(мастера)')

    # кол-во участников в незачет
    count_vnezachet_class_ro_dety = models.IntegerField(verbose_name='Максимум участников внезачет РО-дети', **NULLABLE)
    count_vnezachet_class_ro_shenki = models.IntegerField(verbose_name='Максимум участников внезачет РО-щенки', **NULLABLE)
    count_vnezachet_class_ro_debut = models.IntegerField(verbose_name='Максимум участников внезачет РО-дебют', **NULLABLE)
    count_vnezachet_class_ro_veterany = models.IntegerField(verbose_name='Максимум участников внезачет РО-ветераны', **NULLABLE)
    count_vnezachet_class_ro_1 = models.IntegerField(verbose_name='Максимум участников внезачет РО-1', **NULLABLE)
    count_vnezachet_class_ro_2 = models.IntegerField(verbose_name='Максимум участников внезачет РО-2', **NULLABLE)
    count_vnezachet_class_ro_3 = models.IntegerField(verbose_name='Максимум участников внезачет РО-3', **NULLABLE)
    count_vnezachet_class_ro_4 = models.IntegerField(verbose_name='Максимум участников внезачет РО-4(мастера)',**NULLABLE)
    # КОНЕЦ ПРЕДВАРИТЕЛЬНО СКРЫТЫЕ ПОЛЯ

    max_players = models.IntegerField(default=1, verbose_name='максимиум участников', **NULLABLE)
    more_players = models.BooleanField(default=False, verbose_name='участники сверх максимума', **NULLABLE)

    comment_for_competition = models.TextField(max_length=500, verbose_name='Комментарии')  # комментарии к соревнованиям

    # Тот кто создал соревнование, привязка к аторизованному
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, verbose_name='Создатель соревнования',
                              **NULLABLE)

    def __str__(self):
        return self.name_competition

    def get_selected_classes(self):
        # метод для добавления выбранных классов соревнования для привязки к соревнованию
        selected_classes = []
        if self.class_ro_dety:
            selected_classes.append(('ro_dety', 'РО-дети'))
        if self.class_ro_shenki:
            selected_classes.append(('ro_shenki', 'РО-щенки'))
        if self.class_ro_debut:
            selected_classes.append(('ro_class_ro_debut', 'РО-дебют'))
        if self.class_ro_veterany:
            selected_classes.append(('ro_veterany', 'РО-ветераны'))
        if self.class_ro_1:
            selected_classes.append(('ro_1', 'РО-1'))
        if self.class_ro_2:
            selected_classes.append(('ro_2', 'РО-2'))
        if self.class_ro_3:
            selected_classes.append(('ro_3', 'РО-3'))
        if self.class_ro_4:
            selected_classes.append(('ro_4', 'РО-4(мастера)'))
        print(selected_classes)

        return selected_classes

    class Meta:
        verbose_name = 'Соревнование'
        verbose_name_plural = 'Соревнования'
