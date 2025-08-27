#!/usr/bin/env python3
"""
Middleware de Autenticación para el Sistema de Gestión de Inventario
Protege todas las rutas que requieren autenticación
"""

from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
import sqlite3
from pathlib import Path

def get_user_by_id_direct(user_id):
    """Obtiene usuario por ID usando SQLite directo"""
    try:
        db_path = Path("instance/stock_management.db")
        if not db_path.exists():
            return None
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, first_name, last_name, 
                   role, is_active, created_at, updated_at, last_login
            FROM users 
            WHERE id = ? AND is_active = 1
        """, (user_id,))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'password_hash': user_data[3],
                'first_name': user_data[4],
                'last_name': user_data[5],
                'role': user_data[6],
                'is_active': bool(user_data[7]),
                'created_at': user_data[8],
                'updated_at': user_data[9],
                'last_login': user_data[10]
            }
        
        return None
        
    except Exception as e:
        print(f"Error en get_user_by_id_direct: {e}")
        return None

def require_auth(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = get_user_by_id_direct(current_user_id)
            
            if not current_user or not current_user['is_active']:
                return jsonify({'error': 'Usuario no válido o inactivo'}), 401
            
            # Agregar usuario actual al contexto de la request
            request.current_user = current_user
            
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.warning(f"Autenticación fallida: {str(e)}")
            return jsonify({'error': 'Token de autenticación requerido'}), 401
    
    return decorated_function

def require_permission(permission):
    """Decorador para requerir permisos específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                current_user = get_user_by_id_direct(current_user_id)
                
                if not current_user or not current_user['is_active']:
                    return jsonify({'error': 'Usuario no válido o inactivo'}), 401
                
                # Verificar permisos basados en rol
                user_role = current_user['role']
                
                if permission == 'admin' and user_role != 'admin':
                    return jsonify({'error': 'Se requiere rol de administrador'}), 403
                elif permission == 'gerente' and user_role not in ['admin', 'gerente']:
                    return jsonify({'error': 'Se requiere rol de gerente o superior'}), 403
                elif permission == 'usuario' and user_role not in ['admin', 'gerente', 'usuario']:
                    return jsonify({'error': 'Se requiere rol de usuario o superior'}), 403
                elif permission == 'viewer' and user_role not in ['admin', 'gerente', 'usuario', 'viewer']:
                    return jsonify({'error': 'Se requiere rol de viewer o superior'}), 403
                
                request.current_user = current_user
                return f(*args, **kwargs)
            except Exception as e:
                current_app.logger.warning(f"Verificación de permisos fallida: {str(e)}")
                return jsonify({'error': 'Autenticación requerida'}), 401
        return decorated_function
    return decorator

def require_role(role):
    """Decorador para requerir un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                current_user_id = get_jwt_identity()
                current_user = get_user_by_id_direct(current_user_id)
                
                if not current_user or not current_user['is_active']:
                    return jsonify({'error': 'Usuario no válido o inactivo'}), 401
                
                if current_user['role'] != role and current_user['role'] != 'admin':
                    return jsonify({'error': 'Rol requerido no autorizado'}), 403
                
                request.current_user = current_user
                return f(*args, **kwargs)
            except Exception as e:
                current_app.logger.warning(f"Verificación de rol fallida: {str(e)}")
                return jsonify({'error': 'Autenticación requerida'}), 401
        return decorated_function
    return decorator

def require_admin(f):
    """Decorador para requerir rol de administrador"""
    return require_role('admin')(f)

def require_gerente(f):
    """Decorador para requerir rol de gerente o superior"""
    return require_permission('gerente')(f)

def require_usuario(f):
    """Decorador para requerir rol de usuario o superior"""
    return require_permission('usuario')(f)

def require_viewer(f):
    """Decorador para requerir rol de viewer o superior"""
    return require_permission('viewer')(f)

def can_access_endpoint(endpoint, user_role):
    """Verifica si un usuario puede acceder a un endpoint específico"""
    # Mapeo de endpoints a roles mínimos requeridos
    endpoint_permissions = {
        # Endpoints de administración (solo admin)
        '/api/users/': 'admin',
        '/api/system/': 'admin',
        '/api/backup/': 'admin',
        
        # Endpoints de gestión (admin y gerente)
        '/api/products/': 'gerente',
        '/api/categories/': 'gerente',
        '/api/stock/': 'gerente',
        '/api/orders/': 'gerente',
        '/api/purchases/': 'gerente',
        
        # Endpoints de usuario (admin, gerente, usuario)
        '/api/profile/': 'usuario',
        '/api/reports/': 'usuario',
        
        # Endpoints de visualización (todos los roles)
        '/api/dashboard/': 'viewer',
        '/api/analytics/': 'viewer'
    }
    
    # Buscar el permiso más restrictivo para el endpoint
    for path, required_role in endpoint_permissions.items():
        if endpoint.startswith(path):
            # Verificar jerarquía de roles
            role_hierarchy = {
                'viewer': 1,
                'usuario': 2,
                'gerente': 3,
                'admin': 4
            }
            
            user_level = role_hierarchy.get(user_role, 0)
            required_level = role_hierarchy.get(required_role, 0)
            
            return user_level >= required_level
    
    # Por defecto, permitir acceso a usuarios autenticados
    return True

def log_user_action(action):
    """Decorador para registrar acciones de usuario"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                if hasattr(request, 'current_user'):
                    current_app.logger.info(
                        f"Usuario {request.current_user.username} ({request.current_user.role}) "
                        f"ejecutó: {action} - {request.method} {request.path}"
                    )
            except:
                pass
            
            return f(*args, **kwargs)
        return decorated_function
    return decorator

def get_current_user():
    """Obtiene el usuario actual desde el contexto de la request"""
    return getattr(request, 'current_user', None)

def is_authenticated():
    """Verifica si el usuario está autenticado"""
    try:
        verify_jwt_in_request()
        return True
    except:
        return False

def require_auth_smart(f):
    """Decorador inteligente que verifica permisos automáticamente basado en la ruta"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = get_user_by_id_direct(current_user_id)
            
            if not current_user or not current_user['is_active']:
                return jsonify({'error': 'Usuario no válido o inactivo'}), 401
            
            # Verificar permisos basados en la ruta actual
            current_endpoint = request.path
            user_role = current_user['role']
            
            if not can_access_endpoint(current_endpoint, user_role):
                return jsonify({
                    'error': f'Acceso denegado. Se requiere rol superior a {user_role}',
                    'required_permission': 'Rol superior',
                    'current_role': user_role
                }), 403
            
            # Agregar usuario actual al contexto de la request
            request.current_user = current_user
            
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.warning(f"Autenticación inteligente fallida: {str(e)}")
            return jsonify({'error': 'Token de autenticación requerido'}), 401
    
    return decorated_function
