from django import forms
from history.models import History
from users.models import Dogs


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class HistoryForm(forms.ModelForm):

    class Meta:
        model = History
        exclude = ['user']

        widgets = {
            'date_competition': forms.DateInput(attrs={'type': 'date'}),

        }

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)  # Получаем текущего пользователя из kwargs
        super().__init__(*args, **kwargs)
        if user:
            # Фильтруем queryset собак по пользователю
            self.fields['dog'].queryset = Dogs.objects.filter(owner=user)

