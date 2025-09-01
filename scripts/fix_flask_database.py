#!/usr/bin/env python3
"""
Script para crear la base de datos usando Flask-SQLAlchemy correctamente
"""

import os
import sys
from pathlib import Path

def create_flask_database():
    """Crea la base de datos usando Flask-SQLAlchemy"""
    
    print("🗄️ Creando base de datos con Flask-SQLAlchemy...")
    
    try:
        # Importar Flask y crear la aplicación
        from app import create_app
        from app.database import db
        
        # Crear la aplicación Flask
        app = create_app()
        
        # Verificar configuración
        print(f"📋 DATABASE_URI: {app.config.get('SQLALCHEMY_DATABASE_URI')}")
        print(f"📁 Instance path: {app.instance_path}")
        
        with app.app_context():
            # Crear todas las tablas
            print("📋 Creando todas las tablas...")
            db.create_all()
            print("✅ Tablas creadas correctamente")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando estructura de base de datos: {e}")
        return False

def create_admin_user():
    """Crea un usuario administrador por defecto"""
    
    print("\n👤 Creando usuario administrador...")
    
    try:
        from app import create_app
        from app.database import db
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        
        app = create_app()
        
        with app.app_context():
            # Verificar si ya existe un usuario admin
            admin_user = User.query.filter_by(username='admin').first()
            
            if admin_user:
                print("✅ Usuario administrador ya existe")
                return True
            
            # Crear usuario administrador
            admin_user = User(
                username='admin',
                email='admin@stockmanagement.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Administrador',
                last_name='Sistema',
                role='admin',
                is_active=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuario administrador creado:")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   Email: admin@stockmanagement.com")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        return False

def verify_database():
    """Verifica que la base de datos esté funcionando correctamente"""
    
    print("\n🔍 Verificando base de datos...")
    
    try:
        from app import create_app
        from app.database import db
        from app.models.user import User
        
        app = create_app()
        
        with app.app_context():
            # Verificar conexión
            result = db.session.execute('SELECT 1').scalar()
            if result == 1:
                print("✅ Conexión a base de datos exitosa")
            
            # Verificar tablas
            user_count = User.query.count()
            print(f"✅ Usuarios en BD: {user_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def test_login():
    """Prueba el login con el usuario admin"""
    
    print("\n🔐 Probando login del usuario admin...")
    
    try:
        from app import create_app
        from app.database import db
        from app.models.user import User
        from werkzeug.security import check_password_hash
        
        app = create_app()
        
        with app.app_context():
            # Buscar usuario admin
            admin_user = User.query.filter_by(username='admin').first()
            
            if not admin_user:
                print("❌ Usuario admin no encontrado")
                return False
            
            # Verificar contraseña
            if check_password_hash(admin_user.password_hash, 'admin123'):
                print("✅ Login del usuario admin exitoso")
                print(f"   ID: {admin_user.id}")
                print(f"   Usuario: {admin_user.username}")
                print(f"   Email: {admin_user.email}")
                print(f"   Rol: {admin_user.role}")
                return True
            else:
                print("❌ Contraseña incorrecta para usuario admin")
                return False
            
    except Exception as e:
        print(f"❌ Error probando login: {e}")
        return False

def main():
    """Función principal"""
    
    print("🔧 REPARADOR DE BASE DE DATOS FLASK - STOCK MANAGEMENT")
    print("="*60)
    
    # Crear estructura de base de datos
    if not create_flask_database():
        print("❌ No se pudo crear la estructura de la base de datos")
        return
    
    # Crear usuario administrador
    if not create_admin_user():
        print("❌ No se pudo crear el usuario administrador")
        return
    
    # Verificar que todo funcione
    if not verify_database():
        print("❌ La base de datos no está funcionando correctamente")
        return
    
    # Probar login
    if not test_login():
        print("❌ El login no está funcionando correctamente")
        return
    
    print("\n" + "="*60)
    print("🎉 ¡BASE DE DATOS FLASK CREADA EXITOSAMENTE!")
    print("="*60)
    print("\n💡 Ahora puedes:")
    print("   1. Iniciar el backend: python run.py")
    print("   2. Hacer login con:")
    print("      Usuario: admin")
    print("      Contraseña: admin123")
    print("   3. Probar el frontend en http://localhost:8080")

if __name__ == "__main__":
    main()
