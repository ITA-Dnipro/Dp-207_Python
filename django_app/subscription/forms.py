from django.forms import Form, DateTimeInput, DateTimeField, MultipleChoiceField, CheckboxSelectMultiple, CharField, HiddenInput
from datetime import datetime
from django.core.exceptions import ValidationError
from django.utils import timezone
from subscription.utils.api_handler import get_city
from subscription.models import HotelService, WeatherService, TransportService
from django.forms import ModelForm


# # SubscriptionForm for Subscription
# class SubscriptionForm(Form):

#     # override clean method to validate fields
#     def clean(self):
#         cleaned_data = super().clean()
#         date_of_expire = cleaned_data.get("date_of_expire")
#         today = timezone.now()
#         if date_of_expire.date() < today.date():
#             raise ValidationError('You cant order past date')
#         return cleaned_data


#  widget for DateTimeField
class DateInput(DateTimeInput):
    input_type = 'date'


# class SubscriptionHotelForm(ModelForm, SubscriptionForm):
#     class Meta:
#         model = HotelService
#         fields = ['city', 'date_of_expire']
#         widgets = {'date_of_expire': DateInput()}


# class SubscriptionWeatherForm(ModelForm, SubscriptionForm):
#     class Meta:
#         model = WeatherService
#         fields = ['city', 'date_of_expire']
#         widgets = {'date_of_expire': DateInput()}


# class SubscriptionTransportForm(ModelForm, SubscriptionForm):
#     class Meta:
#         model = TransportService
#         fields = ['city_of_departure', 'city_of_arrival', 'date_of_expire']
#         widgets = {'date_of_expire': DateInput()}


CHOISES = [('weather', 'weather'), ('hotels', 'hotels'), ('transport', 'transport')]


class AdditionalFormForHotelService(Form):

    city_for_hotels = CharField(max_length=100, widget=HiddenInput())

    def clean_city_for_hotels(self):
        # cleaned_data = super().clean()
        city_for_hotels = self.cleaned_data.get("city_for_hotels")
        get_city(city_for_hotels)
        return city_for_hotels


class AdditionalFormForWeatherService(Form):

    city_for_weather = CharField(max_length=100, widget=HiddenInput())

    def clean_city_for_weather(self):
        # cleaned_data = super().clean()
        city_for_weather = self.cleaned_data.get("city_for_weather")
        get_city(city_for_weather)
        return city_for_weather


class AdditionalFormForTransportService(Form):

    city_departure_for_transport = CharField(max_length=100, widget=HiddenInput())
    city_arrival_for_transport = CharField(max_length=100, widget=HiddenInput())

    def clean_city_departure_for_transport(self):
        # cleaned_data = super().clean()
        city_departure_for_transport = self.cleaned_data.get("city_departure_for_transport")
        get_city(city_departure_for_transport)
        return city_departure_for_transport

    def clean_city_arrival_for_transport(self):
        # cleaned_data = super().clean()
        city_arrival_for_transport = self.cleaned_data.get("city_arrival_for_transport")
        get_city(city_arrival_for_transport)
        return city_arrival_for_transport


# SubscriptionForm for Subscription
class SubscriptionForm(AdditionalFormForTransportService, AdditionalFormForWeatherService, AdditionalFormForHotelService):
    period = DateTimeField(widget=DateInput, initial=datetime.utcnow().date())
    services = MultipleChoiceField(widget=CheckboxSelectMultiple, choices=CHOISES)


    # override clean method to validate fields
    def clean(self):
        cleaned_data = super().clean()
        date_of_expire = cleaned_data.get("date_of_expire")
        today = timezone.now()
        if date_of_expire.date() < today.date():
            raise ValidationError('You cant order past date')
        return cleaned_data
