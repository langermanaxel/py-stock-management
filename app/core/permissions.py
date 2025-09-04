#!/usr/bin/env python3
"""
Sistema de Permisos Centralizado
Maneja todos los permisos y roles de manera consistente en toda la aplicación
"""

from enum import Enum
from typing import List, Dict, Set
from functools import wraps
from flask import jsonify, request, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity

class PermissionLevel(Enum):
    """Niveles de permisos del sistema"""
    VIEWER = 0
    USER = 1
    SUPERVISOR = 2
    MANAGER = 3
    ADMIN = 4

class Permission(Enum):
    """Permisos específicos del sistema"""
    # Permisos de lectura
    READ_ONLY = "read_only"
    READ_LIMITED = "read_limited"
    READ = "read"
    
    # Permisos de escritura
    CREATE = "create"
    UPDATE = "update"
    DELETE = "delete"
    
    # Permisos específicos
    CREATE_ORDERS = "create_orders"
    VIEW_PRODUCTS = "view_products"
    VIEW_STOCK = "view_stock"
    VIEW_DASHBOARD = "view_dashboard"
    MANAGE_USERS = "manage_users"
    MANAGE_PRODUCTS = "manage_products"
    MANAGE_CATEGORIES = "manage_categories"
    MANAGE_STOCK = "manage_stock"
    MANAGE_ORDERS = "manage_orders"
    MANAGE_PURCHASES = "manage_purchases"
    VIEW_REPORTS = "view_reports"
    MANAGE_SYSTEM = "manage_system"
    
    # Permiso especial
    ALL = "all"

class Role(Enum):
    """Roles del sistema estandarizados"""
    ADMIN = "admin"
    MANAGER = "manager"
    SUPERVISOR = "supervisor"
    USER = "user"
    VIEWER = "viewer"

class PermissionManager:
    """Gestor centralizado de permisos"""
    
    # Jerarquía de roles con sus niveles
    ROLE_HIERARCHY = {
        Role.ADMIN: PermissionLevel.ADMIN,
        Role.MANAGER: PermissionLevel.MANAGER,
        Role.SUPERVISOR: PermissionLevel.SUPERVISOR,
        Role.USER: PermissionLevel.USER,
        Role.VIEWER: PermissionLevel.VIEWER
    }
    
    # Permisos por rol
    ROLE_PERMISSIONS = {
        Role.ADMIN: [
            Permission.ALL,
            Permission.MANAGE_USERS,
            Permission.MANAGE_PRODUCTS,
            Permission.MANAGE_CATEGORIES,
            Permission.MANAGE_STOCK,
            Permission.MANAGE_ORDERS,
            Permission.MANAGE_PURCHASES,
            Permission.VIEW_REPORTS,
            Permission.MANAGE_SYSTEM,
            Permission.READ,
            Permission.CREATE,
            Permission.UPDATE,
            Permission.DELETE,
            Permission.CREATE_ORDERS
        ],
        Role.MANAGER: [
            Permission.MANAGE_PRODUCTS,
            Permission.MANAGE_CATEGORIES,
            Permission.MANAGE_STOCK,
            Permission.MANAGE_ORDERS,
            Permission.MANAGE_PURCHASES,
            Permission.VIEW_REPORTS,
            Permission.READ,
            Permission.CREATE,
            Permission.UPDATE,
            Permission.CREATE_ORDERS
        ],
        Role.SUPERVISOR: [
            Permission.MANAGE_PRODUCTS,
            Permission.MANAGE_STOCK,
            Permission.MANAGE_ORDERS,
            Permission.VIEW_REPORTS,
            Permission.READ,
            Permission.CREATE_ORDERS
        ],
        Role.USER: [
            Permission.VIEW_PRODUCTS,
            Permission.VIEW_STOCK,
            Permission.CREATE_ORDERS,
            Permission.READ_LIMITED
        ],
        Role.VIEWER: [
            Permission.READ_ONLY,
            Permission.VIEW_DASHBOARD
        ]
    }
    
    # Mapeo de permisos a roles mínimos requeridos
    PERMISSION_REQUIREMENTS = {
        Permission.READ_ONLY: Role.VIEWER,
        Permission.READ_LIMITED: Role.USER,
        Permission.READ: Role.USER,
        Permission.CREATE: Role.MANAGER,
        Permission.UPDATE: Role.MANAGER,
        Permission.DELETE: Role.ADMIN,
        Permission.CREATE_ORDERS: Role.USER,
        Permission.MANAGE_USERS: Role.ADMIN,
        Permission.MANAGE_PRODUCTS: Role.MANAGER,
        Permission.MANAGE_CATEGORIES: Role.MANAGER,
        Permission.MANAGE_STOCK: Role.MANAGER,
        Permission.MANAGE_ORDERS: Role.MANAGER,
        Permission.MANAGE_PURCHASES: Role.MANAGER,
        Permission.VIEW_REPORTS: Role.USER,
        Permission.MANAGE_SYSTEM: Role.ADMIN,
        Permission.ALL: Role.ADMIN
    }
    
    @classmethod
    def get_user_permissions(cls, user_role: str) -> Set[Permission]:
        """Obtiene todos los permisos de un rol"""
        try:
            role = Role(user_role)
            return set(cls.ROLE_PERMISSIONS.get(role, []))
        except ValueError:
            return set()
    
    @classmethod
    def has_permission(cls, user_role: str, permission: Permission) -> bool:
        """Verifica si un rol tiene un permiso específico"""
        user_permissions = cls.get_user_permissions(user_role)
        return permission in user_permissions or Permission.ALL in user_permissions
    
    @classmethod
    def has_role_level(cls, user_role: str, required_level: PermissionLevel) -> bool:
        """Verifica si un rol tiene el nivel mínimo requerido"""
        try:
            role = Role(user_role)
            user_level = cls.ROLE_HIERARCHY.get(role, PermissionLevel.VIEWER)
            return user_level.value >= required_level.value
        except ValueError:
            return False
    
    @classmethod
    def can_access_endpoint(cls, user_role: str, endpoint: str) -> bool:
        """Verifica si un usuario puede acceder a un endpoint específico"""
        # Mapeo de endpoints a permisos requeridos
        endpoint_permissions = {
            '/api/users/': Permission.MANAGE_USERS,
            '/api/system/': Permission.MANAGE_SYSTEM,
            '/api/backup/': Permission.MANAGE_SYSTEM,
            '/api/products/': Permission.MANAGE_PRODUCTS,
            '/api/categories/': Permission.MANAGE_CATEGORIES,
            '/api/stock/': Permission.MANAGE_STOCK,
            '/api/orders/': Permission.MANAGE_ORDERS,
            '/api/purchases/': Permission.MANAGE_PURCHASES,
            '/api/reports/': Permission.VIEW_REPORTS,
            '/api/dashboard/': Permission.READ,
            '/api/analytics/': Permission.READ
        }
        
        # Buscar el permiso requerido para el endpoint
        for path, required_permission in endpoint_permissions.items():
            if endpoint.startswith(path):
                return cls.has_permission(user_role, required_permission)
        
        # Por defecto, permitir acceso a usuarios autenticados
        return True
    
    @classmethod
    def get_role_display_name(cls, role: str) -> str:
        """Obtiene el nombre de visualización de un rol"""
        role_names = {
            Role.ADMIN.value: 'Administrador',
            Role.MANAGER.value: 'Gerente',
            Role.SUPERVISOR.value: 'Supervisor',
            Role.USER.value: 'Usuario',
            Role.VIEWER.value: 'Viewer'
        }
        return role_names.get(role, 'Rol Desconocido')
    
    @classmethod
    def get_role_level(cls, role: str) -> int:
        """Obtiene el nivel numérico de un rol"""
        try:
            role_enum = Role(role)
            return cls.ROLE_HIERARCHY.get(role_enum, PermissionLevel.VIEWER).value
        except ValueError:
            return 0

def require_permission(permission: Permission):
    """Decorador para requerir un permiso específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                
                # Obtener información del usuario desde la base de datos
                from app.middleware.auth_middleware import get_user_by_id_direct
                current_user = get_user_by_id_direct(current_user_id)
                
                if not current_user or not current_user['is_active']:
                    return jsonify({'error': 'Usuario no válido o inactivo'}), 401
                
                user_role = current_user['role']
                
                if not PermissionManager.has_permission(user_role, permission):
                    return jsonify({
                        'error': f'Permiso insuficiente: {permission.value}',
                        'required_permission': permission.value,
                        'user_role': user_role
                    }), 403
                
                request.current_user = current_user
                return f(*args, **kwargs)
                
            except Exception as e:
                current_app.logger.warning(f"Verificación de permisos fallida: {str(e)}")
                return jsonify({'error': 'Autenticación requerida'}), 401
        
        return decorated_function
    return decorator

def require_role(role: Role):
    """Decorador para requerir un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                
                from app.middleware.auth_middleware import get_user_by_id_direct
                current_user = get_user_by_id_direct(current_user_id)
                
                if not current_user or not current_user['is_active']:
                    return jsonify({'error': 'Usuario no válido o inactivo'}), 401
                
                user_role = current_user['role']
                required_level = PermissionManager.ROLE_HIERARCHY.get(role, PermissionLevel.VIEWER)
                
                if not PermissionManager.has_role_level(user_role, required_level):
                    return jsonify({
                        'error': f'Rol insuficiente: se requiere {role.value} o superior',
                        'required_role': role.value,
                        'user_role': user_role
                    }), 403
                
                request.current_user = current_user
                return f(*args, **kwargs)
                
            except Exception as e:
                current_app.logger.warning(f"Verificación de rol fallida: {str(e)}")
                return jsonify({'error': 'Autenticación requerida'}), 401
        
        return decorated_function
    return decorator

def require_any_role(*roles: Role):
    """Decorador para requerir cualquiera de los roles especificados"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                
                from app.middleware.auth_middleware import get_user_by_id_direct
                current_user = get_user_by_id_direct(current_user_id)
                
                if not current_user or not current_user['is_active']:
                    return jsonify({'error': 'Usuario no válido o inactivo'}), 401
                
                user_role = current_user['role']
                
                # Verificar si el usuario tiene alguno de los roles requeridos
                has_required_role = any(
                    PermissionManager.has_role_level(user_role, PermissionManager.ROLE_HIERARCHY.get(role, PermissionLevel.VIEWER))
                    for role in roles
                )
                
                if not has_required_role:
                    required_roles = [role.value for role in roles]
                    return jsonify({
                        'error': f'Rol insuficiente: se requiere uno de {required_roles}',
                        'required_roles': required_roles,
                        'user_role': user_role
                    }), 403
                
                request.current_user = current_user
                return f(*args, **kwargs)
                
            except Exception as e:
                current_app.logger.warning(f"Verificación de roles fallida: {str(e)}")
                return jsonify({'error': 'Autenticación requerida'}), 401
        
        return decorated_function
    return decorator

# Decoradores de conveniencia
def admin_required(f):
    """Decorador que requiere rol de administrador"""
    return require_role(Role.ADMIN)(f)

def manager_or_above_required(f):
    """Decorador que requiere rol de manager o superior"""
    return require_any_role(Role.ADMIN, Role.MANAGER)(f)

def supervisor_or_above_required(f):
    """Decorador que requiere rol de supervisor o superior"""
    return require_any_role(Role.ADMIN, Role.MANAGER, Role.SUPERVISOR)(f)

def user_or_above_required(f):
    """Decorador que requiere rol de user o superior"""
    return require_any_role(Role.ADMIN, Role.MANAGER, Role.SUPERVISOR, Role.USER)(f)

def viewer_or_above_required(f):
    """Decorador que requiere rol de viewer o superior"""
    return require_any_role(Role.ADMIN, Role.MANAGER, Role.SUPERVISOR, Role.USER, Role.VIEWER)(f)
