# ========================================
# DECORADORES PARA CORS EN LA API
# ========================================

from flask import request, make_response
from functools import wraps
from flask_smorest import abort

def add_cors_headers(response):
    """Agregar headers CORS a la respuesta"""
    if hasattr(response, 'headers'):
        response.headers['Access-Control-Allow-Origin'] = '*'
        response.headers['Access-Control-Allow-Methods'] = 'GET, POST, PUT, DELETE, OPTIONS, PATCH'
        response.headers['Access-Control-Allow-Headers'] = 'Content-Type, Authorization, X-Requested-With'
        response.headers['Access-Control-Allow-Credentials'] = 'true'
        response.headers['Access-Control-Max-Age'] = '86400'  # 24 horas
    return response

def handle_cors_preflight():
    """Manejar peticiones OPTIONS (preflight) para CORS"""
    if request.method == 'OPTIONS':
        response = make_response()
        response = add_cors_headers(response)
        response.status_code = 200
        return response

def cors_enabled(f):
    """Decorador para habilitar CORS en endpoints de la API"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Manejar preflight request
        if request.method == 'OPTIONS':
            return handle_cors_preflight()
        
        # Ejecutar la función original
        try:
            result = f(*args, **kwargs)
            
            # Si es una respuesta, agregar headers CORS
            if hasattr(result, 'headers'):
                result = add_cors_headers(result)
            
            return result
        except Exception as e:
            # Manejar errores y agregar headers CORS
            if hasattr(e, 'response'):
                e.response = add_cors_headers(e.response)
            raise e
    
    return decorated_function

def api_cors_enabled(f):
    """Decorador específico para endpoints de la API con CORS"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Agregar headers CORS a la respuesta
        response = f(*args, **kwargs)
        
        if response:
            response = add_cors_headers(response)
        
        return response
    
    return decorated_function
