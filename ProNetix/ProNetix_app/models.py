from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Perfil(models.Model):
    MODALIDAD_CHOICES = [
        ('REMOTO', 'Remoto'),
        ('HIBRIDO', 'Híbrido'),
        ('PRESENCIAL', 'Presencial'),
    ]
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    biografia = models.TextField(max_length=500, blank=True, verbose_name='Biografía')
    profesion = models.CharField(max_length=100, blank=True, verbose_name='Profesión')
    habilidades = models.TextField(blank=True, verbose_name='Habilidades')
    ubicacion = models.CharField(max_length=100, blank=True, verbose_name='Ubicación')
    modalidad_preferida = models.CharField(
        max_length=10, 
        choices=MODALIDAD_CHOICES,
        blank=True,
        verbose_name='Modalidad de trabajo preferida'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')

    def __str__(self):
        return f"Perfil de {self.usuario.get_full_name() or self.usuario.username}"

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'
        app_label = 'ProNetix_app'

class Documento(models.Model):
    TIPO_CHOICES = [
        ('TITULO', 'Título Profesional'),
        ('CERTIFICACION', 'Certificación'),
        ('CURSO', 'Curso'),
        ('OTRO', 'Otro'),
    ]
    
    perfil = models.ForeignKey(Perfil, on_delete=models.CASCADE, related_name='documentos')
    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES, verbose_name='Tipo de documento')
    titulo = models.CharField(max_length=200, verbose_name='Título')
    institucion = models.CharField(max_length=200, verbose_name='Institución')
    fecha_emision = models.DateField(verbose_name='Fecha de emisión')
    archivo = models.FileField(upload_to='documentos/', verbose_name='Archivo')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    fecha_subida = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de subida')

    def __str__(self):
        return f"{self.get_tipo_display()} - {self.titulo}"

    class Meta:
        verbose_name = 'Documento'
        verbose_name_plural = 'Documentos'

class Empresa(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre_empresa = models.CharField(max_length=200, verbose_name='Nombre de la empresa')
    descripcion = models.TextField(verbose_name='Descripción')
    sitio_web = models.URLField(blank=True, verbose_name='Sitio web')
    ubicacion = models.CharField(max_length=100, verbose_name='Ubicación')
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nombre_empresa

    class Meta:
        verbose_name = 'Empresa'
        verbose_name_plural = 'Empresas'

class PublicacionTrabajo(models.Model):
    MODALIDAD_CHOICES = [
        ('REMOTO', 'Remoto'),
        ('HIBRIDO', 'Híbrido'),
        ('PRESENCIAL', 'Presencial'),
    ]
    
    EXPERIENCIA_CHOICES = [
        ('JUNIOR', 'Junior (0-2 años)'),
        ('SEMI_SENIOR', 'Semi-Senior (2-4 años)'),
        ('SENIOR', 'Senior (4+ años)'),
        ('EXPERTO', 'Experto (8+ años)'),
    ]
    
    RANGO_SALARIAL_CHOICES = [
        ('1000000-2000000', '$1.000.000 - $2.000.000'),
        ('2000000-3000000', '$2.000.000 - $3.000.000'),
        ('3000000-4000000', '$3.000.000 - $4.000.000'),
        ('4000000-5000000', '$4.000.000 - $5.000.000'),
        ('5000000-7000000', '$5.000.000 - $7.000.000'),
        ('7000000-9000000', '$7.000.000 - $9.000.000'),
        ('9000000_PLUS', 'Más de $9.000.000'),
        ('POR_ACORDAR', 'Por acordar'),
    ]
    autor = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Autor')
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, verbose_name='Empresa')
    titulo = models.CharField(max_length=200, verbose_name='Título del puesto')
    descripcion = models.TextField(verbose_name='Descripción')
    requisitos = models.TextField(verbose_name='Requisitos')
    ubicacion = models.CharField(max_length=100, verbose_name='Ubicación')
    modalidad = models.CharField(
        max_length=10,
        choices=MODALIDAD_CHOICES,
        verbose_name='Modalidad de trabajo'
    )
    experiencia_requerida = models.CharField(
        max_length=15,
        choices=EXPERIENCIA_CHOICES,
        verbose_name='Experiencia requerida'
    )
    rango_salarial = models.CharField(
        max_length=15,
        choices=RANGO_SALARIAL_CHOICES,
        verbose_name='Rango Salarial'
    )
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de creación')
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name='Última actualización')
    activa = models.BooleanField(default=True, verbose_name='Activa')

    def __str__(self):
        return f"{self.titulo} - {self.empresa.nombre_empresa}"

    class Meta:
        verbose_name = 'Publicación de trabajo'
        verbose_name_plural = 'Publicaciones de trabajo'
        ordering = ['-fecha_creacion']