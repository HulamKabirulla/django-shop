from django.forms import ModelForm, EmailInput, PasswordInput, TextInput
from buyer.models import Buyers


class BuyersForm(ModelForm):
    class Meta:
        model = Buyers
        fields = ['full_name', 'email', 'password']

        widgets = {
            'email': EmailInput(attrs={
                'placeholder': 'Email',
                'required': 'required',
            }),
            'password': PasswordInput(attrs={
                'placeholder': 'Password',
                'required': 'required',
            }),
            'full_name': TextInput(attrs={
                'placeholder': 'Full Name',
                'required': 'required',
            })
        }