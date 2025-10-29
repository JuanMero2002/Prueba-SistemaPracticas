# Guía de Instalación - Sistema de Prácticas Pre Profesionales

## Requisitos Previos

- Python 3.8 o superior
- pip (gestor de paquetes de Python)
- Git (opcional)

## Instrucciones de Instalación

### 1. Clonar o Acceder al Proyecto

Si tienes el proyecto en un repositorio Git:
```bash
git clone <url-del-repositorio>
cd practicas_universidad
```

### 2. Crear Entorno Virtual

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Base de Datos

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Cargar Datos Iniciales (Carreras)

```bash
python manage.py loaddata inscripciones/fixtures/carreras.json
```

### 6. Crear Superusuario

```bash
python manage.py createsuperuser
```

Seguir las instrucciones para crear el usuario administrador.

### 7. Verificar Configuración

```bash
python manage.py check
```

### 8. Ejecutar Servidor de Desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/

## Acceso al Sistema

### Panel de Administración
- URL: http://127.0.0.1:8000/admin/
- Usar las credenciales del superusuario creado

### Acceso para Estudiantes
- URL: http://127.0.0.1:8000/
- Registro: http://127.0.0.1:8000/registro/
- Login: http://127.0.0.1:8000/login/

## Estructura del Sistema

### Para Estudiantes:
1. **Registro**: Crear cuenta completando formulario
2. **Perfil**: Editar información personal y académica
3. **Búsqueda**: Buscar prácticas por título, empresa, sector, fechas
4. **Inscripción**: Inscribirse a prácticas disponibles
5. **Seguimiento**: Ver estado de inscripciones

### Para Administradores:
1. **Gestión de Carreras**: Agregar y editar carreras
2. **Gestión de Empresas**: Registrar empresas participantes
3. **Gestión de Prácticas**: Publicar y administrar oportunidades de práctica
4. **Evaluación**: Aprobar o rechazar inscripciones de estudiantes
5. **Reportes**: Ver estadísticas y reportes del sistema

## Comandos Útiles

### Crear Aplicación
```bash
python manage.py startapp nombre_app
```

### Hacer Migraciones
```bash
python manage.py makemigrations
python manage.py migrate
```

### Crear Superusuario
```bash
python manage.py createsuperuser
```

### Recopilar Archivos Estáticos
```bash
python manage.py collectstatic
```

### Ejecutar Tests
```bash
python manage.py test
```

### Shell de Django
```bash
python manage.py shell
```

## Solución de Problemas

### Error: No se encuentra el módulo
```bash
pip install -r requirements.txt
```

### Error de Migraciones
```bash
python manage.py migrate --run-syncdb
```

### Error de Permisos en Windows
Ejecutar como administrador o usar:
```bash
python -m venv venv
.\venv\Scripts\activate
```

### Base de Datos Bloqueada
Cerrar todas las conexiones y eliminar db.sqlite3:
```bash
del db.sqlite3
python manage.py migrate
```

## Datos de Prueba

Para generar datos de prueba (opcional):
```bash
python manage.py shell
```

Luego en el shell de Python:
```python
from inscripciones.models import Empresa, Practica
from django.utils import timezone
from datetime import timedelta

# Crear empresa de prueba
empresa = Empresa.objects.create(
    nombre="Empresa Ejemplo",
    ruc="12345678901",
    direccion="Calle Principal 123",
    telefono="987654321",
    email="contacto@empresa.com",
    contacto_responsable="Juan Pérez",
    sector="Tecnología",
    descripcion="Empresa líder en desarrollo de software"
)

# Crear práctica de prueba
practica = Practica.objects.create(
    empresa=empresa,
    titulo="Práctica en Desarrollo de Software",
    descripcion="Oportunidad para estudiantes de Ingeniería de Sistemas",
    requisitos="Conocimientos en Python, Django, HTML/CSS",
    duracion_semanas=12,
    horas_semana=20,
    fecha_inicio=timezone.now().date(),
    fecha_fin=(timezone.now() + timedelta(weeks=12)).date(),
    cupos_totales=5,
    cupos_disponibles=5,
    estado='disponible',
    fecha_limite_inscripcion=timezone.now() + timedelta(days=30)
)
```

## Recursos Adicionales

- Documentación Django: https://docs.djangoproject.com/
- Bootstrap 5: https://getbootstrap.com/
- Django Crispy Forms: https://django-crispy-forms.readthedocs.io/

## Soporte

Para problemas o consultas sobre el sistema, contactar al equipo de desarrollo.

---

**Versión**: 1.0.0
**Última Actualización**: 2024

