#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Órdenes
"""

from marshmallow import Schema, fields, validate, validates
from app.validators.order_validators import validate_order_items, validate_order_stock_availability

class OrderItemSchema(Schema):
    """Esquema para items de orden"""
    id = fields.Int(
        dump_only=True
    )
    order_id = fields.Int(
        required=True
    )
    product_id = fields.Int(
        required=True
    )
    quantity = fields.Int(
        required=True, 
        validate=validate.Range(min=1)
    )
    unit_price = fields.Decimal(
        required=True, 
        places=2, 
        validate=validate.Range(min=0)
    )
    subtotal = fields.Decimal(
        dump_only=True, 
        places=2
    )
    
    # Relaciones
    product = fields.Nested(
        'ProductSchema', 
        dump_only=True
    )

class OrderSchema(Schema):
    """Esquema completo para Orden"""
    id = fields.Int(
        dump_only=True
    )
    customer_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200)
    )
    customer_email = fields.Email(
        required=True
    )
    customer_phone = fields.Str(
        required=True
    )
    total = fields.Decimal(
        dump_only=True, 
        places=2
    )
    status = fields.Str(
        dump_only=True
    )
    notes = fields.Str(
        dump_only=True
    )
    created_at = fields.DateTime(
        dump_only=True
    )
    updated_at = fields.DateTime(
        dump_only=True
    )
    completed_at = fields.DateTime(
        dump_only=True
    )
    
    # Relaciones
    items = fields.Nested(
        OrderItemSchema, 
        many=True, 
        dump_only=True
    )
    user = fields.Nested(
        'UserSchema', 
        dump_only=True
    )
    
    # Campos calculados
    item_count = fields.Int(
        dump_only=True
    )
    is_completed = fields.Bool(
        dump_only=True
    )
    can_cancel = fields.Bool(
        dump_only=True
    )

class OrderCreateSchema(Schema):
    """Esquema para crear una nueva orden"""
    customer_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200)
    )
    customer_email = fields.Email(
        required=True
    )
    customer_phone = fields.Str(
        required=True
    )
    notes = fields.Str()
    items = fields.List(
        fields.Dict(), 
        required=True
    )
    
    @validates('items')
    def validate_items(self, value):
        # Validar estructura de items
        validate_order_items(value)
        # Validar disponibilidad de stock
        validate_order_stock_availability(value)
        return value

class OrderUpdateSchema(Schema):
    """Esquema para actualizar una orden existente"""
    customer_name = fields.Str(
        validate=validate.Length(min=1, max=200)
    )
    customer_email = fields.Email()
    customer_phone = fields.Str()
    status = fields.Str(
        validate=validate.OneOf(['pending', 'completed', 'cancelled'])
    )
    notes = fields.Str()

class OrderListSchema(Schema):
    """Esquema para respuesta de lista de órdenes"""
    orders = fields.Nested(
        OrderSchema, 
        many=True
    )
    total = fields.Int()
    pending_count = fields.Int()
    completed_count = fields.Int()
    cancelled_count = fields.Int()

class OrderSearchSchema(Schema):
    """Esquema para búsqueda y filtrado de órdenes"""
    customer_name = fields.Str()
    status = fields.Str(
        validate=validate.OneOf(['pending', 'completed', 'cancelled'])
    )
    min_total = fields.Decimal(
        places=2,
        validate=validate.Range(min=0)
    )
    max_total = fields.Decimal(
        places=2,
        validate=validate.Range(min=0)
    )
    date_from = fields.Date()
    date_to = fields.Date()
    product_id = fields.Int()

class OrderCompleteSchema(Schema):
    """Esquema para completar una orden"""
    notes = fields.Str()
    delivery_method = fields.Str()
    delivery_date = fields.DateTime()
