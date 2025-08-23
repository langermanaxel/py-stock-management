#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Categorías
"""

from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    """Esquema completo para Categoría"""
    id = fields.Int(
        dump_only=True, 
        description="ID único de la categoría (generado automáticamente)"
    )
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100), 
        description="Nombre de la categoría (máximo 100 caracteres)",
        example="Electrónicos"
    )
    description = fields.Str(
        description="Descripción detallada de la categoría",
        example="Productos electrónicos y tecnológicos"
    )
    created_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de creación de la categoría (automático)"
    )
    updated_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de última actualización (automático)"
    )
    
    # Campos relacionados
    products = fields.Nested(
        'ProductSchema', 
        many=True, 
        dump_only=True, 
        description="Lista de productos en esta categoría"
    )
    product_count = fields.Int(
        dump_only=True, 
        description="Número total de productos en esta categoría"
    )

class CategoryCreateSchema(Schema):
    """Esquema para crear una nueva categoría"""
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=100), 
        description="Nombre de la categoría (máximo 100 caracteres)",
        example="Electrónicos"
    )
    description = fields.Str(
        description="Descripción detallada de la categoría",
        example="Productos electrónicos y tecnológicos"
    )

class CategoryUpdateSchema(Schema):
    """Esquema para actualizar una categoría existente"""
    name = fields.Str(
        validate=validate.Length(min=1, max=100), 
        description="Nombre de la categoría (máximo 100 caracteres)",
        example="Electrónicos"
    )
    description = fields.Str(
        description="Descripción detallada de la categoría",
        example="Productos electrónicos y tecnológicos"
    )

class CategoryListSchema(Schema):
    """Esquema para respuesta de lista de categorías"""
    categories = fields.Nested(
        CategorySchema, 
        many=True, 
        description="Lista de categorías"
    )
    total = fields.Int(
        description="Total de categorías en la base de datos"
    )

class CategorySearchSchema(Schema):
    """Esquema para búsqueda de categorías"""
    name = fields.Str(
        description="Buscar categorías por nombre (búsqueda parcial)",
        example="electr"
    )
    has_products = fields.Bool(
        description="Filtrar solo categorías que tienen productos",
        example=True
    )
