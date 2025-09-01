#!/usr/bin/env python3
"""
Script para reparar completamente la base de datos del Sistema de Gestión de Inventario
"""

import os
import sys
from pathlib import Path

def create_database_structure():
    """Crea la estructura completa de la base de datos"""
    
    print("🗄️ Creando estructura de base de datos...")
    
    try:
        # Importar Flask y crear la aplicación
        from app import create_app
        from app.database import db
        
        # Crear la aplicación Flask
        app = create_app()
        
        with app.app_context():
            # Crear todas las tablas
            print("📋 Creando tablas...")
            db.create_all()
            print("✅ Tablas creadas correctamente")
            
            # Verificar que las tablas existen
            from app.models.user import User
            from app.models.category import Category
            from app.models.product import Product
            from app.models.stock import Stock
            from app.models.order import Order
            from app.models.order_item import OrderItem
            from app.models.purchase_order import PurchaseOrder
            
            print("✅ Modelos importados correctamente")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando estructura de base de datos: {e}")
        return False

def create_admin_user():
    """Crea un usuario administrador por defecto"""
    
    print("\n👤 Creando usuario administrador...")
    
    try:
        from app import create_app
        from app.database import db
        from app.models.user import User
        from werkzeug.security import generate_password_hash
        
        app = create_app()
        
        with app.app_context():
            # Verificar si ya existe un usuario admin
            admin_user = User.query.filter_by(username='admin').first()
            
            if admin_user:
                print("✅ Usuario administrador ya existe")
                return True
            
            # Crear usuario administrador
            admin_user = User(
                username='admin',
                email='admin@stockmanagement.com',
                password_hash=generate_password_hash('admin123'),
                first_name='Administrador',
                last_name='Sistema',
                role='admin',
                is_active=True
            )
            
            db.session.add(admin_user)
            db.session.commit()
            
            print("✅ Usuario administrador creado:")
            print("   Usuario: admin")
            print("   Contraseña: admin123")
            print("   Email: admin@stockmanagement.com")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando usuario administrador: {e}")
        return False

def create_sample_data():
    """Crea datos de muestra para testing"""
    
    print("\n📊 Creando datos de muestra...")
    
    try:
        from app import create_app
        from app.database import db
        from app.models.category import Category
        from app.models.product import Product
        from app.models.stock import Stock
        
        app = create_app()
        
        with app.app_context():
            # Crear categorías de ejemplo
            categories = [
                Category(name='Electrónicos', description='Productos electrónicos'),
                Category(name='Ropa', description='Vestimenta y accesorios'),
                Category(name='Hogar', description='Artículos para el hogar')
            ]
            
            for category in categories:
                db.session.add(category)
            
            db.session.commit()
            print("✅ Categorías creadas")
            
            # Crear productos de ejemplo
            products = [
                Product(
                    name='Laptop HP',
                    description='Laptop HP 15.6" Intel Core i5',
                    price=599.99,
                    category_id=1,
                    sku='LAP001'
                ),
                Product(
                    name='Camiseta Básica',
                    description='Camiseta de algodón 100%',
                    price=19.99,
                    category_id=2,
                    sku='CAM001'
                ),
                Product(
                    name='Lámpara de Mesa',
                    description='Lámpara LED ajustable',
                    price=29.99,
                    category_id=3,
                    sku='LAM001'
                )
            ]
            
            for product in products:
                db.session.add(product)
            
            db.session.commit()
            print("✅ Productos creados")
            
            # Crear stock inicial
            stocks = [
                Stock(product_id=1, quantity=10, min_quantity=2),
                Stock(product_id=2, quantity=50, min_quantity=10),
                Stock(product_id=3, quantity=15, min_quantity=3)
            ]
            
            for stock in stocks:
                db.session.add(stock)
            
            db.session.commit()
            print("✅ Stock inicial creado")
            
            return True
            
    except Exception as e:
        print(f"❌ Error creando datos de muestra: {e}")
        return False

def verify_database():
    """Verifica que la base de datos esté funcionando correctamente"""
    
    print("\n🔍 Verificando base de datos...")
    
    try:
        from app import create_app
        from app.database import db
        from app.models.user import User
        from app.models.category import Category
        from app.models.product import Product
        
        app = create_app()
        
        with app.app_context():
            # Verificar conexión
            result = db.session.execute('SELECT 1').scalar()
            if result == 1:
                print("✅ Conexión a base de datos exitosa")
            
            # Verificar tablas
            user_count = User.query.count()
            category_count = Category.query.count()
            product_count = Product.query.count()
            
            print(f"✅ Usuarios en BD: {user_count}")
            print(f"✅ Categorías en BD: {category_count}")
            print(f"✅ Productos en BD: {product_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def main():
    """Función principal"""
    
    print("🔧 REPARADOR DE BASE DE DATOS - STOCK MANAGEMENT")
    print("="*60)
    
    # Crear estructura de base de datos
    if not create_database_structure():
        print("❌ No se pudo crear la estructura de la base de datos")
        return
    
    # Crear usuario administrador
    if not create_admin_user():
        print("❌ No se pudo crear el usuario administrador")
        return
    
    # Crear datos de muestra
    if not create_sample_data():
        print("⚠️ No se pudieron crear datos de muestra, pero la BD funciona")
    
    # Verificar que todo funcione
    if not verify_database():
        print("❌ La base de datos no está funcionando correctamente")
        return
    
    print("\n" + "="*60)
    print("🎉 ¡BASE DE DATOS REPARADA EXITOSAMENTE!")
    print("="*60)
    print("\n💡 Ahora puedes:")
    print("   1. Iniciar el backend: python run.py")
    print("   2. Hacer login con:")
    print("      Usuario: admin")
    print("      Contraseña: admin123")
    print("   3. Probar el frontend en http://localhost:8080")

if __name__ == "__main__":
    main()
