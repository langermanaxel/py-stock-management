from flask import Blueprint, request, jsonify
from ..models.stock import Stock
from ..models.product import Product
from ..database import db

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
    stock = Stock.query.filter_by(product_id=product_id).first_or_404()
    data = request.get_json()

    stock.quantity = data.get('quantity', stock.quantity)
    stock.min_stock = data.get('min_stock', stock.min_stock)
    
    db.session.commit()
    
    return jsonify(stock.to_dict())

@stock_bp.route('/low-stock', methods=['GET'])
def get_low_stock():
    """Obtener productos con stock bajo"""
    low_stock_items = Stock.query.filter(Stock.quantity <= Stock.min_stock).order_by(Stock.id.asc()).all()
    return jsonify([stock.to_dict() for stock in low_stock_items])