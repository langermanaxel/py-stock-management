#!/usr/bin/env python3
"""
Script para inicializar la base de datos
======================================

Este script crea la base de datos SQLite y todas las tablas necesarias
antes de ejecutar el seeding de datos.
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def init_database():
    """Inicializar base de datos y crear tablas"""
    try:
        from app.database import db
        from app.models.category import Category
        from app.models.product import Product
        from app.models.stock import Stock
        from app.models.order import Order
        from app.models.order_item import OrderItem
        from app.models.purchase_order import PurchaseOrder
        from app.models.user import User
        
        # Crear aplicación Flask mínima
        from flask import Flask
        app = Flask(__name__)
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///instance/stock_management.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            print("🗄️  Inicializando base de datos...")
            
            # Crear todas las tablas
            db.create_all()
            
            print("✅ Base de datos inicializada exitosamente!")
            print("✅ Todas las tablas han sido creadas")
            
    except Exception as e:
        print(f"❌ Error al inicializar base de datos: {e}")
        sys.exit(1)


if __name__ == '__main__':
    init_database()
