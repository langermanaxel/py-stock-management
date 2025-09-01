#!/usr/bin/env python3
"""
Script simple para verificar la base de datos
"""

import sqlite3
from pathlib import Path

def check_database():
    """Verifica la base de datos"""
    
    print("🔍 VERIFICANDO BASE DE DATOS")
    print("="*40)
    
    db_path = Path('instance/stock_management.db')
    
    if not db_path.exists():
        print("❌ Base de datos no encontrada")
        return False
    
    print(f"✅ Base de datos encontrada: {db_path}")
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar tablas
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print(f"📋 Tablas encontradas: {len(tables)}")
        for table in tables:
            print(f"   - {table[0]}")
        
        # Verificar usuario admin
        cursor.execute("SELECT username, role, is_active FROM users WHERE username = 'admin'")
        admin_user = cursor.fetchone()
        
        if admin_user:
            print(f"✅ Usuario admin encontrado:")
            print(f"   Usuario: {admin_user[0]}")
            print(f"   Rol: {admin_user[1]}")
            print(f"   Activo: {admin_user[2]}")
        else:
            print("❌ Usuario admin no encontrado")
        
        # Verificar contraseña
        cursor.execute("SELECT password_hash FROM users WHERE username = 'admin'")
        password_result = cursor.fetchone()
        
        if password_result:
            print(f"🔐 Hash de contraseña encontrado: {password_result[0][:20]}...")
        else:
            print("❌ Hash de contraseña no encontrado")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

if __name__ == "__main__":
    check_database()
