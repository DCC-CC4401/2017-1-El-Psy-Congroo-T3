from django.conf.urls import url
from django.conf.urls.static import static
from ElPsyCongroo import settings

from app import views

urlpatterns = [
    #/app/
    url(r'^$', views.index, name='index'),
    #/app/login
    url(r'^login$', views.login_user, name='login'),
    #/app/logout
    url(r'^logout$', views.logout_user, name='logout'),
    #/app/signup
    url(r'^register$', views.register2, name='register'),
    #/app/vendedor
    url(r'^vendedor/(?P<name>.+)$', views.vendedorprofilepage, name='vendedorprofilepage'),
    #/app/productos/edit
    url(r'^productos/(?P<vendedor>.+)/edit/(?P<name>.+)$', views.productos_edit, name='edicionproductos'),
    # /app/productos/vendedor/delete
    url(r'^productos/(?P<vendedor>.+)/delete/(?P<name>.+)$', views.productos_delete, name='eliminarproductos'),
    #/app/productos
    url(r'^productos/(?P<name>.+)$', views.gestionproductos, name='gestionproductos'),
    #/app/usuario
    url(r'^usuario$', views.profile_edit, name='profile_edit'),
    # ajax request to change vendedor active status
    url(r'^ajax/change_active/$', views.change_active, name='change_active'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)