#!/usr/bin/env python3
"""
Script de prueba para verificar la base de datos
==============================================

Este script verifica la conectividad y estructura de la base de datos.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def test_database():
    """Probar conectividad de la base de datos"""
    try:
        print("🔍 Probando conectividad de base de datos...")
        
        # Importar solo la base de datos
        from app.database import db
        print("✅ app.database importado correctamente")
        
        # Crear aplicación Flask mínima
        from flask import Flask
        app = Flask(__name__)
        
        # Usar ruta absoluta para la base de datos
        db_path = project_root / "instance" / "stock_management.db"
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        print(f"✅ Ruta de base de datos: {db_path}")
        print("✅ Aplicación Flask creada")
        
        db.init_app(app)
        print("✅ Base de datos inicializada")
        
        with app.app_context():
            print("✅ Contexto de aplicación activo")
            
            # Probar conexión simple (compatible con SQLAlchemy 2.0+)
            with db.engine.connect() as conn:
                result = conn.execute(db.text("SELECT 1"))
                print("✅ Conexión a base de datos exitosa")
            
            # Verificar tablas existentes
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            tables = inspector.get_table_names()
            print(f"✅ Tablas encontradas: {tables}")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == '__main__':
    test_database()
