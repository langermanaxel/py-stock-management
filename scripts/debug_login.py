#!/usr/bin/env python3
"""
Script para debuggear el login paso a paso
"""

import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash

def debug_login():
    """Debuggea el login paso a paso"""
    
    print("🔍 DEBUGGEANDO LOGIN PASO A PASO")
    print("="*50)
    
    username = 'admin'
    password = 'admin123'
    
    print(f"🔐 Intentando login con:")
    print(f"   Usuario: {username}")
    print(f"   Contraseña: {password}")
    
    # Paso 1: Verificar que la base de datos existe
    db_path = Path('instance/stock_management.db')
    if not db_path.exists():
        print("❌ Paso 1: Base de datos no encontrada")
        return False
    
    print("✅ Paso 1: Base de datos encontrada")
    
    # Paso 2: Conectar a la base de datos
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        print("✅ Paso 2: Conexión a base de datos exitosa")
    except Exception as e:
        print(f"❌ Paso 2: Error conectando a BD: {e}")
        return False
    
    # Paso 3: Buscar usuario
    try:
        cursor.execute("""
            SELECT id, username, email, password_hash, first_name, last_name, 
                   role, is_active, created_at, updated_at, last_login
            FROM users 
            WHERE username = ? AND is_active = 1
        """, (username,))
        
        user_data = cursor.fetchone()
        
        if user_data:
            print("✅ Paso 3: Usuario encontrado en BD")
            print(f"   ID: {user_data[0]}")
            print(f"   Usuario: {user_data[1]}")
            print(f"   Email: {user_data[2]}")
            print(f"   Rol: {user_data[6]}")
            print(f"   Activo: {user_data[7]}")
        else:
            print("❌ Paso 3: Usuario no encontrado o inactivo")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Paso 3: Error buscando usuario: {e}")
        conn.close()
        return False
    
    # Paso 4: Verificar contraseña
    try:
        password_hash = user_data[3]
        print(f"🔐 Paso 4: Hash de contraseña: {password_hash[:30]}...")
        
        is_valid = check_password_hash(password_hash, password)
        
        if is_valid:
            print("✅ Paso 4: Contraseña válida")
        else:
            print("❌ Paso 4: Contraseña inválida")
            print(f"   Hash en BD: {password_hash}")
            print(f"   Contraseña probada: {password}")
            conn.close()
            return False
            
    except Exception as e:
        print(f"❌ Paso 4: Error verificando contraseña: {e}")
        conn.close()
        return False
    
    # Paso 5: Verificar que el usuario está activo
    if user_data[7]:
        print("✅ Paso 5: Usuario está activo")
    else:
        print("❌ Paso 5: Usuario inactivo")
        conn.close()
        return False
    
    # Paso 6: Simular actualización de last_login
    try:
        from datetime import datetime
        current_time = datetime.utcnow().isoformat()
        
        cursor.execute("""
            UPDATE users 
            SET last_login = ?, updated_at = ?
            WHERE id = ?
        """, (current_time, current_time, user_data[0]))
        
        conn.commit()
        print("✅ Paso 6: last_login actualizado correctamente")
        
    except Exception as e:
        print(f"❌ Paso 6: Error actualizando last_login: {e}")
        conn.rollback()
    
    conn.close()
    
    print("\n🎉 ¡LOGIN DEBUGGEADO EXITOSAMENTE!")
    print("Todos los pasos funcionan correctamente")
    return True

if __name__ == "__main__":
    debug_login()
