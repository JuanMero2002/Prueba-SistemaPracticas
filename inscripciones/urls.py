from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Páginas principales
    path('', views.home, name='home'),
    path('practicas/', views.lista_practicas, name='lista_practicas'),
    path('practicas/<int:pk>/', views.detalle_practica, name='detalle_practica'),
    path('empresas/', views.lista_empresas, name='lista_empresas'),
    path('empresas/<int:pk>/', views.detalle_empresa, name='detalle_empresa'),
    
    # Autenticación
    path('registro/', views.registro_estudiante, name='registro_estudiante'),
    path('login/', auth_views.LoginView.as_view(template_name='inscripciones/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    
    # Perfil de estudiante
    path('perfil/', views.perfil_estudiante, name='perfil_estudiante'),
    
    # Inscripciones
    path('inscribirse/<int:pk>/', views.inscribirse_practica, name='inscribirse_practica'),
    path('mis-inscripciones/', views.mis_inscripciones, name='mis_inscripciones'),
    path('inscripcion/<int:pk>/', views.detalle_inscripcion, name='detalle_inscripcion'),
    path('cancelar-inscripcion/<int:pk>/', views.cancelar_inscripcion, name='cancelar_inscripcion'),
    
    # Gestión de documentos
    path('inscripcion/<int:inscripcion_pk>/documentos/', views.gestionar_documentos, name='gestionar_documentos'),
    path('documento/<int:documento_pk>/eliminar/', views.eliminar_documento, name='eliminar_documento'),
]
