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
    app.config["API_VERSION"] = "v1.0.0"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist@5.9.0/"
    app.config["OPENAPI_SWAGGER_UI_CONFIG"] = {
        "dom_id": "#swagger-ui",
        "layout": "BaseLayout",
        "deepLinking": True,
        "showExtensions": True,
        "showCommonExtensions": True,
        "defaultModelsExpandDepth": 1,
        "defaultModelExpandDepth": 1,
        "defaultModelRendering": "example",
        "displayRequestDuration": True,
        "docExpansion": "list",
        "filter": True,
        "showMutatedRequest": True,
        "showRequestHeaders": True,
        "showResponseHeaders": True,
        "syntaxHighlight.theme": "monokai",
        "tryItOutEnabled": True,
        "requestInterceptor": "function(request) { console.log('Request:', request); return request; }",
        "responseInterceptor": "function(response) { console.log('Response:', response); return response; }"
    }
    
    # Configuración de documentación
    app.config["OPENAPI_JSON_PATH"] = "api-spec.json"
    app.config["OPENAPI_YAML_PATH"] = "api-spec.yaml"
    
    # Configuración de esquemas
    app.config["OPENAPI_SPEC_COMPONENTS"] = {
        "securitySchemes": {
            "bearerAuth": {
                "type": "http",
                "scheme": "bearer",
                "bearerFormat": "JWT",
                "description": "Ingresa tu token JWT en el formato: Bearer <token>"
            }
        },
        "schemas": {
            "Error": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Mensaje de error descriptivo"
                    },
                    "errors": {
                        "type": "object",
                        "description": "Detalles de errores de validación"
                    },
                    "status_code": {
                        "type": "integer",
                        "description": "Código de estado HTTP"
                    }
                }
            },
            "Success": {
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Mensaje de éxito"
                    },
                    "data": {
                        "type": "object",
                        "description": "Datos de la respuesta"
                    }
                }
            }
        }
    }
    
    # Configuración de seguridad global
    app.config["OPENAPI_SPEC_COMPONENTS"]["security"] = [
        {"bearerAuth": []}
    ]
    
    # Configuración de información de contacto
    app.config["OPENAPI_SPEC_INFO"] = {
        "title": "Sistema de Gestión de Inventario API",
        "version": "v1.0.0",
        "description": """
## 📖 Descripción

API completa para el Sistema de Gestión de Inventario que permite gestionar productos, categorías, stock, órdenes de compra/venta y usuarios de manera eficiente y profesional.

## 🚀 Características Principales

- **Gestión de Productos**: CRUD completo con categorías y precios
- **Control de Stock**: Inventario en tiempo real con alertas de stock bajo
- **Órdenes de Venta**: Sistema completo de ventas con validaciones de negocio
- **Órdenes de Compra**: Gestión de compras y reposición de inventario
- **Autenticación JWT**: Sistema seguro de usuarios y roles
- **Validaciones de Negocio**: Reglas que garantizan la integridad de los datos

## 🔐 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación:

1. **Login**: `POST /api/auth/login` con credenciales
2. **Autorización**: Incluir `Authorization: Bearer <token>` en headers
3. **Refresh**: `POST /api/auth/refresh` para renovar tokens

## 📚 Endpoints Principales

- **Productos**: `/api/products` - Gestión completa de productos
- **Categorías**: `/api/categories` - Organización de productos
- **Stock**: `/api/stock` - Control de inventario
- **Órdenes**: `/api/orders` - Gestión de ventas
- **Compras**: `/api/purchases` - Gestión de compras
- **Usuarios**: `/api/auth` - Autenticación y gestión de usuarios

## 🧪 Testing

Puedes probar todos los endpoints directamente desde esta interfaz Swagger UI. Para endpoints protegidos:

1. Haz clic en el botón "Authorize" (🔒)
2. Ingresa tu token JWT: `Bearer <tu-token>`
3. ¡Listo para probar todos los endpoints!

## 📊 Códigos de Respuesta

- **200**: Operación exitosa
- **201**: Recurso creado exitosamente
- **400**: Error de validación o datos incorrectos
- **401**: No autorizado (token inválido o expirado)
- **403**: Prohibido (sin permisos suficientes)
- **404**: Recurso no encontrado
- **500**: Error interno del servidor

## 🔗 Enlaces Útiles

- **Documentación JSON**: [OpenAPI JSON](/api-spec.json)
- **Documentación YAML**: [OpenAPI YAML](/api-spec.yaml)
- **Repositorio**: [GitHub](https://github.com/USERNAME/REPO_NAME)
- **README**: [Documentación del Proyecto](https://github.com/USERNAME/REPO_NAME#readme)

## 🆘 Soporte

Si tienes preguntas o necesitas ayuda:

1. Revisa la documentación del proyecto
2. Consulta los ejemplos de uso
3. Abre un issue en el repositorio
        """,
        "contact": {
            "name": "Equipo de Desarrollo",
            "email": "dev@empresa.com",
            "url": "https://github.com/USERNAME/REPO_NAME"
        },
        "license": {
            "name": "MIT License",
            "url": "https://opensource.org/licenses/MIT"
        },
        "termsOfService": "https://github.com/USERNAME/REPO_NAME/blob/main/LICENSE"
    }
    
    # Configuración de servidores
    app.config["OPENAPI_SPEC_SERVERS"] = [
        {
            "url": "http://localhost:5000",
            "description": "Servidor de desarrollo local"
        },
        {
            "url": "https://api.empresa.com",
            "description": "Servidor de producción"
        }
    ]
    
    # Configuración de tags para organizar endpoints
    app.config["OPENAPI_SPEC_TAGS"] = [
        {
            "name": "Autenticación",
            "description": "Endpoints para autenticación y gestión de usuarios"
        },
        {
            "name": "Productos",
            "description": "Gestión completa de productos y categorías"
        },
        {
            "name": "Stock",
            "description": "Control de inventario y alertas de stock"
        },
        {
            "name": "Órdenes",
            "description": "Gestión de órdenes de venta con validaciones de negocio"
        },
        {
            "name": "Compras",
            "description": "Gestión de órdenes de compra y reposición"
        },
        {
            "name": "Reportes",
            "description": "Reportes y estadísticas del sistema"
        }
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
