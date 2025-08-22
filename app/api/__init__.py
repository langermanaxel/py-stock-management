# API endpoints con flask-smorest
from flask_smorest import Api
from .categories import categories_bp
from .products import products_bp
from .stock import stock_bp
from .orders import orders_bp
from .purchases import purchases_bp
from .auth import auth_bp

def init_api(app):
    """Inicializar API con flask-smorest"""
    api = Api(app)
    
    # Registrar blueprints de API
    api.register_blueprint(categories_bp, url_prefix='/api/categories')
    api.register_blueprint(products_bp, url_prefix='/api/products')
    api.register_blueprint(stock_bp, url_prefix='/api/stock')
    api.register_blueprint(orders_bp, url_prefix='/api/orders')
    api.register_blueprint(purchases_bp, url_prefix='/api/purchases')
    api.register_blueprint(auth_bp, url_prefix='/api/auth')
    
    return api
