#!/usr/bin/env python3
"""
Endpoints de Categorías con flask-smorest
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.category import Category
from app.schemas.category import CategorySchema, CategoryUpdateSchema, CategoryListSchema
from flask_jwt_extended import jwt_required, get_jwt_identity

# Crear blueprint para categorías
categories_blp = Blueprint(
    "categories", 
    __name__, 
    description="Operaciones con categorías"
)

@categories_blp.route("/")
class Categories(MethodView):
    """Endpoint para listar y crear categorías"""
    
    @categories_blp.response(200, CategoryListSchema)
    @jwt_required()
    def get(self):
        """Listar todas las categorías"""
        try:
            categories = Category.query.all()
            return {
                "categories": categories,
                "total": len(categories)
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @categories_blp.arguments(CategorySchema)
    @categories_blp.response(201, CategorySchema)
    @jwt_required()
    def post(self, category_data):
        """Crear nueva categoría"""
        try:
            # Verificar si ya existe una categoría con ese nombre
            existing_category = Category.query.filter_by(
                name=category_data["name"]
            ).first()
            
            if existing_category:
                abort(400, message="Ya existe una categoría con ese nombre")
            
            category = Category(**category_data)
            db.session.add(category)
            db.session.commit()
            
            return category
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@categories_blp.route("/<int:category_id>")
class CategoryById(MethodView):
    """Endpoint para obtener, actualizar y eliminar categoría por ID"""
    
    @categories_blp.response(200, CategorySchema)
    @jwt_required()
    def get(self, category_id):
        """Obtener categoría por ID"""
        try:
            category = Category.query.get_or_404(category_id)
            return category
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @categories_blp.arguments(CategoryUpdateSchema)
    @categories_blp.response(200, CategorySchema)
    @jwt_required()
    def put(self, category_data, category_id):
        """Actualizar categoría"""
        try:
            category = Category.query.get_or_404(category_id)
            
            # Verificar si el nuevo nombre ya existe en otra categoría
            if "name" in category_data:
                existing_category = Category.query.filter(
                    Category.name == category_data["name"],
                    Category.id != category_id
                ).first()
                
                if existing_category:
                    abort(400, message="Ya existe una categoría con ese nombre")
            
            # Actualizar campos
            for field, value in category_data.items():
                setattr(category, field, value)
            
            db.session.commit()
            return category
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @categories_blp.response(204)
    @jwt_required()
    def delete(self, category_id):
        """Eliminar categoría"""
        try:
            category = Category.query.get_or_404(category_id)
            
            # Verificar si hay productos asociados
            if category.products:
                abort(400, message="No se puede eliminar una categoría que tiene productos asociados")
            
            db.session.delete(category)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

# Exportar el blueprint con el nombre esperado
categories_bp = categories_blp
