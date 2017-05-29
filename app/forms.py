from django import forms
from .models import *
from app.utils.choices import TIPO_USUARIO_2
from django.contrib.auth.models import Group


class UserForm(forms.ModelForm):
    #username = forms.CharField(label='Username', max_length=30)
    tipo2 = forms.ChoiceField(choices=TIPO_USUARIO_2)
    tipo = forms.ChoiceField(required=False)
    email = forms.EmailField(label='Ingresa tu e-mail', widget=forms.EmailInput())
    password1 = forms.CharField(label='Ingresa tu contraseña',
                                widget=forms.PasswordInput())
    password2 = forms.CharField(label='Repite tu contraseña',
                                widget=forms.PasswordInput())
    horainicial = forms.TimeField(label='Hora Inicial', widget=forms.TimeInput(), required=False, initial='8:00')
    horafinal = forms.TimeField(label='Hora Final', widget=forms.TimeInput(), required=False, initial='18:00')
    pagos = forms.ModelMultipleChoiceField(queryset=PaymentMethod.objects.all(), required=False, initial=PaymentMethod.objects.none())
    #foto = forms.FileField(required=False, initial=None)

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
        fields = ('nombre', 'precio', 'stock', 'categoria', 'descripcion', 'foto')


class ProductoEditForm(forms.ModelForm):

    class Meta:
        model = Producto
        fields = ('nombre', 'precio', 'stock', 'categoria', 'descripcion', 'foto')


class ProfileUpdateForm(forms.ModelForm):
    email = forms.EmailField(label='Ingresa tu e-mail', widget=forms.EmailInput())
    pagos = forms.ModelMultipleChoiceField(queryset=PaymentMethod.objects.all(), required=False, initial=PaymentMethod.objects.none())
    horainicial = forms.TimeField(label='Hora Inicial', widget=forms.TimeInput(), required=False)
    horafinal = forms.TimeField(label='Hora Final', widget=forms.TimeInput(), required=False)
    imagen = forms.ImageField(label='Avatar', widget=forms.FileInput(), required=False, initial=None)
    password = forms.CharField(widget=forms.PasswordInput())

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        if self.user is not None:
            inicial = 0
            final = 0
            if self.user.groups.filter(name='vendedor_fijo').exists():
                inicial = Vendedor.objects.values_list('horario_inicio', flat=True).get(name=self.user.username)
                final = Vendedor.objects.values_list('horario_fin', flat=True).get(name=self.user.username)

            kwargs.update(initial={'email': self.user.email,
                                   'horainicial': inicial,
                                   'horafinal': final})
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = User
        exclude = ('username', 'date_joined')
