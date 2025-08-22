#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Stock
"""

from marshmallow import Schema, fields, validate, validates, ValidationError
from app.validators.stock_validators import validate_stock_quantity, validate_stock_min_quantity

class StockSchema(Schema):
    """Esquema para Stock"""
    id = fields.Int(dump_only=True, description="ID único del registro de stock")
    product_id = fields.Int(required=True, description="ID del producto")
    quantity = fields.Int(required=True, validate=validate.Range(min=0), 
                         description="Cantidad en stock")
    min_stock = fields.Int(validate=validate.Range(min=0), 
                          description="Stock mínimo requerido")
    created_at = fields.DateTime(dump_only=True, description="Fecha de creación")
    updated_at = fields.DateTime(dump_only=True, description="Fecha de última actualización")
    
    # Campos relacionados
    product = fields.Nested('ProductSchema', dump_only=True, description="Producto")

class StockCreateSchema(Schema):
    """Esquema para crear stock"""
    product_id = fields.Int(required=True, description="ID del producto")
    quantity = fields.Int(required=True, description="Cantidad en stock")
    min_stock = fields.Int(description="Stock mínimo requerido")
    
    @validates('quantity')
    def validate_quantity(self, value):
        return validate_stock_quantity(value)
    
    @validates('min_stock')
    def validate_min_stock(self, value):
        if value is not None:
            return validate_stock_min_quantity(value)
        return value

class StockUpdateSchema(Schema):
    """Esquema para actualizar stock"""
    quantity = fields.Int(description="Cantidad en stock")
    min_stock = fields.Int(description="Stock mínimo requerido")
    
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
    """Esquema para lista de stock"""
    stock_items = fields.Nested(StockSchema, many=True, description="Lista de items de stock")
    total = fields.Int(description="Total de items de stock")
    low_stock_count = fields.Int(description="Cantidad de productos con stock bajo")
