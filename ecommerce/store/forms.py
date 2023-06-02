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

    def __init__(self, *args, **kwargs):
        super(CheckOutForm,self).__init__(*args, **kwargs)

        self.fields['name'].widget.attrs['class'] = 'form-control'
        self.fields['name'].widget.attrs['placeholder'] = 'Mario'
        self.fields['surname'].widget.attrs['class'] = 'form-control'
        self.fields['surname'].widget.attrs['placeholder'] = 'Rossi'
        self.fields['email'].widget.attrs['class'] = 'form-control'
        self.fields['email'].widget.attrs['placeholder'] = 'mariorossi@gmail.com'
        self.fields['address'].widget.attrs['class'] = 'form-control'
        self.fields['address'].widget.attrs['placeholder'] = 'Via Roma 1'
        self.fields['city'].widget.attrs['class'] = 'form-control'
        self.fields['city'].widget.attrs['placeholder'] = 'Roma'
        self.fields['country'].widget.attrs['class'] = 'form-control'
        self.fields['country'].widget.attrs['placeholder'] = 'Italy'
        self.fields['postalCode'].widget.attrs['class'] = 'form-control'
        self.fields['postalCode'].widget.attrs['placeholder'] = '00100'


