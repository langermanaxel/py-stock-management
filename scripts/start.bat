@echo off
echo 🚀 Iniciando Sistema de Gestión de Inventario...
echo.

REM Verificar si existe el entorno virtual
if not exist "env" (
    echo ❌ Entorno virtual no encontrado
    echo Ejecuta: python setup.py
    pause
    exit /b 1
)

REM Activar entorno virtual
echo 📦 Activando entorno virtual...
call env\Scripts\activate.bat

REM Verificar si la base de datos existe
if not exist "instance\stock_management.db" (
    echo 🗄️ Inicializando base de datos...
    python -c "from app import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.create_all()"
    
    echo 📋 Cargando datos de ejemplo...
    if exist "load_sample_data.py" (
        python load_sample_data.py
    )
)

REM Ejecutar la aplicación
echo 🌐 Iniciando servidor Flask...
echo.
echo ====================================
echo    Sistema de Gestión de Inventario
echo ====================================
echo.
echo 🌐 URL: http://localhost:5000
echo ⚠️  Presiona Ctrl+C para detener
echo.

python run.py
