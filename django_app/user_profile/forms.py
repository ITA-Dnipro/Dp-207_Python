from django.contrib.auth.models import User
from django import forms


class UpdateProfile(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
