#!/usr/bin/env python3
"""
Script para agregar productos personalizados a la base de datos.
Puedes modificar este script para agregar los productos que necesites.
"""

import sys
import os

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database import db
from app.models.category import Category
from app.models.product import Product
from app.models.stock import Stock

def add_custom_products():
    """Agrega productos personalizados a la base de datos"""
    
    print("🚀 Agregando productos personalizados...")
    
    # Crear la aplicación Flask
    app = create_app()
    
    with app.app_context():
        try:
            # Productos personalizados que quieres agregar
            custom_products = [
                {
                    "name": "Monitor Gaming 27\" 4K",
                    "description": "Monitor de 27 pulgadas con resolución 4K y 144Hz para gaming",
                    "price": 599.99,
                    "category_name": "Electrónicos",
                    "min_stock": 8,
                    "initial_stock": 15
                },
                {
                    "name": "Teclado Mecánico RGB",
                    "description": "Teclado mecánico con switches Cherry MX y iluminación RGB",
                    "price": 129.99,
                    "category_name": "Electrónicos",
                    "min_stock": 12,
                    "initial_stock": 20
                },
                {
                    "name": "Mouse Gaming Logitech G Pro",
                    "description": "Mouse gaming inalámbrico con sensor HERO 25K",
                    "price": 149.99,
                    "category_name": "Electrónicos",
                    "min_stock": 10,
                    "initial_stock": 18
                },
                {
                    "name": "Mesa de Escritorio Gaming",
                    "description": "Mesa de escritorio ergonómica para gaming y trabajo",
                    "price": 299.99,
                    "category_name": "Hogar",
                    "min_stock": 5,
                    "initial_stock": 8
                },
                {
                    "name": "Silla Gaming Ergonómica",
                    "description": "Silla gaming con soporte lumbar y reposabrazos ajustables",
                    "price": 399.99,
                    "category_name": "Hogar",
                    "min_stock": 6,
                    "initial_stock": 10
                },
                {
                    "name": "Kit de Pesas Ajustables",
                    "description": "Set de pesas ajustables de 2.5kg a 25kg",
                    "price": 199.99,
                    "category_name": "Deportes",
                    "min_stock": 8,
                    "initial_stock": 12
                },
                {
                    "name": "Yoga Mat Premium",
                    "description": "Alfombrilla de yoga de alta densidad con diseño antideslizante",
                    "price": 49.99,
                    "category_name": "Deportes",
                    "min_stock": 20,
                    "initial_stock": 35
                },
                {
                    "name": "Libro de Cocina Gourmet",
                    "description": "Recetario completo con técnicas avanzadas de cocina",
                    "price": 34.99,
                    "category_name": "Libros",
                    "min_stock": 15,
                    "initial_stock": 25
                },
                {
                    "name": "Set de Pintura Acrílica",
                    "description": "Set completo de pinturas acrílicas profesionales",
                    "price": 89.99,
                    "category_name": "Juguetes",
                    "min_stock": 10,
                    "initial_stock": 18
                },
                {
                    "name": "Puzzle 1000 Piezas",
                    "description": "Puzzle de paisaje natural de alta calidad",
                    "price": 24.99,
                    "category_name": "Juguetes",
                    "min_stock": 25,
                    "initial_stock": 40
                }
            ]
            
            products_created = 0
            
            for product_data in custom_products:
                # Verificar si el producto ya existe
                existing_product = Product.query.filter_by(name=product_data["name"]).first()
                if existing_product:
                    print(f"⚠️  El producto '{product_data['name']}' ya existe, saltando...")
                    continue
                
                # Buscar la categoría por nombre
                category = Category.query.filter_by(name=product_data["category_name"]).first()
                if category:
                    product = Product(
                        name=product_data["name"],
                        description=product_data["description"],
                        price=product_data["price"],
                        category_id=category.id
                    )
                    db.session.add(product)
                    db.session.flush()  # Para obtener el ID del producto
                    
                    # Crear registro de stock
                    stock = Stock(
                        product_id=product.id,
                        quantity=product_data["initial_stock"],
                        min_stock=product_data["min_stock"]
                    )
                    db.session.add(stock)
                    products_created += 1
                    print(f"✅ Producto creado: {product_data['name']}")
                else:
                    print(f"❌ Categoría '{product_data['category_name']}' no encontrada para: {product_data['name']}")
            
            db.session.commit()
            print(f"\n🎉 ¡{products_created} productos personalizados agregados exitosamente!")
            
            # Mostrar resumen actualizado
            total_products = Product.query.count()
            total_stock = Stock.query.count()
            print(f"📊 Total en la base de datos:")
            print(f"   - Productos: {total_products}")
            print(f"   - Registros de stock: {total_stock}")
            
        except Exception as e:
            print(f"❌ Error agregando productos: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    add_custom_products() 