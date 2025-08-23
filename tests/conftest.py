"""
Configuración de pytest para tests de validaciones de negocio
"""

import pytest
import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app import create_app
from app.database import db


@pytest.fixture(scope='session')
def app():
    """Crear aplicación de prueba para la sesión"""
    app = create_app('testing')
    return app


@pytest.fixture(scope='function')
def app_context(app):
    """Contexto de aplicación para cada test"""
    with app.app_context():
        yield app


@pytest.fixture(scope='function')
def db_session(app_context):
    """Sesión de base de datos para cada test"""
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture(scope='function')
def client(app_context):
    """Cliente de prueba"""
    return app_context.test_client()


@pytest.fixture(scope='function')
def sample_data(db_session):
    """Crear datos de muestra para testing"""
    from app.models.category import Category
    from app.models.product import Product
    from app.models.stock import Stock
    from app.models.user import User
    
    # Crear categoría
    category = Category(name="Electrónicos", description="Productos electrónicos")
    db.session.add(category)
    db.session.flush()
    
    # Crear productos
    product1 = Product(
        name="Laptop",
        description="Laptop de alta gama",
        price=999.99,
        category_id=category.id
    )
    product2 = Product(
        name="Mouse",
        description="Mouse inalámbrico",
        price=29.99,
        category_id=category.id
    )
    db.session.add_all([product1, product2])
    db.session.flush()
    
    # Crear stock
    stock1 = Stock(product_id=product1.id, quantity=10, min_stock=2)
    stock2 = Stock(product_id=product2.id, quantity=50, min_stock=5)
    db.session.add_all([stock1, stock2])
    
    # Crear usuario admin
    admin_user = User(
        username="admin",
        email="admin@test.com",
        password_hash="hashed_password",
        role="admin"
    )
    db.session.add(admin_user)
    
    db.session.commit()
    
    return {
        'category': category,
        'product1': product1,
        'product2': product2,
        'stock1': stock1,
        'stock2': stock2,
        'admin_user': admin_user
    }


@pytest.fixture(scope='function')
def order_with_items(db_session, sample_data):
    """Crear orden con items para testing"""
    from app.models.order import Order
    from app.models.order_item import OrderItem
    
    # Crear orden
    order = Order(status='pending')
    db.session.add(order)
    db.session.flush()
    
    # Agregar items
    item1 = OrderItem(
        order_id=order.id,
        product_id=sample_data['product1'].id,
        quantity=3
    )
    item2 = OrderItem(
        order_id=order.id,
        product_id=sample_data['product2'].id,
        quantity=5
    )
    db.session.add_all([item1, item2])
    db.session.commit()
    
    return {
        'order': order,
        'items': [item1, item2]
    }


@pytest.fixture(scope='function')
def completed_order(db_session, sample_data):
    """Crear orden completada para testing"""
    from app.models.order import Order
    from app.models.order_item import OrderItem
    
    # Crear orden
    order = Order(status='completed')
    db.session.add(order)
    db.session.flush()
    
    # Agregar item
    item = OrderItem(
        order_id=order.id,
        product_id=sample_data['product1'].id,
        quantity=2
    )
    db.session.add(item)
    db.session.commit()
    
    return {
        'order': order,
        'item': item
    }


@pytest.fixture(scope='function')
def negative_stock_data(db_session, sample_data):
    """Crear datos con stock negativo para testing de violaciones"""
    # Modificar stock existente a valor negativo
    sample_data['stock1'].quantity = -5
    sample_data['stock1'].min_stock = -2
    db.session.commit()
    
    return sample_data


@pytest.fixture(scope='function')
def duplicate_products_order(db_session, sample_data):
    """Crear orden con productos duplicados para testing"""
    from app.models.order import Order
    from app.models.order_item import OrderItem
    
    # Crear orden
    order = Order(status='pending')
    db.session.add(order)
    db.session.flush()
    
    # Agregar items duplicados (mismo producto)
    item1 = OrderItem(
        order_id=order.id,
        product_id=sample_data['product1'].id,
        quantity=3
    )
    item2 = OrderItem(
        order_id=order.id,
        product_id=sample_data['product1'].id,  # Mismo producto
        quantity=2
    )
    db.session.add_all([item1, item2])
    db.session.commit()
    
    return {
        'order': order,
        'items': [item1, item2]
    }
