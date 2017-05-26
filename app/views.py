from django.shortcuts import render

from .forms import *
from .models import  *
from django.contrib.auth.models import User
from django.shortcuts import redirect

def index(request):
    return render(request, 'app/index.html', {})

def login(request):
    return render(request, 'app/login.html', {})

def register(request):
    return render(request, 'app/register.html', {})

def vendedorprofilepage(request):
    return render(request, 'app/vendedor-profile-page.html', {})

def gestionproductos(request):
    return render(request, 'app/gestion-productos.html', {})

def profile_edit(request):
    return render(request, 'app/profile-edit.html', {})

def register2(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(username=form.cleaned_data['nombre'],
                                            password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            user2 = Usuario(usuario=user, nombre=form.cleaned_data['nombre'], tipo=form.cleaned_data['tipo'])
            user2.save()
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'app/registration_form2.html', {'form': form})
