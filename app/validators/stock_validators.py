#!/usr/bin/env python3
"""
Validadores para Stock con validaciones de no-negativo
"""

from marshmallow import ValidationError
from app.database import db
from app.models.stock import Stock
from app.models.product import Product

def validate_stock_quantity(quantity):
    """Validar que la cantidad de stock no sea negativa"""
    if quantity < 0:
        raise ValidationError("La cantidad de stock no puede ser negativa")
    return quantity

def validate_stock_min_quantity(min_stock):
    """Validar que el stock mínimo no sea negativa"""
    if min_stock < 0:
        raise ValidationError("El stock mínimo no puede ser negativo")
    return min_stock

def validate_stock_update(stock_id, new_quantity):
    """Validar actualización de stock considerando órdenes pendientes"""
    if new_quantity < 0:
        raise ValidationError("La cantidad de stock no puede ser negativa")
    
    # Obtener stock actual
    stock = Stock.query.get(stock_id)
    if not stock:
        raise ValidationError("Stock no encontrado")
    
    # Verificar si la reducción afectaría órdenes pendientes
    if new_quantity < stock.quantity:
        # Buscar órdenes pendientes que usen este producto
        from app.models.order import Order
        from app.models.order_item import OrderItem
        
        pending_orders = db.session.query(Order).join(OrderItem).filter(
            OrderItem.product_id == stock.product_id,
            Order.status == 'pending'
        ).all()
        
        # Calcular stock comprometido en órdenes pendientes
        committed_stock = sum(
            item.quantity for order in pending_orders 
            for item in order.items if item.product_id == stock.product_id
        )
        
        if new_quantity < committed_stock:
            raise ValidationError(
                f"No se puede reducir el stock a {new_quantity}. "
                f"Hay {committed_stock} unidades comprometidas en órdenes pendientes"
            )
    
    return new_quantity

def validate_product_stock_availability(product_id, requested_quantity):
    """Validar disponibilidad de stock para un producto"""
    stock = Stock.query.filter_by(product_id=product_id).first()
    
    if not stock:
        raise ValidationError(f"No hay stock disponible para el producto {product_id}")
    
    if stock.quantity < requested_quantity:
        raise ValidationError(
            f"Stock insuficiente. Disponible: {stock.quantity}, "
            f"Solicitado: {requested_quantity}"
        )
    
    return stock

def validate_stock_creation(product_id, quantity, min_stock):
    """Validar creación de nuevo stock"""
    # Verificar que el producto existe
    product = Product.query.get(product_id)
    if not product:
        raise ValidationError(f"Producto {product_id} no encontrado")
    
    # Verificar que no existe stock para este producto
    existing_stock = Stock.query.filter_by(product_id=product_id).first()
    if existing_stock:
        raise ValidationError(f"Ya existe stock para el producto {product_id}")
    
    # Validar cantidades
    if quantity < 0:
        raise ValidationError("La cantidad de stock no puede ser negativa")
    
    if min_stock < 0:
        raise ValidationError("El stock mínimo no puede ser negativo")
    
    return True
