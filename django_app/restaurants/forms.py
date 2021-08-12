from django import forms

class RestaurantSearchForm(forms.Form):
    CHOICES = [('1', 'Odin'), ('2', 'Dva')]
    city = forms.ChoiceField(widget=forms.Select, choices=CHOICES)
    restaurant_name = forms.CharField(max_length=300, required=False, widget=forms.TextInput(attrs={'placeholder': 'Restaurant, bar, or cafe name'}))
