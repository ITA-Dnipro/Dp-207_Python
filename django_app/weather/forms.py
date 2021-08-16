from .models import Weather
from django.forms import ModelForm, TextInput


class WeatherForm(ModelForm):
    class Meta:
        model = Weather
        fields = ['city']
