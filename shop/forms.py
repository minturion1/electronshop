from django import forms
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['contact', 'note']
        widgets = {
            'contact': forms.TextInput(attrs={'class': 'input', 'placeholder':'Phone number or messenger'}),
            'note': forms.TextInput(attrs={'class':'input'}),
        }
        labels = {
            'contact': 'Contact',
            'note':'Additional request (optional)',
        }
        required = {
            'note': False,
        }