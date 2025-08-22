#!/usr/bin/env python3
"""
Validadores para Órdenes de Compra con validaciones transaccionales
"""

from marshmallow import ValidationError
from app.database import db
from app.models.purchase_order import PurchaseOrder
from app.models.purchase_order_item import PurchaseOrderItem
from app.models.stock import Stock
from app.models.product import Product

def validate_purchase_order_items(items):
    """Validar items de orden de compra"""
    if not items or len(items) == 0:
        raise ValidationError("La orden de compra debe tener al menos un producto")
    
    # Validar estructura de cada item
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValidationError(f"Item {i}: debe ser un objeto")
        
        if 'product_id' not in item:
            raise ValidationError(f"Item {i}: falta product_id")
        
        if 'quantity' not in item:
            raise ValidationError(f"Item {i}: falta quantity")
        
        if 'unit_price' not in item:
            raise ValidationError(f"Item {i}: falta unit_price")
        
        if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
            raise ValidationError(f"Item {i}: quantity debe ser un número positivo")
        
        if not isinstance(item['unit_price'], (int, float)) or item['unit_price'] < 0:
            raise ValidationError(f"Item {i}: unit_price debe ser un número no negativo")
        
        # Verificar que el producto existe
        product = Product.query.get(item['product_id'])
        if not product:
            raise ValidationError(f"Item {i}: producto {item['product_id']} no encontrado")
    
    return items

def validate_purchase_order_completion(purchase_order_id):
    """Validar que una orden de compra se pueda completar"""
    purchase_order = PurchaseOrder.query.get(purchase_order_id)
    if not purchase_order:
        raise ValidationError("Orden de compra no encontrada")
    
    if purchase_order.status != 'pending':
        raise ValidationError(f"La orden de compra ya está {purchase_order.status}")
    
    if not purchase_order.items or len(purchase_order.items) == 0:
        raise ValidationError("No se puede completar una orden de compra sin productos")
    
    return purchase_order

def update_stock_from_purchase_order(purchase_order_id):
    """Actualizar stock de forma transaccional al completar orden de compra"""
    purchase_order = PurchaseOrder.query.get(purchase_order_id)
    if not purchase_order:
        raise ValidationError("Orden de compra no encontrada")
    
    try:
        # Iniciar transacción
        for item in purchase_order.items:
            # Buscar stock existente
            stock = Stock.query.filter_by(product_id=item.product_id).first()
            
            if stock:
                # Actualizar stock existente
                stock.quantity += item.quantity
                stock.updated_at = db.func.now()
            else:
                # Crear nuevo stock
                new_stock = Stock(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    min_stock=0  # Valor por defecto
                )
                db.session.add(new_stock)
        
        # Marcar orden como completada
        purchase_order.status = 'completed'
        purchase_order.updated_at = db.func.now()
        
        # Commit de la transacción
        db.session.commit()
        
        return True
        
    except Exception as e:
        # Rollback en caso de error
        db.session.rollback()
        raise ValidationError(f"Error al actualizar stock: {str(e)}")

def validate_purchase_order_update(purchase_order_id, new_items):
    """Validar actualización de orden de compra"""
    purchase_order = PurchaseOrder.query.get(purchase_order_id)
    if not purchase_order:
        raise ValidationError("Orden de compra no encontrada")
    
    if purchase_order.status != 'pending':
        raise ValidationError("Solo se pueden actualizar órdenes de compra pendientes")
    
    # Validar nuevos items
    validate_purchase_order_items(new_items)
    
    return purchase_order

def validate_purchase_order_deletion(purchase_order_id):
    """Validar que una orden de compra se pueda eliminar"""
    purchase_order = PurchaseOrder.query.get(purchase_order_id)
    if not purchase_order:
        raise ValidationError("Orden de compra no encontrada")
    
    if purchase_order.status == 'completed':
        raise ValidationError("No se puede eliminar una orden de compra completada")
    
    return purchase_order

def calculate_purchase_order_total(items):
    """Calcular total de la orden de compra"""
    total = 0
    
    for item in items:
        total += item['unit_price'] * item['quantity']
    
    return total
