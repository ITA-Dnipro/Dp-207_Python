from django import forms
import datetime


class RouteForm(forms.Form):
    departure_name = forms.CharField(
        max_length=300,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Departure name'
            }
        )
    )
    arrival_name = forms.CharField(
        max_length=300,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Arrival name'
            }
        )
    )
    departure_date = forms.DateField(
        initial=datetime.date.today,
        input_formats=['%d.%m.%Y', '%Y-%m-%d'],
        widget=forms.DateInput(
            attrs={
                'type': 'date',
            }
        )
    )
