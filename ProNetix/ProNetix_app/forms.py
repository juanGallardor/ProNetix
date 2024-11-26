from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Documento, Empresa, PublicacionTrabajo

class FormularioRegistroUsuario(UserCreationForm):
    first_name = forms.CharField(label='Nombre', required=True)
    last_name = forms.CharField(label='Apellido', required=True)
    email = forms.EmailField(label='Correo Electrónico', required=True)
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].help_text = 'Requerido. 150 caracteres o menos. Letras, dígitos y @/./+/-/_ solamente.'
        self.fields['password1'].help_text = 'Tu contraseña debe contener al menos 8 caracteres.'

class FormularioPerfil(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['biografia', 'profesion', 'habilidades', 'ubicacion', 'modalidad_preferida']
        widgets = {
            'biografia': forms.Textarea(attrs={
                'class': 'textarea-editable',
                'placeholder': 'Cuéntanos sobre ti y tu experiencia profesional'
            }),
            'habilidades': forms.Textarea(attrs={
                'class': 'textarea-editable',
                'placeholder': 'Ingresa tus habilidades separadas por comas'
            }),
            'profesion': forms.TextInput(attrs={
                'class': 'input-editable',
                'placeholder': 'Ej: Desarrollador Full Stack'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'input-editable',
                'placeholder': 'Ej: Bogotá, Colombia'
            }),
            'modalidad_preferida': forms.Select(attrs={
                'class': 'select-editable'
            })
        }

class FormularioDocumento(forms.ModelForm):
    class Meta:
        model = Documento
        fields = ['tipo', 'titulo', 'institucion', 'fecha_emision', 'archivo', 'descripcion']
        widgets = {
            'fecha_emision': forms.DateInput(attrs={'type': 'date'}),
        }

class FormularioEmpresa(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre_empresa', 'descripcion', 'sitio_web', 'ubicacion']
        widgets = {
            'nombre_empresa': forms.TextInput(attrs={'class': 'form-control'}),
            'descripcion': forms.Textarea(attrs={'class': 'form-control'}),
            'sitio_web': forms.URLInput(attrs={'class': 'form-control'}),
            'ubicacion': forms.TextInput(attrs={'class': 'form-control'}),
        }

class FormularioPublicacionNormal(forms.ModelForm):
    class Meta:
        model = PublicacionTrabajo
        fields = ['titulo', 'descripcion', 'imagen']  
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '¿Sobre qué quieres hablar?'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Comparte tu conocimiento o experiencia con la comunidad'
            }),
            'imagen': forms.FileInput(attrs={
                'class': 'form-control',
                'id': 'imagen',
                'accept': 'image/*'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['titulo'].required = True
        self.fields['descripcion'].required = True

class FormularioOfertaTrabajo(forms.ModelForm):
    class Meta:
        model = PublicacionTrabajo
        fields = [
            'titulo', 
            'descripcion',
            'modalidad',
            'experiencia_requerida',
            'rango_salarial',
            'ubicacion',
            'requisitos'
        ]
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Título del puesto'
            }),
            'descripcion': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Describe las responsabilidades y beneficios del puesto'
            }),
            'modalidad': forms.Select(attrs={
                'class': 'form-control'
            }),
            'experiencia_requerida': forms.Select(attrs={
                'class': 'form-control'
            }),
            'rango_salarial': forms.Select(attrs={
                'class': 'form-control'
            }),
            'ubicacion': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ubicación del puesto'
            }),
            'requisitos': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': '4',
                'placeholder': 'Lista los requisitos necesarios para el puesto'
            })
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in ['titulo', 'descripcion', 'modalidad', 'experiencia_requerida', 'rango_salarial', 'ubicacion']:
            self.fields[field].required = True

class FormularioBusqueda(forms.Form):
    TIPO_BUSQUEDA = [
        ('PERFIL', 'Buscar Perfiles'),
        ('EMPRESA', 'Buscar Empresas'),
    ]
    
    tipo = forms.ChoiceField(choices=TIPO_BUSQUEDA, required=False, label='Tipo de búsqueda')
    busqueda = forms.CharField(required=False, label='Palabra clave')
    modalidad = forms.ChoiceField(choices=[('', 'Todas')] + PublicacionTrabajo.MODALIDAD_CHOICES, required=False)
    rango_salarial = forms.ChoiceField(choices=[('', 'Todos')] + PublicacionTrabajo.RANGO_SALARIAL_CHOICES, required=False)
    experiencia = forms.ChoiceField(choices=[('', 'Todas')] + PublicacionTrabajo.EXPERIENCIA_CHOICES, required=False)