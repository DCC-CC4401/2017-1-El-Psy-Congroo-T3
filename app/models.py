# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from app.utils.choices import *
from app.utils.functions import *
import uuid


# Create your models here.

class Usuario(models.Model):
    usuario = models.OneToOneField(User, verbose_name='Usuario', related_name='usuario')
    nombre = models.CharField(u'Nombre', max_length=50, default='')
    tipo = models.IntegerField(u'Tipo de usuario', choices=TIPO_USUARIO, default=2)

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return self.nombre


class Comprador(models.Model):
    unique_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre = models.CharField(u'Nombre', max_length=50, default='')
    favoritos = models.ManyToManyField('Vendedor', 'vendedores_favoritos', blank=True)
    foto = models.ImageField(u'Foto', upload_to='pictures/vendedores', default='static/img/AvatarEstudiante.png',
                             help_text='Recomendado: (que tamaño creen?)')

    class Meta:
        verbose_name = 'Comprador'
        verbose_name_plural = 'Compradores'

    def __str__(self):
        return self.nombre


class Vendedor(models.Model):
    name = models.CharField(u'Nombre', max_length=50, default='', primary_key=True)
    activo = models.BooleanField(u'Activo', default=False)
    tipo = models.IntegerField(u'Tipo Vendedor', choices=TIPO_VENDEDOR, default=1)
    favoritos = models.IntegerField(u'Favoritos', default=0)
    metodopago = models.ManyToManyField('PaymentMethod', 'metodos_de_pago')
    foto = models.ImageField(u'Foto', upload_to='pictures/vendedores', default='static/img/AvatarVendedor1.png',
                             help_text='Recomendado: (que tamaño creen?)')
    horario_inicio = models.TimeField(u'Horario de inicio', null=True)
    horario_fin = models.TimeField(u'Horario fin', null=True)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'

    def __str__(self):
        return self.name


class PaymentMethod(models.Model):
    metodo = models.CharField(u'Método de pago', max_length=30, default='', primary_key=True)

    class Meta:
        verbose_name = 'Método de pago'
        verbose_name_plural = 'Métodos de pago'

    def __str__(self):
        return self.metodo


class Producto(models.Model):
    nombre = models.CharField(u'Nombre', max_length=50, default='')
    stock = models.IntegerField(u'Stock', default=0)
    categoria = models.IntegerField(u'Categoría', choices=CATEGORIA_COMIDA, default=1)
    descripcion = models.TextField(u'Descripción', default='')
    precio = models.IntegerField(u'Precio', default=0)
    foto = models.ImageField(u'Foto', upload_to='pictures/productos', default='static/img/bread.png',
                             help_text='Recomendado: (que tamaño creen?)')
    vendedor = models.ForeignKey('Vendedor', related_name='vendedor_respectivo',
                                 blank=True, null=True)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __str__(self):
        return self.nombre
