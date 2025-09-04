#!/usr/bin/env python3
"""
Script para crear usuarios demo con las credenciales correctas
"""

import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash
from datetime import datetime

def create_demo_users():
    """Crea los usuarios demo con las credenciales correctas"""
    db_path = Path("instance/stock_management.db")
    
    if not db_path.exists():
        print("❌ Base de datos no encontrada")
        return
    
    # Usuarios demo con credenciales correctas - ROLES ESTANDARIZADOS AL INGLÉS
    demo_users = [
        {
            "username": "admin",
            "password": "Admin123!",
            "email": "admin@stockmanagement.com",
            "first_name": "Admin",
            "last_name": "Sistema",
            "role": "admin"
        },
        {
            "username": "gerente",
            "password": "Gerente123!",
            "email": "gerente@stockmanagement.com",
            "first_name": "Gerente",
            "last_name": "Sistema",
            "role": "manager"  # Estandarizado al inglés
        },
        {
            "username": "usuario",
            "password": "Usuario123!",
            "email": "usuario@stockmanagement.com",
            "first_name": "Usuario",
            "last_name": "Sistema",
            "role": "user"  # Estandarizado al inglés
        },
        {
            "username": "viewer",
            "password": "Viewer123!",
            "email": "viewer@stockmanagement.com",
            "first_name": "Viewer",
            "last_name": "Sistema",
            "role": "viewer"
        }
    ]
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().isoformat()
        
        for user_data in demo_users:
            username = user_data["username"]
            
            # Verificar si el usuario ya existe
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if existing_user:
                print(f"🔄 Actualizando usuario existente: {username}")
                # Actualizar contraseña y datos
                cursor.execute("""
                    UPDATE users 
                    SET password_hash = ?, email = ?, first_name = ?, last_name = ?, 
                        role = ?, is_active = 1, updated_at = ?
                    WHERE username = ?
                """, (
                    generate_password_hash(user_data["password"]),
                    user_data["email"],
                    user_data["first_name"],
                    user_data["last_name"],
                    user_data["role"],
                    current_time,
                    username
                ))
            else:
                print(f"➕ Creando nuevo usuario: {username}")
                # Crear nuevo usuario
                cursor.execute("""
                    INSERT INTO users (username, password_hash, email, first_name, last_name, 
                                    role, is_active, created_at, updated_at)
                    VALUES (?, ?, ?, ?, ?, ?, 1, ?, ?)
                """, (
                    username,
                    generate_password_hash(user_data["password"]),
                    user_data["email"],
                    user_data["first_name"],
                    user_data["last_name"],
                    user_data["role"],
                    current_time,
                    current_time
                ))
        
        conn.commit()
        conn.close()
        
        print("\n✅ Usuarios demo creados/actualizados correctamente")
        print("\n🔑 Credenciales de acceso:")
        for user_data in demo_users:
            print(f"   {user_data['username']} / {user_data['password']} (Rol: {user_data['role']})")
        
    except Exception as e:
        print(f"❌ Error al crear usuarios demo: {e}")

if __name__ == "__main__":
    create_demo_users()
