from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db import migrations
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from .models import Perfil, Documento, Empresa, PublicacionTrabajo, Postulacion
from .forms import (
    FormularioRegistroUsuario, 
    FormularioPerfil, 
    FormularioDocumento, 
    FormularioOfertaTrabajo,
    FormularioBusqueda,
    FormularioEmpresa,
    FormularioPublicacionNormal,    
)

def inicio(request):
    return render(request, 'pronetix/inicio.html')


def registro(request):
    if request.method == 'POST':
        formulario = FormularioRegistroUsuario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save(commit=False)
            usuario.email = formulario.cleaned_data['email']
            usuario.first_name = formulario.cleaned_data['first_name']
            usuario.last_name = formulario.cleaned_data['last_name']
            usuario.save()
            
            Perfil.objects.create(usuario=usuario)
            
            login(request, usuario)
            messages.success(request, '¡Registro exitoso! Bienvenido a ProNetix.')
            return redirect('perfil')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        formulario = FormularioRegistroUsuario()
    
    return render(request, 'registration/registro.html', {'form': formulario})


@login_required
def logout_view(request):
    logout(request)
    messages.success(request, "Has cerrado sesión exitosamente.")
    return redirect('inicio')


def terminos(request):
    return render(request, 'ProNetix/terminos.html')


def privacidad(request):
    return render(request, 'ProNetix/privacidad.html')


@login_required
def perfil(request):
    try:
        perfil = request.user.perfil
    except Perfil.DoesNotExist:
        perfil = Perfil.objects.create(usuario=request.user)

    if request.method == 'POST':
        formulario = FormularioPerfil(request.POST, instance=perfil)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        formulario = FormularioPerfil(instance=perfil)

    habilidades = []
    if perfil.habilidades:
        habilidades = [hab.strip() for hab in perfil.habilidades.split(',')]
    
    return render(request, 'perfil/perfil.html', {
        'formulario': formulario,
        'habilidades': habilidades
    })

def crear_perfiles_existentes(apps, schema_editor):
    User = apps.get_model('auth', 'User')
    Perfil = apps.get_model('ProNetix_app', 'Perfil')
    
    for user in User.objects.all():
        Perfil.objects.get_or_create(usuario=user)

class Migration(migrations.Migration):

    dependencies = [
        ('ProNetix_app', '0001_initial'), 
    ]

    operations = [
        migrations.RunPython(crear_perfiles_existentes),
    ]


@login_required
def editar_perfil(request):
    if request.method == 'POST':
        formulario = FormularioPerfil(request.POST, instance=request.user.perfil)
        if formulario.is_valid():
            print("Formulario válido")  
            perfil = formulario.save(commit=False)
            perfil.profesion = formulario.cleaned_data['profesion']
            perfil.ubicacion = formulario.cleaned_data['ubicacion']
            perfil.biografia = formulario.cleaned_data['biografia']
            perfil.habilidades = formulario.cleaned_data['habilidades']
            perfil.modalidad_preferida = formulario.cleaned_data['modalidad_preferida']
            perfil.save()
            
            request.user.first_name = request.POST.get('first_name')
            request.user.last_name = request.POST.get('last_name')
            request.user.save()
            
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
        else:
            print("Errores en el formulario:", formulario.errors) 
    else:
        formulario = FormularioPerfil(instance=request.user.perfil)
    
    return render(request, 'perfil/editar_perfil.html', {'formulario': formulario})


def ver_perfiles(request):
    busqueda = request.GET.get('busqueda', '')
    perfiles = Perfil.objects.select_related('usuario').prefetch_related('documentos').all()
    
    if busqueda:
        perfiles = perfiles.filter(
            Q(usuario__first_name__icontains=busqueda) |
            Q(usuario__last_name__icontains=busqueda) |
            Q(profesion__icontains=busqueda) |
            Q(habilidades__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        ).distinct()

    perfiles_procesados = []
    for perfil in perfiles:
        perfil.habilidades_lista = [hab.strip() for hab in perfil.habilidades.split(',')] if perfil.habilidades else []
        perfiles_procesados.append(perfil)

    return render(request, 'vistas/vista_perfiles.html', {
        'perfiles': perfiles_procesados,
        'busqueda': busqueda
    })


@login_required
def subir_documento(request):
    if request.method == 'POST':
        formulario = FormularioDocumento(request.POST, request.FILES)
        if formulario.is_valid():
            documento = formulario.save(commit=False)
            documento.perfil = request.user.perfil
            documento.save()
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('perfil') 
        else:
            messages.error(request, 'Por favor corrige los errores en el formulario.')
    else:
        formulario = FormularioDocumento()
    
    return render(request, 'perfil/subir_documento.html', {
        'formulario': formulario,
        'form': formulario 
    })


@login_required
def eliminar_documento(request, pk):
    documento = get_object_or_404(Documento, pk=pk, perfil=request.user.perfil)
    documento.delete()
    messages.success(request, 'Documento eliminado exitosamente.')
    return redirect('perfil')


@login_required
def crear_empresa(request):
    empresas_count = Empresa.objects.filter(usuario=request.user).count()
    if empresas_count >= 1:
        messages.warning(request, 'Solo puedes tener 1 empresa por perfil.')
        return redirect('empresas')
    
    if request.method == 'POST':
        formulario = FormularioEmpresa(request.POST)
        if formulario.is_valid():
            empresa = formulario.save(commit=False)
            empresa.usuario = request.user
            empresa.save()
            messages.success(request, 'Empresa creada exitosamente.')

            return redirect('gestionar_empresa')
    else:
        formulario = FormularioEmpresa()

    return render(request, 'empresa/crear_empresa.html', {
        'formulario': formulario,
        'titulo': 'Crear Empresa',
        'es_nueva': True
    })

@login_required
def editar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk, usuario=request.user)
    
    try:
        if request.method == 'POST':
            formulario = FormularioEmpresa(request.POST, instance=empresa)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, 'Información de la empresa actualizada exitosamente.')
                return redirect('gestionar_empresa')
        else:
            formulario = FormularioEmpresa(instance=empresa)

        return render(request, 'empresa/editar_empresa.html', {
            'formulario': formulario,
            'empresa': empresa
        })
        
    except Exception as e:
        messages.error(request, f'Error al procesar el formulario: {str(e)}')
        return redirect('gestionar_empresa')
    
@login_required
def eliminar_empresa(request, pk):
    empresa = get_object_or_404(Empresa, pk=pk, usuario=request.user)
    if request.method == 'POST':
        empresa.delete()
        messages.success(request, 'Empresa eliminada exitosamente.')
        return redirect('empresas')
    return render(request, 'empresa/eliminar_empresa.html', {'empresa': empresa})

def detalles_empresa(request, empresa_id):
    empresa = get_object_or_404(Empresa, id=empresa_id)
    return JsonResponse({
        'nombre_empresa': empresa.nombre_empresa,
        'descripcion': empresa.descripcion,
        'ubicacion': empresa.ubicacion,
        'sitio_web': empresa.sitio_web
    })


@login_required
def gestionar_empresa(request):
    try:
        empresa = request.user.empresas.first() 
        es_nueva = empresa is None
        publicaciones = []
        
        if not es_nueva:
            publicaciones = PublicacionTrabajo.objects.filter(empresa=empresa)
        
        if request.method == 'POST':
            formulario = FormularioEmpresa(request.POST, instance=empresa if not es_nueva else None)
            if formulario.is_valid():
                empresa = formulario.save(commit=False)
                if es_nueva:
                    empresa.usuario = request.user
                empresa.save()
                messages.success(request, 'Empresa {} exitosamente.'.format('registrada' if es_nueva else 'actualizada'))
                return redirect('empresas')
        else:
            formulario = FormularioEmpresa(instance=empresa if not es_nueva else None)
        
        return render(request, 'empresa/gestionar.html', {
            'form': formulario,
            'es_nueva': es_nueva,
            'publicaciones': publicaciones if not es_nueva else [],
            'empresa': empresa
        })
    except Exception as e:
        messages.error(request, f'Error: {str(e)}')
        return redirect('empresas')
 
    
@login_required
def mi_empresa(request):
    empresa = get_object_or_404(Empresa, usuario=request.user)
    publicaciones = PublicacionTrabajo.objects.filter(empresa=empresa, tipo='TRABAJO')
    
    postulaciones = Postulacion.objects.filter(
        publicacion__empresa=empresa
    ).select_related(
        'usuario',
        'usuario__perfil', 
        'publicacion'
    ).order_by('-fecha_postulacion')
    
    return render(request, 'empresa/mi_empresa.html', {
        'empresa': empresa,
        'publicaciones': publicaciones,
        'postulaciones': postulaciones
    })


def ver_empresas(request):
    busqueda = request.GET.get('busqueda', '')
    empresas = Empresa.objects.all()
    
    if busqueda:
        empresas = empresas.filter(
            Q(nombre_empresa__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(ubicacion__icontains=busqueda)
        )

    empresas_usuario = 0
    if request.user.is_authenticated:
        empresas_usuario = Empresa.objects.filter(usuario=request.user).count()
    
    puede_crear = request.user.is_authenticated and empresas_usuario < 3
    
    return render(request, 'empresa/empresas.html', {
        'empresas': empresas,
        'busqueda': busqueda,
        'puede_crear': puede_crear,
        'empresas_restantes': 3 - empresas_usuario if request.user.is_authenticated else 0
    })


def publicaciones(request):
    tipo = request.GET.get('tipo', '')
    busqueda = request.GET.get('busqueda', '')
  
    publicaciones = PublicacionTrabajo.objects.select_related('autor', 'empresa').filter(activa=True)
    
    if tipo in dict(PublicacionTrabajo.TIPO_CHOICES):
        publicaciones = publicaciones.filter(tipo=tipo)
    
    if busqueda:
        publicaciones = publicaciones.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(empresa__nombre_empresa__icontains=busqueda)
        ).distinct()

    paginator = Paginator(publicaciones, 10) 
    page = request.GET.get('page')
    
    try:
        publicaciones_paginadas = paginator.page(page)
    except PageNotAnInteger:
        publicaciones_paginadas = paginator.page(1)
    except EmptyPage:
        publicaciones_paginadas = paginator.page(paginator.num_pages)
    
    context = {
        'publicaciones': publicaciones_paginadas,
        'tipo': tipo,
        'busqueda': busqueda,
        'TIPO_CHOICES': PublicacionTrabajo.TIPO_CHOICES
    }
    
    return render(request, 'publicaciones/lista_publicaciones.html', context)

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(PublicacionTrabajo, pk=pk)
    
    if publicacion.autor != request.user:
        messages.error(request, 'No tienes permiso para editar esta publicación.')
        return redirect('publicaciones')
    
    if request.method == 'POST':
        if publicacion.tipo == 'TRABAJO':
            formulario = FormularioOfertaTrabajo(request.POST, request.FILES, instance=publicacion)
        else:
            formulario = FormularioPublicacionNormal(request.POST, request.FILES, instance=publicacion)
            
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Publicación actualizada exitosamente.')
            return redirect('ver_publicacion', publicacion_id=publicacion.id)
    else:
        if publicacion.tipo == 'TRABAJO':
            formulario = FormularioOfertaTrabajo(instance=publicacion)
        else:
            formulario = FormularioPublicacionNormal(instance=publicacion)
    
    return render(request, 'publicaciones/editar_publicacion.html', {
        'formulario': formulario,
        'publicacion': publicacion,
        'es_oferta_trabajo': publicacion.tipo == 'TRABAJO'
    })
@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(PublicacionTrabajo, pk=pk, autor=request.user)
    
    if request.method == 'POST':
        publicacion.delete()
        messages.success(request, 'Publicación eliminada exitosamente.')
        return redirect('publicaciones')
    
    return render(request, 'publicaciones/confirmar_eliminar.html', {
        'publicacion': publicacion
    })

def ver_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(PublicacionTrabajo, id=publicacion_id, activa=True)
    
    return render(request, 'publicaciones/ver_publicacion.html', {
        'publicacion': publicacion,
        'es_autor': request.user == publicacion.autor if request.user.is_authenticated else False,
        'es_oferta_trabajo': hasattr(publicacion, 'empresa')
    })

@login_required
def seleccionar_tipo_publicacion(request):
    return render(request, 'publicaciones/seleccionar_tipo_publicacion.html')


@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        formulario = FormularioPublicacionNormal(request.POST, request.FILES)  
        if formulario.is_valid():
            publicacion = formulario.save(commit=False)
            publicacion.autor = request.user
            publicacion.tipo = 'NORMAL'
            publicacion.save()
            messages.success(request, 'Publicación creada exitosamente.')
            return redirect('publicaciones')
    else:
        formulario = FormularioPublicacionNormal()
    
    return render(request, 'publicaciones/crear_publicacion.html', {
        'formulario': formulario
    })

@login_required
def crear_oferta_trabajo(request):
    if not request.user.empresas.exists():
        messages.warning(request, 'Necesitas tener una empresa registrada para publicar ofertas de trabajo.')
        return redirect('crear_empresa')

    if request.method == 'POST':
        formulario = FormularioOfertaTrabajo(request.POST)
        if formulario.is_valid():
            oferta = formulario.save(commit=False)
            oferta.autor = request.user
            oferta.tipo = 'TRABAJO'
            oferta.empresa = request.user.empresas.first()
            oferta.save()
            messages.success(request, 'Oferta de trabajo publicada exitosamente.')
            return redirect('publicaciones')
    else:
        formulario = FormularioOfertaTrabajo()
    
    return render(request, 'publicaciones/crear_oferta_trabajo.html', {
        'formulario': formulario
    })

@login_required
def editar_oferta_trabajo(request, pk):
    oferta = get_object_or_404(PublicacionTrabajo, pk=pk, tipo='TRABAJO')
    
    if oferta.autor != request.user:
        messages.error(request, 'No tienes permiso para editar esta oferta de trabajo.')
        return redirect('publicaciones')
    
    if request.method == 'POST':
        formulario = FormularioOfertaTrabajo(request.POST, request.FILES, instance=oferta)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Oferta de trabajo actualizada exitosamente.')
            return redirect('publicaciones')
    else:
        formulario = FormularioOfertaTrabajo(instance=oferta)
        campos_requeridos = ['modalidad', 'experiencia_requerida', 'rango_salarial', 'ubicacion', 'requisitos']
        for campo in campos_requeridos:
            formulario.fields[campo].required = True

    return render(request, 'publicaciones/editar_publicacion.html', {
        'formulario': formulario,
        'publicacion': oferta,
        'titulo': 'Editar Oferta de Trabajo',
        'es_oferta_trabajo': True
    })

@login_required
def eliminar_oferta_trabajo(request, pk):
    oferta = get_object_or_404(PublicacionTrabajo, pk=pk, tipo='TRABAJO', autor=request.user)
    
    if request.method == 'POST':
        oferta.delete()
        messages.success(request, 'Oferta de trabajo eliminada exitosamente.')
        return redirect('publicaciones')
    
    return render(request, 'publicaciones/confirmar_eliminar.html', {
        'publicacion': oferta,
        'titulo': 'Eliminar Oferta de Trabajo',
        'es_oferta_trabajo': True
    })


def busqueda_global(request):
    query = request.GET.get('q', '')
    resultados = {
        'perfiles': [],
        'empresas': [],
        'publicaciones': []
    }
    
    if query:
        resultados['perfiles'] = Perfil.objects.filter(
            Q(usuario__first_name__icontains=query) |
            Q(usuario__last_name__icontains=query) |
            Q(profesion__icontains=query) |
            Q(habilidades__icontains=query) |
            Q(biografia__icontains=query)
        ).distinct()

        resultados['empresas'] = Empresa.objects.filter(
            Q(nombre_empresa__icontains=query) |
            Q(descripcion__icontains=query) |
            Q(sitio_web__icontains=query) |
            Q(ubicacion__icontains=query)
        ).distinct()

        resultados['publicaciones'] = PublicacionTrabajo.objects.filter(
            Q(titulo__icontains=query) |
            Q(descripcion__icontains=query)
        ).values(
            'id', 
            'titulo', 
            'descripcion',
            'empresa__nombre_empresa'
        ).distinct()

    return render(request, 'busqueda/resultados_busqueda.html', {
        'query': query,
        'resultados': resultados,
    })


@login_required
def ver_perfil(request, perfil_id):
    perfil = get_object_or_404(Perfil, id=perfil_id)
    usuario = perfil.usuario
    
    return render(request, 'perfil/ver_perfil.html', {
        'perfil': perfil,
        'usuario': usuario,
        'es_propietario': request.user == usuario
    })


def ver_empresa(request, pk):
    empresa = get_object_or_404(Empresa, id=pk)
    ofertas_trabajo = PublicacionTrabajo.objects.filter(
        empresa=empresa,
        tipo='TRABAJO',
        activa=True
    ).order_by('-fecha_creacion')
    
    return render(request, 'busqueda/ver_empresa.html', {
        'empresa': empresa,
        'ofertas_trabajo': ofertas_trabajo
    })

def ver_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(PublicacionTrabajo, id=publicacion_id)
    return render(request, 'busqueda/ver_publicacion.html', {'publicacion': publicacion})

def ver_publicacion(request, publicacion_id):
    publicacion = get_object_or_404(PublicacionTrabajo, id=publicacion_id)
    es_autor = request.user.is_authenticated and request.user == publicacion.autor
    ya_postulado = request.user.is_authenticated and Postulacion.objects.filter(usuario=request.user, publicacion=publicacion).exists()
    
    return render(request, 'publicaciones/ver_publicacion.html', {
        'publicacion': publicacion,
        'es_autor': es_autor,
        'es_oferta_trabajo': publicacion.tipo == 'TRABAJO',
        'ya_postulado': ya_postulado
    })



@login_required
def postular(request, publicacion_id):
    publicacion = get_object_or_404(PublicacionTrabajo, id=publicacion_id, tipo='TRABAJO', activa=True)
    
    if Postulacion.objects.filter(usuario=request.user, publicacion=publicacion).exists():
        messages.warning(request, 'Ya te has postulado a esta oferta.')
        return redirect('ver_publicacion', publicacion_id=publicacion_id)
    
    if request.method == 'POST':
        mensaje = request.POST.get('mensaje', '')
        Postulacion.objects.create(
            usuario=request.user,
            publicacion=publicacion,
            mensaje=mensaje
        )
        messages.success(request, 'Tu postulación ha sido enviada exitosamente.')
        return redirect('ver_publicacion', publicacion_id=publicacion_id)
    
    return render(request, 'publicaciones/postular.html', {
        'publicacion': publicacion
    })

@login_required
def ver_postulaciones(request, publicacion_id):
    publicacion = get_object_or_404(PublicacionTrabajo, id=publicacion_id)
    
    if request.user != publicacion.autor:
        messages.error(request, 'No tienes permiso para ver las postulaciones.')
        return redirect('ver_publicacion', publicacion_id=publicacion_id)
    
    postulaciones = Postulacion.objects.filter(publicacion=publicacion)
    return render(request, 'publicaciones/ver_postulaciones.html', {
        'publicacion': publicacion,
        'postulaciones': postulaciones
    })

@login_required
def actualizar_estado_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id)
    
    if request.user != postulacion.publicacion.empresa.usuario:
        messages.error(request, 'No tienes permiso para realizar esta acción.')
        return redirect('mi_empresa')
    
    if request.method == 'POST':
        nuevo_estado = request.POST.get('estado')
        if nuevo_estado in dict(Postulacion._meta.get_field('estado').choices):
            postulacion.estado = nuevo_estado
            postulacion.save()
            messages.success(request, f'Estado de la postulación actualizado a {postulacion.get_estado_display()}.')
            return redirect('mi_empresa')
    
    return render(request, 'empresa/actualizar_estado_postulacion.html', {
        'postulacion': postulacion
    })


@login_required
def retirar_postulacion(request, postulacion_id):
    postulacion = get_object_or_404(Postulacion, id=postulacion_id, usuario=request.user)
    
    if request.method == 'POST':
        postulacion.delete()
        messages.success(request, 'Te has retirado exitosamente de la postulación.')
    
    return redirect('perfil')