#!/usr/bin/env python3
"""
Script para inicializar datos de ejemplo en la base de datos
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.database import db
from app.models.category import Category
from app.models.product import Product
from app.models.stock import Stock

def init_sample_data():
    app = create_app()
    
    with app.app_context():
        # Crear categorías de ejemplo
        categories_data = [
            "Electrónicos",
            "Ropa",
            "Hogar",
            "Deportes",
            "Libros"
        ]
        
        categories = []
        for cat_name in categories_data:
            category = Category.query.filter_by(name=cat_name).first()
            if not category:
                category = Category(name=cat_name)
                db.session.add(category)
                categories.append(category)
                print(f"Categoría creada: {cat_name}")
            else:
                categories.append(category)
                print(f"Categoría existente: {cat_name}")
        
        db.session.commit()
        
        # Crear productos de ejemplo
        products_data = [
            {
                "name": "Laptop HP",
                "description": "Laptop HP Pavilion 15 pulgadas, Intel i5, 8GB RAM",
                "price": 899.99,
                "category": "Electrónicos",
                "min_stock": 5
            },
            {
                "name": "Camiseta Nike",
                "description": "Camiseta deportiva Nike Dri-FIT, talla M",
                "price": 29.99,
                "category": "Ropa",
                "min_stock": 20
            },
            {
                "name": "Sofá 3 Plazas",
                "description": "Sofá moderno 3 plazas, color gris",
                "price": 599.99,
                "category": "Hogar",
                "min_stock": 3
            },
            {
                "name": "Balón de Fútbol",
                "description": "Balón oficial FIFA, talla 5",
                "price": 49.99,
                "category": "Deportes",
                "min_stock": 15
            },
            {
                "name": "Python para Principiantes",
                "description": "Libro de programación Python, nivel básico",
                "price": 24.99,
                "category": "Libros",
                "min_stock": 10
            },
            {
                "name": "Smartphone Samsung",
                "description": "Samsung Galaxy A54, 128GB, 6GB RAM",
                "price": 449.99,
                "category": "Electrónicos",
                "min_stock": 8
            },
            {
                "name": "Pantalón Jeans",
                "description": "Jeans Levi's 501, talla 32x32",
                "price": 79.99,
                "category": "Ropa",
                "min_stock": 25
            },
            {
                "name": "Mesa de Comedor",
                "description": "Mesa de comedor extensible, 6-8 personas",
                "price": 299.99,
                "category": "Hogar",
                "min_stock": 2
            }
        ]
        
        for product_info in products_data:
            # Buscar si el producto ya existe
            existing_product = Product.query.filter_by(name=product_info["name"]).first()
            if existing_product:
                print(f"Producto existente: {product_info['name']}")
                continue
            
            # Encontrar la categoría
            category = Category.query.filter_by(name=product_info["category"]).first()
            if not category:
                print(f"Error: Categoría '{product_info['category']}' no encontrada")
                continue
            
            # Crear el producto
            product = Product(
                name=product_info["name"],
                description=product_info["description"],
                price=product_info["price"],
                category_id=category.id
            )
            db.session.add(product)
            db.session.flush()  # Para obtener el ID del producto
            
            # Crear el stock inicial
            stock = Stock(
                product_id=product.id,
                quantity=product_info["min_stock"] + 10,  # Stock inicial por encima del mínimo
                min_stock=product_info["min_stock"]
            )
            db.session.add(stock)
            
            print(f"Producto creado: {product_info['name']} - ${product_info['price']}")
        
        db.session.commit()
        print("\n¡Datos de ejemplo inicializados exitosamente!")
        print(f"Total categorías: {len(categories)}")
        print(f"Total productos: {len(products_data)}")

if __name__ == "__main__":
    init_sample_data()
