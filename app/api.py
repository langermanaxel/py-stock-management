#!/usr/bin/env python3
"""
Configuración principal de la API con flask-smorest
"""

from flask_smorest import Api
from flask import Blueprint

# Crear blueprint principal de la API
api_bp = Blueprint('api', __name__, url_prefix='/api')

# Configurar flask-smorest
api = Api()

def init_api(app):
    """Inicializar la API con flask-smorest"""
    
    # Configuración de la API
    app.config["API_TITLE"] = "Sistema de Gestión de Inventario API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.2"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    
    # Configuración de documentación
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_YAML_PATH"] = "api-spec.yaml"
    
    # Configuración de esquemas
    app.config["OPENAPI_SPEC_COMPONENTS"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT"
            }
        }
    }
    
    # Configuración de seguridad global
    app.config["OPENAPI_SPEC_COMPONENTS"]["security"] = [
        {"bearerAuth": []}
    ]
    
    # Inicializar la API
    api.init_app(app)
    
    # Registrar el blueprint principal
    app.register_blueprint(api_bp)
    
    # Importar y registrar todos los endpoints
    from .api.categories import categories_blp
    from .api.products import products_blp
    from .api.stock import stock_blp
    from .api.orders import orders_blp
    from .api.purchases import purchases_blp
    from .api.auth import auth_blp
    
    # Registrar blueprints de la API
    api.register_blueprint(categories_blp)
    api.register_blueprint(products_blp)
    api.register_blueprint(stock_blp)
    api.register_blueprint(orders_blp)
    api.register_blueprint(purchases_blp)
    api.register_blueprint(auth_blp)
