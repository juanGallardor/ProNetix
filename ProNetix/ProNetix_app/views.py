from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q
from .models import Perfil, Documento, PublicacionTrabajo
from .forms import (
    FormularioRegistroUsuario, 
    FormularioPerfil, 
    FormularioDocumento, 
    FormularioPublicacionTrabajo,
    FormularioBusqueda,
    FormularioEmpresa
)

def inicio(request):
    return render(request, 'pronetix/inicio.html')

def registro(request):
    if request.method == 'POST':
        formulario = FormularioRegistroUsuario(request.POST)
        if formulario.is_valid():
            usuario = formulario.save()
            Perfil.objects.create(usuario=usuario)
            login(request, usuario)
            messages.success(request, '¡Registro exitoso! Bienvenido a ProNetix.')
            return redirect('perfil')
    else:
        formulario = FormularioRegistroUsuario()
    return render(request, 'registration/registro.html', {'formulario': formulario})

@login_required
def perfil(request):
    if request.method == 'POST':
        formulario = FormularioPerfil(request.POST, instance=request.user.perfil)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Perfil actualizado exitosamente.')
            return redirect('perfil')
    else:
        formulario = FormularioPerfil(instance=request.user.perfil)
    return render(request, 'pronetix/perfil.html', {'formulario': formulario})

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
        formulario = FormularioDocumento()
    return render(request, 'pronetix/subir_documento.html', {'formulario': formulario})

@login_required
def crear_publicacion(request):
    if request.method == 'POST':
        formulario = FormularioPublicacionTrabajo(request.POST)
        if formulario.is_valid():
            publicacion = formulario.save(commit=False)
            publicacion.autor = request.user
            publicacion.save()
            messages.success(request, 'Publicación creada exitosamente.')
            return redirect('publicaciones')
    else:
        formulario = FormularioPublicacionTrabajo()
    return render(request, 'pronetix/formulario_publicacion.html', {'formulario': formulario})

def publicaciones(request):
    busqueda = request.GET.get('busqueda', '')
    if busqueda:
        publicaciones = PublicacionTrabajo.objects.filter(
            Q(titulo__icontains=busqueda) |
            Q(descripcion__icontains=busqueda) |
            Q(requisitos__icontains=busqueda)
        ).filter(activa=True)
    else:
        publicaciones = PublicacionTrabajo.objects.filter(activa=True)
    return render(request, 'pronetix/publicaciones.html', {'publicaciones': publicaciones})

@login_required
def gestionar_empresa(request):
    try:
        empresa = request.user.empresa
        if request.method == 'POST':
            formulario = FormularioEmpresa(request.POST, instance=empresa)
            if formulario.is_valid():
                formulario.save()
                messages.success(request, 'Información de la empresa actualizada exitosamente.')
                return redirect('gestionar_empresa')
        else:
            formulario = FormularioEmpresa(instance=empresa)
    except:
        if request.method == 'POST':
            formulario = FormularioEmpresa(request.POST)
            if formulario.is_valid():
                empresa = formulario.save(commit=False)
                empresa.usuario = request.user
                empresa.save()
                messages.success(request, 'Empresa registrada exitosamente.')
                return redirect('gestionar_empresa')
        else:
            formulario = FormularioEmpresa()
    
    return render(request, 'pronetix/gestionar_empresa.html', {
        'formulario': formulario
    })

@login_required
def editar_publicacion(request, pk):
    publicacion = get_object_or_404(PublicacionTrabajo, pk=pk, autor=request.user)
    if request.method == 'POST':
        formulario = FormularioPublicacionTrabajo(request.POST, instance=publicacion)
        if formulario.is_valid():
            formulario.save()
            messages.success(request, 'Publicación actualizada exitosamente.')
            return redirect('publicaciones')
    else:
        formulario = FormularioPublicacionTrabajo(instance=publicacion)
    return render(request, 'pronetix/formulario_publicacion.html', {'formulario': formulario})

@login_required
def eliminar_publicacion(request, pk):
    publicacion = get_object_or_404(PublicacionTrabajo, pk=pk, autor=request.user)
    if request.method == 'POST':
        publicacion.delete()
        messages.success(request, 'Publicación eliminada exitosamente.')
        return redirect('publicaciones')
    return render(request, 'pronetix/confirmar_eliminar_publicacion.html', {'publicacion': publicacion})

def busqueda(request):
    formulario = FormularioBusqueda(request.GET)
    resultados = None
    tipo_busqueda = request.GET.get('tipo', '')
    query = request.GET.get('busqueda', '')
    
    if tipo_busqueda == 'EMPRESA':
        resultados = PublicacionTrabajo.objects.filter(activa=True)
        
        if query:
            resultados = resultados.filter(
                Q(empresa__nombre_empresa__icontains=query) |
                Q(titulo__icontains=query) |
                Q(descripcion__icontains=query)
            )
        
        modalidad = request.GET.get('modalidad')
        if modalidad:
            resultados = resultados.filter(modalidad=modalidad)
            
        rango_salarial = request.GET.get('rango_salarial')
        if rango_salarial:
            resultados = resultados.filter(rango_salarial=rango_salarial)
            
        experiencia = request.GET.get('experiencia')
        if experiencia:
            resultados = resultados.filter(experiencia_requerida=experiencia)
            
    elif tipo_busqueda == 'PERFIL':
        resultados = Perfil.objects.all()
        
        if query:
            resultados = resultados.filter(
                Q(usuario__first_name__icontains=query) |
                Q(usuario__last_name__icontains=query) |
                Q(profesion__icontains=query) |
                Q(habilidades__icontains=query)
            )
    
    return render(request, 'pronetix/resultados_busqueda.html', {
        'formulario': formulario,
        'resultados': resultados,
        'tipo_busqueda': tipo_busqueda,
        'query': query,
    })