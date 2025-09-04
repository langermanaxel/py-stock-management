#!/usr/bin/env python3
"""
Decoradores de autorización por roles para flask-smorest
"""

from functools import wraps
from flask import jsonify, request
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
import sqlite3
from pathlib import Path

def get_user_role_from_db(user_id):
    """Obtiene el rol del usuario desde la base de datos"""
    try:
        db_path = Path("instance/stock_management.db")
        if not db_path.exists():
            return None
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("SELECT role FROM users WHERE id = ? AND is_active = 1", (user_id,))
        result = cursor.fetchone()
        conn.close()
        
        return result[0] if result else None
        
    except Exception as e:
        print(f"Error obteniendo rol del usuario: {e}")
        return None

def roles_required(*allowed_roles):
    """
    Decorador que verifica que el usuario tenga uno de los roles permitidos
    
    Args:
        *allowed_roles: Roles permitidos para acceder al endpoint
        
    Ejemplo:
        @roles_required("admin", "gerente", "usuario")
        def my_endpoint():
            ...
    """
    def wrapper(fn):
        @wraps(fn)
        def inner(*args, **kwargs):
            try:
                verify_jwt_in_request()
                user_id = get_jwt_identity()
                user_role = get_user_role_from_db(user_id)
                
                if not user_role:
                    return jsonify(message="Usuario no válido o inactivo"), 401
                
                if user_role not in allowed_roles:
                    return jsonify(
                        message="Permisos insuficientes", 
                        detail=f"Rol '{user_role}' no tiene acceso a este recurso",
                        required_roles=list(allowed_roles)
                    ), 403
                
                return fn(*args, **kwargs)
            except Exception as e:
                return jsonify(message="Error de autenticación"), 401
        return inner
    return wrapper

def admin_required(fn):
    """Decorador que requiere rol de administrador"""
    return roles_required("admin")(fn)

def manager_or_admin_required(fn):
    """Decorador que requiere rol de manager o administrador"""
    return roles_required("admin", "manager")(fn)

def supervisor_or_above_required(fn):
    """Decorador que requiere rol de supervisor o superior"""
    return roles_required("admin", "manager", "supervisor")(fn)

def user_or_above_required(fn):
    """Decorador que requiere rol de user o superior"""
    return roles_required("admin", "manager", "supervisor", "user")(fn)

def viewer_or_above_required(fn):
    """Decorador que requiere rol de viewer o superior"""
    return roles_required("admin", "manager", "supervisor", "user", "viewer")(fn)

def active_user_required(fn):
    """
    Decorador que solo verifica que el usuario esté autenticado y activo
    No verifica roles específicos
    """
    @wraps(fn)
    def inner(*args, **kwargs):
        try:
            verify_jwt_in_request()
            user_id = get_jwt_identity()
            user_role = get_user_role_from_db(user_id)
            
            if not user_role:
                return jsonify(message="Usuario no válido o inactivo"), 401
            
            return fn(*args, **kwargs)
        except Exception as e:
            return jsonify(message="Error de autenticación"), 401
    return inner
