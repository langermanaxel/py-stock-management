#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Categorías
"""

from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    """Esquema completo para Categoría"""
    id = fields.Int(
        dump_only=True
    )
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        
    )
    description = fields.Str(
        
    )
    created_at = fields.DateTime(
        dump_only=True
    )
    updated_at = fields.DateTime(
        dump_only=True
    )
    
    # Campos relacionados (evitar referencias circulares)
    product_count = fields.Int(
        dump_only=True
    )

class CategoryCreateSchema(Schema):
    """Esquema para crear una nueva categoría"""
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100),
        
    )
    description = fields.Str(
        
    )

class CategoryUpdateSchema(Schema):
    """Esquema para actualizar una categoría existente"""
    name = fields.Str(
        validate=validate.Length(min=1, max=100),
        
    )
    description = fields.Str(
        
    )

class CategoryListSchema(Schema):
    """Esquema para respuesta de lista de categorías"""
    categories = fields.Nested(
        CategorySchema, 
        many=True
    )
    total = fields.Int()

class CategorySearchSchema(Schema):
    """Esquema para búsqueda de categorías"""
    name = fields.Str(
        
    )
    has_products = fields.Bool(
        
    )
