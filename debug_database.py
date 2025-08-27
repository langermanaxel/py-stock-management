#!/usr/bin/env python3
"""
Script para diagnosticar problemas de base de datos
"""

import os
import sys
from pathlib import Path

def debug_database_path():
    """Diagnostica la ruta de la base de datos"""
    
    print("🔍 DIAGNÓSTICO DE RUTA DE BASE DE DATOS")
    print("="*50)
    
    # Obtener directorio actual
    current_dir = os.getcwd()
    print(f"📁 Directorio actual: {current_dir}")
    
    # Verificar si existe el directorio instance
    instance_dir = Path('instance')
    print(f"📁 Directorio 'instance': {instance_dir.absolute()}")
    print(f"   Existe: {instance_dir.exists()}")
    
    if instance_dir.exists():
        print(f"   Es directorio: {instance_dir.is_dir()}")
        print(f"   Permisos: {oct(instance_dir.stat().st_mode)[-3:]}")
    
    # Verificar archivo .env
    env_file = Path('.env')
    print(f"\n📄 Archivo '.env': {env_file.absolute()}")
    print(f"   Existe: {env_file.exists()}")
    
    if env_file.exists():
        print(f"   Tamaño: {env_file.stat().st_size} bytes")
        print(f"   Permisos: {oct(env_file.stat().st_mode)[-3:]}")
    
    # Verificar variables de entorno
    print(f"\n🔧 Variables de entorno:")
    print(f"   DATABASE_URL: {os.getenv('DATABASE_URL', 'NO DEFINIDA')}")
    print(f"   SECRET_KEY: {os.getenv('SECRET_KEY', 'NO DEFINIDA')}")
    print(f"   JWT_SECRET_KEY: {os.getenv('JWT_SECRET_KEY', 'NO DEFINIDA')}")
    
    # Calcular ruta de base de datos
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    database_path = os.path.join(basedir, 'instance', 'stock_management.db')
    
    print(f"\n🗄️ Ruta calculada de base de datos:")
    print(f"   basedir: {basedir}")
    print(f"   database_path: {database_path}")
    print(f"   Existe: {os.path.exists(database_path)}")
    
    # Verificar permisos del directorio padre
    parent_dir = os.path.dirname(database_path)
    if os.path.exists(parent_dir):
        print(f"   Directorio padre existe: {os.path.exists(parent_dir)}")
        print(f"   Permisos directorio padre: {oct(os.stat(parent_dir).st_mode)[-3:]}")
    
    return database_path

def test_sqlite_connection():
    """Prueba la conexión a SQLite"""
    
    print(f"\n🔌 PRUEBA DE CONEXIÓN SQLITE")
    print("="*50)
    
    try:
        import sqlite3
        
        # Probar con ruta absoluta
        current_dir = os.getcwd()
        test_db_path = os.path.join(current_dir, 'instance', 'test.db')
        
        print(f"📁 Probando con ruta: {test_db_path}")
        
        # Crear base de datos de prueba
        conn = sqlite3.connect(test_db_path)
        cursor = conn.cursor()
        
        # Crear tabla de prueba
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_table (
                id INTEGER PRIMARY KEY,
                name TEXT
            )
        ''')
        
        # Insertar dato de prueba
        cursor.execute('INSERT INTO test_table (name) VALUES (?)', ('test',))
        
        # Verificar
        cursor.execute('SELECT * FROM test_table')
        result = cursor.fetchone()
        
        print(f"✅ Conexión SQLite exitosa")
        print(f"   Tabla creada: {result}")
        
        # Cerrar conexión
        conn.close()
        
        # Eliminar archivo de prueba
        os.remove(test_db_path)
        print("   Archivo de prueba eliminado")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en conexión SQLite: {e}")
        return False

def test_flask_sqlalchemy():
    """Prueba Flask-SQLAlchemy"""
    
    print(f"\n🐍 PRUEBA DE FLASK-SQLALCHEMY")
    print("="*50)
    
    try:
        # Importar Flask
        from app import create_app
        from app.database import db
        
        print("✅ Flask y SQLAlchemy importados correctamente")
        
        # Crear aplicación
        app = create_app()
        print("✅ Aplicación Flask creada")
        
        # Verificar configuración
        print(f"   DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print(f"   DEBUG: {app.config.get('DEBUG')}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error en Flask-SQLAlchemy: {e}")
        return False

def create_simple_database():
    """Crea una base de datos simple"""
    
    print(f"\n🔧 CREANDO BASE DE DATOS SIMPLE")
    print("="*50)
    
    try:
        # Crear directorio instance
        instance_dir = Path('instance')
        if not instance_dir.exists():
            instance_dir.mkdir()
            print("✅ Directorio 'instance' creado")
        
        # Crear base de datos SQLite simple
        import sqlite3
        
        db_path = instance_dir / 'stock_management.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla de usuarios simple
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear usuario admin
        from werkzeug.security import generate_password_hash
        
        admin_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT OR REPLACE INTO users 
            (username, email, password_hash, first_name, last_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('admin', 'admin@stockmanagement.com', admin_password, 'Admin', 'Sistema', 'admin', 1))
        
        conn.commit()
        conn.close()
        
        print("✅ Base de datos simple creada")
        print("   Usuario: admin")
        print("   Contraseña: admin123")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando base de datos simple: {e}")
        return False

def main():
    """Función principal"""
    
    print("🔍 DIAGNÓSTICO COMPLETO DE BASE DE DATOS")
    print("="*60)
    
    # Diagnóstico de ruta
    db_path = debug_database_path()
    
    # Prueba de SQLite
    sqlite_ok = test_sqlite_connection()
    
    # Prueba de Flask-SQLAlchemy
    flask_ok = test_flask_sqlalchemy()
    
    # Crear base de datos simple si es necesario
    if sqlite_ok and not os.path.exists(db_path):
        create_simple_database()
    
    print("\n" + "="*60)
    print("📊 RESUMEN DEL DIAGNÓSTICO:")
    print("="*60)
    print(f"🔌 SQLite: {'✅ OK' if sqlite_ok else '❌ FALLO'}")
    print(f"🐍 Flask-SQLAlchemy: {'✅ OK' if flask_ok else '❌ FALLO'}")
    print(f"🗄️ Base de datos: {'✅ EXISTE' if os.path.exists(db_path) else '❌ NO EXISTE'}")
    
    if sqlite_ok and flask_ok:
        print("\n💡 Recomendación:")
        if os.path.exists(db_path):
            print("   La base de datos existe, intenta iniciar el backend")
        else:
            print("   Ejecuta: python create_simple_database.py")
    else:
        print("\n❌ Hay problemas que necesitan ser resueltos")

if __name__ == "__main__":
    main()
