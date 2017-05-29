from django.shortcuts import render

from .forms import *
from .models import  *
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render

def getVendedores():
    vendedores = Vendedor.objects.all()
    vendedorList = []

    for v in vendedores:
        vendedorList.append({'name': v.name})
    return vendedorList

def index(request):
    data = {
        'vendedores': getVendedores(),
    }
    return render(request, 'app/index.html', data)

def login_user(request):
    logout(request)
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']

        username = User.objects.get(email=email.lower()).username
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                tipo = Usuario.objects.get(nombre=username).tipo
                if tipo == 2: #alumno
                    return redirect('index')
                else: #vendedor
                    return redirect('vendedorprofilepage', name=username)
    return render(request, 'app/login.html', {})

def logout_user(request):
    logout(request)
    return redirect('index')

def register(request):
    return render(request, 'app/register.html', {})

def vendedorprofilepage(request, name):
    vendedor = Vendedor.objects.get(name=name)
    data = {
        'nombre': vendedor.name,
        'activo': 'Activo' if vendedor.activo else 'Inactivo',
        'tipo': 'Vendedor fijo' if vendedor.tipo == '4' else 'Vendedor ambulante',
        'metodospago': vendedor.metodopago,
        'horario_inicio': vendedor.horario_inicio,
        'horario_fin': vendedor.horario_fin,
    }
    return render(request, 'app/vendedor-profile-page.html', data)

def gestionproductos(request):
    return render(request, 'app/gestion-productos.html', {})

def profile_edit(request):
    form = ProfileUpdateForm(user=request.user)

    if request.method == "POST":
        form2 = ProfileUpdateForm(request.POST)
        if form2.is_valid():
            user = User.objects.get(username=request.user)
            if user.check_password(form2.cleaned_data['password']):
                user.email = form2.cleaned_data['email']
                user.save()
                foto = form2.cleaned_data['imagen']
                if user.groups.filter(name='alumno').exists(): #usuario es alumno
                    alumno = Comprador.objects.get(username=request.user)
                    alumno.foto = foto
                    alumno.save()
                else: #usuario vendedor
                    vendedor = Vendedor.objects.get(username=request.user)
                    vendedor.foto = foto
                    vendedor.horario_inicio = form2.cleaned_data['horainicial']
                    vendedor.horario_fin = form2.cleaned_data['horafinal']
                    vendedor.save()
        return redirect('index')
    return render(request, 'app/profile-edit.html', {'form': form})

def register2(request):
    if request.method == "POST":

        form = UserForm(request.POST)

        if form.is_valid():
            tipo2=form.cleaned_data['tipo2']
            user = User.objects.create_user(username=form.cleaned_data['nombre'],
                                            password=form.cleaned_data['password1'], email=form.cleaned_data['email'])
            user2 = Usuario(usuario=user, nombre=form.cleaned_data['nombre'], tipo=tipo2)
            user2.save()
            if tipo2 == "2": #alumno
                usuarioAlumno = Comprador(nombre=form.cleaned_data['nombre'])
                usuarioAlumno.save()
                g = Group.objects.get(name='alumno')
            if tipo2 == "3": #ambulante
                usuarioAmbulante = Vendedor(name=form.cleaned_data['nombre'], tipo=2)
                usuarioAmbulante.metodopago.add(form.cleaned_data['pagos'])
                usuarioAmbulante.save()
                g = Group.objects.get(name='vendedor_ambulante')
            if tipo2 == "4": #fijo
                usuarioFijo = Vendedor(name=form.cleaned_data['nombre'], horario_inicio=form.cleaned_data['horainicial'],
                                       horario_fin=form.cleaned_data['horafinal'])
                usuarioFijo.metodopago.add(form.cleaned_data['pagos'])
                usuarioFijo.save()
                g = Group.objects.get(name='vendedor_fijo')
            g.user_set.add(user)
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
            return redirect('vendedorprofilepage', name=request)
    else:
        form = ProductoForm()
    return render(request, 'app/productos2.html', {'form': form})
