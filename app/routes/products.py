from flask import Blueprint, request, jsonify
from ..models.product import Product
from ..models.stock import Stock
from ..models.category import Category
from ..database import db

products_bp = Blueprint('products', __name__)

@products_bp.route('/', methods=['GET'])
def get_products():
    products = Product.query.order_by(Product.id.asc()).all()
    return jsonify([p.to_dict() for p in products])

@products_bp.route('/<int:id>', methods=['GET'])
def get_product(id):
    product = Product.query.get_or_404(id)
    return jsonify(product.to_dict())

@products_bp.route('/', methods=['POST'])
def create_product():
    data = request.get_json()
    category = Category.query.get_or_404(data['category_id'])
    product = Product(
        name=data['name'],
        description=data.get('description'),
        price=data['price'],
        category_id=data['category_id']
    )
    db.session.add(product)
    db.session.flush()

    stock = Stock(
        product_id=product.id,
        quantity=0,
        min_stock=data.get('min_stock', 0)
    )
    db.session.add(stock)
    db.session.commit()

    return jsonify(product.to_dict()), 201

@products_bp.route('/<int:id>', methods=['PUT'])
def update_product(id):
    product = Product.query.get_or_404(id)
    data = request.get_json()
    
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'category_id' in data:
        # Verificar que la nueva categoría existe
        Category.query.get_or_404(data['category_id'])
        product.category_id = data['category_id']
    
    # Actualizar stock mínimo si se proporciona
    if 'min_stock' in data:
        stock = Stock.query.filter_by(product_id=id).first()
        if stock:
            stock.min_stock = data['min_stock']
    
    db.session.commit()
    return jsonify(product.to_dict())

@products_bp.route('/<int:id>', methods=['DELETE'])
def delete_product(id):
    product = Product.query.get_or_404(id)
    
    # Eliminar el stock asociado
    stock = Stock.query.filter_by(product_id=id).first()
    if stock:
        db.session.delete(stock)
    
    # Eliminar el producto
    db.session.delete(product)
    db.session.commit()
    
    return jsonify({'message': 'Producto eliminado exitosamente'})