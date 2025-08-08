from django import forms
from .models import *


class AddPromocodeForm(forms.Form):
    count = forms.IntegerField(label="Count of promo codes:", min_value=0, max_value=100)
    type = forms.ChoiceField(label="Type:", choices=[
        ('G', 'Green'),
        ('Y', 'Yellow'),
        ('R', 'Red'),
    ])

class PromocodeForm(forms.Form):
    code = forms.CharField(label='Enter promo code:',max_length=10, min_length=10, widget=forms.TextInput(attrs={'class': 'input'}))

class CheckPromocodeForm(forms.Form):
    code = forms.CharField(label='Enter promo code:',max_length=10, min_length=10, widget=forms.TextInput(attrs={'class': 'input'}))