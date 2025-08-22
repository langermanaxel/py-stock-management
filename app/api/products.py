#!/usr/bin/env python3
"""
Endpoints de Productos con flask-smorest
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.product import Product
from app.schemas.product import ProductSchema, ProductCreateSchema, ProductUpdateSchema, ProductListSchema
from app.middleware.auth_middleware import require_auth, require_permission

# Crear blueprint para productos
products_blp = Blueprint(
    "products", 
    __name__, 
    description="Operaciones con productos"
)

@products_blp.route("/")
class Products(MethodView):
    """Endpoint para listar y crear productos"""
    
    @products_blp.response(200, ProductListSchema)
    @require_auth
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
    @require_auth
    @require_permission('write')
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
    @require_auth
    def get(self, product_id):
        """Obtener producto por ID"""
        try:
            product = Product.query.get_or_404(product_id)
            return product
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @products_blp.arguments(ProductUpdateSchema)
    @products_blp.response(200, ProductSchema)
    @require_auth
    @require_permission('write')
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
    @require_auth
    @require_permission('delete')
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
