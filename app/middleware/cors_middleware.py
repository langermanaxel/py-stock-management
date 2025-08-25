# ========================================
# MIDDLEWARE PERSONALIZADO PARA CORS
# ========================================

from flask import request, make_response
from functools import wraps

def add_cors_headers(response):
    """Agregar headers CORS a la respuesta"""
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
    response.headers['Access-Control-Allow-Credentials'] = 'true'
    return response

def handle_preflight_request():
    """Manejar peticiones OPTIONS (preflight)"""
    if request.method == 'OPTIONS':
        response = make_response()
        response = add_cors_headers(response)
        response.status_code = 200
        return response

def cors_middleware(f):
    """Decorador para aplicar CORS a rutas específicas"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Manejar preflight request
        if request.method == 'OPTIONS':
            return handle_preflight_request()
        
        # Ejecutar la función original
        response = f(*args, **kwargs)
        
        # Agregar headers CORS si es una respuesta
        if hasattr(response, 'headers'):
            response = add_cors_headers(response)
        
        return response
    return decorated_function
