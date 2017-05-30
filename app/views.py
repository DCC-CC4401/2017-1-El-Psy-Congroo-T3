from django.shortcuts import render

from .forms import *
from .models import  *
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import Group
from django.shortcuts import render
from django.http import HttpResponse
import datetime

def getVendedores():
    vendedores = Vendedor.objects.all()
    vendedorList = []

    for v in vendedores:
        vendedorList.append({'name': v.name})
    return vendedorList

def getProductos(vendedor):
    productos = Producto.objects.filter(vendedor=vendedor).all()
    productoList = []

    for p in productos:
        item = {
            'nombre': p.nombre,
            'stock': p.stock,
            'categoria': CATEGORIA_COMIDA.__getitem__(p.categoria-1)[1],
            'descripcion': p.descripcion,
            'precio': p.precio,
            'foto': p.foto,
        }
        productoList.append(item)
    return productoList

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
    usuario = request.user
    favorito = False
    if usuario.is_authenticated and usuario.groups.filter(name="alumno").exists():
        alumno = Comprador.objects.get(nombre=usuario)
        if vendedor in alumno.favoritos.all():
            favorito = True
    metodospago = ''
    favs = 0
    if usuario.is_authenticated and (usuario.groups.filter(name="vendedor_fijo").exists() or usuario.groups.filter(name="vendedor_ambulante").exists()):
        vendedor2 = Vendedor.objects.get(name=usuario)
        favs = vendedor.users.all().count
    for m in vendedor.metodopago.all():
        metodospago += m.metodo + ' '
    now = datetime.datetime.now().time()
    if vendedor.tipo == 1:
        if now > vendedor.horario_inicio and now < vendedor.horario_fin:
            vendedor.activo = True
            vendedor.save()
    data = {
        'nombre': vendedor.name,
        'estado': 'Activo' if vendedor.activo else 'Inactivo',
        'tipo': 'Vendedor fijo' if vendedor.tipo == 1 else 'Vendedor ambulante',
        'metodospago': metodospago,
        'horario_inicio': vendedor.horario_inicio,
        'horario_fin': vendedor.horario_fin,
        'productos': getProductos(vendedor),
        'favorito': favorito,
        'numero_favs': favs,
    }
    return render(request, 'app/vendedor-profile-page.html', data)

def gestionproductos(request, name):
    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            vendedor = Vendedor.objects.get(name=request.user)
            producto = Producto(nombre=form.cleaned_data['nombre'], stock=form.cleaned_data['stock'],
                                categoria=form.cleaned_data['categoria'],
                                descripcion=form.cleaned_data['descripcion'],
                                precio=form.cleaned_data['precio'],
                                foto=form.cleaned_data['foto'],
                                vendedor=vendedor)
            producto.save()
            return redirect('vendedorprofilepage', name=name)
    else:
        form = ProductoForm()
    return render(request, 'app/productos2.html', {'form': form})

def productos_delete(request, name, vendedor):
    producto = Producto.objects.all().filter(nombre=name).first()
    producto.delete()
    return redirect('vendedorprofilepage', name=vendedor)

def productos_edit(request, name, vendedor):
    producto_inicial = Producto.objects.all().filter(nombre=name).first()
    form = ProductoEditForm(instance=producto_inicial)

    if request.method == "POST":
        form2 = ProductoEditForm(request.POST, request.FILES)
        if form2.is_valid():
            producto_inicial.nombre = form2.cleaned_data['nombre']
            producto_inicial.stock = form2.cleaned_data['stock']
            producto_inicial.categoria = form2.cleaned_data['categoria']
            producto_inicial.descripcion = form2.cleaned_data['descripcion']
            producto_inicial.precio = form2.cleaned_data['precio']
            producto_inicial.foto = form2.cleaned_data['foto']
            producto_inicial.save()
            return redirect('vendedorprofilepage', name=vendedor)
    else:
        form2 = ProductoEditForm()
    return render(request, 'app/editar-productos.html', {'form': form})

def profile_edit(request):
    form = ProfileUpdateForm(user=request.user)

    if request.method == "POST":
        form2 = ProfileUpdateForm(request.POST, request.FILES)
        if form2.is_valid():
            user = User.objects.get(username=request.user)
            if user.check_password(form2.cleaned_data['password']):
                user.email = form2.cleaned_data['email']
                user.save()
                foto = form2.cleaned_data['imagen']
                if user.groups.filter(name='alumno').exists(): #usuario es alumno
                    alumno = Comprador.objects.get(nombre=request.user)
                    alumno.foto = foto
                    alumno.save()
                else: #usuario vendedor
                    vendedor = Vendedor.objects.get(name=request.user)
                    if foto is not None:
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

def change_active(request):
    vendedor = Vendedor.objects.get(name=request.user)
    vendedor.activo = not vendedor.activo
    vendedor.save()
    return HttpResponse("")

def add_favorite(request):
    user = Comprador.objects.get(nombre=request.user)
    vendedor = Vendedor.objects.get(name=request.GET.get('vendedor', None))
    if (vendedor in user.favoritos.all()):
        user.favoritos.remove(vendedor)
    else:
        user.favoritos.add(vendedor)
    user.save()
    vendedor.users.all().count()
    return HttpResponse("")