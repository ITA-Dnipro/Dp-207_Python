from django.forms import Form, Textarea, CharField, ModelForm, \
    DateTimeInput, DateTimeField
from django.core.exceptions import ValidationError
import datetime
from .models import City, Rating, Order


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
class OrderCreateForm(ModelForm):
    check_in = DateTimeField(input_formats=['%m-%d-%Y'], widget=DateInput())
    check_out = DateTimeField(input_formats=['%m-%d-%Y'], widget=DateInput())

    class Meta:
        model = Order
        fields = ['check_in', 'check_out']

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get("check_in")
        check_out = cleaned_data.get("check_out")

        if check_in < datetime.date.today():
            raise ValidationError('YOU CANT GO TO PAST')
