from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Max

from main.models import Competition
from users.models import User, Dogs

NULLABLE = {'blank': True, 'null': True}


# Create your models here.
class Judge(models.Model):
    """Модель судьи привязка к юзеру"""
    id_judge = models.CharField(max_length=20, verbose_name='ID судьи')  # создается только после одобрения админом

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # привязка к юзеру

    judge_status = models.BooleanField(default=False, verbose_name='Статус судьи запрошен')

    check_admin = models.BooleanField(default=False, verbose_name='Одобрен админом')  # проверка админом

    def save(self, *args, **kwargs):
        if not self.id_judge:
            last_judge = Judge.objects.aggregate(Max('id_judge'))['id_judge__max']
            if last_judge is None:
                self.id_judge = 'JD00001'
            else:
                last_number = int(last_judge[2:])
                new_number = last_number + 1
                self.id_judge = f"JD{new_number:05}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Судья'
        verbose_name_plural = 'Судьи'


class Conductor(models.Model):
    """Модель проводника"""
    id_conductor = models.CharField(max_length=10, verbose_name='ID Проводника', unique=True)  # создается только после одобрения админом

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='conductor')  # привязка к юзеру
    dogs = models.ManyToManyField(Dogs, blank=True)  # привязка к собакам

    check_admin = models.BooleanField(default=False, verbose_name='Одобрен админом')  # проверка админом

    def save(self, *args, **kwargs):
        if not self.id_conductor:
            last_conductor = Conductor.objects.aggregate(Max('id_conductor'))['id_conductor__max']
            if last_conductor is None:
                new_number = 1
            else:
                last_number = int(last_conductor[3:])
                new_number = last_number + 1
            self.id_conductor = f"CON{new_number:05}"

        super().save(*args, **kwargs)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Проводник'
        verbose_name_plural = 'Проводники'


class Competitor(models.Model):
    """Модель участника соревнований"""

    GRADE = (
        ('great', 'Отлично'),
        ('very_good', 'Очень хорошо'),
        ('good', 'Хорошо'),
        ('not_enough', 'Недостаточно')
    )

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

    user = models.ForeignKey(User, on_delete=models.CASCADE)  # связь с юзером
    competition = models.ForeignKey(Competition, on_delete=models.CASCADE)  # связь с соревнованиями

    grade_competitor = models.CharField(max_length=20, choices=GRADE, verbose_name='Оценка участника', **NULLABLE)
    points = models.IntegerField(validators=[MaxValueValidator(limit_value=100)], verbose_name='Количество очков', **NULLABLE)

    class_comp = models.CharField(max_length=20, choices=CLASSES, verbose_name='Класс участия', **NULLABLE)

    # Поля времени для выставления
    min_time_competitor = models.IntegerField(verbose_name='Мин', **NULLABLE,
                                              validators=[
                                                  MaxValueValidator(9),
                                                  MinValueValidator(0)
                                              ]
                                              )
    sec_time_competitor = models.IntegerField(verbose_name='Сек', **NULLABLE,
                                              validators=[
                                                  MaxValueValidator(59),
                                                  MinValueValidator(0)
                                              ]
                                              )

    conductor = models.ForeignKey(Conductor, on_delete=models.CASCADE, related_name='competitors')
    # Поле для связи с выбранной собакой участника
    selected_dog = models.ForeignKey(Dogs, on_delete=models.SET_NULL, null=True, blank=True,
                                     verbose_name='Собака для участия')
    competitor_reserve = models.BooleanField(default=False, verbose_name='Участник в резерве')
    competitior_vnezachet = models.BooleanField(default=False, verbose_name='Участник внезачет')
    place_in_competition = models.PositiveIntegerField(verbose_name='Место в соревновании', **NULLABLE)

    # Поля для выставления оценок
    start_field = models.IntegerField(verbose_name='Старт', **NULLABLE)
    finish_field = models.IntegerField(verbose_name='Финиш', **NULLABLE)
    show_field = models.IntegerField(verbose_name='Общие впечатления', **NULLABLE)
    additional_field_1 = models.IntegerField(verbose_name='Знак 1', **NULLABLE)
    additional_field_2 = models.IntegerField(verbose_name='Знак 2', **NULLABLE)
    additional_field_3 = models.IntegerField(verbose_name='Знак 3', **NULLABLE)
    additional_field_4 = models.IntegerField(verbose_name='Знак 4', **NULLABLE)
    additional_field_5 = models.IntegerField(verbose_name='Знак 5', **NULLABLE)
    additional_field_6 = models.IntegerField(verbose_name='Знак 6', **NULLABLE)
    additional_field_7 = models.IntegerField(verbose_name='Знак 7', **NULLABLE)
    additional_field_8 = models.IntegerField(verbose_name='Знак 8', **NULLABLE)
    additional_field_9 = models.IntegerField(verbose_name='Знак 9', **NULLABLE)
    additional_field_10 = models.IntegerField(verbose_name='Знак 10', **NULLABLE)
    additional_field_11 = models.IntegerField(verbose_name='Знак 11', **NULLABLE)
    additional_field_12 = models.IntegerField(verbose_name='Знак 12', **NULLABLE)
    additional_field_13 = models.IntegerField(verbose_name='Знак 13', **NULLABLE)
    additional_field_14 = models.IntegerField(verbose_name='Знак 14', **NULLABLE)
    additional_field_15 = models.IntegerField(verbose_name='Знак 15', **NULLABLE)
    additional_field_16 = models.IntegerField(verbose_name='Знак 16', **NULLABLE)
    additional_field_17 = models.IntegerField(verbose_name='Знак 17', **NULLABLE)
    additional_field_18 = models.IntegerField(verbose_name='Знак 18', **NULLABLE)
    additional_field_19 = models.IntegerField(verbose_name='Знак 19', **NULLABLE)
    additional_field_20 = models.IntegerField(verbose_name='Знак 20', **NULLABLE)

    def __str__(self):
        return self.user.email

    class Meta:
        verbose_name = 'Участник'
        verbose_name_plural = 'Участники'


class AdditionalScore(models.Model):
    """Сохраниение оценок участника"""
    competitor = models.ForeignKey(Competitor, on_delete=models.CASCADE)
    additional_scores = models.JSONField()

