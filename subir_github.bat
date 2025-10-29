@echo off
echo ========================================
echo Subiendo Proyecto a GitHub
echo ========================================
echo.

REM Verificar si Git está instalado
git --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Git no está instalado
    echo Por favor instala Git desde: https://git-scm.com/download/win
    pause
    exit /b 1
)

echo [OK] Git está instalado
echo.

REM Verificar si ya es un repositorio git
if exist .git (
    echo Repositorio Git ya inicializado
) else (
    echo Inicializando repositorio Git...
    git init
    echo [OK] Repositorio inicializado
    echo.
)

echo Agregando archivos...
git add .
echo [OK] Archivos agregados
echo.

echo Creando commit...
git commit -m "Sistema de prácticas pre profesionales v1.1.0 - Funcionalidad completa"
echo [OK] Commit creado
echo.

echo ========================================
echo IMPORTANTE: Próximos pasos manuales
echo ========================================
echo.
echo 1. Crea un repositorio en GitHub.com
echo 2. Ejecuta estos comandos (reemplaza USERNAME y REPO):
echo.
echo    git remote add origin https://github.com/USERNAME/REPO_NAME.git
echo    git branch -M main
echo    git push -u origin main
echo.

pause

