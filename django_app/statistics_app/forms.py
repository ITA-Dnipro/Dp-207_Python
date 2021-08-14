from django import forms
import datetime

TRANSPORT_TYPES = [
    ('car', 'Car'),
    ('train', 'Train')
]


class UserForm(forms.Form):
    username = forms.CharField(
        max_length=300,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )


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
    transport_types = forms.ChoiceField(
        required=True,
        widget=forms.RadioSelect(
            attrs={
                'class': 'transport_types_input',
            }
        ),
        choices=TRANSPORT_TYPES,
        initial='car'
    )
