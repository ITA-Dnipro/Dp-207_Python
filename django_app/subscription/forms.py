from subscription.models import Subscription
from django.forms import ModelForm, DateTimeInput, TextInput
from django.core.exceptions import ValidationError
from django.utils import timezone


class DateInput(DateTimeInput):
    input_type = 'date'


class UpdateTransportSubscriptionForm(ModelForm):

    class Meta:
        model = Subscription
        fields = ["service", "target_city", "city_of_departure", "date_of_expire"]
        widgets = {"date_of_expire": DateInput(format='%Y-%m-%d')}

    def clean_date_of_expire(self):
        date_of_expire = self.cleaned_data.get("date_of_expire")
        today = timezone.now()
        if date_of_expire < today:
            raise ValidationError('You cant order past date')
        return date_of_expire


class UpdateHotelSubscriptionForm(UpdateTransportSubscriptionForm):

    class Meta:
        model = Subscription
        fields = ["service", "target_city", "date_of_expire"]
        widgets = {"date_of_expire": DateInput(format='%Y-%m-%d'),
                   "service": TextInput(attrs={'readonly': True})}


class UpdateWeatherSubscriptionForm(UpdateHotelSubscriptionForm):
    pass
