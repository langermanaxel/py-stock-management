#!/usr/bin/env python3
"""
Rutas del Frontend para el Sistema de Gestión de Inventario
"""

from flask import Blueprint, render_template, redirect, url_for, request, session
from flask_jwt_extended import jwt_required, get_jwt_identity
from functools import wraps

frontend_bp = Blueprint('frontend', __name__)

def login_required(f):
    """Decorador para verificar si el usuario está logueado"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # Verificar si hay token en localStorage (esto se hace en el frontend)
        # Por ahora solo renderizamos la página y el frontend se encarga de la validación
        return f(*args, **kwargs)
    return decorated_function

@frontend_bp.route('/')
def index():
    """Página principal - redirige al login"""
    return redirect(url_for('frontend.login'))

@frontend_bp.route('/login')
def login():
    """Página de login"""
    return render_template('login.html')

@frontend_bp.route('/dashboard')
@login_required
def dashboard():
    """Dashboard principal - requiere autenticación"""
    return render_template('dashboard.html')

@frontend_bp.route('/products')
@login_required
def products():
    """Página de productos"""
    return render_template('products.html')

@frontend_bp.route('/stock')
@login_required
def stock():
    """Página de stock"""
    return render_template('stock.html')

@frontend_bp.route('/categories')
@login_required
def categories():
    """Página de categorías"""
    return render_template('dashboard.html')  # Por ahora redirige al dashboard

@frontend_bp.route('/orders')
@login_required
def orders():
    """Página de órdenes"""
    return render_template('dashboard.html')  # Por ahora redirige al dashboard

@frontend_bp.route('/purchases')
@login_required
def purchases():
    """Página de compras"""
    return render_template('dashboard.html')  # Por ahora redirige al dashboard

@frontend_bp.route('/users')
@login_required
def users():
    """Página de usuarios"""
    return render_template('dashboard.html')  # Por ahora redirige al dashboard

@frontend_bp.route('/profile')
@login_required
def profile():
    """Página de perfil del usuario"""
    return render_template('dashboard.html')  # Por ahora redirige al dashboard 