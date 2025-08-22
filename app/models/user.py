#!/usr/bin/env python3
"""
Modelo de Usuario para el Sistema de Gestión de Inventario
Incluye autenticación, roles y permisos
"""

from datetime import datetime, timedelta
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os

db = SQLAlchemy()

class User(db.Model):
    """Modelo de Usuario con autenticación y roles"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones
    orders_created = db.relationship('Order', backref='created_by', lazy=True)
    purchase_orders_created = db.relationship('PurchaseOrder', backref='created_by', lazy=True)
    
    # Roles disponibles
    ROLES = {
        'admin': 'Administrador',
        'manager': 'Gerente',
        'user': 'Usuario',
        'viewer': 'Solo Lectura'
    }
    
    # Permisos por rol
    PERMISSIONS = {
        'admin': ['read', 'write', 'delete', 'manage_users', 'manage_stock', 'manage_orders'],
        'manager': ['read', 'write', 'manage_stock', 'manage_orders'],
        'user': ['read', 'write'],
        'viewer': ['read']
    }
    
    def __init__(self, username, email, password, first_name, last_name, role='user'):
        self.username = username
        self.email = email
        self.set_password(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
    
    def set_password(self, password):
        """Hashea la contraseña de forma segura"""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def has_permission(self, permission):
        """Verifica si el usuario tiene un permiso específico"""
        return permission in self.PERMISSIONS.get(self.role, [])
    
    def can_read(self):
        """Verifica si puede leer"""
        return self.has_permission('read')
    
    def can_write(self):
        """Verifica si puede escribir"""
        return self.has_permission('write')
    
    def can_delete(self):
        """Verifica si puede eliminar"""
        return self.has_permission('delete')
    
    def can_manage_users(self):
        """Verifica si puede gestionar usuarios"""
        return self.has_permission('manage_users')
    
    def can_manage_stock(self):
        """Verifica si puede gestionar stock"""
        return self.has_permission('manage_stock')
    
    def can_manage_orders(self):
        """Verifica si puede gestionar órdenes"""
        return self.has_permission('manage_orders')
    
    def is_admin(self):
        """Verifica si es administrador"""
        return self.role == 'admin'
    
    def is_manager(self):
        """Verifica si es gerente o superior"""
        return self.role in ['admin', 'manager']
    
    def generate_token(self, expires_in=3600):
        """Genera un token JWT"""
        payload = {
            'user_id': self.id,
            'username': self.username,
            'role': self.role,
            'exp': datetime.utcnow() + timedelta(seconds=expires_in)
        }
        secret_key = os.environ.get('JWT_SECRET_KEY', 'default-secret-key')
        return jwt.encode(payload, secret_key, algorithm='HS256')
    
    def update_last_login(self):
        """Actualiza la fecha del último login"""
        self.last_login = datetime.utcnow()
        db.session.commit()
    
    def to_dict(self):
        """Convierte el usuario a diccionario (sin información sensible)"""
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'role_name': self.ROLES.get(self.role, 'Desconocido'),
            'is_active': self.is_active,
            'last_login': self.last_login.isoformat() if self.last_login else None,
            'created_at': self.created_at.isoformat(),
            'permissions': self.PERMISSIONS.get(self.role, [])
        }
    
    def to_dict_public(self):
        """Convierte el usuario a diccionario público (mínima información)"""
        return {
            'id': self.id,
            'username': self.username,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'role': self.role,
            'role_name': self.ROLES.get(self.role, 'Desconocido')
        }
    
    def __repr__(self):
        return f'<User {self.username}>'
    
    @staticmethod
    def verify_token(token):
        """Verifica y decodifica un token JWT"""
        try:
            secret_key = os.environ.get('JWT_SECRET_KEY', 'default-secret-key')
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            return User.query.get(payload['user_id'])
        except jwt.ExpiredSignatureError:
            return None  # Token expirado
        except jwt.InvalidTokenError:
            return None  # Token inválido
    
    @staticmethod
    def get_by_username(username):
        """Obtiene usuario por nombre de usuario"""
        return User.query.filter_by(username=username).first()
    
    @staticmethod
    def get_by_email(email):
        """Obtiene usuario por email"""
        return User.query.filter_by(email=email).first()
    
    @staticmethod
    def create_admin_user(username, email, password, first_name, last_name):
        """Crea un usuario administrador"""
        if User.query.filter_by(role='admin').first():
            raise ValueError("Ya existe un usuario administrador")
        
        user = User(username, email, password, first_name, last_name, 'admin')
        db.session.add(user)
        db.session.commit()
        return user
