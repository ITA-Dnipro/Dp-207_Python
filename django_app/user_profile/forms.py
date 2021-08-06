from django.contrib.auth.models import User
from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages

class UpdateForm(forms.ModelForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    class Meta:
        model = User
        fields = ['email', 'username', 'old_password', 'new_password1', 'new_password2']

class UpdateNicknameForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username']

class UpdateEmailForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email']

class UpdatePasswordForm(PasswordChangeForm):
    old_password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password1 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    new_password2 = forms.CharField(max_length=100, widget=forms.PasswordInput(attrs={'class': 'form-control', 'type': 'password'}))
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']