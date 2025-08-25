#!/usr/bin/env python3
"""
Endpoints de Órdenes de Compra con flask-smorest
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from app.database import db
from app.models.purchase_order import PurchaseOrder
from app.schemas.purchase_order import PurchaseOrderSchema, PurchaseOrderCreateSchema, PurchaseOrderUpdateSchema, PurchaseOrderListSchema
from app.middleware.auth_middleware import require_auth, require_permission
from app.validators.purchase_order_validators import (
    validate_purchase_order_completion, validate_purchase_order_update,
    validate_purchase_order_deletion, update_stock_from_purchase_order,
    calculate_purchase_order_total
)
from marshmallow import ValidationError

# Crear blueprint para órdenes de compra
purchases_blp = Blueprint(
    "purchases", 
    __name__, 
    description="Operaciones con órdenes de compra"
)

@purchases_blp.route("/")
class PurchaseOrders(MethodView):
    """Endpoint para listar y crear órdenes de compra"""
    
    @purchases_blp.response(200, PurchaseOrderListSchema)
    @require_auth
    def get(self):
        """Listar todas las órdenes de compra"""
        try:
            purchase_orders = PurchaseOrder.query.all()
            pending_count = sum(1 for po in purchase_orders if po.status == 'pending')
            completed_count = sum(1 for po in purchase_orders if po.status == 'completed')
            
            return {
                "purchase_orders": purchase_orders,
                "total": len(purchase_orders),
                "pending_count": pending_count,
                "completed_count": completed_count
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @purchases_blp.arguments(PurchaseOrderCreateSchema)
    @purchases_blp.response(201, PurchaseOrderSchema)
    @require_auth
    @require_permission('write')
    def post(self, purchase_order_data):
        """Crear nueva orden de compra"""
        try:
            # Calcular total de la orden
            total = calculate_purchase_order_total(purchase_order_data["items"])
            
            # Crear la orden de compra
            purchase_order = PurchaseOrder(
                supplier_name=purchase_order_data["supplier_name"],
                total=total,
                status='pending'
            )
            db.session.add(purchase_order)
            db.session.flush()  # Para obtener el ID de la orden
            
            # Crear items de la orden de compra
            from app.models.purchase_order_item import PurchaseOrderItem
            for item_data in purchase_order_data["items"]:
                purchase_order_item = PurchaseOrderItem(
                    purchase_order_id=purchase_order.id,
                    product_id=item_data["product_id"],
                    quantity=item_data["quantity"],
                    unit_price=item_data["unit_price"]
                )
                db.session.add(purchase_order_item)
            
            db.session.commit()
            return purchase_order
        except ValidationError as e:
            db.session.rollback()
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@purchases_blp.route("/<int:purchase_order_id>")
class PurchaseOrderById(MethodView):
    """Endpoint para obtener, actualizar y eliminar orden de compra por ID"""
    
    @purchases_blp.response(200, PurchaseOrderSchema)
    @require_auth
    def get(self, purchase_order_id):
        """Obtener orden de compra por ID"""
        try:
            purchase_order = PurchaseOrder.query.get_or_404(purchase_order_id)
            return purchase_order
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @purchases_blp.arguments(PurchaseOrderUpdateSchema)
    @purchases_blp.response(200, PurchaseOrderSchema)
    @require_auth
    @require_permission('write')
    def put(self, purchase_order_data, purchase_order_id):
        """Actualizar orden de compra"""
        try:
            # Validar actualización
            if 'items' in purchase_order_data:
                validate_purchase_order_update(purchase_order_id, purchase_order_data['items'])
                
                # Actualizar items de la orden
                # Primero eliminar items existentes
                from app.models.purchase_order_item import PurchaseOrderItem
                PurchaseOrderItem.query.filter_by(purchase_order_id=purchase_order_id).delete()
                
                # Crear nuevos items
                for item_data in purchase_order_data["items"]:
                    purchase_order_item = PurchaseOrderItem(
                        purchase_order_id=purchase_order_id,
                        product_id=item_data["product_id"],
                        quantity=item_data["quantity"],
                        unit_price=item_data["unit_price"]
                    )
                    db.session.add(purchase_order_item)
                
                # Recalcular total
                purchase_order_data['total'] = calculate_purchase_order_total(purchase_order_data['items'])
            
            # Actualizar otros campos
            purchase_order = PurchaseOrder.query.get_or_404(purchase_order_id)
            for field, value in purchase_order_data.items():
                if field != 'items':  # items ya se manejaron arriba
                    setattr(purchase_order, field, value)
            
            db.session.commit()
            return purchase_order
        except ValidationError as e:
            db.session.rollback()
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @purchases_blp.response(204)
    @require_auth
    @require_permission('delete')
    def delete(self, purchase_order_id):
        """Eliminar orden de compra"""
        try:
            # Validar eliminación
            validate_purchase_order_deletion(purchase_order_id)
            
            purchase_order = PurchaseOrder.query.get_or_404(purchase_order_id)
            db.session.delete(purchase_order)
            db.session.commit()
        except ValidationError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@purchases_blp.route("/<int:purchase_order_id>/complete")
class CompletePurchaseOrder(MethodView):
    """Endpoint para completar orden de compra"""
    
    @purchases_blp.response(200, PurchaseOrderSchema)
    @require_auth
    @require_permission('write')
    def put(self, purchase_order_id):
        """Completar orden de compra"""
        try:
            # Validar que se pueda completar
            validate_purchase_order_completion(purchase_order_id)
            
            # Actualizar stock de forma transaccional
            update_stock_from_purchase_order(purchase_order_id)
            
            return PurchaseOrder.query.get(purchase_order_id)
        except ValidationError as e:
            abort(400, message=str(e))
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")

# Exportar el blueprint con el nombre esperado
purchases_bp = purchases_blp
