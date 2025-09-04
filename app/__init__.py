from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager, verify_jwt_in_request
from .database import db
from .config import Config
from functools import wraps

def create_app():
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    app.config.from_object(Config)
    
    # Configurar CORS para permitir peticiones desde el frontend
    CORS(app, 
         resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}},
         supports_credentials=True,
         allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
         methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'],
         expose_headers=['Set-Cookie', 'Authorization'])

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
    
    # Configurar JWT para ser más permisivo con endpoints de auth
    app.config['JWT_ACCESS_CSRF_HEADER_NAME'] = 'X-CSRF-TOKEN'
    app.config['JWT_REFRESH_CSRF_HEADER_NAME'] = 'X-CSRF-TOKEN'
    
    # Configurar expiración de tokens JWT
    from datetime import timedelta
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)  # 1 hora
    app.config['JWT_REFRESH_TOKEN_EXPIRES'] = timedelta(days=7)  # 7 días
    
    # Crear un decorador personalizado para excluir endpoints de JWT
    def jwt_optional_if_no_token(f):
        """Decorador que hace JWT opcional si no hay token"""
        @wraps(f)
        def decorated_function(*args, **kwargs):
            try:
                # Intentar verificar JWT
                verify_jwt_in_request()
                return f(*args, **kwargs)
            except:
                # Si no hay token válido, continuar sin autenticación
                return f(*args, **kwargs)
        return decorated_function
    
    # Loaders de JWT para manejar identidad y carga de usuario
    @jwt.user_identity_loader
    def user_identity_lookup(user_or_id):
        """Convierte la identidad del usuario a string para PyJWT 2.x"""
        return str(user_or_id)
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        """Carga automáticamente el usuario desde el token JWT usando SQLite directo"""
        try:
            import sqlite3
            from pathlib import Path
            
            identity = jwt_data["sub"]  # viene como string
            user_id = int(identity)
            
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
                # Crear un objeto similar a User para compatibilidad
                class MockUser:
                    def __init__(self, data):
                        self.id = data[0]
                        self.username = data[1]
                        self.email = data[2]
                        self.password_hash = data[3]
                        self.first_name = data[4]
                        self.last_name = data[5]
                        self.role = data[6]
                        self.is_active = bool(data[7])
                        self.created_at = data[8]
                        self.updated_at = data[9]
                        self.last_login = data[10]
                    
                    def to_dict(self):
                        return {
                            'id': self.id,
                            'username': self.username,
                            'email': self.email,
                            'first_name': self.first_name,
                            'last_name': self.last_name,
                            'role': self.role,
                            'is_active': self.is_active,
                            'created_at': self.created_at,
                            'updated_at': self.updated_at,
                            'last_login': self.last_login
                        }
                
                return MockUser(user_data)
            
            return None
            
        except Exception as e:
            print(f"Error en user_lookup_callback: {e}")
            return None
    
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

        # NO crear tablas automáticamente aquí - usar scripts separados
        # Las tablas ya están creadas por create_working_database.py
    
    return app