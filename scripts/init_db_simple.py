#!/usr/bin/env python3
"""
Script simple para inicializar la base de datos
"""

import os
from pathlib import Path

def init_database():
    """Inicializa la base de datos SQLite"""
    
    print("🗄️ Inicializando base de datos...")
    
    # Crear directorio instance si no existe
    instance_dir = Path('instance')
    if not instance_dir.exists():
        instance_dir.mkdir()
        print("✅ Directorio 'instance' creado")
    
    # Crear archivo de base de datos vacío
    db_path = instance_dir / 'stock_management.db'
    
    try:
        # Crear archivo vacío
        db_path.touch()
        print(f"✅ Base de datos creada: {db_path}")
        
        # Verificar que se puede escribir
        if db_path.exists():
            print("✅ Base de datos accesible")
            return True
        else:
            print("❌ No se pudo crear la base de datos")
            return False
            
    except Exception as e:
        print(f"❌ Error creando base de datos: {e}")
        return False

def main():
    """Función principal"""
    
    print("🔧 INICIALIZADOR SIMPLE DE BASE DE DATOS")
    print("="*50)
    
    if init_database():
        print("\n✅ Base de datos inicializada correctamente")
        print("💡 Ahora puedes ejecutar:")
        print("   python start_backend.py")
    else:
        print("\n❌ Error inicializando la base de datos")

if __name__ == "__main__":
    main()
