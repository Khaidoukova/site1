from django import forms
from history.models import History


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class HistoryForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = History
        exclude = ['user']

        widgets = {
            'date_competition': forms.DateInput(attrs={'type': 'date'}),
            'track1_time': forms.TimeInput(format='%M:%S', attrs={'type':'time'}),
            'track2_time': forms.TimeInput(format='%M:%S', attrs={'type':'time'}),
        }



