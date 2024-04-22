from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.core.exceptions import ValidationError

from django.utils.crypto import get_random_string

from users.models import User, Dogs
UserModel = get_user_model()


class StyleFormMixin:

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    class Meta:
        model = User
        fields = ('email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        if not user.email_confirm_key:
            user.email_confirm_key = get_random_string(length=8)
        if commit:
            user.save()
        return user


class UserProfileForm(UserChangeForm):

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'phone', 'avatar',
                  'user_tegram', 'user_whatsup', 'user_vk', 'user_other',
                  'user_town', 'user_club', 'user_trainer', 'user_about', 'user_hide_info',
                  )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()


class DogsForm(forms.ModelForm):
    class Meta:
        model = Dogs
        fields = ('dog_name', 'dog_avatar', 'home_name',
                  'date_borne', 'breed_dog', 'pedigree_dog', 'other_federation',
                  'pedigree_file', 'number_chip', 'brand_dog', 'female_dog', 'number_bookwork', 'father_name',
                  'father_pedigree_number', 'father_titles', 'mother_name', 'mother_pedigree_number', 'mother_titles')
        widgets = {
            'date_borne': forms.DateInput(attrs={'type': 'date'}),
        }


class UserLoginForm(StyleFormMixin, AuthenticationForm):
    """Форма для контроля авторизации пользователей с подтвержденным почтовым адресом"""
    def clean(self):
        email = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if email and password:
            user = authenticate(username=email, password=password)  # аутентификация пользователя по email

            if user and not user.is_active:
                raise ValidationError('Вам нужно подтвердить свой почтовый адрес, прежде чем войти.')

        return super().clean()
