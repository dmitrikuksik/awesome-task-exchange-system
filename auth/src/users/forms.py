from django import forms
from django.db import models

from users.models import User


class UserRegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'username',
            'password',
        )

    def save(self, commit=True):
        instance = super().save(commit=False)
        instance.email = instance.username
        instance.set_password(self.cleaned_data['password'])

        if commit:
            instance.save()

        return instance


class UserDeleteForm(forms.Form):
    user_id = forms.IntegerField()

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()

        if self.user.id == cleaned_data['user_id']:
            raise forms.ValidationError('User cannot delete his own account.')

        return cleaned_data


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'role',
        )
