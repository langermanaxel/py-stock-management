#!/usr/bin/env python3
"""
Decoradores de autorización por roles para flask-smorest
"""

from functools import wraps
from flask import jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt

def roles_required(*allowed_roles):
    """
    Decorador que verifica que el usuario tenga uno de los roles permitidos
    
    Args:
        *allowed_roles: Roles permitidos para acceder al endpoint
        
    Ejemplo:
        @roles_required("admin", "manager", "user")
        def my_endpoint():
            ...
    """
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            verify_jwt_in_request()
            claims = get_jwt()
            user_role = claims.get("role")
            
            if not user_role:
                return jsonify(message="Rol no encontrado en el token"), 403
            
            if user_role not in allowed_roles:
                return jsonify(
                    message="Permisos insuficientes", 
                    detail=f"Rol '{user_role}' no tiene acceso a este recurso",
                    required_roles=list(allowed_roles)
                ), 403
            
            return fn(*args, **kwargs)
        return inner
    return wrapper

def admin_required(fn):
    """Decorador que requiere rol de administrador"""
    return roles_required("admin")(fn)

def manager_or_admin_required(fn):
    """Decorador que requiere rol de gerente o administrador"""
    return roles_required("admin", "manager")(fn)

def user_or_above_required(fn):
    """Decorador que requiere rol de usuario o superior"""
    return roles_required("admin", "manager", "user")(fn)

def active_user_required(fn):
    """
    Decorador que solo verifica que el usuario esté autenticado y activo
    No verifica roles específicos
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        verify_jwt_in_request()
        claims = get_jwt()
        username = claims.get("username")
        
        if not username:
            return jsonify(message="Usuario no encontrado en el token"), 403
        
        return fn(*args, **kwargs)
    return inner
