#!/usr/bin/env python3
"""
API de Usuarios con flask-smorest
"""

from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import request, jsonify
from marshmallow import Schema, fields, ValidationError
from ..models.user import User
from ..database import db
from ..decorators.role_decorators import roles_required
from werkzeug.security import generate_password_hash

# Crear blueprint
users_blp = Blueprint(
    'users', 'users',
    url_prefix='/users',
    description='Operaciones de gestión de usuarios'
)

# Esquemas de validación
class UserSchema(Schema):
    """Esquema para usuario"""
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    email = fields.Email(allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    role = fields.Str(required=True, validate=lambda x: x in ['admin', 'manager', 'supervisor', 'user'])
    is_active = fields.Bool(dump_only=True)
    created_at = fields.DateTime(dump_only=True)
    updated_at = fields.DateTime(dump_only=True)
    last_login = fields.DateTime(dump_only=True)

class UserCreateSchema(Schema):
    """Esquema para crear usuario"""
    username = fields.Str(required=True, validate=lambda x: len(x) >= 3)
    password = fields.Str(required=True, validate=lambda x: len(x) >= 6)
    email = fields.Email(allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    role = fields.Str(required=True, validate=lambda x: x in ['admin', 'manager', 'supervisor', 'user'])
    is_active = fields.Bool(missing=True)

class UserUpdateSchema(Schema):
    """Esquema para actualizar usuario"""
    username = fields.Str(validate=lambda x: len(x) >= 3)
    email = fields.Email(allow_none=True)
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    role = fields.Str(validate=lambda x: x in ['admin', 'manager', 'supervisor', 'user'])
    is_active = fields.Bool()
    password = fields.Str(validate=lambda x: len(x) >= 6)

class UserProfileSchema(Schema):
    """Esquema para perfil de usuario"""
    first_name = fields.Str(allow_none=True)
    last_name = fields.Str(allow_none=True)
    email = fields.Email(allow_none=True)
    password = fields.Str(validate=lambda x: len(x) >= 6)

# Endpoints
@users_blp.route('/')
class UsersList(MethodView):
    """Lista de usuarios - Solo admin"""
    
    @users_blp.response(200, UserSchema(many=True))
    @roles_required('admin')
    def get(self):
        """Obtener lista de usuarios"""
        users = User.query.order_by(User.id.asc()).all()
        return users

    @users_blp.arguments(UserCreateSchema)
    @users_blp.response(201, UserSchema)
    @roles_required('admin')
    def post(self, user_data):
        """Crear nuevo usuario"""
        # Verificar si el username ya existe
        if User.query.filter_by(username=user_data['username']).first():
            abort(400, message="El username ya existe")
        
        # Crear usuario
        new_user = User(
            username=user_data['username'],
            password_hash=generate_password_hash(user_data['password']),
            first_name=user_data.get('first_name', ''),
            last_name=user_data.get('last_name', ''),
            email=user_data.get('email', ''),
            role=user_data['role'],
            is_active=user_data.get('is_active', True)
        )
        
        db.session.add(new_user)
        db.session.commit()
        
        return new_user

@users_blp.route('/<int:user_id>')
class UsersResource(MethodView):
    """Operaciones con usuario específico - Solo admin"""
    
    @users_blp.response(200, UserSchema)
    @roles_required('admin')
    def get(self, user_id):
        """Obtener usuario específico"""
        user = User.query.get_or_404(user_id)
        return user

    @users_blp.arguments(UserUpdateSchema)
    @users_blp.response(200, UserSchema)
    @roles_required('admin')
    def put(self, user_data, user_id):
        """Actualizar usuario"""
        user = User.query.get_or_404(user_id)
        
        # Actualizar campos permitidos
        if 'username' in user_data:
            # Verificar que el username no esté en uso por otro usuario
            existing_user = User.query.filter_by(username=user_data['username']).first()
            if existing_user and existing_user.id != user_id:
                abort(400, message="El username ya está en uso")
            user.username = user_data['username']
        
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        
        if 'email' in user_data:
            user.email = user_data['email']
        
        if 'role' in user_data:
            user.role = user_data['role']
        
        if 'is_active' in user_data:
            user.is_active = user_data['is_active']
        
        if 'password' in user_data and user_data['password']:
            user.password_hash = generate_password_hash(user_data['password'])
        
        db.session.commit()
        return user

    @users_blp.response(200, description="Usuario eliminado exitosamente")
    @roles_required('admin')
    def delete(self, user_id):
        """Eliminar usuario"""
        user = User.query.get_or_404(user_id)
        
        # No permitir eliminar el propio usuario
        if user.id == request.user_id:
            abort(400, message="No puedes eliminar tu propio usuario")
        
        # No permitir eliminar el último admin
        if user.role == 'admin':
            admin_count = User.query.filter_by(role='admin').count()
            if admin_count <= 1:
                abort(400, message="No se puede eliminar el último administrador")
        
        db.session.delete(user)
        db.session.commit()
        
        return {"message": "Usuario eliminado exitosamente"}

@users_blp.route('/<int:user_id>/toggle-status')
class UserToggleStatus(MethodView):
    """Activar/desactivar usuario - Solo admin"""
    
    @users_blp.response(200, description="Estado del usuario cambiado")
    @roles_required('admin')
    def put(self, user_id):
        """Cambiar estado del usuario"""
        user = User.query.get_or_404(user_id)
        
        # No permitir desactivar el propio usuario
        if user.id == request.user_id:
            abort(400, message="No puedes desactivar tu propio usuario")
        
        # No permitir desactivar el último admin
        if user.role == 'admin' and user.is_active:
            admin_count = User.query.filter_by(role='admin', is_active=True).count()
            if admin_count <= 1:
                abort(400, message="No se puede desactivar el último administrador")
        
        user.is_active = not user.is_active
        db.session.commit()
        
        return {
            "message": f"Usuario {'activado' if user.is_active else 'desactivado'} exitosamente",
            "is_active": user.is_active
        }

@users_blp.route('/profile')
class UserProfile(MethodView):
    """Perfil del usuario actual"""
    
    @users_blp.response(200, UserSchema)
    @roles_required('admin', 'manager', 'supervisor', 'user')
    def get(self):
        """Obtener perfil del usuario actual"""
        user_id = request.user_id
        user = User.query.get_or_404(user_id)
        return user

    @users_blp.arguments(UserProfileSchema)
    @users_blp.response(200, UserSchema)
    @roles_required('admin', 'manager', 'supervisor', 'user')
    def put(self, profile_data):
        """Actualizar perfil del usuario actual"""
        user_id = request.user_id
        user = User.query.get_or_404(user_id)
        
        # Solo permitir actualizar campos del perfil
        if 'first_name' in profile_data:
            user.first_name = profile_data['first_name']
        
        if 'last_name' in profile_data:
            user.last_name = profile_data['last_name']
        
        if 'email' in profile_data:
            user.email = profile_data['email']
        
        if 'password' in profile_data and profile_data['password']:
            user.password_hash = generate_password_hash(profile_data['password'])
        
        db.session.commit()
        return user

@users_blp.route('/stats')
class UserStats(MethodView):
    """Estadísticas de usuarios - Solo admin"""
    
    @users_blp.response(200, description="Estadísticas de usuarios")
    @roles_required('admin')
    def get(self):
        """Obtener estadísticas de usuarios"""
        total_users = User.query.count()
        active_users = User.query.filter_by(is_active=True).count()
        inactive_users = total_users - active_users
        
        role_stats = {}
        for role in ['admin', 'manager', 'supervisor', 'user']:
            role_stats[role] = User.query.filter_by(role=role).count()
        
        return {
            'total_users': total_users,
            'active_users': active_users,
            'inactive_users': inactive_users,
            'role_distribution': role_stats
        }
