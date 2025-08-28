from .auth import auth_bp
from .products import products_bp
from .categories import categories_bp
from .stock import stock_bp
from .orders import orders_bp
from .purchases import purchases_bp
from .users import users_bp

__all__ = [
    'auth_bp',
    'products_bp', 
    'categories_bp',
    'stock_bp',
    'orders_bp',
    'purchases_bp',
    'users_bp'
]
