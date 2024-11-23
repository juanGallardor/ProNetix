from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Perfil, Documento, PublicacionTrabajo, Empresa

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
            'habilidades': forms.Textarea(attrs={'placeholder': 'Ingresa tus habilidades separadas por comas'}),
            'biografia': forms.Textarea(attrs={'placeholder': 'Cuéntanos sobre ti y tu experiencia'}),
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

class FormularioPublicacionTrabajo(forms.ModelForm):
    class Meta:
        model = PublicacionTrabajo
        fields = [
            'titulo', 'descripcion', 'requisitos', 'ubicacion', 
            'modalidad', 'experiencia_requerida', 'rango_salarial'
        ]
        widgets = {
            'descripcion': forms.Textarea(attrs={'placeholder': 'Describe el puesto y las responsabilidades'}),
            'requisitos': forms.Textarea(attrs={'placeholder': 'Lista los requisitos necesarios para el puesto'}),
        }

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