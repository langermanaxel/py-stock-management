from flask import Blueprint, request, jsonify
from ..models.purchase_order import PurchaseOrder, PurchaseOrderItem
from ..models.stock import Stock
from ..database import db

purchases_bp = Blueprint('purchases', __name__)

@purchases_bp.route('/', methods=['GET'])
def get_purchases():
    purchases = PurchaseOrder.query.order_by(PurchaseOrder.id.asc()).all()
    return jsonify([purchase.to_dict() for purchase in purchases])

@purchases_bp.route('/<int:id>', methods=['GET'])
def get_purchase(id):
    purchase = PurchaseOrder.query.get_or_404(id)
    return jsonify(purchase.to_dict())

@purchases_bp.route('/', methods=['POST'])
def create_purchase_order():
    data = request.get_json()
    
    # Crear la orden de compra
    purchase = PurchaseOrder(status='pending')
    db.session.add(purchase)
    db.session.flush()  # Para obtener el ID de la orden
    
    # Agregar los items de la orden
    for item_data in data['items']:
        item = PurchaseOrderItem(
            purchase_order_id=purchase.id,
            product_id=item_data['product_id'],
            quantity=item_data['quantity']
        )
        db.session.add(item)
    
    db.session.commit()
    return jsonify(purchase.to_dict()), 201

@purchases_bp.route('/<int:id>', methods=['PUT'])
def update_purchase_order(id):
    purchase = PurchaseOrder.query.get_or_404(id)
    data = request.get_json()
    
    if 'status' in data:
        purchase.status = data['status']
    
    db.session.commit()
    return jsonify(purchase.to_dict())

@purchases_bp.route('/<int:id>', methods=['DELETE'])
def delete_purchase_order(id):
    purchase = PurchaseOrder.query.get_or_404(id)
    
    # Solo permitir eliminar órdenes pendientes
    if purchase.status != 'pending':
        return jsonify({'error': 'Solo se pueden eliminar órdenes de compra pendientes'}), 400
    
    db.session.delete(purchase)
    db.session.commit()
    
    return jsonify({'message': 'Orden de compra eliminada exitosamente'})

@purchases_bp.route('/<int:id>/complete', methods=['PUT'])
def complete_purchase_order(id):
    purchase = PurchaseOrder.query.get_or_404(id)
    if purchase.status != 'pending':
        return jsonify({'error':'Order is not pending'}), 400
    
    purchase.status = 'completed'

    # Actualizar el stock para todos los items de la orden
    for item in purchase.items:
        stock = Stock.query.filter_by(product_id=item.product_id).first()
        if stock:
            stock.quantity += item.quantity
    
    db.session.commit()
    return jsonify(purchase.to_dict())