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
            tipo2=form.cleaned_data['tipo']
            user = User.objects.create_user(username=form.cleaned_data['nombre'],
                                            password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            user2 = Usuario(usuario=user, nombre=form.cleaned_data['nombre'], tipo=tipo2)
            user2.save()
            if tipo2 == 2: #alumno
                usuarioAlumno = Comprador(nombre=form.cleaned_data['nombre'])
                usuarioAlumno.save()
            if tipo2 == 3: #ambulante
                print("a")
                usuarioAmbulante = Vendedor(name=form.cleaned_data['nombre'])
                usuarioAmbulante.metodopago.add(form.cleaned_data['pagos'])
                usuarioAmbulante.save()
            if tipo2 == 4: #fijo
                print("b")
                usuarioFijo = Vendedor(name=form.cleaned_data['nombre'], horario_inicio=form.cleaned_data['horainicial'],
                                       horario_fin=form.cleaned_data['horafinal'])
                usuarioFijo.metodopago.add(form.cleaned_data['pagos'])
                usuarioFijo.save()
            return redirect('index')
    else:
        form = UserForm()
    return render(request, 'app/registration_form2.html', {'form': form})

def productos2(request):
    if request.method == "POST":
        form = ProductoForm(request.POST)
        if form.is_valid():
            producto = Producto(nombre=form.cleaned_data['nombre'], stock=form.cleaned_data['stock'],
                                categoria=form.cleaned_data['categoria'],
                                descripcion=form.cleaned_data['descripcion'],
                                precio = form.cleaned_data['precio'])
            producto.save()
            return redirect('vendedorprofilepage')
    else:
        form = ProductoForm()
    return render(request, 'app/productos2.html', {'form': form})
