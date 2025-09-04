#!/usr/bin/env python3
"""
Endpoints de Stock con flask-smorest
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.stock import Stock
from app.schemas.stock import StockSchema, StockCreateSchema, StockUpdateSchema, StockListSchema
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.decorators import user_or_above_required, manager_or_admin_required, admin_required
from app.validators.stock_validators import validate_stock_creation, validate_stock_update

# Crear blueprint para stock
stock_blp = Blueprint(
    "stock", 
    __name__, 
    description="Operaciones con stock"
)

@stock_blp.route("/")
class StockItems(MethodView):
    """Endpoint para listar y crear items de stock"""
    
    @stock_blp.response(200, StockListSchema)
    @jwt_required()
    @user_or_above_required
    def get(self):
        """Listar todo el stock"""
        try:
            stock_items = Stock.query.all()
            low_stock_count = sum(1 for item in stock_items if item.quantity <= item.min_stock)
            
            return {
                "stock_items": stock_items,
                "total": len(stock_items),
                "low_stock_count": low_stock_count
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @stock_blp.arguments(StockCreateSchema)
    @stock_blp.response(201, StockSchema)
    @jwt_required()
    @manager_or_admin_required
    def post(self, stock_data):
        """Crear nuevo item de stock"""
        try:
            # Validar datos antes de crear
            validate_stock_creation(
                stock_data["product_id"],
                stock_data["quantity"],
                stock_data.get("min_stock", 0)
            )
            
            stock = Stock(**stock_data)
            db.session.add(stock)
            db.session.commit()
            
            return stock
        except ValidationError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@stock_blp.route("/<int:stock_id>")
class StockById(MethodView):
    """Endpoint para obtener, actualizar y eliminar stock por ID"""
    
    @stock_blp.response(200, StockSchema)
    @jwt_required()
    @user_or_above_required
    def get(self, stock_id):
        """Obtener stock por ID"""
        try:
            stock = Stock.query.get_or_404(stock_id)
            return stock
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @stock_blp.arguments(StockUpdateSchema)
    @stock_blp.response(200, StockSchema)
    @jwt_required()
    @manager_or_admin_required
    def put(self, stock_data, stock_id):
        """Actualizar stock"""
        try:
            stock = Stock.query.get_or_404(stock_id)
            
            # Validar actualización
            if 'quantity' in stock_data:
                stock_data['quantity'] = validate_stock_update(stock_id, stock_data['quantity'])
            
            # Actualizar campos
            for field, value in stock_data.items():
                setattr(stock, field, value)
            
            db.session.commit()
            return stock
        except ValidationError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @stock_blp.response(204)
    @jwt_required()
    @admin_required
    def delete(self, stock_id):
        """Eliminar stock"""
        try:
            stock = Stock.query.get_or_404(stock_id)
            db.session.delete(stock)
            db.session.commit()
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

# Exportar el blueprint con el nombre esperado
stock_bp = stock_blp
