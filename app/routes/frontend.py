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
            flash('Usuario o contraseña incorrectos', 'error')
    
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
            flash('La contraseña debe tener al menos 6 caracteres', 'error')
        else:
            user.set_password(new_password)
            from app.database import db
            db.session.commit()
            flash('Contraseña cambiada exitosamente', 'success')
            return redirect(url_for('frontend.profile'))
    
    return render_template('change_password.html')

# Función helper para obtener usuario actual en templates
@frontend_bp.context_processor
def inject_user():
    """Inyecta el usuario actual en todos los templates"""
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
        return {'current_user': user}
    return {'current_user': None} 