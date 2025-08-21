#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Setup script para el Sistema de Gestión de Inventario
Automatiza la configuración inicial del proyecto
"""

import os
import sys
import subprocess
import json
from pathlib import Path

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"📋 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} - Completado")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e.stderr}")
        return False

def check_python_version():
    """Verifica que la versión de Python sea compatible"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 7):
        print("❌ Se requiere Python 3.7 o superior")
        print(f"   Versión actual: {version.major}.{version.minor}.{version.micro}")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - Compatible")
    return True

def create_virtual_environment():
    """Crea el entorno virtual"""
    if os.path.exists("env"):
        print("⚠️  El entorno virtual ya existe")
        return True
    
    return run_command("python -m venv env", "Creando entorno virtual")

def activate_and_install():
    """Activa el entorno virtual e instala dependencias"""
    if os.name == 'nt':  # Windows
        activation_script = "env\\Scripts\\activate.bat"
        pip_command = "env\\Scripts\\pip.exe"
    else:  # Linux/Mac
        activation_script = "source env/bin/activate"
        pip_command = "env/bin/pip"
    
    # Instalar dependencias
    if not os.path.exists("requirements.txt"):
        print("❌ Archivo requirements.txt no encontrado")
        return False
    
    return run_command(f"{pip_command} install -r requirements.txt", "Instalando dependencias")

def setup_database():
    """Configura la base de datos inicial"""
    # Crear directorio instance si no existe
    os.makedirs("instance", exist_ok=True)
    
    # Script para crear las tablas
    setup_script = '''
from app import create_app
from app.database import db

app = create_app()
with app.app_context():
    db.create_all()
    print("✅ Base de datos inicializada")
'''
    
    # Escribir script temporal
    with open("temp_setup_db.py", "w", encoding="utf-8") as f:
        f.write(setup_script)
    
    # Ejecutar script
    if os.name == 'nt':  # Windows
        python_command = "env\\Scripts\\python.exe"
    else:  # Linux/Mac
        python_command = "env/bin/python"
    
    success = run_command(f"{python_command} temp_setup_db.py", "Inicializando base de datos")
    
    # Limpiar archivo temporal
    if os.path.exists("temp_setup_db.py"):
        os.remove("temp_setup_db.py")
    
    return success

def load_sample_data():
    """Carga datos de ejemplo"""
    if not os.path.exists("load_sample_data.py"):
        print("⚠️  Archivo de datos de ejemplo no encontrado")
        return True
    
    if os.name == 'nt':  # Windows
        python_command = "env\\Scripts\\python.exe"
    else:  # Linux/Mac
        python_command = "env/bin/python"
    
    return run_command(f"{python_command} load_sample_data.py", "Cargando datos de ejemplo")

def create_env_file():
    """Crea archivo .env si no existe"""
    if os.path.exists(".env"):
        print("⚠️  Archivo .env ya existe")
        return True
    
    env_content = '''# Configuración del Sistema de Gestión de Inventario
DATABASE_URL=sqlite:///instance/stock_management.db
SECRET_KEY=tu-clave-secreta-muy-segura-aqui-cambiar-en-produccion
FLASK_ENV=development
DEBUG=True
PORT=5000
'''
    
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        print("✅ Archivo .env creado")
        return True
    except Exception as e:
        print(f"❌ Error creando .env: {e}")
        return False

def show_next_steps():
    """Muestra los siguientes pasos"""
    print("\n" + "="*60)
    print("🎉 ¡CONFIGURACIÓN COMPLETADA!")
    print("="*60)
    print("\n📋 Siguientes pasos:")
    print("\n1. 🚀 Ejecutar la aplicación:")
    
    if os.name == 'nt':  # Windows
        print("   env\\Scripts\\activate.bat")
        print("   python run.py")
    else:  # Linux/Mac
        print("   source env/bin/activate")
        print("   python run.py")
    
    print("\n2. 🌐 Abrir en el navegador:")
    print("   http://localhost:5000")
    
    print("\n3. 📖 Revisar documentación:")
    print("   README.md - Documentación completa")
    print("   DEPLOY_GITHUB.md - Guía para subir a GitHub")
    
    print("\n4. 🔧 Configurar (opcional):")
    print("   .env - Variables de entorno")
    print("   app/config.py - Configuración de la aplicación")
    
    print("\n" + "="*60)
    print("🎯 El sistema incluye datos de ejemplo para probar")
    print("💡 Revisa verify_data.py para validar la instalación")
    print("="*60)

def main():
    """Función principal de configuración"""
    print("🚀 Sistema de Gestión de Inventario - Setup")
    print("=" * 50)
    
    # Verificar Python
    if not check_python_version():
        return False
    
    # Crear entorno virtual
    if not create_virtual_environment():
        return False
    
    # Instalar dependencias
    if not activate_and_install():
        return False
    
    # Crear archivo .env
    if not create_env_file():
        return False
    
    # Configurar base de datos
    if not setup_database():
        return False
    
    # Cargar datos de ejemplo
    load_sample_data()  # No crítico si falla
    
    # Mostrar siguientes pasos
    show_next_steps()
    
    return True

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n❌ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)
