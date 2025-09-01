#!/usr/bin/env python3
"""
Sistema de Gestión Unificado Simplificado para Stock Management
============================================================

Versión simplificada del CLI que se enfoca en las operaciones básicas
de seeding de datos sin dependencias complejas de Flask.

Uso:
    python manage_simple.py --help                    # Ver ayuda general
    python manage_simple.py seed --demo               # Cargar datos de demostración
    python manage_simple.py seed --custom             # Cargar productos personalizados
    python manage_simple.py seed --all                # Cargar todos los datos
"""

import os
import sys
import click
from pathlib import Path

# Agregar el directorio raíz al path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Importar solo lo básico
try:
    from app.database import db
    from app.models.category import Category
    from app.models.product import Product
    from app.models.stock import Stock
    from app.models.user import User
    from app import create_app
    FLASK_AVAILABLE = True
except ImportError as e:
    click.echo(f"⚠️  Advertencia: No se pudo importar Flask app: {e}")
    FLASK_AVAILABLE = False


@click.group()
@click.version_option(version="1.0.0", prog_name="Stock Management CLI Simple")
def cli():
    """Sistema de Gestión Unificado Simplificado para Stock Management"""
    pass


@cli.group()
def seed():
    """Operaciones de seeding de datos"""
    pass


@seed.command()
def demo():
    """Cargar datos de demostración completos"""
    if not FLASK_AVAILABLE:
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    
    try:
        app = create_app()
        with app.app_context():
            click.echo("🌱 Cargando datos de demostración...")
            
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
                    click.echo(f"  ✅ Categoría creada: {cat_data['name']}")
                else:
                    click.echo(f"  ℹ️  Categoría existente: {cat_data['name']}")
            
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
                    click.echo(f"  ✅ Producto creado: {prod_data['name']}")
                else:
                    click.echo(f"  ℹ️  Producto existente: {prod_data['name']}")
            
            db.session.commit()
            
            # Crear stock inicial
            for product in Product.query.all():
                stock = Stock.query.filter_by(product_id=product.id).first()
                if not stock:
                    initial_quantity = 50 if product.category_id == 1 else 100
                    stock = Stock(
                        product_id=product.id,
                        quantity=initial_quantity,
                        min_stock=10,
                        location="Almacén Principal"
                    )
                    db.session.add(stock)
                    click.echo(f"  ✅ Stock creado: {product.name} - {initial_quantity} unidades")
                else:
                    click.echo(f"  ℹ️  Stock existente: {product.name} - {stock.quantity} unidades")
            
            db.session.commit()
            
            click.echo("🎉 Datos de demostración cargados exitosamente!")
            
    except Exception as e:
        click.echo(f"❌ Error al cargar datos: {e}")
        if 'db' in locals():
            db.session.rollback()
        sys.exit(1)


@seed.command()
def custom():
    """Cargar productos personalizados adicionales"""
    if not FLASK_AVAILABLE:
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    
    try:
        app = create_app()
        with app.app_context():
            click.echo("🎨 Cargando productos personalizados...")
            
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
                    click.echo(f"  ✅ Producto personalizado creado: {prod_data['name']}")
                    
                    # Crear stock para el producto
                    stock = Stock(
                        product_id=product.id,
                        quantity=25,
                        min_stock=5,
                        location="Almacén Secundario"
                    )
                    db.session.add(stock)
                else:
                    click.echo(f"  ℹ️  Producto personalizado existente: {prod_data['name']}")
            
            db.session.commit()
            click.echo("🎉 Productos personalizados cargados exitosamente!")
            
    except Exception as e:
        click.echo(f"❌ Error al cargar productos personalizados: {e}")
        if 'db' in locals():
            db.session.rollback()
        sys.exit(1)


@seed.command()
def all():
    """Cargar todos los datos (demo + personalizados)"""
    click.echo("🚀 Cargando todos los datos...")
    
    # Ejecutar demo primero
    demo()
    
    # Luego ejecutar custom
    custom()
    
    click.echo("🎉 Todos los datos han sido cargados exitosamente!")


@cli.command()
def status():
    """Mostrar estado actual de la aplicación"""
    if not FLASK_AVAILABLE:
        click.echo("❌ Error: Flask app no disponible")
        sys.exit(1)
    
    try:
        app = create_app()
        with app.app_context():
            click.echo("📊 Estado de la aplicación:")
            click.echo("=" * 40)
            
            # Contar registros
            categories_count = Category.query.count()
            products_count = Product.query.count()
            stock_count = Stock.query.count()
            users_count = User.query.count()
            
            click.echo(f"📁 Categorías: {categories_count}")
            click.echo(f"📦 Productos: {products_count}")
            click.echo(f"📊 Stock: {stock_count}")
            click.echo(f"👥 Usuarios: {users_count}")
            
            # Verificar base de datos
            db.engine.execute("SELECT 1")
            click.echo("🗄️  Base de datos: ✅ Conectada")
            
    except Exception as e:
        click.echo(f"❌ Error al obtener estado: {e}")


if __name__ == '__main__':
    cli()
