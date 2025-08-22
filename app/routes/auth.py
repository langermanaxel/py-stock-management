#!/usr/bin/env python3
"""
Rutas de Autenticación para el Sistema de Gestión de Inventario
"""

from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash
from app.database import db
from app.models.user import User
from functools import wraps
import os

auth_bp = Blueprint('auth', __name__)

def require_permission(permission):
    """Decorador para requerir permisos específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            current_user = get_current_user()
            if not current_user or not current_user.has_permission(permission):
                return jsonify({'error': 'Permiso denegado'}), 403
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Obtiene el usuario actual desde el token JWT"""
    try:
        from flask_jwt_extended import get_jwt_identity
        user_id = get_jwt_identity()
        if user_id:
            return User.query.get(user_id)
    except:
        pass
    return None

@auth_bp.route('/login', methods=['POST'])
def login():
    """Endpoint de login"""
    try:
        data = request.get_json()
        
        if not data or not data.get('username') or not data.get('password'):
            return jsonify({'error': 'Usuario y contraseña son requeridos'}), 400
        
        username = data['username']
        password = data['password']
        
        # Buscar usuario
        user = User.get_by_username(username)
        if not user or not user.check_password(password):
            return jsonify({'error': 'Credenciales inválidas'}), 401
        
        if not user.is_active:
            return jsonify({'error': 'Usuario desactivado'}), 401
        
        # Actualizar último login
        user.update_last_login()
        
        # Generar tokens
        access_token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        
        return jsonify({
            'message': 'Login exitoso',
            'access_token': access_token,
            'refresh_token': refresh_token,
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error en login: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/register', methods=['POST'])
@jwt_required()
@require_permission('manage_users')
def register():
    """Endpoint de registro (solo para usuarios con permisos)"""
    try:
        data = request.get_json()
        
        # Validar datos requeridos
        required_fields = ['username', 'email', 'password', 'first_name', 'last_name']
        for field in required_fields:
            if not data.get(field):
                return jsonify({'error': f'Campo {field} es requerido'}), 400
        
        # Verificar si el usuario ya existe
        if User.get_by_username(data['username']):
            return jsonify({'error': 'El nombre de usuario ya existe'}), 400
        
        if User.get_by_email(data['email']):
            return jsonify({'error': 'El email ya existe'}), 400
        
        # Crear nuevo usuario
        role = data.get('role', 'user')
        if role not in User.ROLES:
            return jsonify({'error': 'Rol inválido'}), 400
        
        user = User(
            username=data['username'],
            email=data['email'],
            password=data['password'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            role=role
        )
        
        db.session.add(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario creado exitosamente',
            'user': user.to_dict()
        }), 201
        
    except Exception as e:
        current_app.logger.error(f"Error en registro: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():
    """Endpoint para refrescar token"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user or not user.is_active:
            return jsonify({'error': 'Usuario no válido'}), 401
        
        new_access_token = create_access_token(identity=current_user_id)
        
        return jsonify({
            'access_token': new_access_token
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error en refresh: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/profile', methods=['GET'])
@jwt_required()
def get_profile():
    """Obtener perfil del usuario actual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        return jsonify({
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error obteniendo perfil: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Actualizar perfil del usuario actual"""
    try:
        current_user_id = get_jwt_identity()
        user = User.query.get(current_user_id)
        
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Campos que se pueden actualizar
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            # Verificar que el email no esté en uso
            existing_user = User.get_by_email(data['email'])
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'El email ya está en uso'}), 400
            user.email = data['email']
        
        # Cambiar contraseña si se proporciona
        if 'password' in data and data['password']:
            user.set_password(data['password'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Perfil actualizado exitosamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error actualizando perfil: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/users', methods=['GET'])
@jwt_required()
@require_permission('manage_users')
def get_users():
    """Obtener lista de usuarios (solo para administradores)"""
    try:
        users = User.query.all()
        return jsonify({
            'users': [user.to_dict() for user in users]
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error obteniendo usuarios: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/users/<int:user_id>', methods=['PUT'])
@jwt_required()
@require_permission('manage_users')
def update_user(user_id):
    """Actualizar usuario (solo para administradores)"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        data = request.get_json()
        
        # Campos que se pueden actualizar
        if 'first_name' in data:
            user.first_name = data['first_name']
        if 'last_name' in data:
            user.last_name = data['last_name']
        if 'email' in data:
            existing_user = User.get_by_email(data['email'])
            if existing_user and existing_user.id != user.id:
                return jsonify({'error': 'El email ya está en uso'}), 400
            user.email = data['email']
        if 'role' in data:
            if data['role'] not in User.ROLES:
                return jsonify({'error': 'Rol inválido'}), 400
            user.role = data['role']
        if 'is_active' in data:
            user.is_active = bool(data['is_active'])
        
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario actualizado exitosamente',
            'user': user.to_dict()
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error actualizando usuario: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/users/<int:user_id>', methods=['DELETE'])
@jwt_required()
@require_permission('manage_users')
def delete_user(user_id):
    """Eliminar usuario (solo para administradores)"""
    try:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': 'Usuario no encontrado'}), 404
        
        # No permitir eliminar el último administrador
        if user.role == 'admin':
            admin_count = User.query.filter_by(role='admin').count()
            if admin_count <= 1:
                return jsonify({'error': 'No se puede eliminar el último administrador'}), 400
        
        db.session.delete(user)
        db.session.commit()
        
        return jsonify({
            'message': 'Usuario eliminado exitosamente'
        }), 200
        
    except Exception as e:
        current_app.logger.error(f"Error eliminando usuario: {str(e)}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@auth_bp.route('/logout', methods=['POST'])
@jwt_required()
def logout():
    """Endpoint de logout (el token se invalida en el frontend)"""
    return jsonify({
        'message': 'Logout exitoso'
    }), 200
