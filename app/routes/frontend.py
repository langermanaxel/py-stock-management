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

@frontend_bp.route('/')
def index():
    """Página principal - la autenticación se maneja en el frontend con JWT"""
    return render_template('index.html')

@frontend_bp.route('/login', methods=['GET'])
def login():
    """Página de login - la autenticación se maneja en el frontend con JWT"""
    return render_template('login.html')

@frontend_bp.route('/logout')
def logout():
    """Cerrar sesión - se maneja en el frontend con JWT"""
    return redirect(url_for('frontend.login'))

@frontend_bp.route('/profile')
def profile():
    """Página de perfil del usuario - se maneja en el frontend con JWT"""
    return render_template('profile.html')

@frontend_bp.route('/change-password', methods=['GET'])
def change_password():
    """Cambiar contraseña - se maneja en el frontend con JWT"""
    return render_template('change_password.html')

# Función helper para obtener usuario actual en templates
@frontend_bp.context_processor
def inject_user():
    """Inyecta el usuario actual en todos los templates"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None} 