from flask import Blueprint, request, jsonify
from ..models.user import User
from ..database import db
from ..decorators.role_decorators import roles_required
from werkzeug.security import generate_password_hash, check_password_hash

users_bp = Blueprint('users', __name__)

@users_bp.route('/', methods=['GET'])
@roles_required('admin')
def get_users():
    """Obtener lista de usuarios - Solo admin"""
    users = User.query.order_by(User.id.asc()).all()
    return jsonify([user.to_dict() for user in users])

@users_bp.route('/<int:id>', methods=['GET'])
@roles_required('admin')
def get_user(id):
    """Obtener usuario específico - Solo admin"""
    user = User.query.get_or_404(id)
    return jsonify(user.to_dict())

@users_bp.route('/', methods=['POST'])
@roles_required('admin')
def create_user():
    """Crear nuevo usuario - Solo admin"""
    data = request.get_json()
    
    # Validar datos requeridos
    if not data.get('username') or not data.get('password') or not data.get('role'):
        return jsonify({'error': 'Username, password y role son requeridos'}), 400
    
    # Verificar si el username ya existe
    if User.query.filter_by(username=data['username']).first():
        return jsonify({'error': 'El username ya existe'}), 400
    
    # Validar rol
    valid_roles = ['admin', 'manager', 'supervisor', 'user']
    if data['role'] not in valid_roles:
        return jsonify({'error': f'Rol inválido. Roles válidos: {", ".join(valid_roles)}'}), 400
    
    # Crear usuario
    new_user = User(
        username=data['username'],
        password_hash=generate_password_hash(data['password']),
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', ''),
        email=data.get('email', ''),
        role=data['role'],
        is_active=data.get('is_active', True)
    )
    
    db.session.add(new_user)
    db.session.commit()
    
    return jsonify(new_user.to_dict()), 201

@users_bp.route('/<int:id>', methods=['PUT'])
@roles_required('admin')
def update_user(id):
    """Actualizar usuario - Solo admin"""
    user = User.query.get_or_404(id)
    data = request.get_json()
    
    # Actualizar campos permitidos
    if 'username' in data:
        # Verificar que el username no esté en uso por otro usuario
        existing_user = User.query.filter_by(username=data['username']).first()
        if existing_user and existing_user.id != id:
            return jsonify({'error': 'El username ya está en uso'}), 400
        user.username = data['username']
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'email' in data:
        user.email = data['email']
    
    if 'role' in data:
        valid_roles = ['admin', 'manager', 'supervisor', 'user']
        if data['role'] not in valid_roles:
            return jsonify({'error': f'Rol inválido. Roles válidos: {", ".join(valid_roles)}'}), 400
        user.role = data['role']
    
    if 'is_active' in data:
        user.is_active = data['is_active']
    
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    return jsonify(user.to_dict())

@users_bp.route('/<int:id>', methods=['DELETE'])
@roles_required('admin')
def delete_user(id):
    """Eliminar usuario - Solo admin"""
    user = User.query.get_or_404(id)
    
    # No permitir eliminar el propio usuario
    if user.id == request.user_id:
        return jsonify({'error': 'No puedes eliminar tu propio usuario'}), 400
    
    # No permitir eliminar el último admin
    if user.role == 'admin':
        admin_count = User.query.filter_by(role='admin').count()
        if admin_count <= 1:
            return jsonify({'error': 'No se puede eliminar el último administrador'}), 400
    
    db.session.delete(user)
    db.session.commit()
    
    return jsonify({'message': 'Usuario eliminado exitosamente'})

@users_bp.route('/<int:id>/toggle-status', methods=['PUT'])
@roles_required('admin')
def toggle_user_status(id):
    """Activar/desactivar usuario - Solo admin"""
    user = User.query.get_or_404(id)
    
    # No permitir desactivar el propio usuario
    if user.id == request.user_id:
        return jsonify({'error': 'No puedes desactivar tu propio usuario'}), 400
    
    # No permitir desactivar el último admin
    if user.role == 'admin' and user.is_active:
        admin_count = User.query.filter_by(role='admin', is_active=True).count()
        if admin_count <= 1:
            return jsonify({'error': 'No se puede desactivar el último administrador'}), 400
    
    user.is_active = not user.is_active
    db.session.commit()
    
    return jsonify({
        'message': f'Usuario {"activado" if user.is_active else "desactivado"} exitosamente',
        'is_active': user.is_active
    })

@users_bp.route('/profile', methods=['GET'])
@roles_required('admin', 'manager', 'supervisor', 'user')
def get_profile():
    """Obtener perfil del usuario actual"""
    user_id = request.user_id
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict())

@users_bp.route('/profile', methods=['PUT'])
@roles_required('admin', 'manager', 'supervisor', 'user')
def update_profile():
    """Actualizar perfil del usuario actual"""
    user_id = request.user_id
    user = User.query.get_or_404(user_id)
    data = request.get_json()
    
    # Solo permitir actualizar campos del perfil
    if 'first_name' in data:
        user.first_name = data['first_name']
    
    if 'last_name' in data:
        user.last_name = data['last_name']
    
    if 'email' in data:
        user.email = data['email']
    
    if 'password' in data and data['password']:
        user.password_hash = generate_password_hash(data['password'])
    
    db.session.commit()
    return jsonify(user.to_dict())

@users_bp.route('/stats', methods=['GET'])
@roles_required('admin')
def get_user_stats():
    """Obtener estadísticas de usuarios - Solo admin"""
    total_users = User.query.count()
    active_users = User.query.filter_by(is_active=True).count()
    inactive_users = total_users - active_users
    
    role_stats = {}
    for role in ['admin', 'manager', 'supervisor', 'user']:
        role_stats[role] = User.query.filter_by(role=role).count()
    
    return jsonify({
        'total_users': total_users,
        'active_users': active_users,
        'inactive_users': inactive_users,
        'role_distribution': role_stats
    })
