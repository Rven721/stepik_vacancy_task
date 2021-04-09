from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django import forms


class MyRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='Имя', max_length=120, required=True)
    last_name = forms.CharField(label='Фамилия', max_length=120, required=True)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name')
