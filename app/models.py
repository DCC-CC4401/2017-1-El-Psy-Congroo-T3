# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User
from app.utils.choices import *


# Create your models here.

class Usuario(models.Model):
    usuario = models.OneToOneField(User, verbose_name='Usuario', related_name='usuario')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __unicode__(self):
        return self.usuario


class Comprador(models.Model):
    nombre = models.CharField(u'Nombre', max_length=50, default='')

    class Meta:
        verbose_name = 'Comprador'
        verbose_name_plural = 'Compradores'

    def __unicode__(self):
        return self.nombre

class Vendedor(models.Model):
    nombre = models.CharField(u'Nombre', max_length=50, default='')
    activo = models.BooleanField(u'Activo', default=False)
    tipo = models.BooleanField(u'Tipo Vendedor', choices=TIPO_VENDEDOR, default=1)
    #metodos = models.IntegerField(u'Métodos de pago', choices=PAYMENT_METHODS, default=1)
    favoritos = models.IntegerField(u'Favoritos', default=0)

    class Meta:
        verbose_name = 'Vendedor'
        verbose_name_plural = 'Vendedores'

    def __unicode__(self):
        return self.name


class Producto(models.Model):
    nombre = models.CharField(u'Nombre', max_length=50, default='')
    stock = models.IntegerField(u'Stock', default=0)
    categoria = models.IntegerField(u'Categoría',  choices=CATEGORIA_COMIDA, default=1)
    descripcion = models.TextField(u'Descripción', default='')
    precio = models.IntegerField(u'Precio', default=0)

    class Meta:
        verbose_name = 'Producto'
        verbose_name_plural = 'Productos'

    def __unicode__(self):
        return self.nombre

