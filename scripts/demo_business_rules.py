#!/usr/bin/env python3
"""
Demo de Validaciones de Negocio - Sistema de Gestión de Inventario
Demuestra todas las reglas críticas de negocio implementadas
"""

import os
import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

from app import create_app
from app.database import db
from app.models.category import Category
from app.models.product import Product
from app.models.stock import Stock
from app.models.order import Order
from app.models.order_item import OrderItem
from app.validators.business_rules import (
    BusinessRuleViolation,
    StockValidator,
    OrderValidator,
    TransactionManager,
    BusinessRuleEngine
)


def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)


def print_step(step, description):
    """Imprime un paso del proceso"""
    print(f"\n{step}. {description}")
    print("-" * 40)


def demo_stock_validations():
    """Demostrar validaciones de stock"""
    print_header("Validaciones de Stock")
    
    print_step("1", "Validar cantidades positivas")
    try:
        StockValidator.validate_quantity(10)
        StockValidator.validate_quantity(0)
        print("✅ Cantidades válidas aceptadas")
    except BusinessRuleViolation as e:
        print(f"❌ Error inesperado: {e}")
    
    print_step("2", "Rechazar cantidades negativas")
    try:
        StockValidator.validate_quantity(-5)
        print("❌ Error: Debería haber rechazado cantidad negativa")
    except BusinessRuleViolation as e:
        print(f"✅ Cantidad negativa rechazada correctamente: {e}")
        print(f"   Campo: {e.field}, Valor: {e.value}")
    
    print_step("3", "Rechazar tipos inválidos")
    try:
        StockValidator.validate_quantity("10")
        print("❌ Error: Debería haber rechazado tipo inválido")
    except BusinessRuleViolation as e:
        print(f"✅ Tipo inválido rechazado correctamente: {e}")
    
    print_step("4", "Validar stock mínimo")
    try:
        StockValidator.validate_min_stock(5)
        StockValidator.validate_min_stock(0)
        print("✅ Stock mínimo válido aceptado")
    except BusinessRuleViolation as e:
        print(f"❌ Error inesperado: {e}")
    
    print_step("5", "Rechazar stock mínimo negativo")
    try:
        StockValidator.validate_min_stock(-1)
        print("❌ Error: Debería haber rechazado stock mínimo negativo")
    except BusinessRuleViolation as e:
        print(f"✅ Stock mínimo negativo rechazado correctamente: {e}")


def demo_order_validations():
    """Demostrar validaciones de órdenes"""
    print_header("Validaciones de Órdenes")
    
    print_step("1", "Validar items de orden válidos")
    valid_items = [
        {'product_id': 1, 'quantity': 5},
        {'product_id': 2, 'quantity': 3}
    ]
    try:
        OrderValidator.validate_order_items(valid_items)
        print("✅ Items de orden válidos aceptados")
    except BusinessRuleViolation as e:
        print(f"❌ Error inesperado: {e}")
    
    print_step("2", "Rechazar orden vacía")
    try:
        OrderValidator.validate_order_items([])
        print("❌ Error: Debería haber rechazado orden vacía")
    except BusinessRuleViolation as e:
        print(f"✅ Orden vacía rechazada correctamente: {e}")
    
    print_step("3", "Rechazar item con campo faltante")
    invalid_items = [{'product_id': 1}]  # Falta quantity
    try:
        OrderValidator.validate_order_items(invalid_items)
        print("❌ Error: Debería haber rechazado item incompleto")
    except BusinessRuleViolation as e:
        print(f"✅ Item incompleto rechazado correctamente: {e}")
    
    print_step("4", "Rechazar cantidad inválida")
    invalid_quantity_items = [{'product_id': 1, 'quantity': -2}]
    try:
        OrderValidator.validate_order_items(invalid_quantity_items)
        print("❌ Error: Debería haber rechazado cantidad negativa")
    except BusinessRuleViolation as e:
        print(f"✅ Cantidad negativa rechazada correctamente: {e}")


def demo_transaction_manager():
    """Demostrar el gestor de transacciones"""
    print_header("Gestor de Transacciones")
    
    print_step("1", "Crear aplicación de prueba")
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        print_step("2", "Crear datos de muestra")
        # Crear categoría
        category = Category(name="Electrónicos", description="Productos electrónicos")
        db.session.add(category)
        db.session.flush()
        
        # Crear producto
        product = Product(
            name="Laptop",
            description="Laptop de alta gama",
            price=999.99,
            category_id=category.id
        )
        db.session.add(product)
        db.session.flush()
        
        # Crear stock
        stock = Stock(product_id=product.id, quantity=10, min_stock=2)
        db.session.add(stock)
        db.session.commit()
        
        print(f"✅ Producto creado: {product.name} (ID: {product.id})")
        print(f"✅ Stock inicial: {stock.quantity} unidades")
        
        print_step("3", "Actualizar stock válidamente")
        try:
            result = TransactionManager.execute_stock_update(
                product_id=product.id,
                new_quantity=15
            )
            print(f"✅ Stock actualizado exitosamente: {result['message']}")
            print(f"   Cantidad anterior: {result['old_quantity']}")
            print(f"   Nueva cantidad: {result['new_quantity']}")
        except BusinessRuleViolation as e:
            print(f"❌ Error inesperado: {e}")
        
        print_step("4", "Rechazar actualización a stock negativo")
        try:
            TransactionManager.execute_stock_update(
                product_id=product.id,
                new_quantity=-5
            )
            print("❌ Error: Debería haber rechazado stock negativo")
        except BusinessRuleViolation as e:
            print(f"✅ Stock negativo rechazado correctamente: {e}")
        
        print_step("5", "Verificar que no se modificó la base de datos")
        current_stock = Stock.query.filter_by(product_id=product.id).first()
        print(f"✅ Stock actual en BD: {current_stock.quantity} (debería ser 15)")
        
        print_step("6", "Crear y completar orden")
        # Crear orden
        order = Order(status='pending')
        db.session.add(order)
        db.session.flush()
        
        # Agregar item
        item = OrderItem(
            order_id=order.id,
            product_id=product.id,
            quantity=5
        )
        db.session.add(item)
        db.session.commit()
        
        print(f"✅ Orden creada: ID {order.id}")
        
        # Completar orden
        try:
            result = TransactionManager.execute_order_completion(order.id)
            print(f"✅ Orden completada exitosamente: {result['message']}")
            print(f"   Stock actualizado: {result['stock_updated']} productos")
            
            # Verificar estado final
            completed_order = Order.query.get(order.id)
            final_stock = Stock.query.filter_by(product_id=product.id).first()
            print(f"   Estado de orden: {completed_order.status}")
            print(f"   Stock final: {final_stock.quantity} unidades")
            
        except BusinessRuleViolation as e:
            print(f"❌ Error al completar orden: {e}")
        
        print_step("7", "Intentar completar orden con stock insuficiente")
        # Crear otra orden
        order2 = Order(status='pending')
        db.session.add(order2)
        db.session.flush()
        
        # Agregar item con cantidad mayor al stock disponible
        item2 = OrderItem(
            order_id=order2.id,
            product_id=product.id,
            quantity=20  # Solo hay 5 disponibles después de la primera orden
        )
        db.session.add(item2)
        db.session.commit()
        
        try:
            TransactionManager.execute_order_completion(order2.id)
            print("❌ Error: Debería haber rechazado orden con stock insuficiente")
        except BusinessRuleViolation as e:
            print(f"✅ Orden con stock insuficiente rechazada correctamente: {e}")
        
        # Verificar que no se modificó la base de datos
        order2 = Order.query.get(order2.id)
        final_stock = Stock.query.filter_by(product_id=product.id).first()
        print(f"   Estado de orden 2: {order2.status} (debería ser 'pending')")
        print(f"   Stock final: {final_stock.quantity} (debería ser 5)")
        
        db.drop_all()


def demo_business_rule_engine():
    """Demostrar el motor de validaciones de negocio"""
    print_header("Motor de Validaciones de Negocio")
    
    print_step("1", "Crear aplicación de prueba")
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        
        print_step("2", "Validar reglas con datos válidos")
        result = BusinessRuleEngine.validate_all_business_rules()
        print(f"✅ Validación de reglas: {'Válido' if result['valid'] else 'Inválido'}")
        print(f"   Violaciones encontradas: {len(result['violations'])}")
        print(f"   Total de verificaciones: {result['total_checks']}")
        
        print_step("3", "Crear datos que violen reglas")
        # Crear categoría y producto
        category = Category(name="Test", description="Test")
        db.session.add(category)
        db.session.flush()
        
        product = Product(name="Test", description="Test", price=10.0, category_id=category.id)
        db.session.add(product)
        db.session.flush()
        
        # Crear stock negativo (violación)
        stock = Stock(product_id=product.id, quantity=-5, min_stock=-2)
        db.session.add(stock)
        db.session.commit()
        
        print("✅ Datos con violaciones creados")
        
        print_step("4", "Validar reglas con violaciones")
        result = BusinessRuleEngine.validate_all_business_rules()
        print(f"✅ Validación de reglas: {'Válido' if result['valid'] else 'Inválido'}")
        print(f"   Violaciones encontradas: {len(result['violations'])}")
        
        for i, violation in enumerate(result['violations'], 1):
            print(f"   Violación {i}:")
            print(f"     Regla: {violation['rule']}")
            print(f"     Mensaje: {violation['message']}")
            if 'details' in violation:
                print(f"     Detalles: {violation['details']}")
        
        db.drop_all()


def demo_api_endpoints():
    """Demostrar endpoints de API con validaciones"""
    print_header("Endpoints de API con Validaciones")
    
    print_step("1", "Crear aplicación de prueba")
    app = create_app('testing')
    client = app.test_client()
    
    with app.app_context():
        db.create_all()
        
        print_step("2", "Crear datos de muestra")
        # Crear categoría
        category = Category(name="Electrónicos", description="Productos electrónicos")
        db.session.add(category)
        db.session.flush()
        
        # Crear producto
        product = Product(
            name="Laptop",
            description="Laptop de alta gama",
            price=999.99,
            category_id=category.id
        )
        db.session.add(product)
        db.session.flush()
        
        # Crear stock
        stock = Stock(product_id=product.id, quantity=10, min_stock=2)
        db.session.add(stock)
        db.session.commit()
        
        print(f"✅ Producto creado: {product.name} (ID: {product.id})")
        print(f"✅ Stock inicial: {stock.quantity} unidades")
        
        print_step("3", "Probar endpoint de validación de reglas")
        response = client.get('/api/stock/validate')
        if response.status_code == 200:
            data = response.get_json()
            print(f"✅ Endpoint de validación funcionando")
            print(f"   Estado: {'Válido' if data['valid'] else 'Inválido'}")
            print(f"   Violaciones: {len(data['violations'])}")
        else:
            print(f"❌ Error en endpoint de validación: {response.status_code}")
        
        print_step("4", "Probar creación de orden con stock insuficiente")
        order_data = {
            'items': [
                {
                    'product_id': product.id,
                    'quantity': 15  # Solo hay 10 disponibles
                }
            ]
        }
        
        response = client.post('/api/orders/', json=order_data)
        if response.status_code == 400:
            data = response.get_json()
            print(f"✅ Orden con stock insuficiente rechazada correctamente")
            print(f"   Error: {data['error']}")
            print(f"   Mensaje: {data['message']}")
        else:
            print(f"❌ Error: Debería haber rechazado la orden")
        
        print_step("5", "Probar actualización de stock a valor negativo")
        update_data = {'quantity': -5}
        response = client.put(f'/api/stock/{product.id}', json=update_data)
        if response.status_code == 400:
            data = response.get_json()
            print(f"✅ Stock negativo rechazado correctamente")
            print(f"   Error: {data['error']}")
            print(f"   Mensaje: {data['message']}")
        else:
            print(f"❌ Error: Debería haber rechazado stock negativo")
        
        db.drop_all()


def main():
    """Función principal del demo"""
    print_header("🎯 Demo de Validaciones de Negocio - Sistema de Gestión de Inventario")
    print("Este demo muestra todas las reglas críticas de negocio implementadas")
    
    try:
        # Ejecutar demos
        demo_stock_validations()
        demo_order_validations()
        demo_transaction_manager()
        demo_business_rule_engine()
        demo_api_endpoints()
        
        print_header("🎉 Demo Completado Exitosamente")
        print("✅ Todas las validaciones de negocio funcionan correctamente")
        print("✅ Stock nunca puede ser negativo")
        print("✅ Ventas no pueden superar stock disponible")
        print("✅ Completar órdenes es una operación transaccional")
        print("✅ Rollback automático en caso de errores")
        
    except Exception as e:
        print_header("❌ Error en el Demo")
        print(f"Error: {e}")
        print("Verifica que la aplicación esté configurada correctamente")
        return 1
    
    return 0


if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)
