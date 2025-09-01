#!/usr/bin/env python3
"""
Script para verificar qué usuarios existen en la base de datos
"""

import sqlite3
from pathlib import Path

def check_users():
    """Verifica qué usuarios existen en la base de datos"""
    db_path = Path("instance/stock_management.db")
    
    if not db_path.exists():
        print("❌ Base de datos no encontrada")
        return
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar estructura de la tabla
        cursor.execute("PRAGMA table_info(users)")
        columns = cursor.fetchall()
        print("📋 Estructura de la tabla users:")
        for col in columns:
            print(f"   {col[1]} ({col[2]})")
        
        print("\n" + "="*50)
        
        # Verificar usuarios existentes
        cursor.execute("""
            SELECT id, username, email, first_name, last_name, role, is_active, created_at
            FROM users 
            ORDER BY id
        """)
        
        users = cursor.fetchall()
        
        if not users:
            print("❌ No hay usuarios en la base de datos")
        else:
            print(f"👥 Usuarios encontrados ({len(users)}):")
            for user in users:
                status = "✅ Activo" if user[6] else "❌ Inactivo"
                print(f"   ID: {user[0]}")
                print(f"   Usuario: {user[1]}")
                print(f"   Email: {user[2]}")
                print(f"   Nombre: {user[3]} {user[4]}")
                print(f"   Rol: {user[5]}")
                print(f"   Estado: {status}")
                print(f"   Creado: {user[7]}")
                print("   " + "-"*30)
        
        conn.close()
        
    except Exception as e:
        print(f"❌ Error al verificar usuarios: {e}")

if __name__ == "__main__":
    check_users()
