from flask import Blueprint, jsonify, request
from ..models.category import Category
from ..models.product import Product
from ..database import db
from ..decorators.role_decorators import roles_required

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('/', methods=['GET'])
@roles_required('admin', 'manager', 'supervisor', 'user')
def get_categories():
    categories = Category.query.order_by(Category.id.asc()).all()
    categories_with_count = []
    
    for category in categories:
        category_data = category.to_dict()
        # Contar productos en esta categoría
        product_count = Product.query.filter_by(category_id=category.id).count()
        category_data['product_count'] = product_count
        categories_with_count.append(category_data)
    
    return jsonify(categories_with_count)

@categories_bp.route('/<int:id>', methods=['GET'])
@roles_required('admin', 'manager', 'supervisor', 'user')
def get_category(id):
    category = Category.query.get_or_404(id)
    category_data = category.to_dict()
    # Contar productos en esta categoría
    product_count = Product.query.filter_by(category_id=category.id).count()
    category_data['product_count'] = product_count
    return jsonify(category_data)

@categories_bp.route('/', methods=['POST'])
@roles_required('admin', 'manager')
def create_category():
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Nombre de categoría requerido'}), 400
    
    # Verificar si la categoría ya existe
    existing_category = Category.query.filter_by(name=data['name']).first()
    if existing_category:
        return jsonify({'error': 'La categoría ya existe'}), 400
    
    category = Category(name=data['name'])
    db.session.add(category)
    db.session.commit()
    
    return jsonify(category.to_dict()), 201

@categories_bp.route('/<int:id>', methods=['PUT'])
@roles_required('admin', 'manager')
def update_category(id):
    category = Category.query.get_or_404(id)
    data = request.get_json()
    
    if not data or 'name' not in data:
        return jsonify({'error': 'Nombre de categoría requerido'}), 400
    
    # Verificar si el nuevo nombre ya existe en otra categoría
    existing_category = Category.query.filter_by(name=data['name']).first()
    if existing_category and existing_category.id != id:
        return jsonify({'error': 'El nombre de categoría ya existe'}), 400
    
    category.name = data['name']
    db.session.commit()
    
    return jsonify(category.to_dict())

@categories_bp.route('/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_category(id):
    category = Category.query.get_or_404(id)
    
    # Verificar si la categoría tiene productos
    if category.products:
        return jsonify({'error': 'No se puede eliminar una categoría que tiene productos'}), 400
    
    db.session.delete(category)
    db.session.commit()
    
    return jsonify({'message': 'Categoría eliminada exitosamente'})

@categories_bp.route('/<int:id>/products', methods=['GET'])
@roles_required('admin', 'manager', 'supervisor', 'user')
def get_products_by_category(id):
    category = Category.query.get_or_404(id)
    products = category.products
    # Ordenar productos por ID de menor a mayor
    sorted_products = sorted(products, key=lambda x: x.id)
    return jsonify([product.to_dict() for product in sorted_products])