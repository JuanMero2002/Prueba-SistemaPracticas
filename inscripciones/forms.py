from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Estudiante, Empresa, Practica, Inscripcion, DocumentoInscripcion, Carrera


class EstudianteRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    codigo_estudiante = forms.CharField(max_length=20, required=True)
    carrera = forms.ModelChoiceField(queryset=Carrera.objects.filter(activa=True), required=True)
    ciclo_actual = forms.IntegerField(min_value=1, max_value=12, required=True)
    telefono = forms.CharField(max_length=15, required=False)
    direccion = forms.CharField(widget=forms.Textarea, required=False)
    fecha_nacimiento = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=False)
    foto = forms.ImageField(required=False)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Estudiante.objects.create(
                user=user,
                codigo_estudiante=self.cleaned_data['codigo_estudiante'],
                carrera=self.cleaned_data['carrera'],
                ciclo_actual=self.cleaned_data['ciclo_actual'],
                telefono=self.cleaned_data['telefono'],
                direccion=self.cleaned_data['direccion'],
                fecha_nacimiento=self.cleaned_data['fecha_nacimiento'],
                foto=self.cleaned_data['foto']
            )
        return user


class EstudianteUpdateForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['ciclo_actual', 'telefono', 'direccion', 'fecha_nacimiento', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
        }


class EmpresaForm(forms.ModelForm):
    class Meta:
        model = Empresa
        fields = ['nombre', 'ruc', 'direccion', 'telefono', 'email', 'contacto_responsable', 'sector', 'descripcion', 'logo']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }


class PracticaForm(forms.ModelForm):
    class Meta:
        model = Practica
        fields = ['empresa', 'titulo', 'descripcion', 'requisitos', 'duracion_semanas', 'horas_semana', 
                 'fecha_inicio', 'fecha_fin', 'cupos_totales', 'fecha_limite_inscripcion']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite_inscripcion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(activa=True)


class InscripcionForm(forms.ModelForm):
    class Meta:
        model = Inscripcion
        fields = ['observaciones']


class DocumentoInscripcionForm(forms.ModelForm):
    class Meta:
        model = DocumentoInscripcion
        fields = ['tipo', 'nombre', 'archivo']


class BusquedaPracticasForm(forms.Form):
    titulo = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar por título'}))
    empresa = forms.ModelChoiceField(queryset=Empresa.objects.filter(activa=True), required=False, empty_label="Todas las empresas")
    sector = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar por sector'}))
    fecha_inicio_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_inicio_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['empresa'].queryset = Empresa.objects.filter(activa=True)
