from django import forms
from main.models import Competition


class CompetitionForm(forms.ModelForm):
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
                   'max_players', 'more_players'
                   ]

        widgets = {

            'date_competition': forms.DateInput(attrs={'type': 'date'}),
            'start_date_competition': forms.DateInput(attrs={'type': 'date'}),
            'end_date_competition': forms.DateInput(attrs={'type': 'date'}),
        }
