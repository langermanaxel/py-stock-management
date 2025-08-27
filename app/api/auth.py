#!/usr/bin/env python3
"""
Endpoints de Autenticación con flask-smorest
"""

from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity
from app.database import db
from app.models.user import User
from app.schemas.user import UserSchema, UserCreateSchema, UserUpdateSchema, UserLoginSchema, UserListSchema
from app.middleware.auth_middleware import require_permission
import sqlite3
from pathlib import Path
from werkzeug.security import check_password_hash
from datetime import datetime

# Crear blueprint para autenticación
auth_blp = Blueprint(
    "auth", 
    __name__, 
    description="Operaciones de autenticación y usuarios"
)

def get_user_by_username_direct(username):
    """Obtiene usuario por username usando SQLite directo"""
    try:
        db_path = Path("instance/stock_management.db")
        if not db_path.exists():
            return None
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT id, username, email, password_hash, first_name, last_name, 
                   role, is_active, created_at, updated_at, last_login
            FROM users 
            WHERE username = ? AND is_active = 1
        """, (username,))
        
        user_data = cursor.fetchone()
        conn.close()
        
        if user_data:
            return {
                'id': user_data[0],
                'username': user_data[1],
                'email': user_data[2],
                'password_hash': user_data[3],
                'first_name': user_data[4],
                'last_name': user_data[5],
                'role': user_data[6],
                'is_active': bool(user_data[7]),
                'created_at': user_data[8],
                'updated_at': user_data[9],
                'last_login': user_data[10]
            }
        
        return None
        
    except Exception as e:
        print(f"Error en get_user_by_username_direct: {e}")
        return None

def update_last_login_direct(user_id):
    """Actualiza last_login usando SQLite directo"""
    try:
        db_path = Path("instance/stock_management.db")
        if not db_path.exists():
            return False
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        current_time = datetime.now().isoformat()
        cursor.execute("""
            UPDATE users 
            SET last_login = ?, updated_at = ?
            WHERE id = ?
        """, (current_time, current_time, user_id))
        
        conn.commit()
        conn.close()
        return True
        
    except Exception as e:
        print(f"Error en update_last_login_direct: {e}")
        return False

@auth_blp.route("/login")
class Login(MethodView):
    """Endpoint para login de usuario"""
    
    @auth_blp.arguments(UserLoginSchema)
    @auth_blp.response(200, description="Login exitoso")
    def post(self, login_data):
        """Login de usuario"""
        try:
            username = login_data["username"]
            password = login_data["password"]
            
            print(f"🔐 Intentando login para usuario: {username}")
            
            # Buscar usuario usando SQLite directo
            user = get_user_by_username_direct(username)
            if not user:
                print(f"❌ Usuario no encontrado: {username}")
                abort(401, message="Credenciales inválidas")
            
            print(f"✅ Usuario encontrado: {user['username']}")
            
            # Verificar contraseña
            if not check_password_hash(user['password_hash'], password):
                print(f"❌ Contraseña inválida para usuario: {username}")
                abort(401, message="Credenciales inválidas")
            
            print(f"✅ Contraseña válida para usuario: {username}")
            
            if not user['is_active']:
                print(f"❌ Usuario inactivo: {username}")
                abort(401, message="Usuario desactivado")
            
            # Actualizar último login
            update_last_login_direct(user['id'])
            print(f"✅ Last login actualizado para usuario: {username}")
            
            # Generar tokens
            access_token = create_access_token(
                identity=str(user['id']),  # Convertir a string para PyJWT 2.x
                additional_claims={"role": user['role'], "username": user['username']}
            )
            refresh_token = create_refresh_token(
                identity=str(user['id']),  # Convertir a string para PyJWT 2.x
                additional_claims={"role": user['role'], "username": user['username']}
            )
            
            print(f"✅ Tokens generados para usuario: {username}")
            
            return {
                "message": "Login exitoso",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": {
                    'id': user['id'],
                    'username': user['username'],
                    'email': user['email'],
                    'first_name': user['first_name'],
                    'last_name': user['last_name'],
                    'role': user['role'],
                    'is_active': user['is_active']
                }
            }
        except Exception as e:
            print(f"❌ Error en login: {e}")
            abort(500, message="Error interno del servidor")

@auth_blp.route("/refresh")
class Refresh(MethodView):
    """Endpoint para refrescar token"""
    
    @auth_blp.response(200, description="Token refrescado")
    @jwt_required(refresh=True)
    def post(self):
        """Refrescar token de acceso"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get(current_user_id)
            
            if not user or not user.is_active:
                abort(401, message="Usuario no válido")
            
            new_access_token = create_access_token(
                identity=str(current_user_id),  # Convertir a string para PyJWT 2.x
                additional_claims={"role": user.role, "username": user.username}
            )
            
            return {
                "access_token": new_access_token
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")

@auth_blp.route("/profile")
class Profile(MethodView):
    """Endpoint para perfil de usuario"""
    
    @auth_blp.response(200, UserSchema)
    @jwt_required()
    def get(self):
        """Obtener perfil del usuario actual"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get_or_404(current_user_id)
            return user
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @auth_blp.arguments(UserUpdateSchema)
    @auth_blp.response(200, UserSchema)
    @jwt_required()
    def put(self, user_data):
        """Actualizar perfil del usuario actual"""
        try:
            current_user_id = get_jwt_identity()
            user = User.query.get_or_404(current_user_id)
            
            # Actualizar campos permitidos
            for field, value in user_data.items():
                if field in ['first_name', 'last_name', 'email']:
                    setattr(user, field, value)
            
            db.session.commit()
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@auth_blp.route("/users")
class Users(MethodView):
    """Endpoint para gestión de usuarios (solo admin)"""
    
    @auth_blp.response(200, UserListSchema)
    @jwt_required()
    @require_permission('manage_users')
    def get(self):
        """Listar todos los usuarios"""
        try:
            users = User.query.all()
            active_count = sum(1 for user in users if user.is_active)
            
            return {
                "users": users,
                "total": len(users),
                "active_count": active_count
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")
    
    @auth_blp.arguments(UserCreateSchema)
    @auth_blp.response(201, UserSchema)
    @jwt_required()
    @require_permission('manage_users')
    def post(self, user_data):
        """Crear nuevo usuario"""
        try:
            # Verificar si el usuario ya existe
            if User.get_by_username(user_data["username"]):
                abort(400, message="El nombre de usuario ya existe")
            
            if User.get_by_email(user_data["email"]):
                abort(400, message="El email ya existe")
            
            user = User(**user_data)
            db.session.add(user)
            db.session.commit()
            
            return user
        except SQLAlchemyError as e:
            db.session.rollback()
            abort(500, message=f"Error de base de datos: {str(e)}")

@auth_blp.route("/logout")
class Logout(MethodView):
    """Endpoint para logout"""
    
    @auth_blp.response(200, description="Logout exitoso")
    @jwt_required()
    def post(self):
        """Logout de usuario"""
        # En JWT, el logout se maneja en el frontend invalidando el token
        return {"message": "Logout exitoso"}

# Exportar el blueprint con el nombre esperado
auth_bp = auth_blp
