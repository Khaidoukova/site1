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
        fields = ['class_comp', 'selected_dog']


class CompetitorUpdateForm(forms.ModelForm):
    class Meta:
        model = Competitor
        fields = ['min_time_competitor', 'sec_time_competitor']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for i in range(1, 21):
            field_name = f'additional_field_{i}'
            self.fields[field_name] = forms.IntegerField(label=f'Знак {i}', required=False)

        impression_field = 'impression_field'
        self.fields[impression_field] = forms.IntegerField(label='общее впечатление', required=False)

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

        impression_field = 'impression_field'
        field_value = self.cleaned_data.get(impression_field)
        if field_value:
            total_points -= field_value
            additional_scores.append(field_value)

        instance.points = total_points  # итоговые баллы

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
