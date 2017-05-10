from django.shortcuts import render


def index(request):
    return render(request, 'app/index.html', {})

def login(request):
    return render(request, 'app/login.html', {})

def signup(request):
    return render(request, 'app/signup.html', {})

def vendedorprofilepage(request):
    return render(request, 'app/vendedor-profile-page.html', {})


def gestionproductos(request):
    return render(request, 'app/gestion-productos.html', {})