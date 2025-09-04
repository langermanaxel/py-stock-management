#!/usr/bin/env python3
"""
Script para corregir los roles en la base de datos
Estandariza todos los roles al inglés
"""

import sqlite3
from pathlib import Path
from werkzeug.security import generate_password_hash
from datetime import datetime

def fix_roles_database():
    """Corrige los roles en la base de datos para usar nomenclatura en inglés"""
    db_path = Path("instance/stock_management.db")
    
    if not db_path.exists():
        print("❌ Base de datos no encontrada")
        return False
    
    # Mapeo de roles antiguos a nuevos
    role_mapping = {
        'gerente': 'manager',
        'usuario': 'user',
        'viewer': 'viewer',  # Ya está correcto
        'admin': 'admin'     # Ya está correcto
    }
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("🔧 Corrigiendo roles en la base de datos...")
        
        # Obtener todos los usuarios
        cursor.execute("SELECT id, username, role FROM users")
        users = cursor.fetchall()
        
        updated_count = 0
        
        for user_id, username, current_role in users:
            if current_role in role_mapping:
                new_role = role_mapping[current_role]
                
                if current_role != new_role:
                    print(f"🔄 Actualizando {username}: {current_role} → {new_role}")
                    
                    # Actualizar el rol
                    cursor.execute("""
                        UPDATE users 
                        SET role = ?, updated_at = ?
                        WHERE id = ?
                    """, (new_role, datetime.now().isoformat(), user_id))
                    
                    updated_count += 1
                else:
                    print(f"✅ {username}: {current_role} (ya correcto)")
            else:
                print(f"⚠️  {username}: {current_role} (rol desconocido, manteniendo)")
        
        # Verificar que no haya roles duplicados o incorrectos
        cursor.execute("SELECT DISTINCT role FROM users")
        roles = [row[0] for row in cursor.fetchall()]
        print(f"\n📊 Roles actuales en la base de datos: {roles}")
        
        # Validar roles
        valid_roles = ['admin', 'manager', 'supervisor', 'user', 'viewer']
        invalid_roles = [role for role in roles if role not in valid_roles]
        
        if invalid_roles:
            print(f"⚠️  Roles inválidos encontrados: {invalid_roles}")
        else:
            print("✅ Todos los roles son válidos")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Base de datos actualizada correctamente")
        print(f"   Usuarios actualizados: {updated_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error actualizando base de datos: {e}")
        return False

def create_missing_users():
    """Crea usuarios que puedan estar faltando"""
    db_path = Path("instance/stock_management.db")
    
    if not db_path.exists():
        print("❌ Base de datos no encontrada")
        return False
    
    # Usuarios que deberían existir
    required_users = [
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
            "role": "manager"
        },
        {
            "username": "usuario",
            "password": "Usuario123!",
            "email": "usuario@stockmanagement.com",
            "first_name": "Usuario",
            "last_name": "Sistema",
            "role": "user"
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
        
        print("\n👥 Verificando usuarios requeridos...")
        
        current_time = datetime.now().isoformat()
        created_count = 0
        
        for user_data in required_users:
            username = user_data["username"]
            
            # Verificar si el usuario existe
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            existing_user = cursor.fetchone()
            
            if not existing_user:
                print(f"➕ Creando usuario faltante: {username}")
                
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
                
                created_count += 1
            else:
                print(f"✅ Usuario ya existe: {username}")
        
        conn.commit()
        conn.close()
        
        print(f"\n✅ Verificación de usuarios completada")
        print(f"   Usuarios creados: {created_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error creando usuarios: {e}")
        return False

def verify_database_integrity():
    """Verifica la integridad de la base de datos después de los cambios"""
    db_path = Path("instance/stock_management.db")
    
    if not db_path.exists():
        print("❌ Base de datos no encontrada")
        return False
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        print("\n🔍 Verificando integridad de la base de datos...")
        
        # Verificar estructura de la tabla users
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print(f"✅ Estructura de tabla users: {len(columns)} columnas")
        
        # Contar usuarios por rol
        cursor.execute("SELECT role, COUNT(*) FROM users GROUP BY role")
        role_counts = cursor.fetchall()
        
        print("\n📊 Distribución de usuarios por rol:")
        for role, count in role_counts:
            print(f"   {role}: {count} usuarios")
        
        # Verificar usuarios activos
        cursor.execute("SELECT COUNT(*) FROM users WHERE is_active = 1")
        active_users = cursor.fetchone()[0]
        print(f"\n✅ Usuarios activos: {active_users}")
        
        # Verificar que todos los roles sean válidos
        valid_roles = ['admin', 'manager', 'supervisor', 'user', 'viewer']
        cursor.execute("SELECT DISTINCT role FROM users")
        roles = [row[0] for row in cursor.fetchall()]
        
        invalid_roles = [role for role in roles if role not in valid_roles]
        if invalid_roles:
            print(f"❌ Roles inválidos encontrados: {invalid_roles}")
            return False
        else:
            print("✅ Todos los roles son válidos")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando integridad: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 CORRECTOR DE ROLES - SISTEMA DE GESTIÓN DE STOCK")
    print("="*60)
    
    # Paso 1: Corregir roles existentes
    if not fix_roles_database():
        print("❌ Error corrigiendo roles")
        return
    
    # Paso 2: Crear usuarios faltantes
    if not create_missing_users():
        print("❌ Error creando usuarios")
        return
    
    # Paso 3: Verificar integridad
    if not verify_database_integrity():
        print("❌ Error en verificación de integridad")
        return
    
    print("\n" + "="*60)
    print("🎉 CORRECCIÓN DE ROLES COMPLETADA EXITOSAMENTE!")
    print("\n🔑 Credenciales de acceso actualizadas:")
    print("   admin / Admin123! (Rol: admin)")
    print("   gerente / Gerente123! (Rol: manager)")
    print("   usuario / Usuario123! (Rol: user)")
    print("   viewer / Viewer123! (Rol: viewer)")

if __name__ == "__main__":
    main()
