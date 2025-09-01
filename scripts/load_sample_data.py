#!/usr/bin/env python3
"""
Script para cargar datos de ejemplo en la base de datos de gestión de stock.
Ejecuta este script después de crear la base de datos para tener datos de prueba.
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

def load_sample_data():
    """Carga datos de ejemplo en la base de datos"""
    
    print("🚀 Cargando datos de ejemplo en la base de datos...")
    
    # Crear la aplicación Flask
    app = create_app()
    
    with app.app_context():
        try:
            # Limpiar datos existentes (opcional)
            print("🧹 Limpiando datos existentes...")
            Stock.query.delete()
            Product.query.delete()
            Category.query.delete()
            db.session.commit()
            
            # Crear categorías
            print("📂 Creando categorías...")
            categories = [
                Category(name="Electrónicos"),
                Category(name="Ropa"),
                Category(name="Hogar"),
                Category(name="Deportes"),
                Category(name="Libros"),
                Category(name="Juguetes"),
                Category(name="Alimentos"),
                Category(name="Belleza")
            ]
            
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            print(f"✅ {len(categories)} categorías creadas")
            
            # Crear productos
            print("📦 Creando productos...")
            products_data = [
                # Electrónicos
                {
                    "name": "Laptop Gaming ASUS ROG",
                    "description": "Laptop para juegos de alto rendimiento con RTX 4060",
                    "price": 1299.99,
                    "category_name": "Electrónicos",
                    "min_stock": 5
                },
                {
                    "name": "Smartphone Samsung Galaxy S24",
                    "description": "Teléfono inteligente con cámara de 200MP",
                    "price": 899.99,
                    "category_name": "Electrónicos",
                    "min_stock": 10
                },
                {
                    "name": "Auriculares Sony WH-1000XM5",
                    "description": "Auriculares inalámbricos con cancelación de ruido",
                    "price": 349.99,
                    "category_name": "Electrónicos",
                    "min_stock": 8
                },
                
                # Ropa
                {
                    "name": "Camiseta Nike Dri-FIT",
                    "description": "Camiseta deportiva de secado rápido",
                    "price": 29.99,
                    "category_name": "Ropa",
                    "min_stock": 50
                },
                {
                    "name": "Jeans Levi's 501",
                    "description": "Jeans clásicos de alta calidad",
                    "price": 79.99,
                    "category_name": "Ropa",
                    "min_stock": 25
                },
                {
                    "name": "Zapatillas Adidas Ultraboost",
                    "description": "Zapatillas de running con tecnología Boost",
                    "price": 189.99,
                    "category_name": "Ropa",
                    "min_stock": 15
                },
                
                # Hogar
                {
                    "name": "Cafetera Nespresso Vertuo",
                    "description": "Cafetera automática con cápsulas",
                    "price": 199.99,
                    "category_name": "Hogar",
                    "min_stock": 12
                },
                {
                    "name": "Aspiradora Dyson V15",
                    "description": "Aspiradora inalámbrica con láser",
                    "price": 699.99,
                    "category_name": "Hogar",
                    "min_stock": 6
                },
                {
                    "name": "Sartén Antiadherente Tefal",
                    "description": "Sartén de 28cm con revestimiento antiadherente",
                    "price": 39.99,
                    "category_name": "Hogar",
                    "min_stock": 30
                },
                
                # Deportes
                {
                    "name": "Pelota de Fútbol Nike",
                    "description": "Pelota oficial de competición",
                    "price": 89.99,
                    "category_name": "Deportes",
                    "min_stock": 20
                },
                {
                    "name": "Raqueta de Tenis Wilson",
                    "description": "Raqueta profesional con encordado",
                    "price": 159.99,
                    "category_name": "Deportes",
                    "min_stock": 12
                },
                {
                    "name": "Bicicleta de Spinning",
                    "description": "Bicicleta estática para entrenamiento indoor",
                    "price": 299.99,
                    "category_name": "Deportes",
                    "min_stock": 8
                },
                
                # Libros
                {
                    "name": "El Señor de los Anillos",
                    "description": "Trilogía completa de J.R.R. Tolkien",
                    "price": 49.99,
                    "category_name": "Libros",
                    "min_stock": 25
                },
                {
                    "name": "Cien Años de Soledad",
                    "description": "Obra maestra de Gabriel García Márquez",
                    "price": 19.99,
                    "category_name": "Libros",
                    "min_stock": 40
                },
                {
                    "name": "Harry Potter y la Piedra Filosofal",
                    "description": "Primera entrega de la saga de J.K. Rowling",
                    "price": 24.99,
                    "category_name": "Libros",
                    "min_stock": 35
                },
                
                # Juguetes
                {
                    "name": "LEGO Star Wars Millennium Falcon",
                    "description": "Set de construcción con 1329 piezas",
                    "price": 159.99,
                    "category_name": "Juguetes",
                    "min_stock": 10
                },
                {
                    "name": "Nintendo Switch OLED",
                    "description": "Consola de videojuegos portátil",
                    "price": 349.99,
                    "category_name": "Juguetes",
                    "min_stock": 15
                },
                {
                    "name": "Peluche Gigante de Oso",
                    "description": "Oso de peluche de 1.5 metros",
                    "price": 79.99,
                    "category_name": "Juguetes",
                    "min_stock": 8
                },
                
                # Alimentos
                {
                    "name": "Café Colombiano Premium",
                    "description": "Café 100% arábica de altura",
                    "price": 24.99,
                    "category_name": "Alimentos",
                    "min_stock": 100
                },
                {
                    "name": "Chocolate Lindt Excellence",
                    "description": "Chocolate negro 70% cacao",
                    "price": 4.99,
                    "category_name": "Alimentos",
                    "min_stock": 200
                },
                {
                    "name": "Aceite de Oliva Extra Virgen",
                    "description": "Aceite de oliva español de primera prensada",
                    "price": 19.99,
                    "category_name": "Alimentos",
                    "min_stock": 80
                },
                
                # Belleza
                {
                    "name": "Crema Hidratante La Mer",
                    "description": "Crema facial de lujo con algas marinas",
                    "price": 349.99,
                    "category_name": "Belleza",
                    "min_stock": 20
                },
                {
                    "name": "Perfume Chanel N°5",
                    "description": "Perfume icónico de la casa Chanel",
                    "price": 129.99,
                    "category_name": "Belleza",
                    "min_stock": 15
                },
                {
                    "name": "Set de Brochas MAC",
                    "description": "Set completo de brochas profesionales",
                    "price": 89.99,
                    "category_name": "Belleza",
                    "min_stock": 25
                }
            ]
            
            products_created = 0
            for product_data in products_data:
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
                        quantity=product_data["min_stock"] + 10,  # Stock inicial por encima del mínimo
                        min_stock=product_data["min_stock"]
                    )
                    db.session.add(stock)
                    products_created += 1
            
            db.session.commit()
            print(f"✅ {products_created} productos creados con stock inicial")
            
            print("\n🎉 ¡Datos de ejemplo cargados exitosamente!")
            print(f"📊 Resumen:")
            print(f"   - Categorías: {len(categories)}")
            print(f"   - Productos: {products_created}")
            print(f"   - Registros de stock: {products_created}")
            
        except Exception as e:
            print(f"❌ Error cargando datos: {e}")
            db.session.rollback()
            raise

if __name__ == "__main__":
    load_sample_data() 