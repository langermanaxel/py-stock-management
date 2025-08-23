#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Órdenes
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.validators.order_validators import validate_order_items, validate_order_stock_availability

class OrderItemSchema(Schema):
    """Esquema completo para Item de Orden"""
    id = fields.Int(
        dump_only=True, 
        description="ID único del item de orden (generado automáticamente)"
    )
    order_id = fields.Int(
        required=True, 
        description="ID de la orden a la que pertenece este item",
        example=1
    )
    product_id = fields.Int(
        required=True, 
        description="ID del producto en este item",
        example=1
    )
    quantity = fields.Int(
        required=True, 
        validate=validate.Range(min=1), 
        description="Cantidad del producto (mínimo 1)",
        example=2
    )
    unit_price = fields.Decimal(
        required=True, 
        places=2, 
        validate=validate.Range(min=0), 
        description="Precio unitario del producto al momento de la orden",
        example="1299.99"
    )
    subtotal = fields.Decimal(
        dump_only=True, 
        places=2, 
        description="Subtotal calculado del item (quantity × unit_price)"
    )
    
    # Campos relacionados
    product = fields.Nested(
        'ProductSchema', 
        dump_only=True, 
        description="Información completa del producto"
    )

class OrderSchema(Schema):
    """Esquema completo para Orden"""
    id = fields.Int(
        dump_only=True, 
        description="ID único de la orden (generado automáticamente)"
    )
    customer_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200), 
        description="Nombre completo del cliente (máximo 200 caracteres)",
        example="Juan Pérez"
    )
    customer_email = fields.Email(
        description="Email del cliente para notificaciones",
        example="juan.perez@email.com"
    )
    customer_phone = fields.Str(
        description="Teléfono de contacto del cliente",
        example="+34 123 456 789"
    )
    total = fields.Decimal(
        required=True, 
        places=2, 
        validate=validate.Range(min=0), 
        description="Total calculado de la orden (suma de todos los items)",
        example="2599.98"
    )
    status = fields.Str(
        validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
        description="Estado actual de la orden",
        example="pending"
    )
    notes = fields.Str(
        description="Notas adicionales sobre la orden",
        example="Entregar en horario de mañana"
    )
    created_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de creación de la orden (automático)"
    )
    updated_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de última actualización (automático)"
    )
    completed_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de completado de la orden"
    )
    
    # Campos relacionados
    items = fields.Nested(
        OrderItemSchema, 
        many=True, 
        description="Lista de items de la orden"
    )
    created_by = fields.Nested(
        'UserSchema', 
        dump_only=True, 
        description="Usuario que creó la orden"
    )
    
    # Campos calculados
    item_count = fields.Int(
        dump_only=True, 
        description="Número total de items en la orden"
    )
    is_completed = fields.Bool(
        dump_only=True, 
        description="Indica si la orden está completada"
    )
    can_cancel = fields.Bool(
        dump_only=True, 
        description="Indica si la orden puede ser cancelada"
    )

class OrderCreateSchema(Schema):
    """Esquema para crear una nueva orden"""
    customer_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200), 
        description="Nombre completo del cliente (máximo 200 caracteres)",
        example="Juan Pérez"
    )
    customer_email = fields.Email(
        description="Email del cliente para notificaciones",
        example="juan.perez@email.com"
    )
    customer_phone = fields.Str(
        description="Teléfono de contacto del cliente",
        example="+34 123 456 789"
    )
    notes = fields.Str(
        description="Notas adicionales sobre la orden",
        example="Entregar en horario de mañana"
    )
    items = fields.List(
        fields.Dict(), 
        required=True, 
        description="Lista de items con product_id y quantity",
        example=[
            {"product_id": 1, "quantity": 2},
            {"product_id": 3, "quantity": 1}
        ]
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
        validate=validate.Length(min=1, max=200), 
        description="Nombre completo del cliente (máximo 200 caracteres)",
        example="Juan Pérez"
    )
    customer_email = fields.Email(
        description="Email del cliente para notificaciones",
        example="juan.perez@email.com"
    )
    customer_phone = fields.Str(
        description="Teléfono de contacto del cliente",
        example="+34 123 456 789"
    )
    status = fields.Str(
        validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
        description="Nuevo estado de la orden",
        example="completed"
    )
    notes = fields.Str(
        description="Notas adicionales sobre la orden",
        example="Entregar en horario de mañana"
    )

class OrderListSchema(Schema):
    """Esquema para respuesta de lista de órdenes"""
    orders = fields.Nested(
        OrderSchema, 
        many=True, 
        description="Lista de órdenes"
    )
    total = fields.Int(
        description="Total de órdenes en la base de datos"
    )
    pending_count = fields.Int(
        description="Cantidad de órdenes pendientes"
    )
    completed_count = fields.Int(
        description="Cantidad de órdenes completadas"
    )
    cancelled_count = fields.Int(
        description="Cantidad de órdenes canceladas"
    )

class OrderSearchSchema(Schema):
    """Esquema para búsqueda y filtrado de órdenes"""
    customer_name = fields.Str(
        description="Buscar por nombre del cliente (búsqueda parcial)",
        example="juan"
    )
    status = fields.Str(
        validate=validate.OneOf(['pending', 'completed', 'cancelled']),
        description="Filtrar por estado específico de la orden",
        example="pending"
    )
    min_total = fields.Decimal(
        places=2,
        validate=validate.Range(min=0),
        description="Total mínimo de la orden",
        example="100.00"
    )
    max_total = fields.Decimal(
        places=2,
        validate=validate.Range(min=0),
        description="Total máximo de la orden",
        example="5000.00"
    )
    date_from = fields.Date(
        description="Filtrar órdenes desde esta fecha",
        example="2024-01-01"
    )
    date_to = fields.Date(
        description="Filtrar órdenes hasta esta fecha",
        example="2024-12-31"
    )
    product_id = fields.Int(
        description="Filtrar órdenes que contengan un producto específico",
        example=1
    )

class OrderCompletionSchema(Schema):
    """Esquema para completar una orden"""
    notes = fields.Str(
        description="Notas adicionales sobre la completación",
        example="Orden entregada exitosamente"
    )
    delivery_method = fields.Str(
        validate=validate.OneOf(['pickup', 'delivery', 'shipping']),
        description="Método de entrega utilizado",
        example="delivery"
    )
    delivery_date = fields.DateTime(
        description="Fecha y hora de entrega",
        example="2024-01-15T14:30:00"
    )
