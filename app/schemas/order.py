#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Órdenes
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.validators.order_validators import validate_order_items, validate_order_stock_availability

class OrderItemSchema(Schema):
    """Esquema para Item de Orden"""
    id = fields.Int(dump_only=True, description="ID único del item")
    order_id = fields.Int(required=True, description="ID de la orden")
    product_id = fields.Int(required=True, description="ID del producto")
    quantity = fields.Int(required=True, validate=validate.Range(min=1), 
                         description="Cantidad del producto")
    unit_price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                               description="Precio unitario")
    subtotal = fields.Decimal(dump_only=True, places=2, description="Subtotal del item")
    
    # Campos relacionados
    product = fields.Nested('ProductSchema', dump_only=True, description="Producto")

class OrderSchema(Schema):
    """Esquema para Orden"""
    id = fields.Int(dump_only=True, description="ID único de la orden")
    customer_name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                              description="Nombre del cliente")
    total = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                          description="Total de la orden")
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
                       description="Estado de la orden")
    created_at = fields.DateTime(dump_only=True, description="Fecha de creación")
    updated_at = fields.DateTime(dump_only=True, description="Fecha de última actualización")
    
    # Campos relacionados
    items = fields.Nested(OrderItemSchema, many=True, description="Items de la orden")
    created_by = fields.Nested('UserSchema', dump_only=True, description="Usuario que creó la orden")

class OrderCreateSchema(Schema):
    """Esquema para crear orden"""
    customer_name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                              description="Nombre del cliente")
    items = fields.List(fields.Dict(), required=True, 
                       description="Lista de items con product_id y quantity")
    
    @validates('items')
    def validate_items(self, value):
        # Validar estructura de items
        validate_order_items(value)
        # Validar disponibilidad de stock
        validate_order_stock_availability(value)
        return value

class OrderUpdateSchema(Schema):
    """Esquema para actualizar orden"""
    customer_name = fields.Str(validate=validate.Length(min=1, max=200), 
                              description="Nombre del cliente")
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
                       description="Estado de la orden")

class OrderListSchema(Schema):
    """Esquema para lista de órdenes"""
    orders = fields.Nested(OrderSchema, many=True, description="Lista de órdenes")
    total = fields.Int(description="Total de órdenes")
    pending_count = fields.Int(description="Cantidad de órdenes pendientes")
    completed_count = fields.Int(description="Cantidad de órdenes completadas")
