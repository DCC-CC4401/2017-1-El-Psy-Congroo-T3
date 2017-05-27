from django import forms
from .models import *
from app.utils.choices import TIPO_USUARIO_2



class UserForm(forms.ModelForm):
    #username = forms.CharField(label='Username', max_length=30)
    tipo2 = forms.ChoiceField(choices=TIPO_USUARIO_2)
    email = forms.EmailField(label='Ingresa tu e-mail', widget=forms.EmailInput())
    password1 = forms.CharField(label='Ingresa tu contraseña',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repite tu contraseña',
                                widget=forms.PasswordInput())
    horainicial = forms.TimeField(label='Hora Inicial', widget=forms.TimeInput(), initial='8:00')
    horafinal = forms.TimeField(label='Hora Final', widget=forms.TimeInput(), initial='18:00')
    pagos = forms.ModelMultipleChoiceField(queryset=PaymentMethod.objects.all(), required=False)

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

class ProductoForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('nombre', 'precio', 'stock', 'categoria', 'descripcion',)

