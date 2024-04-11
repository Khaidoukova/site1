from django import forms

from drag_and_drop_app.models import Image


class ImageUpdateForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['competition', 'image_class_com']

