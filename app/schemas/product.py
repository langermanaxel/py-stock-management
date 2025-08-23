#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Productos
"""

from marshmallow import Schema, fields, validate

class ProductSchema(Schema):
    """Esquema completo para Producto"""
    id = fields.Int(
        dump_only=True, 
        description="ID único del producto (generado automáticamente)"
    )
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200), 
        description="Nombre del producto (máximo 200 caracteres)",
        example="Laptop Dell XPS 13"
    )
    description = fields.Str(
        description="Descripción detallada del producto",
        example="Laptop ultrabook de 13 pulgadas con procesador Intel i7"
    )
    price = fields.Decimal(
        required=True, 
        places=2, 
        validate=validate.Range(min=0), 
        description="Precio del producto en la moneda local (mínimo 0)",
        example="1299.99"
    )
    category_id = fields.Int(
        required=True, 
        description="ID de la categoría a la que pertenece el producto",
        example=1
    )
    min_stock = fields.Int(
        validate=validate.Range(min=0), 
        description="Stock mínimo requerido para alertas de inventario (mínimo 0)",
        example=5
    )
    created_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de creación del producto (automático)"
    )
    updated_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de última actualización (automático)"
    )
    
    # Campos relacionados
    category = fields.Nested(
        'CategorySchema', 
        dump_only=True, 
        description="Información completa de la categoría del producto"
    )
    stock = fields.Nested(
        'StockSchema', 
        dump_only=True, 
        description="Información actual del stock del producto"
    )

class ProductCreateSchema(Schema):
    """Esquema para crear un nuevo producto"""
    name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=200), 
        description="Nombre del producto (máximo 200 caracteres)",
        example="Laptop Dell XPS 13"
    )
    description = fields.Str(
        description="Descripción detallada del producto",
        example="Laptop ultrabook de 13 pulgadas con procesador Intel i7"
    )
    price = fields.Decimal(
        required=True, 
        places=2, 
        validate=validate.Range(min=0), 
        description="Precio del producto en la moneda local (mínimo 0)",
        example="1299.99"
    )
    category_id = fields.Int(
        required=True, 
        description="ID de la categoría a la que pertenece el producto",
        example=1
    )
    min_stock = fields.Int(
        validate=validate.Range(min=0), 
        description="Stock mínimo requerido para alertas de inventario (mínimo 0)",
        example=5
    )

class ProductUpdateSchema(Schema):
    """Esquema para actualizar un producto existente"""
    name = fields.Str(
        validate=validate.Length(min=1, max=200), 
        description="Nombre del producto (máximo 200 caracteres)",
        example="Laptop Dell XPS 13"
    )
    description = fields.Str(
        description="Descripción detallada del producto",
        example="Laptop ultrabook de 13 pulgadas con procesador Intel i7"
    )
    price = fields.Decimal(
        places=2, 
        validate=validate.Range(min=0), 
        description="Precio del producto en la moneda local (mínimo 0)",
        example="1299.99"
    )
    category_id = fields.Int(
        description="ID de la categoría a la que pertenece el producto",
        example=1
    )
    min_stock = fields.Int(
        validate=validate.Range(min=0), 
        description="Stock mínimo requerido para alertas de inventario (mínimo 0)",
        example=5
    )

class ProductListSchema(Schema):
    """Esquema para respuesta de lista de productos"""
    products = fields.Nested(
        ProductSchema, 
        many=True, 
        description="Lista de productos"
    )
    total = fields.Int(
        description="Total de productos en la base de datos"
    )
    page = fields.Int(
        description="Número de página actual"
    )
    per_page = fields.Int(
        description="Número de productos por página"
    )

class ProductSearchSchema(Schema):
    """Esquema para búsqueda de productos"""
    name = fields.Str(
        description="Buscar productos por nombre (búsqueda parcial)",
        example="laptop"
    )
    category_id = fields.Int(
        description="Filtrar por ID de categoría específica",
        example=1
    )
    min_price = fields.Decimal(
        places=2,
        validate=validate.Range(min=0),
        description="Precio mínimo para filtrar productos",
        example="100.00"
    )
    max_price = fields.Decimal(
        places=2,
        validate=validate.Range(min=0),
        description="Precio máximo para filtrar productos",
        example="2000.00"
    )
    in_stock = fields.Bool(
        description="Filtrar solo productos con stock disponible",
        example=True
    )
