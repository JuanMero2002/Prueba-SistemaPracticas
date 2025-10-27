from django.contrib import admin
from .models import Carrera, Estudiante, Empresa, Practica, Inscripcion, DocumentoInscripcion, Facultad, PracticaInterna, InscripcionInterna


@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'activa']
    list_filter = ['activa']
    search_fields = ['nombre', 'codigo']
    ordering = ['nombre']


@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ['codigo_estudiante', 'user', 'carrera', 'ciclo_actual', 'activo']
    list_filter = ['carrera', 'ciclo_actual', 'activo']
    search_fields = ['codigo_estudiante', 'user__first_name', 'user__last_name', 'user__email']
    ordering = ['codigo_estudiante']
    readonly_fields = ['fecha_registro']


@admin.register(Empresa)
class EmpresaAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'ruc', 'sector', 'activa']
    list_filter = ['sector', 'activa']
    search_fields = ['nombre', 'ruc', 'contacto_responsable']
    ordering = ['nombre']
    readonly_fields = ['fecha_registro']


@admin.register(Practica)
class PracticaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'empresa', 'estado', 'cupos_disponibles', 'fecha_inicio', 'fecha_limite_inscripcion']
    list_filter = ['estado', 'empresa', 'fecha_inicio', 'activa']
    search_fields = ['titulo', 'empresa__nombre', 'descripcion']
    ordering = ['-fecha_publicacion']
    readonly_fields = ['fecha_publicacion']
    date_hierarchy = 'fecha_inicio'


@admin.register(Inscripcion)
class InscripcionAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'practica', 'estado', 'fecha_inscripcion', 'fecha_evaluacion']
    list_filter = ['estado', 'fecha_inscripcion', 'practica__empresa']
    search_fields = ['estudiante__user__first_name', 'estudiante__user__last_name', 'practica__titulo']
    ordering = ['-fecha_inscripcion']
    readonly_fields = ['fecha_inscripcion']
    date_hierarchy = 'fecha_inscripcion'


@admin.register(DocumentoInscripcion)
class DocumentoInscripcionAdmin(admin.ModelAdmin):
    list_display = ['inscripcion', 'tipo', 'nombre', 'fecha_subida']
    list_filter = ['tipo', 'fecha_subida']
    search_fields = ['nombre', 'inscripcion__estudiante__user__first_name']
    ordering = ['-fecha_subida']
    readonly_fields = ['fecha_subida']


@admin.register(Facultad)
class FacultadAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'codigo', 'decano', 'activa']
    list_filter = ['activa']
    search_fields = ['nombre', 'codigo', 'decano', 'contacto_responsable']
    ordering = ['nombre']
    readonly_fields = ['fecha_registro']


@admin.register(PracticaInterna)
class PracticaInternaAdmin(admin.ModelAdmin):
    list_display = ['titulo', 'facultad', 'tipo_servicio', 'estado', 'cupos_disponibles', 'fecha_inicio', 'fecha_limite_inscripcion']
    list_filter = ['estado', 'facultad', 'tipo_servicio', 'fecha_inicio', 'activa']
    search_fields = ['titulo', 'facultad__nombre', 'descripcion']
    ordering = ['-fecha_publicacion']
    readonly_fields = ['fecha_publicacion']
    date_hierarchy = 'fecha_inicio'


@admin.register(InscripcionInterna)
class InscripcionInternaAdmin(admin.ModelAdmin):
    list_display = ['estudiante', 'practica_interna', 'estado', 'fecha_inscripcion', 'fecha_evaluacion']
    list_filter = ['estado', 'fecha_inscripcion', 'practica_interna__facultad']
    search_fields = ['estudiante__user__first_name', 'estudiante__user__last_name', 'practica_interna__titulo']
    ordering = ['-fecha_inscripcion']
    readonly_fields = ['fecha_inscripcion']
    date_hierarchy = 'fecha_inscripcion'
