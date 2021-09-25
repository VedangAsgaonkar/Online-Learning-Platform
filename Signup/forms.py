from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class SignUpForm(UserCreationForm):
    ordered_field_names = ['username', 'Email-ID', 'Institute_Name']
    Email-ID = forms.EmailField(required=True)
    Institute_Name = forms.CharField(required=True)
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2','Email-ID', 'Institute_Name')
        field_order = ['username', 'password1', 'password2', 'Email-ID', 'Institute_Name']
