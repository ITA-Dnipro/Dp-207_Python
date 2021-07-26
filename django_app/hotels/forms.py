from django.forms import Form, Textarea, CharField, ModelForm, \
    DateTimeInput, DateTimeField
from django.core.exceptions import ValidationError
from datetime import datetime
from django.utils import timezone
from .models import City, Rating


# city model form to get city from main page
class CityModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Введите город'

    class Meta:
        model = City
        fields = ['name']


# Hotel comment create form for HotelDetails
class HotelCommentCreateForm(Form):
    author = CharField(label='author', max_length=50)
    text = CharField(label='comment', max_length=200, widget=Textarea)


# Hotel rating create form for HotelDetails
class RatingCreateForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['mark']


# widget for DateTimeField
class DateInput(DateTimeInput):
    input_type = 'date'


# OrderCreateForm for HotelDetails
class OrderCreateForm(Form):
    check_in = DateTimeField(widget=DateInput, initial=datetime.utcnow().date())
    check_out = DateTimeField(widget=DateInput, initial=datetime.utcnow().date())

    # override clean method to validate fields
    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")
        today = timezone.now()
        if check_in.date() < today.date() or check_in.month < today.month:
            raise ValidationError('You cant order past date')
        if check_out.date() < check_in.date():
            raise ValidationError('Incorrect date')
        return cleaned_data
