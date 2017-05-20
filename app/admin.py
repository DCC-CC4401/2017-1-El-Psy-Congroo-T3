from django.contrib import admin

from app.models import *

admin.site.register(Usuario)
admin.site.register(Comprador)
admin.site.register(Vendedor)
admin.site.register(Producto)
admin.site.register(PaymentMethod)
