from django.forms import Form, Textarea, CharField, ModelForm, ChoiceField, Select, RadioSelect
from .models import City, HotelComment, Rating


class CityModelForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['name'].label = 'Введите город'

    class Meta:
        model = City
        fields = ['name']


class HotelCommentCreateForm(Form):
    author = CharField(label='author', max_length=50)
    text = CharField(label='comment', max_length=200, widget=Textarea)


class RatingCreateForm(ModelForm):
    class Meta:
        model = Rating
        fields = ['mark']
