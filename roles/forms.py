from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator

from roles.models import Competitor, AdditionalScore


class CreateCompetitorForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        selected_classes = kwargs.pop('selected_classes', None)
        conductor = kwargs.pop('conductor', None)
        super(CreateCompetitorForm, self).__init__(*args, **kwargs)
        if selected_classes:
            self.fields['class_comp'].choices = selected_classes
        if conductor:
            self.fields['selected_dog'].queryset = conductor.dogs.all()

    class Meta:
        model = Competitor
        fields = ['class_comp', 'selected_dog', 'competitior_vnezachet']


class CompetitorUpdateForm(forms.ModelForm):
    class Meta:
        model = Competitor
        fields = ['min_time_competitor', 'sec_time_competitor',
                  'start_field',
                  'additional_field_1',
                  'additional_field_2',
                  'additional_field_3',
                  'additional_field_4',
                  'additional_field_5',
                  'additional_field_6',
                  'additional_field_7',
                  'additional_field_8',
                  'additional_field_9',
                  'additional_field_10',
                  'additional_field_11',
                  'additional_field_12',
                  'additional_field_13',
                  'additional_field_14',
                  'additional_field_15',
                  'additional_field_16',
                  'additional_field_17',
                  'additional_field_18',
                  'additional_field_19',
                  'additional_field_20',
                  'finish_field',
                  'show_field',
                  ]

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     for i in range(1, 21):
    #         field_name = f'additional_field_{i}'
    #         self.fields[field_name] = forms.IntegerField(label=f'Знак {i}', required=False)
    #
    #     impression_field = 'show_field'
    #     self.fields[impression_field] = forms.IntegerField(label='общее впечатление', required=False)

    def save(self, commit=True, total_points=100, grade_competitor=None):
        instance = super().save(commit=False)

        additional_scores = []
        for i in range(1, 21):
            field_name = f'additional_field_{i}'
            field_value = self.cleaned_data.get(field_name)
            if field_value is not None:
                total_points -= field_value
                additional_scores.append(field_value)
            else:
                additional_scores.append(0)

        impression_field = 'show_field'
        field_value = self.cleaned_data.get(impression_field)
        if field_value:
            total_points -= field_value
            additional_scores.append(field_value)

        instance.points = total_points  # итоговые баллы
        # считаем оценку в зависимости от выставленных баллов
        if 0 < total_points < 69.8:
            grade_competitor = 'Недостаточно'
        elif 69.9 < total_points < 79.8:
            grade_competitor = 'Хорошо'
        elif 79.9 < total_points < 89.8:
            grade_competitor = 'Очень хорошо'
        else:
            grade_competitor = 'Отлично'

        instance.grade_competitor = grade_competitor

        if commit:
            instance.save()

            # Удаляем все связанные объекты AdditionalScore
            instance.additionalscore_set.all().delete()
            # Создаем новый объект AdditionalScore с обновленным списком оценок
            AdditionalScore.objects.create(competitor=instance, additional_scores=additional_scores)
        return instance
