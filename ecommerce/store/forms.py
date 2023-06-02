from django import forms
from django.forms import ModelForm
from .models import CheckOutModel
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CheckOutForm(forms.ModelForm):
    class Meta:
        model = CheckOutModel
        fields = ('name', 'surname', 'email', 'address', 'city', 'country', 'postalCode')

    labels = {
        'name': 'First Name',
        'surname': 'Last Name',
        'email': 'Email',
        'address': 'Address',
        'city': 'City',
        'country': 'Country',
        'postalCode': 'Postal Code',
    }

    widgets = {
        'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Mario'}),
        'surname': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Rossi'}),
        'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'mariorossi@gmail.com'}),
        'address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Via Roma 1'}),
        'city': forms.TextInput(attrs={'class': 'form-control','placeholder': 'Roma'}),
        'country': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Italia'}),
        'postalCode': forms.TextInput(attrs={'class': 'form-control', 'placeholder': '00100'}),
    }
