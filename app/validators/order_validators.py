#!/usr/bin/env python3
"""
Validadores para Órdenes con validaciones de stock y completitud
"""

from marshmallow import ValidationError
from app.database import db
from app.models.order import Order
from app.models.order_item import OrderItem
from app.models.stock import Stock
from app.models.product import Product
from .stock_validators import validate_product_stock_availability

def validate_order_items(items):
    """Validar items de orden antes de crear/actualizar"""
    if not items or len(items) == 0:
        raise ValidationError("La orden debe tener al menos un producto")
    
    # Validar estructura de cada item
    for i, item in enumerate(items):
        if not isinstance(item, dict):
            raise ValidationError(f"Item {i}: debe ser un objeto")
        
        if 'product_id' not in item:
            raise ValidationError(f"Item {i}: falta product_id")
        
        if 'quantity' not in item:
            raise ValidationError(f"Item {i}: falta quantity")
        
        if not isinstance(item['quantity'], int) or item['quantity'] <= 0:
            raise ValidationError(f"Item {i}: quantity debe ser un número positivo")
        
        # Verificar que el producto existe
        product = Product.query.get(item['product_id'])
        if not product:
            raise ValidationError(f"Item {i}: producto {item['product_id']} no encontrado")
    
    return items

def validate_order_stock_availability(items, order_id=None):
    """Validar disponibilidad de stock para todos los items de la orden"""
    stock_issues = []
    
    for item in items:
        product_id = item['product_id']
        quantity = item['quantity']
        
        try:
            # Verificar stock disponible
            stock = validate_product_stock_availability(product_id, quantity)
            
            # Si es una actualización, considerar stock ya reservado por esta orden
            if order_id:
                current_order = Order.query.get(order_id)
                if current_order:
                    # Calcular stock ya reservado por esta orden (excluyendo el item actual)
                    reserved_by_order = sum(
                        oi.quantity for oi in current_order.items 
                        if oi.product_id == product_id and oi.id != item.get('id')
                    )
                    available_stock = stock.quantity + reserved_by_order
                    
                    if available_stock < quantity:
                        stock_issues.append(
                            f"Producto {product_id}: stock insuficiente. "
                            f"Disponible: {available_stock}, Solicitado: {quantity}"
                        )
            else:
                # Nueva orden: verificar stock disponible
                if stock.quantity < quantity:
                    stock_issues.append(
                        f"Producto {product_id}: stock insuficiente. "
                        f"Disponible: {stock.quantity}, Solicitado: {quantity}"
                    )
                    
        except ValidationError as e:
            stock_issues.append(str(e))
    
    if stock_issues:
        raise ValidationError("Problemas de stock: " + "; ".join(stock_issues))
    
    return True

def validate_order_completion(order_id):
    """Validar que una orden se pueda completar"""
    order = Order.query.get(order_id)
    if not order:
        raise ValidationError("Orden no encontrada")
    
    if order.status != 'pending':
        raise ValidationError(f"La orden ya está {order.status}")
    
    if not order.items or len(order.items) == 0:
        raise ValidationError("No se puede completar una orden sin productos")
    
    # Verificar stock disponible para completar
    for item in order.items:
        try:
            validate_product_stock_availability(item.product_id, item.quantity)
        except ValidationError as e:
            raise ValidationError(f"No se puede completar la orden: {str(e)}")
    
    return order

def validate_order_update(order_id, new_items):
    """Validar actualización de orden"""
    order = Order.query.get(order_id)
    if not order:
        raise ValidationError("Orden no encontrada")
    
    if order.status != 'pending':
        raise ValidationError("Solo se pueden actualizar órdenes pendientes")
    
    # Validar nuevos items
    validate_order_items(new_items)
    
    # Validar stock disponible
    validate_order_stock_availability(new_items, order_id)
    
    return order

def validate_order_deletion(order_id):
    """Validar que una orden se pueda eliminar"""
    order = Order.query.get(order_id)
    if not order:
        raise ValidationError("Orden no encontrada")
    
    if order.status == 'completed':
        raise ValidationError("No se puede eliminar una orden completada")
    
    return order

def calculate_order_total(items):
    """Calcular total de la orden basado en precios actuales"""
    total = 0
    
    for item in items:
        product = Product.query.get(item['product_id'])
        if product:
            total += product.price * item['quantity']
    
    return total
