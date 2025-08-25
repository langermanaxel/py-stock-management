#!/usr/bin/env python3
"""
Endpoints de Órdenes con flask-smorest
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.order import Order
from app.schemas.order import OrderSchema, OrderCreateSchema, OrderUpdateSchema, OrderListSchema
from app.middleware.auth_middleware import require_auth, require_permission
from app.validators.order_validators import (
    validate_order_completion, validate_order_update, 
    validate_order_deletion, calculate_order_total
)
from marshmallow import ValidationError

# Crear blueprint para órdenes
orders_blp = Blueprint(
    "orders", 
    __name__, 
    description="Operaciones con órdenes de venta"
)

@orders_blp.route("/")
class Orders(MethodView):
    """Endpoint para listar y crear órdenes"""
    
    @orders_blp.response(200, OrderListSchema)
    @require_auth
    def get(self):
        """Listar todas las órdenes"""
        try:
            orders = Order.query.all()
            pending_count = sum(1 for order in orders if order.status == 'pending')
            completed_count = sum(1 for order in orders if order.status == 'completed')
            
            return {
                "orders": orders,
                "total": len(orders),
                "pending_count": pending_count,
                "completed_count": completed_count
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @orders_blp.arguments(OrderCreateSchema)
    @orders_blp.response(201, OrderSchema)
    @require_auth
    @require_permission('write')
    def post(self, order_data):
        """Crear nueva orden"""
        try:
            # Calcular total de la orden
            total = calculate_order_total(order_data["items"])
            
            # Crear la orden
            order = Order(
                customer_name=order_data["customer_name"],
                total=total,
                status='pending'
            )
            db.session.add(order)
            db.session.flush()  # Para obtener el ID de la orden
            
            # Crear items de la orden
            from app.models.order_item import OrderItem
            from app.models.product import Product
            for item_data in order_data["items"]:
                order_item = OrderItem(
                    order_id=order.id,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    unit_price=Product.query.get(item_data["product_id"]).price
                )
                db.session.add(order_item)
            
            db.session.commit()
            return order
        except ValidationError as e:
            db.session.rollback()
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@orders_blp.route("/<int:order_id>")
class OrderById(MethodView):
    """Endpoint para obtener, actualizar y eliminar orden por ID"""
    
    @orders_blp.response(200, OrderSchema)
    @require_auth
    def get(self, order_id):
        """Obtener orden por ID"""
        try:
            order = Order.query.get_or_404(order_id)
            return order
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @orders_blp.arguments(OrderUpdateSchema)
    @orders_blp.response(200, OrderSchema)
    @require_auth
    @require_permission('write')
    def put(self, order_data, order_id):
        """Actualizar orden"""
        try:
            # Validar actualización
            if 'items' in order_data:
                validate_order_update(order_id, order_data['items'])
                
                # Actualizar items de la orden
                # Primero eliminar items existentes
                from app.models.order_item import OrderItem
                OrderItem.query.filter_by(order_id=order_id).delete()
                
                # Crear nuevos items
                from app.models.product import Product
                for item_data in order_data["items"]:
                    order_item = OrderItem(
                        order_id=order_id,
                        product_id=item_data["product_id"],
                        quantity=item_data["quantity"],
                        unit_price=Product.query.get(item_data["product_id"]).price
                    )
                    db.session.add(order_item)
                
                # Recalcular total
                order_data['total'] = calculate_order_total(order_data['items'])
            
            # Actualizar otros campos
            order = Order.query.get_or_404(order_id)
            for field, value in order_data.items():
                if field != 'items':  # items ya se manejaron arriba
                    setattr(order, field, value)
            
            db.session.commit()
            return order
        except ValidationError as e:
            db.session.rollback()
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @orders_blp.response(204)
    @require_auth
    @require_permission('delete')
    def delete(self, order_id):
        """Eliminar orden"""
        try:
            # Validar eliminación
            validate_order_deletion(order_id)
            
            order = Order.query.get_or_404(order_id)
            db.session.delete(order)
            db.session.commit()
        except ValidationError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@orders_blp.route("/<int:order_id>/complete")
class CompleteOrder(MethodView):
    """Endpoint para completar orden"""
    
    @orders_blp.response(200, OrderSchema)
    @require_auth
    @require_permission('write')
    def put(self, order_id):
        """Completar orden"""
        try:
            # Validar que se pueda completar
            order = validate_order_completion(order_id)
            
            # Actualizar stock (descontar productos vendidos)
            from app.models.stock import Stock
            for item in order.items:
                stock = Stock.query.filter_by(product_id=item.product_id).first()
                if stock:
                    stock.quantity -= item.quantity
                    if stock.quantity < 0:
                        raise ValidationError(f"Stock insuficiente para completar la orden")
                    stock.updated_at = db.func.now()
            
            # Marcar orden como completada
            order.status = 'completed'
            order.updated_at = db.func.now()
            
            db.session.commit()
            return order
        except ValidationError as e:
            db.session.rollback()
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

# Exportar el blueprint con el nombre esperado
orders_bp = orders_blp
