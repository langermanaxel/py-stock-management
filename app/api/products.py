#!/usr/bin/env python3
"""
Endpoints de Productos con flask-smorest
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.product import Product
from app.schemas.product import (
    ProductSchema, ProductCreateSchema, ProductUpdateSchema, 
    ProductListSchema, ProductSearchSchema
)
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import usuario_or_above_required, gerente_or_admin_required, admin_required

# Crear blueprint para productos
products_blp = Blueprint(
    "products", 
    __name__, 
    description="Operaciones con productos del inventario"
)

@products_blp.route("/")
class Products(MethodView):
    """Endpoint para listar y crear productos"""
    
    @products_blp.response(200, ProductListSchema)
    @products_blp.doc(
        summary="Listar productos",
        description="Obtiene una lista paginada de todos los productos en el sistema",
        responses={
            200: {
                "description": "Lista de productos obtenida exitosamente",
                "example": {
                    "products": [
                        {
                            "id": 1,
                            "name": "Laptop Dell XPS 13",
                            "description": "Laptop ultrabook de 13 pulgadas",
                            "price": "1299.99",
                            "category_id": 1,
                            "min_stock": 5,
                            "created_at": "2024-01-15T10:00:00",
                            "updated_at": "2024-01-15T10:00:00"
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "per_page": 1
                }
            },
            401: {"description": "No autorizado - Token JWT requerido"},
            500: {"description": "Error interno del servidor"}
        }
    )
    @jwt_required()
    @usuario_or_above_required
    def get(self):
        """Listar todos los productos"""
        try:
            products = Product.query.all()
            return {
                "products": products,
                "total": len(products),
                "page": 1,
                "per_page": len(products)
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @products_blp.arguments(ProductCreateSchema)
    @products_blp.response(201, ProductSchema)
    @products_blp.doc(
        summary="Crear producto",
        description="Crea un nuevo producto en el sistema. El nombre debe ser único.",
        responses={
            201: {
                "description": "Producto creado exitosamente",
                "example": {
                    "id": 1,
                    "name": "Laptop Dell XPS 13",
                    "description": "Laptop ultrabook de 13 pulgadas",
                    "price": "1299.99",
                    "category_id": 1,
                    "min_stock": 5,
                    "created_at": "2024-01-15T10:00:00",
                    "updated_at": "2024-01-15T10:00:00"
                }
            },
            400: {
                "description": "Error de validación o producto duplicado",
                "example": {
                    "message": "Ya existe un producto con ese nombre"
                }
            },
            401: {"description": "No autorizado - Token JWT requerido"},
            403: {"description": "Prohibido - Permisos insuficientes"},
            500: {"description": "Error interno del servidor"}
        }
    )
    @jwt_required()
    @gerente_or_admin_required
    def post(self, product_data):
        """Crear nuevo producto"""
        try:
            # Verificar si ya existe un producto con ese nombre
            existing_product = Product.query.filter_by(
                name=product_data["name"]
            ).first()
            
            if existing_product:
                abort(400, message="Ya existe un producto con ese nombre")
            
            product = Product(**product_data)
            db.session.add(product)
            db.session.commit()
            
            return product
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@products_blp.route("/<int:product_id>")
class ProductById(MethodView):
    """Endpoint para obtener, actualizar y eliminar producto por ID"""
    
    @products_blp.response(200, ProductSchema)
    @products_blp.doc(
        summary="Obtener producto",
        description="Obtiene la información completa de un producto específico por su ID",
        parameters=[
            {
                "name": "product_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "description": "ID único del producto"
            }
        ],
        responses={
            200: {
                "description": "Producto obtenido exitosamente",
                "example": {
                    "id": 1,
                    "name": "Laptop Dell XPS 13",
                    "description": "Laptop ultrabook de 13 pulgadas",
                    "price": "1299.99",
                    "category_id": 1,
                    "min_stock": 5,
                    "created_at": "2024-01-15T10:00:00",
                    "updated_at": "2024-01-15T10:00:00"
                }
            },
            401: {"description": "No autorizado - Token JWT requerido"},
            404: {"description": "Producto no encontrado"},
            500: {"description": "Error interno del servidor"}
        }
    )
    @jwt_required()
    @usuario_or_above_required
    def get(self, product_id):
        """Obtener producto por ID"""
        try:
            product = Product.query.get_or_404(product_id)
            return product
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @products_blp.arguments(ProductUpdateSchema)
    @products_blp.response(200, ProductSchema)
    @products_blp.doc(
        summary="Actualizar producto",
        description="Actualiza la información de un producto existente. Solo se pueden modificar los campos proporcionados.",
        parameters=[
            {
                "name": "product_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "description": "ID único del producto a actualizar"
            }
        ],
        responses={
            200: {
                "description": "Producto actualizado exitosamente",
                "example": {
                    "id": 1,
                    "name": "Laptop Dell XPS 13 Pro",
                    "description": "Laptop ultrabook de 13 pulgadas con procesador Intel i7",
                    "price": "1499.99",
                    "category_id": 1,
                    "min_stock": 10,
                    "created_at": "2024-01-15T10:00:00",
                    "updated_at": "2024-01-15T11:30:00"
                }
            },
            400: {
                "description": "Error de validación o producto duplicado",
                "example": {
                    "message": "Ya existe un producto con ese nombre"
                }
            },
            401: {"description": "No autorizado - Token JWT requerido"},
            403: {"description": "Prohibido - Permisos insuficientes"},
            404: {"description": "Producto no encontrado"},
            500: {"description": "Error interno del servidor"}
        }
    )
    @jwt_required()
    @gerente_or_admin_required
    def put(self, product_data, product_id):
        """Actualizar producto"""
        try:
            product = Product.query.get_or_404(product_id)
            
            # Verificar si el nuevo nombre ya existe en otro producto
            if "name" in product_data:
                existing_product = Product.query.filter(
                    Product.name == product_data["name"],
                    Product.id != product_id
                ).first()
                
                if existing_product:
                    abort(400, message="Ya existe un producto con ese nombre")
            
            # Actualizar campos
            for field, value in product_data.items():
                setattr(product, field, value)
            
            db.session.commit()
            return product
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @products_blp.response(204)
    @products_blp.doc(
        summary="Eliminar producto",
        description="Elimina un producto del sistema. Solo se puede eliminar si no tiene stock asociado.",
        parameters=[
            {
                "name": "product_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "description": "ID único del producto a eliminar"
            }
        ],
        responses={
            204: {"description": "Producto eliminado exitosamente"},
            400: {
                "description": "No se puede eliminar el producto",
                "example": {
                    "message": "No se puede eliminar un producto que tiene stock asociado"
                }
            },
            401: {"description": "No autorizado - Token JWT requerido"},
            403: {"description": "Prohibido - Permisos insuficientes"},
            404: {"description": "Producto no encontrado"},
            500: {"description": "Error interno del servidor"}
        }
    )
    @jwt_required()
    @admin_required
    def delete(self, product_id):
        """Eliminar producto"""
        try:
            product = Product.query.get_or_404(product_id)
            
            # Verificar si hay stock asociado
            if hasattr(product, 'stock') and product.stock:
                abort(400, message="No se puede eliminar un producto que tiene stock asociado")
            
            db.session.delete(product)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@products_blp.route("/search")
class ProductSearch(MethodView):
    """Endpoint para búsqueda y filtrado de productos"""
    
    @products_blp.arguments(ProductSearchSchema, location="query")
    @products_blp.response(200, ProductListSchema)
    @products_blp.doc(
        summary="Buscar productos",
        description="Busca y filtra productos según criterios específicos",
        responses={
            200: {
                "description": "Productos encontrados según los criterios de búsqueda",
                "example": {
                    "products": [
                        {
                            "id": 1,
                            "name": "Laptop Dell XPS 13",
                            "description": "Laptop ultrabook de 13 pulgadas",
                            "price": "1299.99",
                            "category_id": 1,
                            "min_stock": 5,
                            "created_at": "2024-01-15T10:00:00",
                            "updated_at": "2024-01-15T10:00:00"
                        }
                    ],
                    "total": 1,
                    "page": 1,
                    "per_page": 1
                }
            },
            401: {"description": "No autorizado - Token JWT requerido"},
            500: {"description": "Error interno del servidor"}
        }
    )
    @jwt_required()
    @usuario_or_above_required
    def get(self, search_params):
        """Buscar productos según criterios"""
        try:
            query = Product.query
            
            # Aplicar filtros de búsqueda
            if search_params.get('name'):
                query = query.filter(Product.name.ilike(f"%{search_params['name']}%"))
            
            if search_params.get('category_id'):
                query = query.filter(Product.category_id == search_params['category_id'])
            
            if search_params.get('min_price'):
                query = query.filter(Product.price >= search_params['min_price'])
            
            if search_params.get('max_price'):
                query = query.filter(Product.price <= search_params['max_price'])
            
            if search_params.get('in_stock'):
                # Filtrar solo productos con stock disponible
                query = query.join(Product.stock).filter(Product.stock.quantity > 0)
            
            products = query.all()
            
            return {
                "products": products,
                "total": len(products),
                "page": 1,
                "per_page": len(products)
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")

@products_blp.route("/<int:product_id>/stock")
class ProductStock(MethodView):
    """Endpoint para obtener información de stock de un producto específico"""
    
    @products_blp.response(200, ProductSchema)
    @products_blp.doc(
        summary="Obtener stock del producto",
        description="Obtiene la información completa de un producto incluyendo su stock actual",
        parameters=[
            {
                "name": "product_id",
                "in": "path",
                "required": True,
                "schema": {"type": "integer"},
                "description": "ID único del producto"
            }
        ],
        responses={
            200: {
                "description": "Producto con información de stock obtenido exitosamente"
            },
            401: {"description": "No autorizado - Token JWT requerido"},
            404: {"description": "Producto no encontrado"},
            500: {"description": "Error interno del servidor"}
        }
    )
    @jwt_required()
    @usuario_or_above_required
    def get(self, product_id):
        """Obtener producto con información de stock"""
        try:
            product = Product.query.get_or_404(product_id)
            return product
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")

# Exportar el blueprint con el nombre esperado
products_bp = products_blp
