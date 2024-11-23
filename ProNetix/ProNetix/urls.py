"""
URL configuration for ProNetix project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include  
from django.conf import settings
from django.conf.urls.static import static
from ProNetix_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/subir-documento/', views.subir_documento, name='subir_documento'),
    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('publicaciones/nueva/', views.crear_publicacion, name='crear_publicacion'),
    path('publicaciones/<int:pk>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('publicaciones/<int:pk>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),
    path('buscar/', views.busqueda, name='busqueda'),
    path('empresa/', views.gestionar_empresa, name='gestionar_empresa'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)