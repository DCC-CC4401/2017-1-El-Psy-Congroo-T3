from django import forms

from .models import Usuario
import re
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist


class UserForm(forms.ModelForm):
    #username = forms.CharField(label='Username', max_length=30)
    email = forms.EmailField(label='Ingresa tu e-mail')
    password1 = forms.CharField(label='Ingresa tu contraseña',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repite tu contraseña',
                                widget=forms.PasswordInput())
    def clean_password2(self):
        if 'password1' in self.cleaned_data:
            password1 = self.cleaned_data['password1']
            password2 = self.cleaned_data['password2']
            if password1 == password2:
                return password2
        raise forms.ValidationError('Passwords do not match.')

    class Meta:
        model = Usuario
        fields = ('tipo', 'nombre',)