#!/usr/bin/env python3
"""
Modelo de Usuario para el Sistema de Gestión de Inventario
Incluye autenticación, roles y permisos
"""

from datetime import datetime, timedelta
from ..database import db
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import os
from flask import current_app

class User(db.Model):
    """Modelo de Usuario con autenticación y roles"""
    
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    is_active = db.Column(db.Boolean, default=True)
    last_login = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relaciones - comentadas temporalmente para evitar problemas de inicialización
    # orders_created = db.relationship('Order', back_populates='created_by', lazy='dynamic', cascade='all, delete-orphan')
    # purchase_orders_created = db.relationship('PurchaseOrder', back_populates='created_by', lazy='dynamic', cascade='all, delete-orphan')
    
    # Roles disponibles - ESTANDARIZADOS AL INGLÉS
    ROLES = {
        'admin': 'Administrador',
        'manager': 'Gerente',
        'supervisor': 'Supervisor',
        'user': 'Usuario',
        'viewer': 'Viewer'
    }
    
    # Permisos por rol - ESTANDARIZADOS Y COMPLETOS
    PERMISSIONS = {
        'admin': [
            'manage_users', 'manage_products', 'manage_categories',
            'manage_stock', 'manage_orders', 'manage_purchases',
            'view_reports', 'manage_system', 'all'
        ],
        'manager': [
            'manage_products', 'manage_categories', 'manage_stock',
            'manage_orders', 'manage_purchases', 'view_reports',
            'read', 'create', 'update'
        ],
        'supervisor': [
            'manage_products', 'manage_stock', 'manage_orders',
            'view_reports', 'read', 'create_orders'
        ],
        'user': [
            'view_products', 'view_stock', 'create_orders',
            'read_limited'
        ],
        'viewer': [
            'read_only', 'view_dashboard'
        ]
    }
    
    def __init__(self, username, email, password, first_name, last_name, role='user'):
        self.username = username
        self.email = email
        self.password_hash = generate_password_hash(password)
        self.first_name = first_name
        self.last_name = last_name
        self.role = role
        self.is_active = True
        self.created_at = datetime.utcnow()
        self.updated_at = datetime.utcnow()
    
    def check_password(self, password):
        """Verifica la contraseña"""
        return check_password_hash(self.password_hash, password)
    
    def set_password(self, password):
        """Establece una nueva contraseña"""
        self.password_hash = generate_password_hash(password)
        self.updated_at = datetime.utcnow()
    
    def has_permission(self, permission):
        """Verifica si el usuario tiene un permiso específico"""
        return permission in self.PERMISSIONS.get(self.role, [])
    
    def get_permissions(self):
        """Obtiene todos los permisos del usuario"""
        return self.PERMISSIONS.get(self.role, [])
    
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
        try:
            self.last_login = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            db.session.commit()
        except Exception as e:
            print(f"Error actualizando last_login: {e}")
            db.session.rollback()
    
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
        try:
            # Usar solo SQLAlchemy estándar
            return User.query.filter_by(username=username, is_active=True).first()
        except Exception as e:
            print(f"Error en get_by_username: {e}")
            return None
    
    @staticmethod
    def get_by_email(email):
        """Obtiene usuario por email"""
        try:
            # Usar solo SQLAlchemy estándar
            return User.query.filter_by(email=email, is_active=True).first()
        except Exception as e:
            print(f"Error en get_by_email: {e}")
            return None
    
    @staticmethod
    def create_admin_user(username, email, password, first_name, last_name):
        """Crea un usuario administrador"""
        try:
            # Verificar si ya existe un admin
            if User.query.filter_by(role='admin').first():
                raise ValueError("Ya existe un usuario administrador")
            
            # Crear nuevo usuario admin
            user = User(username, email, password, first_name, last_name, 'admin')
            db.session.add(user)
            db.session.commit()
            return user
        except Exception as e:
            print(f"Error en create_admin_user: {e}")
            db.session.rollback()
            raise e
