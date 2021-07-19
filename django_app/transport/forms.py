from django import forms

from django.forms.widgets import NumberInput


class JourneyDetailsForm(forms.Form):
    departure_name = forms.CharField(label='From', max_length=30)
    arrival_name = forms.CharField(label='To', max_length=30)
    departure_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

