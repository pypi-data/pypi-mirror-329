from operator import mod
from pyexpat import model
from django.forms import ModelForm
from django import forms
from .models import Account, Message
from phone.models import Category


class registerForm(ModelForm):

    password = forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder': 'Enter Your Password'

    }))

    confirm_password = forms.CharField(widget=forms.PasswordInput(attrs={

        'placeholder': 'Confirm  Your Password'

    }))

    class Meta:
        model = Account
        fields = ['first_name', 'last_name', 'email',
                  'phone_number', 'profile_image', 'password']


def clean(self):
    cleaned_data = super(registerForm, self).clean()

    password = cleaned_data.get('password')

    confirm_password = cleaned_data.get('confirm_password')

    if password != confirm_password:

        raise forms.ValidationError("password not the some! ")


class formmessage(ModelForm):
    class Meta:
        model = Message

        fields = ['subject', 'body']


class Categoryform(ModelForm):

    class Meta:

        model = Category

        fields = ['Category_name', 'description_cat']
