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
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),

    path('', views.inicio, name='inicio'),
    path('registro/', views.registro, name='registro'),
    path('terminos/', views.terminos, name='terminos'),
    path('privacidad/', views.privacidad, name='privacidad'),

    path('logout/', views.logout_view, name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('perfil/editar/', views.editar_perfil, name='editar_perfil'),
    path('perfiles/', views.ver_perfiles, name='perfiles'),
    path('', views.ver_perfiles, name='ver_perfiles'),
    path('perfil/<int:perfil_id>/', views.ver_perfil, name='ver_perfil'),

    path('perfil/subir-documento/', views.subir_documento, name='subir_documento'),
    path('perfil/documento/<int:pk>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
    path('perfil/subir-documento/', views.subir_documento, name='subir_documento'),

    path('publicaciones/', views.publicaciones, name='publicaciones'),
    path('publicacion/<int:publicacion_id>/', views.ver_publicacion, name='ver_publicacion'),
    path('publicaciones/seleccionar/', views.seleccionar_tipo_publicacion, name='seleccionar_tipo_publicacion'),
    path('publicaciones/nueva/', views.crear_publicacion, name='crear_publicacion'),
    path('publicaciones/<int:pk>/editar/', views.editar_publicacion, name='editar_publicacion'),
    path('publicaciones/<int:pk>/eliminar/', views.eliminar_publicacion, name='eliminar_publicacion'),

    path('publicaciones/nueva/trabajo/', views.crear_oferta_trabajo, name='crear_oferta_trabajo'), 
    path('ofertas/<int:pk>/editar/', views.editar_oferta_trabajo, name='editar_oferta_trabajo'),
    path('ofertas/<int:pk>/eliminar/', views.eliminar_oferta_trabajo, name='eliminar_oferta_trabajo'),

    path('buscar/', views.busqueda_global, name='busqueda_global'),

    path('empresas/', views.ver_empresas, name='empresas'),
    path('empresa/mi-empresa/', views.mi_empresa, name='mi_empresa'),  
    path('empresa/crear/', views.crear_empresa, name='crear_empresa'), 
    path('empresa/gestionar/', views.gestionar_empresa, name='gestionar_empresa'), 
    path('empresa/<int:pk>/', views.ver_empresa, name='ver_empresa'),
    path('empresa/<int:pk>/editar/', views.editar_empresa, name='editar_empresa'), 
    path('empresa/<int:pk>/eliminar/', views.eliminar_empresa, name='eliminar_empresa'),
     path('empresas/detalles/<int:empresa_id>/', views.detalles_empresa, name='detalles_empresa'),

    path('publicaciones/<int:publicacion_id>/postular/', views.postular, name='postular'),
    path('publicaciones/<int:publicacion_id>/postulaciones/', views.ver_postulaciones, name='ver_postulaciones'),
    path('postulaciones/<int:postulacion_id>/actualizar-estado/', views.actualizar_estado_postulacion, name='actualizar_estado_postulacion'),
    path('postulaciones/<int:postulacion_id>/retirar/', views.retirar_postulacion, name='retirar_postulacion'),
    

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)