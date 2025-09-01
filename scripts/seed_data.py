#!/usr/bin/env python3
"""
Script de Seeding Directo para Stock Management
============================================

Este script carga datos de demostración directamente sin pasar por
la inicialización compleja de Flask, evitando problemas de importación.

Uso:
    python seed_data.py --demo      # Cargar datos de demostración
    python seed_data.py --custom    # Cargar productos personalizados
    python seed_data.py --all       # Cargar todos los datos
"""

import os
import sys
import argparse
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def load_demo_data():
    """Cargar datos de demostración"""
    try:
        # Importar solo lo necesario
        from app.database import db
        from app.models.category import Category
        from app.models.product import Product
        from app.models.stock import Stock
        
        # Crear aplicación Flask mínima
        from flask import Flask
        app = Flask(__name__)
        
        # Usar ruta absoluta para la base de datos
        db_path = project_root / "instance" / "stock_management.db"
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            print("🌱 Cargando datos de demostración...")
            
            # Crear categorías
            categories_data = [
                {"name": "Electrónicos", "description": "Productos electrónicos y tecnología"},
                {"name": "Ropa", "description": "Vestimenta y accesorios"},
                {"name": "Hogar", "description": "Artículos para el hogar"},
                {"name": "Deportes", "description": "Equipamiento deportivo"},
                {"name": "Libros", "description": "Libros y material educativo"}
            ]
            
            for cat_data in categories_data:
                category = Category.query.filter_by(name=cat_data["name"]).first()
                if not category:
                    category = Category(**cat_data)
                    db.session.add(category)
                    print(f"  ✅ Categoría creada: {cat_data['name']}")
                else:
                    print(f"  ℹ️  Categoría existente: {cat_data['name']}")
            
            db.session.commit()
            
            # Crear productos
            products_data = [
                {"name": "Laptop HP", "description": "Laptop HP Pavilion 15", "category_id": 1, "price": 899.99},
                {"name": "Smartphone Samsung", "description": "Samsung Galaxy S21", "category_id": 1, "price": 699.99},
                {"name": "Camiseta Básica", "description": "Camiseta de algodón 100%", "category_id": 2, "price": 19.99},
                {"name": "Jeans Clásicos", "description": "Jeans azules de alta calidad", "category_id": 2, "price": 49.99},
                {"name": "Sofá 3 Plazas", "description": "Sofá moderno y cómodo", "category_id": 3, "price": 599.99},
                {"name": "Mesa de Centro", "description": "Mesa de centro de madera", "category_id": 3, "price": 129.99},
                {"name": "Pelota de Fútbol", "description": "Pelota oficial FIFA", "category_id": 4, "price": 29.99},
                {"name": "Raqueta de Tenis", "description": "Raqueta profesional Wilson", "category_id": 4, "price": 89.99},
                {"name": "Python para Principiantes", "description": "Libro de Python básico", "category_id": 5, "price": 24.99},
                {"name": "Historia del Arte", "description": "Compendio de historia del arte", "category_id": 5, "price": 34.99}
            ]
            
            for prod_data in products_data:
                product = Product.query.filter_by(name=prod_data["name"]).first()
                if not product:
                    product = Product(**prod_data)
                    db.session.add(product)
                    print(f"  ✅ Producto creado: {prod_data['name']}")
                else:
                    print(f"  ℹ️  Producto existente: {prod_data['name']}")
            
            db.session.commit()
            
            # Crear stock inicial
            for product in Product.query.all():
                stock = Stock.query.filter_by(product_id=product.id).first()
                if not stock:
                    initial_quantity = 50 if product.category_id == 1 else 100
                    stock = Stock(
                        product_id=product.id,
                        quantity=initial_quantity,
                        min_stock=10
                    )
                    db.session.add(stock)
                    print(f"  ✅ Stock creado: {product.name} - {initial_quantity} unidades")
                else:
                    print(f"  ℹ️  Stock existente: {product.name} - {stock.quantity} unidades")
            
            db.session.commit()
            
            print("🎉 Datos de demostración cargados exitosamente!")
            
    except Exception as e:
        print(f"❌ Error al cargar datos: {e}")
        try:
            if 'app' in locals() and 'db' in locals():
                with app.app_context():
                    db.session.rollback()
        except:
            pass
        sys.exit(1)


def load_custom_data():
    """Cargar productos personalizados"""
    try:
        from app.database import db
        from app.models.product import Product
        from app.models.stock import Stock
        
        from flask import Flask
        app = Flask(__name__)
        
        # Usar ruta absoluta para la base de datos
        db_path = project_root / "instance" / "stock_management.db"
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        
        db.init_app(app)
        
        with app.app_context():
            print("🎨 Cargando productos personalizados...")
            
            # Productos personalizados adicionales
            custom_products = [
                {"name": "Auriculares Bluetooth", "description": "Auriculares inalámbricos premium", "category_id": 1, "price": 79.99},
                {"name": "Reloj Inteligente", "description": "Smartwatch con monitor cardíaco", "category_id": 1, "price": 199.99},
                {"name": "Zapatillas Running", "description": "Zapatillas para correr profesionales", "category_id": 4, "price": 119.99},
                {"name": "Mochila Escolar", "description": "Mochila resistente para estudiantes", "category_id": 3, "price": 39.99},
                {"name": "Cafetera Express", "description": "Cafetera automática profesional", "category_id": 3, "price": 299.99}
            ]
            
            for prod_data in custom_products:
                product = Product.query.filter_by(name=prod_data["name"]).first()
                if not product:
                    product = Product(**prod_data)
                    db.session.add(product)
                    db.session.flush()  # Flush para obtener el ID
                    print(f"  ✅ Producto personalizado creado: {prod_data['name']}")
                    
                    # Crear stock para el producto
                    stock = Stock(
                        product_id=product.id,
                        quantity=25,
                        min_stock=5
                    )
                    db.session.add(stock)
                else:
                    print(f"  ℹ️  Producto personalizado existente: {prod_data['name']}")
            
            db.session.commit()
            print("🎉 Productos personalizados cargados exitosamente!")
            
    except Exception as e:
        print(f"❌ Error al cargar productos personalizados: {e}")
        try:
            if 'app' in locals() and 'db' in locals():
                with app.app_context():
                    db.session.rollback()
        except:
            pass
        sys.exit(1)


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description='Script de Seeding para Stock Management')
    parser.add_argument('--demo', action='store_true', help='Cargar datos de demostración')
    parser.add_argument('--custom', action='store_true', help='Cargar productos personalizados')
    parser.add_argument('--all', action='store_true', help='Cargar todos los datos')
    
    args = parser.parse_args()
    
    if not any([args.demo, args.custom, args.all]):
        parser.print_help()
        return
    
    if args.demo or args.all:
        load_demo_data()
    
    if args.custom or args.all:
        load_custom_data()
    
    if args.all:
        print("🎉 Todos los datos han sido cargados exitosamente!")


if __name__ == '__main__':
    main()
