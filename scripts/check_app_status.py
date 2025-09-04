#!/usr/bin/env python3
"""
Script para verificar el estado de la aplicación
"""

import sqlite3
from pathlib import Path
import sys

def check_database():
    """Verificar estado de la base de datos"""
    print("🔍 VERIFICANDO BASE DE DATOS")
    print("=" * 40)
    
    db_path = Path("instance/stock_management.db")
    
    if not db_path.exists():
        print("❌ Base de datos no encontrada")
        return False
    
    print(f"✅ Base de datos existe: {db_path.absolute()}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tabla users
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"✅ Usuarios en la base de datos: {count}")
        
        if count > 0:
            cursor.execute("SELECT username, role, is_active FROM users LIMIT 5")
            users = cursor.fetchall()
            print("📋 Usuarios disponibles:")
            for user in users:
                status = "✅ Activo" if user[2] else "❌ Inactivo"
                print(f"   - {user[0]} ({user[1]}) - {status}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error accediendo a la base de datos: {e}")
        return False

def check_app_creation():
    """Verificar que la aplicación se puede crear"""
    print("\n🔍 VERIFICANDO CREACIÓN DE APLICACIÓN")
    print("=" * 40)
    
    try:
        from app import create_app
        app = create_app()
        print("✅ Aplicación creada correctamente")
        
        # Verificar configuración
        print(f"✅ Debug mode: {app.config.get('DEBUG', 'No definido')}")
        print(f"✅ Secret key: {'✅ Configurado' if app.config.get('SECRET_KEY') else '❌ No configurado'}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando aplicación: {e}")
        return False

def check_dependencies():
    """Verificar dependencias"""
    print("\n🔍 VERIFICANDO DEPENDENCIAS")
    print("=" * 40)
    
    required_modules = [
        'flask',
        'flask_sqlalchemy',
        'flask_jwt_extended',
        'flask_cors',
        'flask_migrate',
        'werkzeug'
    ]
    
    missing = []
    
    for module in required_modules:
        try:
            __import__(module)
            print(f"✅ {module}")
        except ImportError:
            print(f"❌ {module} - NO INSTALADO")
            missing.append(module)
    
    if missing:
        print(f"\n❌ Módulos faltantes: {', '.join(missing)}")
        print("💡 Instala con: pip install -r requirements.txt")
        return False
    
    return True

def check_files():
    """Verificar archivos importantes"""
    print("\n🔍 VERIFICANDO ARCHIVOS IMPORTANTES")
    print("=" * 40)
    
    important_files = [
        "run.py",
        "app/__init__.py",
        "app/api/auth.py",
        "static/js/unified-auth.js",
        "templates/login.html",
        "templates/index.html"
    ]
    
    all_exist = True
    
    for file_path in important_files:
        if Path(file_path).exists():
            print(f"✅ {file_path}")
        else:
            print(f"❌ {file_path} - NO ENCONTRADO")
            all_exist = False
    
    return all_exist

def main():
    """Función principal"""
    print("🔧 DIAGNÓSTICO DE LA APLICACIÓN")
    print("=" * 50)
    print("Verificando el estado de la aplicación...")
    print()
    
    checks = [
        ("Dependencias", check_dependencies),
        ("Archivos", check_files),
        ("Base de datos", check_database),
        ("Creación de app", check_app_creation)
    ]
    
    results = []
    
    for name, check_func in checks:
        try:
            result = check_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error en verificación {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 RESUMEN DE VERIFICACIONES")
    print("=" * 50)
    
    all_passed = True
    
    for name, result in results:
        status = "✅ PASÓ" if result else "❌ FALLÓ"
        print(f"{name}: {status}")
        if not result:
            all_passed = False
    
    print("\n" + "=" * 50)
    
    if all_passed:
        print("🎉 TODAS LAS VERIFICACIONES PASARON!")
        print("✅ La aplicación debería funcionar correctamente")
        print("\n🚀 Para ejecutar la aplicación:")
        print("   python run.py")
        print("   Luego ve a: http://localhost:5000")
    else:
        print("❌ ALGUNAS VERIFICACIONES FALLARON")
        print("💡 Revisa los errores mostrados arriba y corrígelos")
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
