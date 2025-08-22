#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Órdenes de Compra
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.validators.purchase_order_validators import validate_purchase_order_items

class PurchaseOrderItemSchema(Schema):
    """Esquema para Item de Orden de Compra"""
    id = fields.Int(dump_only=True, description="ID único del item")
    purchase_order_id = fields.Int(required=True, description="ID de la orden de compra")
    product_id = fields.Int(required=True, description="ID del producto")
    quantity = fields.Int(required=True, validate=validate.Range(min=1), 
                         description="Cantidad del producto")
    unit_price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                               description="Precio unitario")
    subtotal = fields.Decimal(dump_only=True, places=2, description="Subtotal del item")
    
    # Campos relacionados
    product = fields.Nested('ProductSchema', dump_only=True, description="Producto")

class PurchaseOrderSchema(Schema):
    """Esquema para Orden de Compra"""
    id = fields.Int(dump_only=True, description="ID único de la orden de compra")
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                              description="Nombre del proveedor")
    total = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                          description="Total de la orden")
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
                       description="Estado de la orden")
    created_at = fields.DateTime(dump_only=True, description="Fecha de creación")
    updated_at = fields.DateTime(dump_only=True, description="Fecha de última actualización")
    
    # Campos relacionados
    items = fields.Nested(PurchaseOrderItemSchema, many=True, description="Items de la orden")
    created_by = fields.Nested('UserSchema', dump_only=True, description="Usuario que creó la orden")

class PurchaseOrderCreateSchema(Schema):
    """Esquema para crear orden de compra"""
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                              description="Nombre del proveedor")
    items = fields.List(fields.Dict(), required=True, 
                       description="Lista de items con product_id, quantity y unit_price")
    
    @validates('items')
    def validate_items(self, value):
        return validate_purchase_order_items(value)

class PurchaseOrderUpdateSchema(Schema):
    """Esquema para actualizar orden de compra"""
    supplier_name = fields.Str(validate=validate.Length(min=1, max=200), 
                              description="Nombre del proveedor")
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
                       description="Estado de la orden")

class PurchaseOrderListSchema(Schema):
    """Esquema para lista de órdenes de compra"""
    purchase_orders = fields.Nested(PurchaseOrderSchema, many=True, 
                                  description="Lista de órdenes de compra")
    total = fields.Int(description="Total de órdenes de compra")
    pending_count = fields.Int(description="Cantidad de órdenes pendientes")
    completed_count = fields.Int(description="Cantidad de órdenes completadas")
