#!/usr/bin/env python3
"""
Script híbrido para crear una base de datos funcional
"""

import os
import sqlite3
from pathlib import Path

def create_database_structure():
    """Crea la estructura de la base de datos con SQLite puro"""
    
    print("🗄️ Creando estructura de base de datos con SQLite puro...")
    
    try:
        # Crear directorio instance si no existe
        instance_dir = Path('instance')
        if not instance_dir.exists():
            instance_dir.mkdir()
            print("✅ Directorio 'instance' creado")
        
        # Ruta de la base de datos
        db_path = instance_dir / 'stock_management.db'
        print(f"🗄️ Ruta de BD: {db_path.absolute()}")
        
        # Crear base de datos SQLite
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear tabla de usuarios con todas las columnas necesarias
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                email TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                first_name TEXT,
                last_name TEXT,
                role TEXT DEFAULT 'user',
                is_active BOOLEAN DEFAULT 1,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                last_login TIMESTAMP
            )
        ''')
        
        # Crear tabla de categorías
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS categories (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT UNIQUE NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        # Crear tabla de productos
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                description TEXT,
                price REAL NOT NULL,
                category_id INTEGER,
                sku TEXT UNIQUE,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (category_id) REFERENCES categories (id)
            )
        ''')
        
        # Crear tabla de stock
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS stock (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL DEFAULT 0,
                min_quantity INTEGER DEFAULT 0,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Crear tabla de órdenes
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        ''')
        
        # Crear tabla de items de orden
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS order_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                unit_price REAL NOT NULL,
                total_price REAL NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (order_id) REFERENCES orders (id),
                FOREIGN KEY (product_id) REFERENCES products (id)
            )
        ''')
        
        # Crear tabla de órdenes de compra
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS purchase_orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                supplier_name TEXT NOT NULL,
                total_amount REAL NOT NULL,
                status TEXT DEFAULT 'pending',
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
        
        conn.commit()
        conn.close()
        
        print("✅ Estructura de base de datos creada correctamente")
        return True
        
    except Exception as e:
        print(f"❌ Error creando estructura de base de datos: {e}")
        return False

def create_admin_user():
    """Crea un usuario administrador por defecto"""
    
    print("\n👤 Creando usuario administrador...")
    
    try:
        from werkzeug.security import generate_password_hash
        
        # Conectar a la base de datos
        db_path = Path('instance') / 'stock_management.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar si ya existe un usuario admin
        cursor.execute('SELECT username FROM users WHERE username = ?', ('admin',))
        if cursor.fetchone():
            print("✅ Usuario administrador ya existe")
            conn.close()
            return True
        
        # Crear usuario administrador
        admin_password = generate_password_hash('admin123')
        cursor.execute('''
            INSERT INTO users 
            (username, email, password_hash, first_name, last_name, role, is_active)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', ('admin', 'admin@stockmanagement.com', admin_password, 'Admin', 'Sistema', 'admin', 1))
        
        conn.commit()
        conn.close()
        
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
        # Conectar a la base de datos
        db_path = Path('instance') / 'stock_management.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Crear categorías de ejemplo
        categories = [
            ('Electrónicos', 'Productos electrónicos'),
            ('Ropa', 'Vestimenta y accesorios'),
            ('Hogar', 'Artículos para el hogar')
        ]
        
        for name, description in categories:
            cursor.execute('INSERT OR IGNORE INTO categories (name, description) VALUES (?, ?)', (name, description))
        
        conn.commit()
        print("✅ Categorías creadas")
        
        # Crear productos de ejemplo
        products = [
            ('Laptop HP', 'Laptop HP 15.6" Intel Core i5', 599.99, 1, 'LAP001'),
            ('Camiseta Básica', 'Camiseta de algodón 100%', 19.99, 2, 'CAM001'),
            ('Lámpara de Mesa', 'Lámpara LED ajustable', 29.99, 3, 'LAM001')
        ]
        
        for name, description, price, category_id, sku in products:
            cursor.execute('''
                INSERT OR IGNORE INTO products (name, description, price, category_id, sku) 
                VALUES (?, ?, ?, ?, ?)
            ''', (name, description, price, category_id, sku))
        
        conn.commit()
        print("✅ Productos creados")
        
        # Crear stock inicial
        stocks = [
            (1, 10, 2),
            (2, 50, 10),
            (3, 15, 3)
        ]
        
        for product_id, quantity, min_quantity in stocks:
            cursor.execute('''
                INSERT OR IGNORE INTO stock (product_id, quantity, min_quantity) 
                VALUES (?, ?, ?)
            ''', (product_id, quantity, min_quantity))
        
        conn.commit()
        print("✅ Stock inicial creado")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error creando datos de muestra: {e}")
        return False

def verify_database():
    """Verifica que la base de datos esté funcionando correctamente"""
    
    print("\n🔍 Verificando base de datos...")
    
    try:
        # Conectar a la base de datos
        db_path = Path('instance') / 'stock_management.db'
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Verificar conexión
        cursor.execute('SELECT 1')
        result = cursor.fetchone()
        if result and result[0] == 1:
            print("✅ Conexión a base de datos exitosa")
        
        # Verificar tablas
        cursor.execute('SELECT COUNT(*) FROM users')
        user_count = cursor.fetchone()[0]
        print(f"✅ Usuarios en BD: {user_count}")
        
        cursor.execute('SELECT COUNT(*) FROM categories')
        category_count = cursor.fetchone()[0]
        print(f"✅ Categorías en BD: {category_count}")
        
        cursor.execute('SELECT COUNT(*) FROM products')
        product_count = cursor.fetchone()[0]
        print(f"✅ Productos en BD: {product_count}")
        
        conn.close()
        return True
        
    except Exception as e:
        print(f"❌ Error verificando base de datos: {e}")
        return False

def test_flask_connection():
    """Prueba si Flask puede conectar a la base de datos"""
    
    print("\n🐍 Probando conexión de Flask-SQLAlchemy...")
    
    try:
        from app import create_app
        from app.database import db
        from app.models.user import User
        
        app = create_app()
        
        with app.app_context():
            # Verificar conexión
            result = db.session.execute('SELECT 1').scalar()
            if result == 1:
                print("✅ Flask-SQLAlchemy conecta correctamente")
            
            # Verificar que puede leer usuarios
            user_count = User.query.count()
            print(f"✅ Flask puede leer usuarios: {user_count}")
            
            return True
            
    except Exception as e:
        print(f"❌ Error en Flask-SQLAlchemy: {e}")
        return False

def main():
    """Función principal"""
    
    print("🔧 CREADOR DE BASE DE DATOS HÍBRIDO - STOCK MANAGEMENT")
    print("="*70)
    
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
    
    # Probar conexión de Flask
    if not test_flask_connection():
        print("⚠️ Flask-SQLAlchemy no puede conectar, pero la BD funciona")
    
    print("\n" + "="*70)
    print("🎉 ¡BASE DE DATOS CREADA EXITOSAMENTE!")
    print("="*70)
    print("\n💡 Ahora puedes:")
    print("   1. Iniciar el backend: python run.py")
    print("   2. Hacer login con:")
    print("      Usuario: admin")
    print("      Contraseña: admin123")
    print("   3. Probar el frontend en http://localhost:8080")

if __name__ == "__main__":
    main()
