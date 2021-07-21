from django import forms
import datetime
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django.forms.widgets import NumberInput


class JourneyDetailsForm(forms.Form):
    departure_name = forms.CharField(label='From', max_length=30)
    arrival_name = forms.CharField(label='To', max_length=30)
    departure_date = forms.DateField(widget=NumberInput(attrs={'type': 'date'}))

    # class Meta:
    #     fields = ['name']

    def clean_departure_date(self):
        data = self.cleaned_data['departure_date']

        # Check id date is not from past.
        if data < datetime.date.today():
            raise ValidationError(_('Invalid date - departure date in past'))

        return data


