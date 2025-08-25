#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Productos
"""

from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    """Esquema completo para Producto"""
    id = fields.Int(
        dump_only=True, 
        
    )
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200), 
        
        
    )
    description = fields.Str(
        
        
    )
    price = fields.Decimal(
        required=True, 
        places=2, 
        validate=validate.Range(min=0), 
        
        
    )
    category_id = fields.Int(
        required=True, 
        
        
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
    
    # Campos relacionados (evitar referencias circulares)
    category_name = fields.Str(
        dump_only=True,
        attribute='category.name'
    )

class ProductCreateSchema(Schema):
    """Esquema para crear un nuevo producto"""
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200), 
        
        
    )
    description = fields.Str(
        
        
    )
    price = fields.Decimal(
        required=True, 
        places=2, 
        validate=validate.Range(min=0), 
        
        
    )
    category_id = fields.Int(
        required=True, 
        
        
    )
    min_stock = fields.Int(
        validate=validate.Range(min=0), 
        
        
    )

class ProductUpdateSchema(Schema):
    """Esquema para actualizar un producto existente"""
    name = fields.Str(
        validate=validate.Length(min=1, max=200), 
        
        
    )
    description = fields.Str(
        
        
    )
    price = fields.Decimal(
        places=2, 
        validate=validate.Range(min=0), 
        
        
    )
    category_id = fields.Int(
        
        
    )
    min_stock = fields.Int(
        validate=validate.Range(min=0), 
        
        
    )

class ProductListSchema(Schema):
    """Esquema para respuesta de lista de productos"""
    products = fields.Nested(
        ProductSchema, 
        many=True, 
        
    )
    total = fields.Int(
        
    )
    page = fields.Int(
        
    )
    per_page = fields.Int(
        
    )

class ProductSearchSchema(Schema):
    """Esquema para búsqueda de productos"""
    name = fields.Str(
        
        
    )
    category_id = fields.Int(
        
        
    )
    min_price = fields.Decimal(
        places=2,
        validate=validate.Range(min=0),
        
        
    )
    max_price = fields.Decimal(
        places=2,
        validate=validate.Range(min=0),
        
        
    )
    in_stock = fields.Bool(
        
        
    )
