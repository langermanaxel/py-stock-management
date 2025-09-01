#!/usr/bin/env python3
"""
Script para iniciar el backend del Sistema de Gestión de Inventario
con verificación de dependencias y configuración.
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_dependencies():
    """Verifica que todas las dependencias estén instaladas"""
    print("🔍 Verificando dependencias...")
    
    required_packages = [
        'flask', 'flask-cors', 'flask-jwt-extended', 
        'flask-sqlalchemy', 'flask-migrate', 'flask-smorest'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NO INSTALADO")
    
    if missing_packages:
        print(f"\n❌ Faltan dependencias: {', '.join(missing_packages)}")
        print("💡 Instala con: pip install -r requirements.txt")
        return False
    
    print("✅ Todas las dependencias están instaladas")
    return True

def check_environment():
    """Verifica la configuración del entorno"""
    print("\n🔧 Verificando configuración del entorno...")
    
    # Verificar archivo .env
    env_file = Path('.env')
    if not env_file.exists():
        print("⚠️ Archivo .env no encontrado")
        print("💡 Ejecuta: python setup_cors.py")
        return False
    
    # Verificar variables críticas
    from dotenv import load_dotenv
    load_dotenv()
    
    critical_vars = ['SECRET_KEY', 'JWT_SECRET_KEY', 'CORS_ORIGINS']
    missing_vars = []
    
    for var in critical_vars:
        if not os.getenv(var):
            missing_vars.append(var)
    
    if missing_vars:
        print(f"⚠️ Variables de entorno faltantes: {', '.join(missing_vars)}")
        print("💡 Ejecuta: python setup_cors.py")
        return False
    
    print("✅ Configuración del entorno correcta")
    return True

def check_database():
    """Verifica que la base de datos esté accesible"""
    print("\n🗄️ Verificando base de datos...")
    
    try:
        # Intentar importar y verificar la base de datos
        from app import create_app
        from app.database import db
        
        app = create_app()
        with app.app_context():
            # Verificar conexión
            db.engine.execute('SELECT 1')
            print("✅ Base de datos accesible")
            return True
    except Exception as e:
        print(f"❌ Error en base de datos: {e}")
        print("💡 Verifica que la base de datos esté configurada correctamente")
        return False

def start_backend():
    """Inicia el backend"""
    print("\n🚀 Iniciando backend...")
    
    try:
        # Iniciar el servidor en segundo plano
        process = subprocess.Popen([
            sys.executable, 'run.py'
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ Esperando que el servidor se inicie...")
        
        # Esperar un poco para que el servidor se inicie
        time.sleep(3)
        
        # Verificar si el servidor está respondiendo
        try:
            response = requests.get('http://127.0.0.1:5000', timeout=5)
            if response.status_code == 200:
                print("✅ Backend iniciado correctamente en http://127.0.0.1:5000")
                print("🌐 API disponible en http://127.0.0.1:5000/api")
                print("📚 Documentación en http://127.0.0.1:5000/swagger-ui")
                return process
            else:
                print(f"⚠️ Servidor respondiendo pero con status: {response.status_code}")
                return process
        except requests.exceptions.RequestException:
            print("⚠️ Servidor iniciado pero no responde aún")
            print("💡 Espera unos segundos más y verifica en el navegador")
            return process
            
    except Exception as e:
        print(f"❌ Error iniciando backend: {e}")
        return None

def show_status():
    """Muestra el estado actual del sistema"""
    print("\n" + "="*60)
    print("📊 ESTADO DEL SISTEMA:")
    print("="*60)
    
    # Verificar puerto 5000
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 5000))
        sock.close()
        
        if result == 0:
            print("🔌 Puerto 5000: ✅ EN USO (Backend ejecutándose)")
        else:
            print("🔌 Puerto 5000: ❌ LIBRE (Backend no ejecutándose)")
    except:
        print("🔌 Puerto 5000: ❓ NO SE PUDO VERIFICAR")
    
    # Verificar puerto 8080
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('127.0.0.1', 8080))
        sock.close()
        
        if result == 0:
            print("🌐 Puerto 8080: ✅ EN USO (Frontend ejecutándose)")
        else:
            print("🌐 Puerto 8080: ❌ LIBRE (Frontend no ejecutándose)")
    except:
        print("🌐 Puerto 8080: ❓ NO SE PUDO VERIFICAR")
    
    print("\n💡 Para probar el sistema:")
    print("   1. Backend: http://127.0.0.1:5000")
    print("   2. Frontend: http://localhost:8080")
    print("   3. API: http://127.0.0.1:5000/api")
    print("   4. Swagger: http://127.0.0.1:5000/swagger-ui")

def main():
    """Función principal"""
    
    print("🚀 INICIADOR DE BACKEND - STOCK MANAGEMENT")
    print("="*50)
    
    # Verificaciones previas
    if not check_dependencies():
        return
    
    if not check_environment():
        return
    
    if not check_database():
        return
    
    # Iniciar backend
    process = start_backend()
    
    if process:
        print("\n✅ Backend iniciado exitosamente!")
        print("💡 Presiona Ctrl+C para detener el servidor")
        
        try:
            # Mantener el proceso activo
            process.wait()
        except KeyboardInterrupt:
            print("\n🛑 Deteniendo servidor...")
            process.terminate()
            process.wait()
            print("✅ Servidor detenido")
    else:
        print("❌ No se pudo iniciar el backend")
        print("💡 Verifica los logs de error")

if __name__ == "__main__":
    main()
