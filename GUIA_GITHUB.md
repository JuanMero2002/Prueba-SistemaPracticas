# Guía para Subir el Proyecto a GitHub

## 📋 Requisitos Previos

1. **Instalar Git**
   - Descargar desde: https://git-scm.com/download/win
   - Instalar con configuración predeterminada
   - Reiniciar la terminal después de instalar

2. **Crear cuenta en GitHub**
   - Visitar: https://github.com
   - Crear cuenta (si no tienes una)
   - Verificar email

## 🚀 Pasos para Subir el Proyecto

### 1. Instalar Git (Si aún no lo tienes)

```bash
# Verificar si git está instalado
git --version
```

Si no está instalado, descárgalo desde: https://git-scm.com/download/win

### 2. Configurar Git (Primera vez)

```bash
# Configurar tu nombre
git config --global user.name "Tu Nombre"

# Configurar tu email
git config --global user.email "tu.email@ejemplo.com"
```

### 3. Inicializar el Repositorio

```bash
# Navegar al directorio del proyecto (ya estás ahí)
cd C:\Users\JuanTCS\practicas_universidad

# Inicializar Git
git init

# Agregar todos los archivos
git add .

# Hacer el primer commit
git commit -m "Sistema de prácticas pre profesionales - versión 1.1.0"
```

### 4. Crear Repositorio en GitHub

1. Ve a: https://github.com/new
2. Nombre del repositorio: `sistema-practicas-universidad` (o el que prefieras)
3. Descripción: "Sistema web Django para gestión de prácticas pre profesionales"
4. Marca como **Público** o **Privado**
5. **NO marques** "Add a README file" (ya tienes uno)
6. Haz clic en "Create repository"

### 5. Conectar y Subir

```bash
# Agregar el repositorio remoto (reemplaza USERNAME y REPO_NAME)
git remote add origin https://github.com/USERNAME/REPO_NAME.git

# Verificar que está conectado
git remote -v

# Subir el código (primera vez)
git branch -M main
git push -u origin main
```

## 📝 Ejemplo Completo

```bash
# 1. Inicializar
git init

# 2. Agregar archivos
git add .

# 3. Hacer commit
git commit -m "Sistema de prácticas pre profesionales v1.1.0"

# 4. Conectar a GitHub (reemplaza con tu repo)
git remote add origin https://github.com/tu-usuario/tu-repositorio.git

# 5. Subir
git branch -M main
git push -u origin main
```

## 🔧 Solución de Problemas

### Error: "Please tell me who you are"
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@ejemplo.com"
```

### Error: "fatal: remote origin already exists"
```bash
git remote remove origin
git remote add origin https://github.com/USERNAME/REPO_NAME.git
```

### Error de autenticación
```bash
# Usar SSH en lugar de HTTPS
git remote set-url origin git@github.com:USERNAME/REPO_NAME.git
```

## 📦 Archivos que NO se suben (gracias a .gitignore)

- `db.sqlite3` - Base de datos local
- `__pycache__/` - Archivos compilados de Python
- `venv/` - Entorno virtual
- `.env` - Variables de entorno
- Archivos `.pyc` - Bytecode de Python

## ✅ Archivos que SÍ se suben

- ✅ Todo el código fuente
- ✅ Templates HTML
- ✅ Modelos y vistas
- ✅ Formularios
- ✅ Configuración
- ✅ README y documentación
- ✅ requirements.txt

## 🌟 Después de Subir

### Crear README con imágenes
Puedes actualizar el README con badges:

```markdown
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Django](https://img.shields.io/badge/django-5.2.7-green.svg)
![License](https://img.shields.io/badge/license-MIT-red.svg)
```

### Agregar topics en GitHub
En la página del repositorio, agrega estos topics:
- python
- django
- web-development
- university
- internships
- bootstrap

## 📊 Estructura del Proyecto

Tu repositorio tendrá esta estructura:

```
sistema-practicas-universidad/
├── .gitignore
├── README.md
├── requirements.txt
├── manage.py
├── inscripciones/
│   ├── models.py
│   ├── views.py
│   ├── forms.py
│   └── admin.py
├── sistema_practicas/
│   ├── settings.py
│   └── urls.py
├── templates/
│   └── inscripciones/
└── static/
```

## 🎯 Siguientes Pasos

Una vez subido:

1. **Agregar colaboradores** (opcional)
2. **Configurar GitHub Actions** para CI/CD (opcional)
3. **Agregar Issues** para bugs o features
4. **Usar Pull Requests** para mejoras
5. **Configurar Pages** para documentación (opcional)

## 💡 Tips

- Haz commits frecuentes con mensajes descriptivos
- Usa branches para features nuevas
- Documenta los cambios importantes
- Mantén el .gitignore actualizado

---

**¡Listo!** Con estos pasos tendrás tu proyecto en GitHub.

