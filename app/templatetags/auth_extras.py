from django import template
from django.contrib.auth.models import Group
from app.models import Comprador, Vendedor

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
    else:
        vendedor = Vendedor.objects.get(name=user.username)
        foto = vendedor.foto
    return foto.url