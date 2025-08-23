#!/usr/bin/env python3
"""
Rutas del Frontend con Autenticación Básica
"""

from flask import Blueprint, render_template, request, redirect, url_for, session, flash, jsonify
from functools import wraps
from app.models.user import User
from werkzeug.security import check_password_hash
import os

frontend_bp = Blueprint('frontend', __name__)

# Configuración de sesión
frontend_bp.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

def login_required(f):
    """Decorador para requerir autenticación en rutas del frontend"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Debes iniciar sesión para acceder a esta página', 'error')
            return redirect(url_for('frontend.login'))
        return f(*args, **kwargs)
    return decorated_function

def permission_required(permission):
    """Decorador para requerir permisos específicos"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión para acceder a esta página', 'error')
                return redirect(url_for('frontend.login'))
            
            user = User.query.get(session['user_id'])
            if not user or not user.is_active:
                session.clear()
                flash('Sesión inválida, por favor inicia sesión nuevamente', 'error')
                return redirect(url_for('frontend.login'))
            
            if not user.has_permission(permission):
                flash('No tienes permisos para acceder a esta página', 'error')
                return redirect(url_for('frontend.index'))
            
            return f(*args, **kwargs)
        return decorator
    return decorator

def role_required(role):
    """Decorador para requerir un rol específico"""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if 'user_id' not in session:
                flash('Debes iniciar sesión para acceder a esta página', 'error')
                return redirect(url_for('frontend.login'))
            
            user = User.query.get(session['user_id'])
            if not user or not user.is_active:
                session.clear()
                flash('Sesión inválida, por favor inicia sesión nuevamente', 'error')
                return redirect(url_for('frontend.login'))
            
            if user.role != role and not user.is_admin():
                flash(f'Se requiere rol de {role} para acceder a esta página', 'error')
                return redirect(url_for('frontend.index'))
            
            return f(*args, **kwargs)
        return decorator
    return decorator

@frontend_bp.route('/')
@login_required
def index():
    """Página principal - requiere autenticación"""
    user = User.query.get(session['user_id'])
    return render_template('index.html', user=user)

@frontend_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login"""
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if not username or not password:
            flash('Usuario y contraseña son requeridos', 'error')
            return render_template('login.html')
        
        user = User.get_by_username(username)
        if user and user.check_password(password) and user.is_active:
            session['user_id'] = user.id
            session['username'] = user.username
            session['role'] = user.role
            session['permissions'] = user.get_permissions()
            
            flash(f'¡Bienvenido, {user.first_name}!', 'success')
            return redirect(url_for('frontend.index'))
        else:
            flash('Credenciales inválidas o usuario inactivo', 'error')
    
    return render_template('login.html')

@frontend_bp.route('/logout')
def logout():
    """Cerrar sesión"""
    session.clear()
    flash('Has cerrado sesión exitosamente', 'success')
    return redirect(url_for('frontend.login'))

@frontend_bp.route('/profile')
@login_required
def profile():
    """Página de perfil del usuario"""
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@frontend_bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Cambiar contraseña"""
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')
        
        user = User.query.get(session['user_id'])
        
        if not user.check_password(current_password):
            flash('Contraseña actual incorrecta', 'error')
        elif new_password != confirm_password:
            flash('Las contraseñas nuevas no coinciden', 'error')
        elif len(new_password) < 6:
            flash('La nueva contraseña debe tener al menos 6 caracteres', 'error')
        else:
            user.set_password(new_password)
            user.save()
            flash('Contraseña cambiada exitosamente', 'success')
            return redirect(url_for('frontend.profile'))
    
    return render_template('change_password.html')

# Rutas protegidas por permisos específicos
@frontend_bp.route('/admin')
@role_required('admin')
def admin_panel():
    """Panel de administración - solo para admins"""
    user = User.query.get(session['user_id'])
    return render_template('admin.html', user=user)

@frontend_bp.route('/users')
@permission_required('manage_users')
def user_management():
    """Gestión de usuarios - requiere permisos"""
    user = User.query.get(session['user_id'])
    users = User.query.all()
    return render_template('users.html', user=user, users=users)

# Rutas de API del frontend (para operaciones CRUD)
@frontend_bp.route('/api/categories', methods=['POST'])
@permission_required('write')
def create_category():
    """Crear categoría - requiere permisos de escritura"""
    from app.routes.categories import create_category as api_create_category
    return api_create_category()

@frontend_bp.route('/api/categories/<int:category_id>', methods=['PUT', 'DELETE'])
@permission_required('write')
def manage_category(category_id):
    """Gestionar categoría - requiere permisos de escritura"""
    from app.routes.categories import update_category, delete_category
    
    if request.method == 'PUT':
        return update_category(category_id)
    elif request.method == 'DELETE':
        return delete_category(category_id)

@frontend_bp.route('/api/products', methods=['POST'])
@permission_required('write')
def create_product():
    """Crear producto - requiere permisos de escritura"""
    from app.routes.products import create_product as api_create_product
    return api_create_product()

@frontend_bp.route('/api/products/<int:product_id>', methods=['PUT', 'DELETE'])
@permission_required('write')
def manage_product(product_id):
    """Gestionar producto - requiere permisos de escritura"""
    from app.routes.products import update_product, delete_product
    
    if request.method == 'PUT':
        return update_product(product_id)
    elif request.method == 'DELETE':
        return delete_product(product_id)

@frontend_bp.route('/api/stock', methods=['POST', 'PUT'])
@permission_required('write')
def manage_stock():
    """Gestionar stock - requiere permisos de escritura"""
    from app.routes.stock import create_stock, update_stock
    
    if request.method == 'POST':
        return create_stock()
    elif request.method == 'PUT':
        stock_id = request.json.get('id')
        return update_stock(stock_id)

@frontend_bp.route('/api/orders', methods=['POST'])
@permission_required('write')
def create_order():
    """Crear orden - requiere permisos de escritura"""
    from app.routes.orders import create_order as api_create_order
    return api_create_order()

@frontend_bp.route('/api/orders/<int:order_id>', methods=['PUT', 'DELETE'])
@permission_required('write')
def manage_order(order_id):
    """Gestionar orden - requiere permisos de escritura"""
    from app.routes.orders import update_order, delete_order
    
    if request.method == 'PUT':
        return update_order(order_id)
    elif request.method == 'DELETE':
        return delete_order(order_id)

@frontend_bp.route('/api/orders/<int:order_id>/complete', methods=['POST'])
@permission_required('write')
def complete_order(order_id):
    """Completar orden - requiere permisos de escritura"""
    from app.routes.orders import complete_order as api_complete_order
    return api_complete_order(order_id)

@frontend_bp.route('/api/purchases', methods=['POST'])
@permission_required('write')
def create_purchase():
    """Crear orden de compra - requiere permisos de escritura"""
    from app.routes.purchases import create_purchase as api_create_purchase
    return api_create_purchase()

@frontend_bp.route('/api/purchases/<int:purchase_id>', methods=['PUT', 'DELETE'])
@permission_required('write')
def manage_purchase(purchase_id):
    """Gestionar orden de compra - requiere permisos de escritura"""
    from app.routes.purchases import update_purchase, delete_purchase
    
    if request.method == 'PUT':
        return update_purchase(purchase_id)
    elif request.method == 'DELETE':
        return delete_purchase(purchase_id)

# Rutas de solo lectura (no requieren permisos especiales)
@frontend_bp.route('/api/categories', methods=['GET'])
@login_required
def get_categories():
    """Obtener categorías - solo requiere autenticación"""
    from app.routes.categories import get_categories as api_get_categories
    return api_get_categories()

@frontend_bp.route('/api/products', methods=['GET'])
@login_required
def get_products():
    """Obtener productos - solo requiere autenticación"""
    from app.routes.products import get_products as api_get_products
    return api_get_products()

@frontend_bp.route('/api/stock', methods=['GET'])
@login_required
def get_stock():
    """Obtener stock - solo requiere autenticación"""
    from app.routes.stock import get_stock as api_get_stock
    return api_get_stock()

@frontend_bp.route('/api/orders', methods=['GET'])
@login_required
def get_orders():
    """Obtener órdenes - solo requiere autenticación"""
    from app.routes.orders import get_orders as api_get_orders
    return api_get_orders()

@frontend_bp.route('/api/purchases', methods=['GET'])
@login_required
def get_purchases():
    """Obtener órdenes de compra - solo requiere autenticación"""
    from app.routes.purchases import get_purchases as api_get_purchases
    return api_get_purchases()

# Función helper para obtener usuario actual en templates
@frontend_bp.context_processor
def inject_user():
    """Inyecta el usuario actual en todos los templates"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None} 