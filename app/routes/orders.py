from flask import Blueprint, request, jsonify
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.stock import Stock
from ..database import db
from ..validators.business_rules import (
    OrderValidator, 
    TransactionManager, 
    BusinessRuleViolation
)

orders_bp = Blueprint('orders', __name__)

@orders_bp.route('/', methods=['GET'])
def get_orders():
    orders = Order.query.order_by(Order.id.asc()).all()
    return jsonify([order.to_dict() for order in orders])

@orders_bp.route('/<int:id>', methods=['GET'])
def get_order(id):
    order = Order.query.get_or_404(id)
    return jsonify(order.to_dict())

@orders_bp.route('/', methods=['POST'])
def create_order():
    try:
        data = request.get_json()
        items = data.get('items', [])

        # Validar items usando las reglas de negocio
        OrderValidator.validate_order_creation(items)

        # Crear orden
        order = Order(status='pending')
        db.session.add(order)
        db.session.flush()

        # Crear items de la orden
        for item in items:
            order_item = OrderItem(
                order_id=order.id,
                product_id=item['product_id'],
                quantity=item['quantity']
            )
            db.session.add(order_item)

        db.session.commit()
        return jsonify(order.to_dict()), 201

    except BusinessRuleViolation as e:
        db.session.rollback()
        return jsonify({
            'error': 'Violación de regla de negocio',
            'message': str(e),
            'field': e.field,
            'value': e.value
        }), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@orders_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    try:
        order = Order.query.get_or_404(id)
        data = request.get_json()
        
        if 'status' in data:
            # Validar cambio de estado
            new_status = data['status']
            if new_status not in ['pending', 'completed', 'cancelled']:
                return jsonify({'error': 'Estado inválido'}), 400
            
            order.status = new_status
        
        db.session.commit()
        return jsonify(order.to_dict())

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@orders_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    try:
        order = Order.query.get_or_404(id)
        
        # Solo permitir eliminar órdenes pendientes
        if order.status != 'pending':
            return jsonify({'error': 'Solo se pueden eliminar órdenes pendientes'}), 400
        
        db.session.delete(order)
        db.session.commit()
        
        return jsonify({'message': 'Orden eliminada exitosamente'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@orders_bp.route('/<int:id>/complete', methods=['PUT'])
def complete_order(id):
    try:
        # Usar el gestor de transacciones para completar la orden
        result = TransactionManager.execute_order_completion(id)
        return jsonify(result)

    except BusinessRuleViolation as e:
        return jsonify({
            'error': 'Violación de regla de negocio',
            'message': str(e),
            'field': e.field,
            'value': e.value
        }), 400
    except Exception as e:
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@orders_bp.route('/<int:id>/cancel', methods=['PUT'])
def cancel_order(id):
    try:
        order = Order.query.get_or_404(id)
        
        if order.status != 'pending':
            return jsonify({'error': 'Solo se pueden cancelar órdenes pendientes'}), 400
        
        order.status = 'cancelled'
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Orden {id} cancelada exitosamente',
            'order': order.to_dict()
        })

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@orders_bp.route('/<int:id>/items', methods=['GET'])
def get_order_items(id):
    order = Order.query.get_or_404(id)
    return jsonify([item.to_dict() for item in order.items])

@orders_bp.route('/<int:id>/items', methods=['POST'])
def add_item_to_order(id):
    try:
        order = Order.query.get_or_404(id)
        
        if order.status != 'pending':
            return jsonify({'error': 'Solo se pueden modificar órdenes pendientes'}), 400
        
        data = request.get_json()
        product_id = data.get('product_id')
        quantity = data.get('quantity')
        
        if not product_id or not quantity:
            return jsonify({'error': 'product_id y quantity son requeridos'}), 400
        
        # Validar que no se duplique el producto en la orden
        existing_item = OrderItem.query.filter_by(
            order_id=id, 
            product_id=product_id
        ).first()
        
        if existing_item:
            return jsonify({'error': 'El producto ya está en la orden'}), 400
        
        # Validar disponibilidad de stock
        stock = Stock.query.filter_by(product_id=product_id).first()
        if not stock or stock.quantity < quantity:
            return jsonify({'error': 'Stock insuficiente'}), 400
        
        # Agregar item
        order_item = OrderItem(
            order_id=id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(order_item)
        db.session.commit()
        
        return jsonify(order_item.to_dict()), 201

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500