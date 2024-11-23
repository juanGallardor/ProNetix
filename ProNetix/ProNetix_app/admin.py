from django.contrib import admin
from .models import Perfil, Documento, Empresa, PublicacionTrabajo

@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ['usuario', 'profesion', 'ubicacion', 'fecha_creacion']
    search_fields = ['usuario__username', 'profesion', 'habilidades']

@admin.register(Documento)
class DocumentoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'tipo', 'perfil', 'fecha_subida']
    list_filter = ['tipo', 'fecha_subida']
    search_fields = ['titulo', 'descripcion']

@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre_empresa', 'usuario', 'ubicacion']
    search_fields = ['nombre_empresa', 'descripcion']

@admin.register(PublicacionTrabajo)
class PublicacionTrabajoAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empresa', 'modalidad', 'experiencia_requerida', 'fecha_creacion', 'activa']
    list_filter = ['modalidad', 'experiencia_requerida', 'activa']
    search_fields = ['titulo', 'descripcion', 'requisitos']