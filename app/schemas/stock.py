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
        description="ID único del registro de stock (generado automáticamente)"
    )
    product_id = fields.Int(
        required=True, 
        description="ID del producto al que pertenece este stock",
        example=1
    )
    quantity = fields.Int(
        required=True, 
        validate=validate.Range(min=0), 
        description="Cantidad actual en stock (nunca puede ser negativa)",
        example=50
    )
    min_stock = fields.Int(
        validate=validate.Range(min=0), 
        description="Stock mínimo requerido para alertas de inventario",
        example=5
    )
    created_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de creación del registro de stock (automático)"
    )
    updated_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de última actualización del stock (automático)"
    )
    
    # Campos relacionados
    product = fields.Nested(
        'ProductSchema', 
        dump_only=True, 
        description="Información completa del producto"
    )
    
    # Campos calculados
    is_low_stock = fields.Bool(
        dump_only=True, 
        description="Indica si el stock está por debajo del mínimo requerido"
    )
    stock_status = fields.Str(
        dump_only=True, 
        description="Estado del stock: 'Disponible', 'Bajo', 'Agotado'"
    )

class StockCreateSchema(Schema):
    """Esquema para crear un nuevo registro de stock"""
    product_id = fields.Int(
        required=True, 
        description="ID del producto al que pertenece este stock",
        example=1
    )
    quantity = fields.Int(
        required=True, 
        description="Cantidad inicial en stock (mínimo 0)",
        example=50
    )
    min_stock = fields.Int(
        description="Stock mínimo requerido para alertas de inventario (mínimo 0)",
        example=5
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
        description="Nueva cantidad en stock (mínimo 0)",
        example=45
    )
    min_stock = fields.Int(
        description="Nuevo stock mínimo requerido (mínimo 0)",
        example=10
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
        description="Lista de registros de stock"
    )
    total = fields.Int(
        description="Total de registros de stock en la base de datos"
    )
    low_stock_count = fields.Int(
        description="Cantidad de productos con stock por debajo del mínimo"
    )
    out_of_stock_count = fields.Int(
        description="Cantidad de productos sin stock disponible"
    )

class StockSearchSchema(Schema):
    """Esquema para búsqueda y filtrado de stock"""
    product_name = fields.Str(
        description="Buscar por nombre del producto (búsqueda parcial)",
        example="laptop"
    )
    category_id = fields.Int(
        description="Filtrar por ID de categoría específica",
        example=1
    )
    min_quantity = fields.Int(
        validate=validate.Range(min=0),
        description="Filtrar productos con stock mínimo",
        example=10
    )
    max_quantity = fields.Int(
        validate=validate.Range(min=0),
        description="Filtrar productos con stock máximo",
        example=100
    )
    low_stock_only = fields.Bool(
        description="Mostrar solo productos con stock bajo",
        example=True
    )
    out_of_stock_only = fields.Bool(
        description="Mostrar solo productos sin stock",
        example=False
    )

class StockAdjustmentSchema(Schema):
    """Esquema para ajustes de stock (incrementos/decrementos)"""
    adjustment_type = fields.Str(
        required=True,
        validate=validate.OneOf(['increment', 'decrement']),
        description="Tipo de ajuste: incremento o decremento",
        example="increment"
    )
    quantity = fields.Int(
        required=True,
        validate=validate.Range(min=1),
        description="Cantidad a ajustar (mínimo 1)",
        example=10
    )
    reason = fields.Str(
        description="Motivo del ajuste de stock",
        example="Ajuste de inventario físico"
    )
    allow_negative = fields.Bool(
        description="Permitir stock negativo (solo para casos especiales)",
        example=False
    )
