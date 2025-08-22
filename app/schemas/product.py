#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Productos
"""

from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    """Esquema para Producto"""
    id = fields.Int(dump_only=True, description="ID único del producto")
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                      description="Nombre del producto")
    description = fields.Str(description="Descripción del producto")
    price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                          description="Precio del producto")
    category_id = fields.Int(required=True, description="ID de la categoría")
    min_stock = fields.Int(validate=validate.Range(min=0), 
                          description="Stock mínimo requerido")
    created_at = fields.DateTime(dump_only=True, description="Fecha de creación")
    updated_at = fields.DateTime(dump_only=True, description="Fecha de última actualización")
    
    # Campos relacionados
    category = fields.Nested('CategorySchema', dump_only=True, description="Categoría del producto")
    stock = fields.Nested('StockSchema', dump_only=True, description="Información de stock")

class ProductCreateSchema(Schema):
    """Esquema para crear producto"""
    name = fields.Str(required=True, validate=validate.Length(min=1, max=200), 
                      description="Nombre del producto")
    description = fields.Str(description="Descripción del producto")
    price = fields.Decimal(required=True, places=2, validate=validate.Range(min=0), 
                          description="Precio del producto")
    category_id = fields.Int(required=True, description="ID de la categoría")
    min_stock = fields.Int(validate=validate.Range(min=0), 
                          description="Stock mínimo requerido")

class ProductUpdateSchema(Schema):
    """Esquema para actualizar producto"""
    name = fields.Str(validate=validate.Length(min=1, max=200), 
                      description="Nombre del producto")
    description = fields.Str(description="Descripción del producto")
    price = fields.Decimal(places=2, validate=validate.Range(min=0), 
                          description="Precio del producto")
    category_id = fields.Int(description="ID de la categoría")
    min_stock = fields.Int(validate=validate.Range(min=0), 
                          description="Stock mínimo requerido")

class ProductListSchema(Schema):
    """Esquema para lista de productos"""
    products = fields.Nested(ProductSchema, many=True, description="Lista de productos")
    total = fields.Int(description="Total de productos")
    page = fields.Int(description="Página actual")
    per_page = fields.Int(description="Productos por página")
