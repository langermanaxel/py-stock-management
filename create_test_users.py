#!/usr/bin/env python3
"""
Script para crear usuarios de prueba con diferentes roles
"""

import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database import db
from app.models.user import User

def create_test_users():
    """Crear usuarios de prueba con diferentes roles"""
    app = create_app()
    
    with app.app_context():
        # Verificar si los usuarios ya existen
        existing_users = {
            'gerente': User.get_by_username('gerente'),
            'usuario': User.get_by_username('usuario'),
            'viewer': User.get_by_username('viewer')
        }
        
        users_to_create = []
        
        # Usuario Gerente
        if not existing_users['gerente']:
            gerente_data = {
                'username': 'gerente',
                'email': 'gerente@stockmanagement.com',
                'password': 'Gerente123!',
                'first_name': 'Gerente',
                'last_name': 'Sistema',
                'role': 'manager'
            }
            users_to_create.append(('gerente', gerente_data))
            print("✅ Usuario gerente creado")
        else:
            print("ℹ️  Usuario gerente ya existe")
        
        # Usuario Normal
        if not existing_users['usuario']:
            usuario_data = {
                'username': 'usuario',
                'email': 'usuario@stockmanagement.com',
                'password': 'Usuario123!',
                'first_name': 'Usuario',
                'last_name': 'Normal',
                'role': 'user'
            }
            users_to_create.append(('usuario', usuario_data))
            print("✅ Usuario normal creado")
        else:
            print("ℹ️  Usuario normal ya existe")
        
        # Usuario Solo Lectura
        if not existing_users['viewer']:
            viewer_data = {
                'username': 'viewer',
                'email': 'viewer@stockmanagement.com',
                'password': 'Viewer123!',
                'first_name': 'Lector',
                'last_name': 'Solo',
                'role': 'viewer'
            }
            users_to_create.append(('viewer', viewer_data))
            print("✅ Usuario solo lectura creado")
        else:
            print("ℹ️  Usuario solo lectura ya existe")
        
        # Crear usuarios
        for username, user_data in users_to_create:
            try:
                user = User(**user_data)
                db.session.add(user)
                print(f"✅ Usuario {username} agregado a la sesión")
            except Exception as e:
                print(f"❌ Error creando usuario {username}: {e}")
        
        # Commit si hay usuarios para crear
        if users_to_create:
            try:
                db.session.commit()
                print("✅ Todos los usuarios creados exitosamente")
            except Exception as e:
                db.session.rollback()
                print(f"❌ Error en commit: {e}")
        else:
            print("ℹ️  No hay usuarios nuevos para crear")
        
        # Mostrar resumen de usuarios
        print("\n📋 Resumen de usuarios disponibles:")
        all_users = User.query.all()
        for user in all_users:
            status = "🟢 Activo" if user.is_active else "🔴 Inactivo"
            print(f"  • {user.username} ({user.role}) - {status}")

if __name__ == "__main__":
    print("🚀 Creando usuarios de prueba...")
    create_test_users()
    print("✨ Proceso completado!")
