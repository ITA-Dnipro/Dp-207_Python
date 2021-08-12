from django import forms


class UserForm(forms.Form):
    username = forms.CharField(
        max_length=300,
        widget=forms.TextInput(
            attrs={
                'placeholder': 'Username'
            }
        )
    )
