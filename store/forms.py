from django import forms
from .models import CheckOutModel, Review


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


class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ('content',)

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        self.fields['content'].widget.attrs['class'] = 'form-control'
        self.fields['content'].widget.attrs['placeholder'] = 'Write your review'

