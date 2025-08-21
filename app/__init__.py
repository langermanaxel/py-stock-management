from flask import Flask
from flask_cors import CORS
from flask_migrate import Migrate
from .database import db
from .config import Config

def create_app():
    app = Flask(__name__, 
                static_folder='../static',
                template_folder='../templates')
    app.config.from_object(Config)
    
    # Configurar CORS para permitir peticiones desde el frontend
    CORS(app, resources={r"/api/*": {"origins": ["http://127.0.0.1:8080", "http://localhost:8080"]}})

    db.init_app(app)
    
    # Configurar Flask-Migrate
    migrate = Migrate(app, db)

    # Importar modelos después de inicializar db
    from .models.category import Category
    from .models.product import Product
    from .models.stock import Stock
    from .models.order import Order
    from .models.order_item import OrderItem
    from .models.purchase_order import PurchaseOrder

    # Importar rutas después de importar modelos
    from .routes.frontend import frontend_bp
    from .routes.products import products_bp
    from .routes.stock import stock_bp
    from .routes.purchases import purchases_bp
    from .routes.categories import categories_bp
    from .routes.orders import orders_bp

    # Registrar blueprints
    app.register_blueprint(frontend_bp)
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(stock_bp, url_prefix='/api/stock')
    app.register_blueprint(purchases_bp, url_prefix='/api/purchases')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(orders_bp, url_prefix='/api/orders')

    # with app.app_context():
    #     db.create_all()
    
    return app