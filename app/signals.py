# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from app.models import *

dict_favoritos = {}


@receiver(pre_save, sender=Comprador)
def preActualizarFavoritos(sender, instance, **kwargs):
    dict_favoritos[instance.unique_id] = instance.favoritos.all()
