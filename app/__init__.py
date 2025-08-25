from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from .database import db
from .config import Config

def create_app():
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    app.config.from_object(Config)
    
    # Configurar CORS para permitir peticiones desde el frontend
    CORS(app, resources={r"/api/*": {"origins": app.config["CORS_ORIGINS"]}})

    # Inicializar SQLAlchemy PRIMERO
    db.init_app(app)
    
    # Configurar Flask-Migrate
    migrate = Migrate(app, db)
    
    # Configurar JWT
    jwt = JWTManager(app)
    
    # Configuración adicional de JWT
    app.config['JWT_TOKEN_LOCATION'] = ['headers']
    app.config['JWT_HEADER_NAME'] = 'Authorization'
    app.config['JWT_HEADER_TYPE'] = 'Bearer'
    
    # Loaders de JWT para manejar identidad y carga de usuario
    @jwt.user_identity_loader
    def user_identity_lookup(user_or_id):
        """Convierte la identidad del usuario a string para PyJWT 2.x"""
        return str(user_or_id)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Carga automáticamente el usuario desde el token JWT"""
        from app.models.user import User
        identity = jwt_data["sub"]  # viene como string
        return User.query.get(int(identity))
    
    # Error handlers de JWT para respuestas consistentes con flask-smorest
    @jwt.unauthorized_loader
    def missing_token(reason):
        """Maneja tokens JWT faltantes"""
        from flask import jsonify
        return jsonify(message="JWT requerido", detail=reason), 401
    
    @jwt.invalid_token_loader
    def invalid_token(reason):
        """Maneja tokens JWT inválidos"""
        from flask import jsonify
        return jsonify(message="Token inválido", detail=reason), 401
    
    @jwt.expired_token_loader
    def expired_token(jwt_header, jwt_payload):
        """Maneja tokens JWT expirados"""
        from flask import jsonify
        return jsonify(message="Token expirado"), 401
    
    @jwt.revoked_token_loader
    def revoked_token_callback(jwt_header, jwt_payload):
        """Maneja tokens JWT revocados"""
        from flask import jsonify
        return jsonify(message="Token revocado"), 401

    # Crear contexto de aplicación para importar modelos
    with app.app_context():
        # Importar modelos DESPUÉS de inicializar db y dentro del contexto
        from .models.user import User
        from .models.category import Category
        from .models.product import Product
        from .models.stock import Stock
        from .models.order import Order
        from .models.order_item import OrderItem
        from .models.purchase_order import PurchaseOrder

        # Importar rutas DESPUÉS de importar modelos
        from .routes.frontend import frontend_bp
        
        # Inicializar API con flask-smorest
        from .api import init_api

        # Registrar blueprints
        app.register_blueprint(frontend_bp)
        
        # Inicializar API con flask-smorest
        init_api(app)

        # Crear tablas si no existen
        try:
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"⚠️  Advertencia al crear tablas: {e}")
    
    return app