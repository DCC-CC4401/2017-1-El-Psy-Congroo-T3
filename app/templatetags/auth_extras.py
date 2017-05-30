from django import template
from django.contrib.auth.models import Group
from app.models import Comprador, Vendedor, Producto

register = template.Library()


@register.filter(name='has_group')
def has_group(user, group_name):
    group = Group.objects.get(name=group_name)
    return True if group in user.groups.all() else False


@register.simple_tag(name='getprofilepic', takes_context=True)
def getprofilepic(context):
    user = context['user']
    if has_group(user, "alumno"):
        alumno = Comprador.objects.get(nombre=user.username)
        foto = alumno.foto
    elif has_group(user, "vendedor_fijo") or has_group(user, "vendedor_ambulante"):
        vendedor = Vendedor.objects.get(name=user.username)
        foto = vendedor.foto
    else:
        return "media/AvatarPenguin.png"
    return foto.url

@register.simple_tag(name='getvendedorpic')
def getvendedorpic(name):
    vendedor = Vendedor.objects.get(name=name)
    foto = vendedor.foto
    return foto.url

@register.simple_tag(name='getproductopic')
def getproductopic(name):
    producto = Producto.objects.get(nombre=name)
    foto = producto.foto
    return foto.url
