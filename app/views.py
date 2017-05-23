from django.shortcuts import render


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