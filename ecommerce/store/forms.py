from django import forms
from django.forms import ModelForm
from .models import CheckOutModel
from django.urls import reverse_lazy
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit


class CheckOutForm(ModelForm):
    class Meta:
        model = CheckOutModel
        fields = ('name', 'surname', 'email', 'address', 'city', 'country', 'postalCode')

"""
class CheckOutForm(forms.Form):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper(self)
        self.helper.form_action = reverse_lazy('checkout')
        self.helper.form_method = 'POST'
        self.helper.add_input(Submit('submit', 'Submit'))

    SUBJECT_CHOICES = [
        ('AL', 'Albania'),
        ('AD', 'Andorra'),
        ('AT', 'Austria'),
        ('BY', 'Bielorussia'),
        ('BE', 'Belgio'),
        ('BA', 'Bosnia-Erzegovina'),
        ('BG', 'Bulgaria'),
        ('HR', 'Croazia'),
        ('CY', 'Cipro'),
        ('CZ', 'Repubblica Ceca'),
        ('DK', 'Danimarca'),
        ('EE', 'Estonia'),
        ('FI', 'Finlandia'),
        ('FR', 'Francia'),
        ('DE', 'Germania'),
        ('GR', 'Grecia'),
        ('HU', 'Ungheria'),
        ('IS', 'Islanda'),
        ('IE', 'Irlanda'),
        ('IT', 'Italia'),
        ('LV', 'Lettonia'),
        ('LI', 'Liechtenstein'),
        ('LT', 'Lituania'),
        ('LU', 'Lussemburgo'),
        ('MK', 'Macedonia del Nord'),
        ('MT', 'Malta'),
        ('MD', 'Moldavia'),
        ('MC', 'Monaco'),
        ('ME', 'Montenegro'),
        ('NL', 'Paesi Bassi'),
        ('NO', 'Norvegia'),
        ('PL', 'Polonia'),
        ('PT', 'Portogallo'),
        ('RO', 'Romania'),
        ('RU', 'Russia'),
        ('SM', 'San Marino'),
        ('RS', 'Serbia'),
        ('SK', 'Slovacchia'),
        ('SI', 'Slovenia'),
        ('ES', 'Spagna'),
        ('SE', 'Svezia'),
        ('CH', 'Svizzera'),
        ('UA', 'Ucraina'),
        ('GB', 'Regno Unito'),
        ('VA', 'Città del Vaticano'),
    ]

    name = forms.CharField(label='* First name', max_length=20, required=True)
    surname = forms.CharField(label='* Last Name', max_length=20, required=True)
    email = forms.EmailField(label='* Email', required=True)
    address = forms.CharField(label='* Address', max_length=40, required=True)
    city = forms.CharField(label='* City', max_length=20, required=True)
    country = forms.ChoiceField(label='* Country', choices=SUBJECT_CHOICES, required=True)
    postalCode = forms.CharField(label='* Postal Code', max_length=10, required=True)
"""