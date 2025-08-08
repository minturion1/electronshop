from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class LoginForm(forms.Form):
    username = forms.CharField(label="Username:", max_length=100, initial='', widget=forms.TextInput(attrs={'class': 'input'}))
    password = forms.CharField(label="Password:", widget=forms.PasswordInput(attrs={'class': 'input'}))

class RegisterForm(forms.Form):
    first_name = forms.CharField(label="Name:", max_length=100, initial='', widget=forms.TextInput(attrs={'class': 'input'}))
    username = forms.CharField(label="Username:", max_length=100, initial='', widget=forms.TextInput(attrs={'class': 'input'}))
    password1 = forms.CharField(label="Password:", widget=forms.PasswordInput(attrs={'class': 'input'}))
    password2 = forms.CharField(label="Confirm password:", widget=forms.PasswordInput(attrs={'class': 'input'}))
    invite_code= forms.CharField(max_length=12, label='Invite code (optional):', required=False, widget=forms.TextInput(attrs={'class': 'input'}))
    