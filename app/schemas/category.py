#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Categorías
"""

from marshmallow import Schema, fields, validate

class CategorySchema(Schema):
    """Esquema para Categoría"""
    id = fields.Int(dump_only=True, description="ID único de la categoría")
    name = fields.Str(required=True, validate=validate.Length(min=1, max=100), 
                      description="Nombre de la categoría")
    description = fields.Str(description="Descripción de la categoría")
    created_at = fields.DateTime(dump_only=True, description="Fecha de creación")
    updated_at = fields.DateTime(dump_only=True, description="Fecha de última actualización")

class CategoryUpdateSchema(Schema):
    """Esquema para actualizar categoría"""
    name = fields.Str(validate=validate.Length(min=1, max=100), 
                      description="Nombre de la categoría")
    description = fields.Str(description="Descripción de la categoría")

class CategoryListSchema(Schema):
    """Esquema para lista de categorías"""
    categories = fields.Nested(CategorySchema, many=True, description="Lista de categorías")
    total = fields.Int(description="Total de categorías")
