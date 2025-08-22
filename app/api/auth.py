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

# Crear blueprint para autenticación
auth_blp = Blueprint(
    "auth", 
    __name__, 
    description="Operaciones de autenticación y usuarios"
)

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
            
            # Buscar usuario
            user = User.get_by_username(username)
            if not user or not user.check_password(password):
                abort(401, message="Credenciales inválidas")
            
            if not user.is_active:
                abort(401, message="Usuario desactivado")
            
            # Actualizar último login
            user.update_last_login()
            
            # Generar tokens
            access_token = create_access_token(identity=user.id)
            refresh_token = create_refresh_token(identity=user.id)
            
            return {
                "message": "Login exitoso",
                "access_token": access_token,
                "refresh_token": refresh_token,
                "user": user.to_dict()
            }
        except SQLAlchemyError as e:
            abort(500, message=f"Error de base de datos: {str(e)}")

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
            
            new_access_token = create_access_token(identity=current_user_id)
            
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
