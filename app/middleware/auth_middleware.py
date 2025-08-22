#!/usr/bin/env python3
"""
Middleware de Autenticación para el Sistema de Gestión de Inventario
Protege todas las rutas que requieren autenticación
"""

from functools import wraps
from flask import request, jsonify, current_app
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from app.models.user import User

def require_auth(f):
    """Decorador para requerir autenticación"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user or not current_user.is_active:
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
                current_user = User.query.get(current_user_id)
                
                if not current_user or not current_user.is_active:
                    return jsonify({'error': 'Usuario no válido o inactivo'}), 401
                
                if not current_user.has_permission(permission):
                    return jsonify({'error': 'Permiso denegado'}), 403
                
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
                current_user = User.query.get(current_user_id)
                
                if not current_user or not current_user.is_active:
                    return jsonify({'error': 'Usuario no válido o inactivo'}), 401
                
                if current_user.role != role and not current_user.is_admin():
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

def require_manager(f):
    """Decorador para requerir rol de gerente o superior"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            current_user = User.query.get(current_user_id)
            
            if not current_user or not current_user.is_active:
                return jsonify({'error': 'Usuario no válido o inactivo'}), 401
            
            if not current_user.is_manager():
                return jsonify({'error': 'Se requiere rol de gerente o superior'}), 403
            
            request.current_user = current_user
            return f(*args, **kwargs)
        except Exception as e:
            current_app.logger.warning(f"Verificación de gerente fallida: {str(e)}")
            return jsonify({'error': 'Autenticación requerida'}), 401
    
    return decorated_function

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
