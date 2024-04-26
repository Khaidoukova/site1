from django import forms
from main.models import Competition


class CompetitionForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Получаем экземпляр объекта, если он уже существует
        instance = kwargs.get('instance')

        # Если объект уже существует и имеет значения дат, то добавляем их к label_suffix
        if instance and instance.date_competition:
            date_label = instance.date_competition.strftime('%d.%m.%Y')
            self.fields['date_competition'].label = f'Дата соревнований (ранее указанная дата {date_label})'
        if instance and instance.start_date_competition:
            date_label1 = instance.start_date_competition.strftime('%d.%m.%Y')
            self.fields['start_date_competition'].label = f'Дата начала регистрации (ранее указанная дата {date_label1})'
        if instance and instance.end_date_competition:
            date_label3 = instance.end_date_competition.strftime('%d.%m.%Y')
            self.fields['end_date_competition'].label = f'Дата окончания регистрации (ранее указанная дата {date_label3})'

    class Meta:
        model = Competition
        exclude = ['owner',
                   'max_players', 'more_players', 'invitation_competition'
                   ]

        widgets = {
            # Виджеты для даты
            'date_competition': forms.DateInput(attrs={'type': 'date'}),
            'start_date_competition': forms.DateInput(attrs={'type': 'date'}),
            'end_date_competition': forms.DateInput(attrs={'type': 'date'}),
            # Плейсхолдеры для полей
            'judge_class_ro_dety': forms.TextInput(attrs={'placeholder': 'Добавьте судью'}),
            'judge_class_ro_shenki': forms.TextInput(attrs={'placeholder': 'Добавьте судью '}),
            'judge_class_ro_debut': forms.TextInput(attrs={'placeholder': 'Добавьте судью '}),
            'judge_class_ro_veterany': forms.TextInput(attrs={'placeholder': 'Добавьте судью '}),
            'judge_class_ro_1': forms.TextInput(attrs={'placeholder': 'Добавьте судью '}),
            'judge_class_ro_2': forms.TextInput(attrs={'placeholder': 'Добавьте судью '}),
            'judge_class_ro_3': forms.TextInput(attrs={'placeholder': 'Добавьте судью '}),
            'judge_class_ro_4': forms.TextInput(attrs={'placeholder': 'Добавьте судью '}),

            'count_class_ro_dety': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),
            'count_class_ro_shenki': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),
            'count_class_ro_debut': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),
            'count_class_ro_veterany': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),
            'count_class_ro_1': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),
            'count_class_ro_2': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),
            'count_class_ro_3': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),
            'count_class_ro_4': forms.TextInput(attrs={'placeholder': 'Максимум участников'}),

            'count_vnezachet_class_ro_dety': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),
            'count_vnezachet_class_ro_shenki': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),
            'count_vnezachet_class_ro_debut': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),
            'count_vnezachet_class_ro_veterany': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),
            'count_vnezachet_class_ro_1': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),
            'count_vnezachet_class_ro_2': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),
            'count_vnezachet_class_ro_3': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),
            'count_vnezachet_class_ro_4': forms.TextInput(attrs={'placeholder': 'Максимум внезачет'}),

        }

    # def save(self, commit=True):
    #     # Сначала вызываем метод save родительского класса, чтобы сохранить основные данные модели
    #     instance = super().save(commit=False)
    #
    #     заполняем поля
