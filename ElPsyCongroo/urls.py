from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [

    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('app.urls')),
    url(r'^accounts/', include('registration.backends.simple.urls')),
]
