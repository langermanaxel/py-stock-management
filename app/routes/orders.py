from flask import Blueprint, request, jsonify
from ..models.order import Order
from ..models.order_item import OrderItem
from ..models.stock import Stock
from ..database import db

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
    data = request.get_json()
    items = data.get('items', [])

    if not items:
        return jsonify({'error': 'No items provided'}), 400

    order = Order(status='pending')
    db.session.add(order)
    db.session.flush()

    for item in items:
        product_id = item['product_id']
        quantity = item['quantity']
        stock = Stock.query.filter_by(product_id=product_id).first_or_404()
        
        if stock.quantity < quantity:
            return jsonify({'error': f'Insufficient stock for product ID {product_id}'}), 400

        order_item = OrderItem(
            order_id=order.id,
            product_id=product_id,
            quantity=quantity
        )
        db.session.add(order_item)

    db.session.commit()
    return jsonify(order.to_dict()), 201

@orders_bp.route('/<int:id>', methods=['PUT'])
def update_order(id):
    order = Order.query.get_or_404(id)
    data = request.get_json()
    
    if 'status' in data:
        order.status = data['status']
    
    db.session.commit()
    return jsonify(order.to_dict())

@orders_bp.route('/<int:id>', methods=['DELETE'])
def delete_order(id):
    order = Order.query.get_or_404(id)
    
    # Solo permitir eliminar órdenes pendientes
    if order.status != 'pending':
        return jsonify({'error': 'Solo se pueden eliminar órdenes pendientes'}), 400
    
    db.session.delete(order)
    db.session.commit()
    
    return jsonify({'message': 'Orden eliminada exitosamente'})

@orders_bp.route('/<int:id>/complete', methods=['PUT'])
def complete_order(id):
    order = Order.query.get_or_404(id)
    if order.status != 'pending':
        return jsonify({'error': 'Order is not pending'}), 400

    for item in order.items:
        stock = Stock.query.filter_by(product_id=item.product_id).first_or_404()
        stock.quantity -= item.quantity
        if stock.quantity < 0:
            db.session.rollback()
            return jsonify({'error': f'Insufficient stock for product ID {item.product_id}'}), 400

    order.status = 'completed'
    db.session.commit()
    return jsonify(order.to_dict())