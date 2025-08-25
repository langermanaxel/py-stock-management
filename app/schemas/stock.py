#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Stock
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.validators.stock_validators import validate_stock_quantity, validate_stock_min_quantity

class StockSchema(Schema):
    """Esquema completo para Stock"""
    id = fields.Int(
        dump_only=True, 
        
    )
    product_id = fields.Int(
        required=True, 
        
        
    )
    quantity = fields.Int(
        required=True, 
        validate=validate.Range(min=0), 
        
        
    )
    min_stock = fields.Int(
        validate=validate.Range(min=0), 
        
        
    )
    created_at = fields.DateTime(
        dump_only=True, 
        
    )
    updated_at = fields.DateTime(
        dump_only=True, 
        
    )
    
    # Campos relacionados
    product = fields.Nested(
        'ProductSchema', 
        dump_only=True, 
        
    )
    
    # Campos calculados
    is_low_stock = fields.Bool(
        dump_only=True, 
        
    )
    stock_status = fields.Str(
        dump_only=True, 
        
    )

class StockCreateSchema(Schema):
    """Esquema para crear un nuevo registro de stock"""
    product_id = fields.Int(
        required=True, 
        
        
    )
    quantity = fields.Int(
        required=True, 
        
        
    )
    min_stock = fields.Int(
        
        
    )
    
    @validates('quantity')
    def validate_quantity(self, value):
        return validate_stock_quantity(value)
    
    @validates('min_stock')
    def validate_min_stock(self, value):
        if value is not None:
            return validate_stock_min_quantity(value)
        return value

class StockUpdateSchema(Schema):
    """Esquema para actualizar un registro de stock existente"""
    quantity = fields.Int(
        
        
    )
    min_stock = fields.Int(
        
        
    )
    
    @validates('quantity')
    def validate_quantity(self, value):
        if value is not None:
            return validate_stock_quantity(value)
        return value
    
    @validates('min_stock')
    def validate_min_stock(self, value):
        if value is not None:
            return validate_stock_min_quantity(value)
        return value

class StockListSchema(Schema):
    """Esquema para respuesta de lista de stock"""
    stock_items = fields.Nested(
        StockSchema, 
        many=True, 
        
    )
    total = fields.Int(
        
    )
    low_stock_count = fields.Int(
        
    )
    out_of_stock_count = fields.Int(
        
    )

class StockSearchSchema(Schema):
    """Esquema para búsqueda y filtrado de stock"""
    product_name = fields.Str(
        
        
    )
    category_id = fields.Int(
        
        
    )
    min_quantity = fields.Int(
        validate=validate.Range(min=0),
        
        
    )
    max_quantity = fields.Int(
        validate=validate.Range(min=0),
        
        
    )
    low_stock_only = fields.Bool(
        
        
    )
    out_of_stock_only = fields.Bool(
        
        
    )

class StockAdjustmentSchema(Schema):
    """Esquema para ajustes de stock (incrementos/decrementos)"""
    adjustment_type = fields.Str(
        required=True,
        validate=validate.OneOf(['increment', 'decrement']),
        
        
    )
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        
        
    )
    reason = fields.Str(
        
        
    )
    allow_negative = fields.Bool(
        
        
    )
