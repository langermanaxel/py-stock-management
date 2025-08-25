#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Órdenes de Compra
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.validators.purchase_order_validators import validate_purchase_order_items

class PurchaseOrderItemSchema(Schema):
    """Esquema para Item de Orden de Compra"""
    id = fields.Int(dump_only=True, )
    purchase_order_id = fields.Int(required=True, )
    product_id = fields.Int(required=True, )
    quantity = fields.Int(required=True, validate=validate.Range(min=1), 
                         )
    unit_price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                               )
    subtotal = fields.Decimal(dump_only=True, places=2, )
    
    # Campos relacionados
    product = fields.Nested('ProductSchema', dump_only=True, )

class PurchaseOrderSchema(Schema):
    """Esquema para Orden de Compra"""
    id = fields.Int(dump_only=True, )
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                              )
    total = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                          )
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
                       )
    created_at = fields.DateTime(dump_only=True, )
    updated_at = fields.DateTime(dump_only=True, )
    
    # Campos relacionados
    items = fields.Nested(PurchaseOrderItemSchema, many=True, )
    created_by = fields.Nested('UserSchema', dump_only=True, )

class PurchaseOrderCreateSchema(Schema):
    """Esquema para crear orden de compra"""
    supplier_name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                              )
    items = fields.List(fields.Dict(), required=True, 
                       )
    
    @validates('items')
    def validate_items(self, value):
        return validate_purchase_order_items(value)

class PurchaseOrderUpdateSchema(Schema):
    """Esquema para actualizar orden de compra"""
    supplier_name = fields.Str(validate=validate.Length(min=1, max=200), 
                              )
    status = fields.Str(validate=validate.OneOf(['pending', 'completed', 'cancelled']), 
                       )

class PurchaseOrderListSchema(Schema):
    """Esquema para lista de órdenes de compra"""
    purchase_orders = fields.Nested(PurchaseOrderSchema, many=True, 
                                  )
    total = fields.Int()
    pending_count = fields.Int()
    completed_count = fields.Int()
