# -*- coding: utf-8 -*-
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from app.models import *

dict_favoritos = {}


@receiver(pre_save, sender=Comprador)
def preActualizarFavoritos(sender, instance, **kwargs):
    dict_favoritos[instance.unique_id] = instance.favoritos.all()


@receiver(post_save, sender=Comprador)
def postActualizarFavoritos(sender, instance, **kwargs):
    print("Largo post es:")
    print(len(instance.favoritos.all()))

    #if len(instance.favoritos.all()) == len(dict_favoritos[instance.unique_id]):
    #    return

    #elif len(instance.favoritos.all()) > len(dict_favoritos[instance.unique_id]):
    #    for i in instance.favoritos.all():
    #        if i not in dict_favoritos[instance.unique_id]:
    #            i.favoritos += 1

    #elif len(instance.favoritos.all()) < len(dict_favoritos[instance.unique_id]):
    #    for i in dict_favoritos[instance.unique_id]:
    #        if i not in instance.favoritos.all():
    #            i.favoritos -= 1

