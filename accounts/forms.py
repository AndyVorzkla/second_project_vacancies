from django import forms
from django.contrib.auth.models import User
from vacancies.models import *


class SignUpForm(forms.Form):
    username = forms.CharField(
        min_length=3,
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputLogin'
        })
    )

    password = forms.CharField(
        required=True,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': 'inputPassword'
        })
    )
    # class Meta:
    #     model = User
    #     fields = ('username', 'password',)


class RegistrationForm(SignUpForm):
    first_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputName'
        })
    )

    last_name = forms.CharField(
        max_length=50,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'id': 'inputSurname'
        })
    )




