from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.utils import timezone
from django.http import JsonResponse
from .models import Practica, Inscripcion, Estudiante, Empresa, Carrera, DocumentoInscripcion, Facultad, PracticaInterna, InscripcionInterna
from .forms import (
    EstudianteRegistrationForm, EstudianteUpdateForm, EmpresaForm, 
    PracticaForm, InscripcionForm, DocumentoInscripcionForm, BusquedaPracticasForm,
    EmpresaRegistrationForm, FacultadRegistrationForm, PracticaInternaForm, 
    InscripcionInternaForm, BusquedaPracticasInternasForm, EstudianteProfileForm,
    UserUpdateForm
)


def home(request):
    """Vista principal del sistema"""
    practicas_destacadas = Practica.objects.filter(
        activa=True, 
        estado='disponible',
        fecha_limite_inscripcion__gte=timezone.now()
    ).order_by('-fecha_publicacion')[:6]
    
    empresas_destacadas = Empresa.objects.filter(activa=True).order_by('-fecha_registro')[:4]
    
    context = {
        'practicas_destacadas': practicas_destacadas,
        'empresas_destacadas': empresas_destacadas,
    }
    return render(request, 'inscripciones/home.html', context)


def lista_practicas(request):
    """Lista todas las prácticas disponibles con filtros"""
    practicas = Practica.objects.filter(
        activa=True,
        fecha_limite_inscripcion__gte=timezone.now()
    ).order_by('-fecha_publicacion')
    
    form = BusquedaPracticasForm(request.GET)
    
    if form.is_valid():
        titulo = form.cleaned_data.get('titulo')
        empresa = form.cleaned_data.get('empresa')
        sector = form.cleaned_data.get('sector')
        fecha_desde = form.cleaned_data.get('fecha_inicio_desde')
        fecha_hasta = form.cleaned_data.get('fecha_inicio_hasta')
        
        if titulo:
            practicas = practicas.filter(titulo__icontains=titulo)
        if empresa:
            practicas = practicas.filter(empresa=empresa)
        if sector:
            practicas = practicas.filter(empresa__sector__icontains=sector)
        if fecha_desde:
            practicas = practicas.filter(fecha_inicio__gte=fecha_desde)
        if fecha_hasta:
            practicas = practicas.filter(fecha_inicio__lte=fecha_hasta)
    
    paginator = Paginator(practicas, 9)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
        'form': form,
    }
    return render(request, 'inscripciones/lista_practicas.html', context)


def detalle_practica(request, pk):
    """Detalle de una práctica específica"""
    practica = get_object_or_404(Practica, pk=pk, activa=True)
    
    # Verificar si el usuario está inscrito
    inscrito = False
    inscripcion = None
    if request.user.is_authenticated:
        try:
            estudiante = Estudiante.objects.get(user=request.user)
            inscripcion = Inscripcion.objects.get(estudiante=estudiante, practica=practica)
            inscrito = True
        except (Estudiante.DoesNotExist, Inscripcion.DoesNotExist):
            pass
    
    context = {
        'practica': practica,
        'inscrito': inscrito,
        'inscripcion': inscripcion,
    }
    return render(request, 'inscripciones/detalle_practica.html', context)


@login_required
def inscribirse_practica(request, pk):
    """Inscripción a una práctica"""
    practica = get_object_or_404(Practica, pk=pk, activa=True)
    
    try:
        estudiante = Estudiante.objects.get(user=request.user)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de estudiante primero.')
        return redirect('perfil_estudiante')
    
    # Verificar si ya está inscrito
    if Inscripcion.objects.filter(estudiante=estudiante, practica=practica).exists():
        messages.warning(request, 'Ya estás inscrito en esta práctica.')
        return redirect('detalle_practica', pk=pk)
    
    # Verificar si puede inscribirse
    if not practica.puede_inscribirse:
        messages.error(request, 'No puedes inscribirte en esta práctica.')
        return redirect('detalle_practica', pk=pk)
    
    if request.method == 'POST':
        form = InscripcionForm(request.POST)
        if form.is_valid():
            inscripcion = form.save(commit=False)
            inscripcion.estudiante = estudiante
            inscripcion.practica = practica
            inscripcion.save()
            
            # Reducir cupos disponibles
            practica.cupos_disponibles -= 1
            practica.save()
            
            messages.success(request, 'Te has inscrito exitosamente en la práctica.')
            return redirect('mis_inscripciones')
    else:
        form = InscripcionForm()
    
    context = {
        'practica': practica,
        'form': form,
    }
    return render(request, 'inscripciones/inscribirse_practica.html', context)


@login_required
def mis_inscripciones(request):
    """Lista las inscripciones del estudiante"""
    try:
        estudiante = Estudiante.objects.get(user=request.user)
        inscripciones = Inscripcion.objects.filter(estudiante=estudiante).order_by('-fecha_inscripcion')
        
        # Filtro por estado si está presente
        estado = request.GET.get('estado')
        if estado:
            inscripciones = inscripciones.filter(estado=estado)
        
        context = {
            'inscripciones': inscripciones,
        }
        return render(request, 'inscripciones/mis_inscripciones.html', context)
    except Estudiante.DoesNotExist:
        messages.error(request, 'Debes completar tu perfil de estudiante primero.')
        return redirect('perfil_estudiante')


@login_required
def cancelar_inscripcion(request, pk):
    """Cancelar una inscripción"""
    inscripcion = get_object_or_404(Inscripcion, pk=pk, estudiante__user=request.user)
    
    if inscripcion.estado == 'pendiente':
        inscripcion.estado = 'cancelada'
        inscripcion.save()
        
        # Aumentar cupos disponibles
        inscripcion.practica.cupos_disponibles += 1
        inscripcion.practica.save()
        
        messages.success(request, 'Inscripción cancelada exitosamente.')
    else:
        messages.error(request, 'No puedes cancelar esta inscripción.')
    
    return redirect('mis_inscripciones')


def registro_estudiante(request):
    """Registro de nuevos estudiantes"""
    if request.user.is_authenticated:
        # Si el usuario autenticado ya tiene un perfil, redirigir a home.
        if hasattr(request.user, 'estudiante'):
            return redirect('home')
        # Si no tiene perfil, se podría redirigir a una página para crearlo,
        # pero por ahora, lo más simple es permitir que la vista continúe
        # para que pueda crear su perfil si llega aquí.
        # Sin embargo, el flujo normal es que sea redirigido a 'perfil_estudiante'
        # y desde allí se le pida crear el perfil.
        pass

    if request.method == 'POST':
        form = EstudianteRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Cuenta creada exitosamente.')
            return redirect('home')
    else:
        form = EstudianteRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inscripciones/registro_estudiante.html', context)


def registro_empresa(request):
    """Registro de nuevas empresas"""
    if request.method == 'POST':
        form = EmpresaRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Empresa registrada exitosamente. Bienvenido al sistema.')
            return redirect('home')
    else:
        form = EmpresaRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inscripciones/registro_empresa.html', context)


def registro_facultad(request):
    """Registro de nuevas facultades"""
    if request.method == 'POST':
        form = FacultadRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Facultad registrada exitosamente. Bienvenido al sistema.')
            return redirect('home')
    else:
        form = FacultadRegistrationForm()
    
    context = {
        'form': form,
    }
    return render(request, 'inscripciones/registro_facultad.html', context)


@login_required
def perfil_estudiante(request):
    """Perfil del estudiante"""
    try:
        estudiante = Estudiante.objects.get(user=request.user)
        # Si el perfil existe, se usan los formularios de actualización
        if request.method == 'POST':
            user_form = UserUpdateForm(request.POST, instance=request.user)
            estudiante_form = EstudianteUpdateForm(request.POST, request.FILES, instance=estudiante)
            if user_form.is_valid() and estudiante_form.is_valid():
                user_form.save()
                estudiante_form.save()
                messages.success(request, 'Perfil actualizado exitosamente.')
                return redirect('perfil_estudiante')
        else:
            user_form = UserUpdateForm(instance=request.user)
            estudiante_form = EstudianteUpdateForm(instance=estudiante)
        
        context = {
            'estudiante': estudiante,
            'user_form': user_form,
            'estudiante_form': estudiante_form,
            'has_profile': True
        }
        return render(request, 'inscripciones/perfil_estudiante.html', context)

    except Estudiante.DoesNotExist:
        # Si el perfil no existe, se usa el formulario de creación de perfil
        if request.method == 'POST':
            form = EstudianteProfileForm(request.POST, request.FILES)
            if form.is_valid():
                perfil = form.save(commit=False)
                perfil.user = request.user
                perfil.save()
                messages.success(request, 'Perfil completado exitosamente.')
                return redirect('perfil_estudiante')
        else:
            form = EstudianteProfileForm()
        
        context = {
            'form': form,
            'has_profile': False
        }
        return render(request, 'inscripciones/perfil_estudiante.html', context)


def lista_empresas(request):
    """Lista todas las empresas"""
    empresas = Empresa.objects.filter(activa=True).order_by('nombre')
    
    paginator = Paginator(empresas, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'page_obj': page_obj,
    }
    return render(request, 'inscripciones/lista_empresas.html', context)


def detalle_empresa(request, pk):
    """Detalle de una empresa"""
    empresa = get_object_or_404(Empresa, pk=pk, activa=True)
    practicas = Practica.objects.filter(empresa=empresa, activa=True).order_by('-fecha_publicacion')
    
    context = {
        'empresa': empresa,
        'practicas': practicas,
    }
    return render(request, 'inscripciones/detalle_empresa.html', context)


@login_required
def gestionar_documentos(request, inscripcion_pk):
    """Gestión de documentos de una inscripción"""
    inscripcion = get_object_or_404(Inscripcion, pk=inscripcion_pk, estudiante__user=request.user)
    
    if request.method == 'POST':
        form = DocumentoInscripcionForm(request.POST, request.FILES)
        if form.is_valid():
            documento = form.save(commit=False)
            documento.inscripcion = inscripcion
            documento.save()
            messages.success(request, 'Documento subido exitosamente.')
            return redirect('gestionar_documentos', inscripcion_pk=inscripcion_pk)
    else:
        form = DocumentoInscripcionForm()
    
    documentos = inscripcion.documentos.all()
    
    context = {
        'inscripcion': inscripcion,
        'documentos': documentos,
        'form': form,
    }
    return render(request, 'inscripciones/gestionar_documentos.html', context)


@login_required
def eliminar_documento(request, documento_pk):
    """Eliminar un documento"""
    documento = get_object_or_404(DocumentoInscripcion, pk=documento_pk, inscripcion__estudiante__user=request.user)
    inscripcion_pk = documento.inscripcion.pk
    documento.delete()
    messages.success(request, 'Documento eliminado exitosamente.')
    return redirect('gestionar_documentos', inscripcion_pk=inscripcion_pk)


@login_required
def detalle_inscripcion(request, pk):
    """Ver detalles de una inscripción específica"""
    inscripcion = get_object_or_404(Inscripcion, pk=pk, estudiante__user=request.user)
    documentos = inscripcion.documentos.all()
    
    context = {
        'inscripcion': inscripcion,
        'documentos': documentos,
    }
    return render(request, 'inscripciones/detalle_inscripcion.html', context)
