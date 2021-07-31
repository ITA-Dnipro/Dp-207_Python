from django.contrib.auth.models import User
from django import forms

class UpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'username', 'password']

class UpdateNicknameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class UpdatePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['password']