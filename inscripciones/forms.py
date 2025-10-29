from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Estudiante, Empresa, Practica, Inscripcion, DocumentoInscripcion, Carrera, Facultad, PracticaInterna, InscripcionInterna


class EmpresaRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre del Contacto")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido del Contacto")
    
    # Campos específicos de la empresa
    nombre = forms.CharField(max_length=200, required=True, label="Nombre de la Empresa")
    ruc = forms.CharField(max_length=11, required=True, label="RUC")
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label="Dirección")
    telefono = forms.CharField(max_length=15, required=True, label="Teléfono")
    contacto_responsable = forms.CharField(max_length=100, required=True, label="Nombre del Responsable")
    sector = forms.CharField(max_length=100, required=True, label="Sector")
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label="Descripción")
    logo = forms.ImageField(required=False, label="Logo de la Empresa")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels
        self.fields['username'].label = "Usuario"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

    def clean_ruc(self):
        ruc = self.cleaned_data['ruc']
        if Empresa.objects.filter(ruc=ruc).exists():
            raise forms.ValidationError("Ya existe una empresa registrada con este RUC.")
        return ruc

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Empresa.objects.create(
                nombre=self.cleaned_data['nombre'],
                ruc=self.cleaned_data['ruc'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                email=self.cleaned_data['email'],
                contacto_responsable=self.cleaned_data['contacto_responsable'],
                sector=self.cleaned_data['sector'],
                descripcion=self.cleaned_data['descripcion'],
                logo=self.cleaned_data['logo']
            )
        return user


class FacultadRegistrationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True, label="Nombre del Contacto")
    last_name = forms.CharField(max_length=30, required=True, label="Apellido del Contacto")
    
    # Campos específicos de la facultad
    nombre = forms.CharField(max_length=200, required=True, label="Nombre de la Facultad")
    codigo = forms.CharField(max_length=10, required=True, label="Código de la Facultad")
    decano = forms.CharField(max_length=100, required=True, label="Nombre del Decano")
    direccion = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True, label="Dirección")
    telefono = forms.CharField(max_length=15, required=True, label="Teléfono")
    contacto_responsable = forms.CharField(max_length=100, required=True, label="Nombre del Responsable")
    descripcion = forms.CharField(widget=forms.Textarea(attrs={'rows': 4}), required=False, label="Descripción")
    logo = forms.ImageField(required=False, label="Logo de la Facultad")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personalizar labels
        self.fields['username'].label = "Usuario"
        self.fields['email'].label = "Correo Electrónico"
        self.fields['password1'].label = "Contraseña"
        self.fields['password2'].label = "Confirmar Contraseña"

    def clean_codigo(self):
        codigo = self.cleaned_data['codigo']
        if Facultad.objects.filter(codigo=codigo).exists():
            raise forms.ValidationError("Ya existe una facultad registrada con este código.")
        return codigo

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("Ya existe un usuario registrado con este correo electrónico.")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            Facultad.objects.create(
                nombre=self.cleaned_data['nombre'],
                codigo=self.cleaned_data['codigo'],
                decano=self.cleaned_data['decano'],
                direccion=self.cleaned_data['direccion'],
                telefono=self.cleaned_data['telefono'],
                email=self.cleaned_data['email'],
                contacto_responsable=self.cleaned_data['contacto_responsable'],
                descripcion=self.cleaned_data['descripcion'],
                logo=self.cleaned_data['logo']
            )
        return user


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


class EstudianteProfileForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo_estudiante', 'carrera', 'ciclo_actual', 'telefono', 'direccion', 'fecha_nacimiento', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']


class EstudianteUpdateForm(forms.ModelForm):
    class Meta:
        model = Estudiante
        fields = ['codigo_estudiante', 'carrera', 'ciclo_actual', 'telefono', 'direccion', 'fecha_nacimiento', 'foto']
        widgets = {
            'fecha_nacimiento': forms.DateInput(attrs={'type': 'date'}),
            'direccion': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['carrera'].queryset = Carrera.objects.filter(activa=True)


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


class PracticaInternaForm(forms.ModelForm):
    class Meta:
        model = PracticaInterna
        fields = ['facultad', 'titulo', 'descripcion', 'tipo_servicio', 'requisitos', 'duracion_semanas', 'horas_semana', 
                 'fecha_inicio', 'fecha_fin', 'cupos_totales', 'fecha_limite_inscripcion', 'beneficios']
        widgets = {
            'fecha_inicio': forms.DateInput(attrs={'type': 'date'}),
            'fecha_fin': forms.DateInput(attrs={'type': 'date'}),
            'fecha_limite_inscripcion': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'descripcion': forms.Textarea(attrs={'rows': 4}),
            'requisitos': forms.Textarea(attrs={'rows': 4}),
            'beneficios': forms.Textarea(attrs={'rows': 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facultad'].queryset = Facultad.objects.filter(activa=True)


class InscripcionInternaForm(forms.ModelForm):
    class Meta:
        model = InscripcionInterna
        fields = ['observaciones']


class BusquedaPracticasInternasForm(forms.Form):
    titulo = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={'placeholder': 'Buscar por título'}))
    facultad = forms.ModelChoiceField(queryset=Facultad.objects.filter(activa=True), required=False, empty_label="Todas las facultades")
    tipo_servicio = forms.ChoiceField(choices=[('', 'Todos los tipos')] + list(PracticaInterna.TIPO_SERVICIO_CHOICES), required=False)
    fecha_inicio_desde = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    fecha_inicio_hasta = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['facultad'].queryset = Facultad.objects.filter(activa=True)
