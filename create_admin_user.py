#!/usr/bin/env python3
"""
Script para crear el usuario administrador inicial
Ejecutar solo una vez después de la primera migración
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.database import db
from app.models.user import User

def create_admin_user():
    """Crea el usuario administrador inicial"""
    print("🔐 Creando usuario administrador inicial...")
    
    try:
        # Crear aplicación una sola vez
        app = create_app()
        
        with app.app_context():
            # Crear todas las tablas si no existen
            from app.database import db
            db.create_all()
            
            # Verificar si ya existe un administrador
            existing_admin = User.query.filter_by(role='admin').first()
            if existing_admin:
                print("⚠️  Ya existe un usuario administrador:")
                print(f"   Usuario: {existing_admin.username}")
                print(f"   Email: {existing_admin.email}")
                print(f"   Rol: {existing_admin.role}")
                return
            
            # Datos del administrador
            admin_data = {
                'username': 'admin',
                'email': 'admin@stockmanagement.com',
                'password': 'Admin123!',
                'first_name': 'Administrador',
                'last_name': 'Sistema',
                'role': 'admin'
            }
            
            # Crear usuario administrador
            admin_user = User(
                username=admin_data['username'],
                email=admin_data['email'],
                password=admin_data['password'],
                first_name=admin_data['first_name'],
                last_name=admin_data['last_name'],
                role=admin_data['role']
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuario administrador creado exitosamente!")
            print(f"   Usuario: {admin_data['username']}")
            print(f"   Contraseña: {admin_data['password']}")
            print(f"   Email: {admin_data['email']}")
            print(f"   Rol: {admin_data['role']}")
            print("\n⚠️  IMPORTANTE: Cambia la contraseña después del primer login!")
            
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        sys.exit(1)

def create_sample_users():
    """Crea usuarios de ejemplo para testing"""
    print("\n👥 Creando usuarios de ejemplo...")
    
    try:
        # Usar la misma instancia de la aplicación
        with app.app_context():
            # Usuario Gerente
            manager_data = {
                'username': 'gerente',
                'email': 'gerente@stockmanagement.com',
                'password': 'Gerente123!',
                'first_name': 'Juan',
                'last_name': 'Gerente',
                'role': 'manager'
            }
            
            if not User.get_by_username(manager_data['username']):
                manager_user = User(**manager_data)
                db.session.add(manager_user)
                print(f"✅ Usuario gerente creado: {manager_data['username']}")
            
            # Usuario Normal
            user_data = {
                'username': 'usuario',
                'email': 'usuario@stockmanagement.com',
                'password': 'Usuario123!',
                'first_name': 'María',
                'last_name': 'Usuario',
                'role': 'user'
            }
            
            if not User.get_by_username(user_data['username']):
                user = User(**user_data)
                db.session.add(user)
                print(f"✅ Usuario normal creado: {user_data['username']}")
            
            # Usuario Solo Lectura
            viewer_data = {
                'username': 'viewer',
                'email': 'viewer@stockmanagement.com',
                'password': 'Viewer123!',
                'first_name': 'Carlos',
                'last_name': 'Lector',
                'role': 'viewer'
            }
            
            if not User.get_by_username(viewer_data['username']):
                viewer_user = User(**viewer_data)
                db.session.add(viewer_user)
                print(f"✅ Usuario viewer creado: {viewer_data['username']}")
            
            db.session.commit()
            print("✅ Usuarios de ejemplo creados exitosamente!")
            
    except Exception as e:
        print(f"❌ Error creando usuarios de ejemplo: {e}")

def main():
    """Función principal"""
    print("🚀 Sistema de Gestión de Inventario - Setup de Usuarios")
    print("=" * 60)
    
    # Crear administrador
    create_admin_user()
    
    # Crear usuarios de ejemplo
    create_sample_users()
    
    print("\n" + "=" * 60)
    print("🎉 Setup de usuarios completado!")
    print("\n📋 Credenciales de acceso:")
    print("   🔐 Admin: admin / Admin123!")
    print("   👔 Gerente: gerente / Gerente123!")
    print("   👤 Usuario: usuario / Usuario123!")
    print("   👁️  Viewer: viewer / Viewer123!")
    print("\n⚠️  RECUERDA: Cambia las contraseñas después del primer login!")
    print("=" * 60)

if __name__ == "__main__":
    main()
