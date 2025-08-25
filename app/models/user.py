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
    
    # Roles disponibles
    ROLES = {
        'admin': 'Administrador',
        'manager': 'Gerente',
        'supervisor': 'Supervisor',
        'user': 'Usuario'
    }
    
    # Permisos por rol
    PERMISSIONS = {
        'admin': [
            'manage_users', 'manage_products', 'manage_categories',
            'manage_stock', 'manage_orders', 'manage_purchases',
            'view_reports', 'manage_system'
        ],
        'manager': [
            'manage_products', 'manage_categories', 'manage_stock',
            'manage_orders', 'manage_purchases', 'view_reports'
        ],
        'supervisor': [
            'manage_products', 'manage_stock', 'manage_orders',
            'view_reports'
        ],
        'user': [
            'view_products', 'view_stock', 'create_orders'
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
        from flask import current_app
        
        # Método 1: Intentar usar SQLAlchemy con current_app
        if hasattr(current_app, 'extensions') and 'sqlalchemy' in current_app.extensions:
            try:
                with current_app.app_context():
                    return User.query.filter_by(username=username).first()
            except Exception as e:
                print(f"Error en get_by_username con current_app: {e}")
                # Continuar con el siguiente método
        
        # Método 2: Intentar usar SQLAlchemy global
        try:
            return User.query.filter_by(username=username).first()
        except Exception as e:
            print(f"Error en get_by_username con instancia global: {e}")
            # Continuar con el siguiente método
        
        # Método 3: Fallback a SQL directo
        try:
            from sqlite3 import connect
            from pathlib import Path
            
            # Ruta de la base de datos
            db_path = Path("instance/stock_management.db")
            if not db_path.exists():
                print("❌ Base de datos no encontrada para fallback SQL")
                return None
            
            # Conectar y ejecutar SQL directo
            conn = connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, password_hash, first_name, last_name, 
                       role, is_active, created_at, updated_at, last_login
                FROM users 
                WHERE username = ? AND is_active = 1
            """, (username,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data:
                # Crear instancia de usuario con los datos obtenidos
                user = User.__new__(User)
                user.id = user_data[0]
                user.username = user_data[1]
                user.email = user_data[2]
                user.password_hash = user_data[3]
                user.first_name = user_data[4]
                user.last_name = user_data[5]
                user.role = user_data[6]
                user.is_active = bool(user_data[7])
                user.created_at = user_data[8]
                user.updated_at = user_data[9]
                user.last_login = user_data[10]
                return user
            
            return None
            
        except Exception as e:
            print(f"Error en get_by_username con fallback SQL: {e}")
            return None
    
    @staticmethod
    def get_by_email(email):
        """Obtiene usuario por email"""
        from flask import current_app
        
        # Método 1: Intentar usar SQLAlchemy con current_app
        if hasattr(current_app, 'extensions') and 'sqlalchemy' in current_app.extensions:
            try:
                with current_app.app_context():
                    return User.query.filter_by(email=email).first()
            except Exception as e:
                print(f"Error en get_by_email con current_app: {e}")
                # Continuar con el siguiente método
        
        # Método 2: Intentar usar SQLAlchemy global
        try:
            return User.query.filter_by(email=email).first()
        except Exception as e:
            print(f"Error en get_by_email con instancia global: {e}")
            # Continuar con el siguiente método
        
        # Método 3: Fallback a SQL directo
        try:
            from sqlite3 import connect
            from pathlib import Path
            
            # Ruta de la base de datos
            db_path = Path("instance/stock_management.db")
            if not db_path.exists():
                print("❌ Base de datos no encontrada para fallback SQL")
                return None
            
            # Conectar y ejecutar SQL directo
            conn = connect(db_path)
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT id, username, email, password_hash, first_name, last_name, 
                       role, is_active, created_at, updated_at, last_login
                FROM users 
                WHERE email = ? AND is_active = 1
            """, (email,))
            
            user_data = cursor.fetchone()
            conn.close()
            
            if user_data:
                # Crear instancia de usuario con los datos obtenidos
                user = User.__new__(User)
                user.id = user_data[0]
                user.username = user_data[1]
                user.email = user_data[2]
                user.password_hash = user_data[3]
                user.first_name = user_data[4]
                user.last_name = user_data[5]
                user.role = user_data[6]
                user.is_active = bool(user_data[7])
                user.created_at = user_data[8]
                user.updated_at = user_data[9]
                user.last_login = user_data[10]
                return user
            
            return None
            
        except Exception as e:
            print(f"Error en get_by_email con fallback SQL: {e}")
            return None
    
    @staticmethod
    def create_admin_user(username, email, password, first_name, last_name):
        """Crea un usuario administrador"""
        from flask import current_app
        
        # Intentar usar current_app directamente
        if hasattr(current_app, 'extensions') and 'sqlalchemy' in current_app.extensions:
            with current_app.app_context():
                if User.query.filter_by(role='admin').first():
                    raise ValueError("Ya existe un usuario administrador")
                
                user = User(username, email, password, first_name, last_name, 'admin')
                db.session.add(user)
                db.session.commit()
                return user
        else:
            # Fallback: intentar usar la instancia global
            try:
                if User.query.filter_by(role='admin').first():
                    raise ValueError("Ya existe un usuario administrador")
                
                user = User(username, email, password, first_name, last_name, 'admin')
                db.session.add(user)
                db.session.commit()
                return user
            except Exception as e:
                print(f"Error en create_admin_user: {e}")
                raise e
