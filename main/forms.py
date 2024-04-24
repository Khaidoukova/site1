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
        exclude = ['owner', 'judge_class_ro_dety', 'judge_class_ro_shenki', 'judge_class_ro_debut',
                   'judge_class_ro_veterany', 'judge_class_ro_1', 'judge_class_ro_2', 'judge_class_ro_3', 'judge_class_ro_4',
                   'count_class_ro_dety', 'count_class_ro_shenki', 'count_class_ro_debut', 'count_class_ro_veterany',
                   'count_class_ro_1', 'count_class_ro_2', 'count_class_ro_3', 'count_class_ro_4',
                   'reserve_class_ro_dety', 'reserve_class_ro_shenki', 'reserve_class_ro_debut',
                   'reserve_class_ro_veterany', 'reserve_class_ro_1', 'reserve_class_ro_2', 'reserve_class_ro_3', 'reserve_class_ro_4',
                   'count_reserve_class_ro_dety', 'count_reserve_class_ro_shenki', 'count_reserve_class_ro_debut',
                   'count_reserve_class_ro_veterany', 'count_reserve_class_ro_1', 'count_reserve_class_ro_2',
                   'count_reserve_class_ro_3', 'count_reserve_class_ro_4',
                   'vnezachet_class_ro_dety',
                   'vnezachet_class_ro_shenki', 'vnezachet_class_ro_debut', 'vnezachet_class_ro_veterany',
                   'vnezachet_class_ro_1', 'vnezachet_class_ro_2', 'vnezachet_class_ro_3', 'vnezachet_class_ro_4',
                   'count_vnezachet_class_ro_dety', 'count_vnezachet_class_ro_shenki', 'count_vnezachet_class_ro_debut',
                   'count_vnezachet_class_ro_veterany', 'count_vnezachet_class_ro_1', 'count_vnezachet_class_ro_2',
                   'count_vnezachet_class_ro_3', 'count_vnezachet_class_ro_4',
                   'max_players', 'more_players', 'invitation_competition'
                   ]

        widgets = {

            'date_competition': forms.DateInput(attrs={'type': 'date'}),
            'start_date_competition': forms.DateInput(attrs={'type': 'date'}),
            'end_date_competition': forms.DateInput(attrs={'type': 'date'}),
        }
