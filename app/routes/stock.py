from flask import Blueprint, request, jsonify
from ..models.stock import Stock
from ..models.product import Product
from ..database import db
from ..validators.business_rules import (
    StockValidator, 
    TransactionManager, 
    BusinessRuleViolation
)

stock_bp = Blueprint('stock', __name__)

@stock_bp.route('/', methods=['GET'])
def get_all_stock():
    stock_items = Stock.query.order_by(Stock.id.asc()).all()
    return jsonify([stock.to_dict() for stock in stock_items])

@stock_bp.route('/<int:product_id>', methods=['GET'])
def get_stock(product_id):
    stock = Stock.query.filter_by(product_id=product_id).first_or_404()
    return jsonify(stock.to_dict())

@stock_bp.route('/<int:product_id>', methods=['PUT'])
def update_stock(product_id):
    try:
        data = request.get_json()
        new_quantity = data.get('quantity')
        new_min_stock = data.get('min_stock')
        
        if new_quantity is None and new_min_stock is None:
            return jsonify({'error': 'Debe proporcionar al menos quantity o min_stock'}), 400
        
        # Usar el gestor de transacciones para actualizar stock
        result = TransactionManager.execute_stock_update(
            product_id=product_id,
            new_quantity=new_quantity if new_quantity is not None else 0,
            new_min_stock=new_min_stock
        )
        
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

@stock_bp.route('/<int:product_id>', methods=['POST'])
def create_stock(product_id):
    try:
        # Verificar que el producto existe
        product = Product.query.get(product_id)
        if not product:
            return jsonify({'error': f'Producto {product_id} no existe'}), 404
        
        # Verificar que no existe stock para este producto
        existing_stock = Stock.query.filter_by(product_id=product_id).first()
        if existing_stock:
            return jsonify({'error': f'Ya existe stock para el producto {product_id}'}), 400
        
        data = request.get_json()
        quantity = data.get('quantity', 0)
        min_stock = data.get('min_stock', 0)
        
        # Validar parámetros
        StockValidator.validate_quantity(quantity, "quantity")
        StockValidator.validate_min_stock(min_stock, "min_stock")
        
        # Crear stock
        stock = Stock(
            product_id=product_id,
            quantity=quantity,
            min_stock=min_stock
        )
        
        db.session.add(stock)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': f'Stock creado para producto {product_id}',
            'stock': stock.to_dict()
        }), 201

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

@stock_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_stock(product_id):
    try:
        stock = Stock.query.filter_by(product_id=product_id).first_or_404()
        
        # Verificar que no hay órdenes pendientes para este producto
        from ..models.order_item import OrderItem
        from ..models.order import Order
        
        pending_orders = db.session.query(Order).join(OrderItem).filter(
            OrderItem.product_id == product_id,
            Order.status == 'pending'
        ).all()
        
        if pending_orders:
            return jsonify({
                'error': f'No se puede eliminar stock del producto {product_id} porque tiene órdenes pendientes'
            }), 400
        
        db.session.delete(stock)
        db.session.commit()
        
        return jsonify({'message': f'Stock del producto {product_id} eliminado exitosamente'})

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': f'Error interno: {str(e)}'}), 500

@stock_bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    """Obtener productos con stock bajo"""
    low_stock_items = Stock.query.filter(Stock.quantity <= Stock.min_stock).order_by(Stock.id.asc()).all()
    return jsonify([stock.to_dict() for stock in low_stock_items])

@stock_bp.route('/negative-stock', methods=['GET'])
def get_negative_stock():
    """Obtener productos con stock negativo (violación de regla de negocio)"""
    negative_stock_items = Stock.query.filter(Stock.quantity < 0).order_by(Stock.id.asc()).all()
    return jsonify([stock.to_dict() for stock in negative_stock_items])

@stock_bp.route('/validate', methods=['GET'])
def validate_stock_rules():
    """Validar todas las reglas de stock"""
    try:
        from ..validators.business_rules import BusinessRuleEngine
        result = BusinessRuleEngine.validate_all_business_rules()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': f'Error al validar reglas: {str(e)}'}), 500

@stock_bp.route('/<int:product_id>/adjust', methods=['POST'])
def adjust_stock(product_id):
    """Ajustar stock (incrementar o decrementar)"""
    try:
        data = request.get_json()
        adjustment = data.get('adjustment', 0)
        reason = data.get('reason', 'Ajuste manual')
        
        if not isinstance(adjustment, int):
            return jsonify({'error': 'adjustment debe ser un entero'}), 400
        
        stock = Stock.query.filter_by(product_id=product_id).first_or_404()
        
        # Calcular nueva cantidad
        new_quantity = stock.quantity + adjustment
        
        # Validar que no resulte en stock negativo
        if new_quantity < 0:
            return jsonify({
                'error': f'Ajuste resultaría en stock negativo: {stock.quantity} + {adjustment} = {new_quantity}'
            }), 400
        
        # Usar el gestor de transacciones para el ajuste
        result = TransactionManager.execute_stock_update(
            product_id=product_id,
            new_quantity=new_quantity
        )
        
        # Agregar información del ajuste
        result['adjustment'] = adjustment
        result['reason'] = reason
        result['old_quantity'] = stock.quantity
        
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