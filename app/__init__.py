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
    CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:8080", "http://localhost:8080"]}})

    # Inicializar SQLAlchemy PRIMERO
    db.init_app(app)
    
    # Configurar Flask-Migrate
    migrate = Migrate(app, db)
    
    # Configurar JWT
    jwt = JWTManager(app)

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
        from .routes.products import products_bp
        from .routes.stock import stock_bp
        from .routes.purchases import purchases_bp
        from .routes.categories import categories_bp
        from .routes.orders import orders_bp
        from .routes.auth import auth_bp
        
        # Inicializar API con flask-smorest
        from .api import init_api

        # Registrar blueprints
        app.register_blueprint(frontend_bp)
        # Los blueprints de API se registran a través de init_api()
        # app.register_blueprint(products_bp, url_prefix='/api/products')
        # app.register_blueprint(stock_bp, url_prefix='/api/stock')
        # app.register_blueprint(purchases_bp, url_prefix='/api/purchases')
        # app.register_blueprint(categories_bp, url_prefix='/api/categories')
        # app.register_blueprint(orders_bp, url_prefix='/api/orders')
        # app.register_blueprint(auth_bp, url_prefix='/api/auth')
        
        # Inicializar API con flask-smorest
        init_api(app)

        # Crear tablas si no existen
        try:
            db.create_all()
            print("✅ Base de datos inicializada correctamente")
        except Exception as e:
            print(f"⚠️  Advertencia al crear tablas: {e}")
    
    return app