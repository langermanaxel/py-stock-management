#!/bin/bash

echo "🚀 Iniciando Sistema de Gestión de Inventario..."
echo

# Verificar si existe el entorno virtual
if [ ! -d "env" ]; then
    echo "❌ Entorno virtual no encontrado"
    echo "Ejecuta: python3 setup.py"
    exit 1
fi

# Activar entorno virtual
echo "📦 Activando entorno virtual..."
source env/bin/activate

# Verificar si la base de datos existe
if [ ! -f "instance/stock_management.db" ]; then
    echo "🗄️ Inicializando base de datos..."
    python -c "from app import create_app; from app.database import db; app = create_app(); app.app_context().push(); db.create_all()"
    
    echo "📋 Cargando datos de ejemplo..."
    if [ -f "load_sample_data.py" ]; then
        python load_sample_data.py
    fi
fi

# Ejecutar la aplicación
echo "🌐 Iniciando servidor Flask..."
echo
echo "===================================="
echo "   Sistema de Gestión de Inventario"
echo "===================================="
echo
echo "🌐 URL: http://localhost:5000"
echo "⚠️  Presiona Ctrl+C para detener"
echo

python run.py
