#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Usuarios
"""

from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """Esquema completo para Usuario"""
    id = fields.Int(
        dump_only=True, 
        description="ID único del usuario (generado automáticamente)"
    )
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=80), 
        description="Nombre de usuario único (3-80 caracteres)",
        example="juan.perez"
    )
    email = fields.Email(
        required=True, 
        description="Email único del usuario",
        example="juan.perez@empresa.com"
    )
    first_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        description="Nombre del usuario (1-50 caracteres)",
        example="Juan"
    )
    last_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        description="Apellido del usuario (1-50 caracteres)",
        example="Pérez"
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
        description="Rol del usuario en el sistema",
        example="manager"
    )
    is_active = fields.Bool(
        description="Indica si el usuario está activo y puede acceder al sistema",
        example=True
    )
    last_login = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora del último inicio de sesión"
    )
    created_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de creación del usuario (automático)"
    )
    updated_at = fields.DateTime(
        dump_only=True, 
        description="Fecha y hora de última actualización (automático)"
    )
    
    # Campos relacionados
    permissions = fields.List(
        fields.Str(), 
        description="Lista de permisos específicos del usuario"
    )
    
    # Campos calculados
    full_name = fields.Str(
        dump_only=True, 
        description="Nombre completo del usuario (first_name + last_name)"
    )
    can_login = fields.Bool(
        dump_only=True, 
        description="Indica si el usuario puede iniciar sesión"
    )

class UserCreateSchema(Schema):
    """Esquema para crear un nuevo usuario"""
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=80), 
        description="Nombre de usuario único (3-80 caracteres)",
        example="juan.perez"
    )
    email = fields.Email(
        required=True, 
        description="Email único del usuario",
        example="juan.perez@empresa.com"
    )
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=6), 
        description="Contraseña del usuario (mínimo 6 caracteres)",
        example="password123"
    )
    first_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        description="Nombre del usuario (1-50 caracteres)",
        example="Juan"
    )
    last_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        description="Apellido del usuario (1-50 caracteres)",
        example="Pérez"
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
        description="Rol del usuario en el sistema (por defecto: 'user')",
        example="manager"
    )
    is_active = fields.Bool(
        description="Indica si el usuario estará activo al crearlo",
        example=True
    )

class UserUpdateSchema(Schema):
    """Esquema para actualizar un usuario existente"""
    first_name = fields.Str(
        validate=validate.Length(min=1, max=50), 
        description="Nombre del usuario (1-50 caracteres)",
        example="Juan"
    )
    last_name = fields.Str(
        validate=validate.Length(min=1, max=50), 
        description="Apellido del usuario (1-50 caracteres)",
        example="Pérez"
    )
    email = fields.Email(
        description="Email único del usuario",
        example="juan.perez@empresa.com"
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
        description="Rol del usuario en el sistema",
        example="manager"
    )
    is_active = fields.Bool(
        description="Indica si el usuario está activo y puede acceder al sistema",
        example=True
    )

class UserLoginSchema(Schema):
    """Esquema para inicio de sesión de usuario"""
    username = fields.Str(
        required=True, 
        description="Nombre de usuario o email",
        example="juan.perez"
    )
    password = fields.Str(
        required=True, 
        description="Contraseña del usuario",
        example="password123"
    )

class UserPasswordChangeSchema(Schema):
    """Esquema para cambio de contraseña"""
    current_password = fields.Str(
        required=True, 
        description="Contraseña actual del usuario",
        example="password123"
    )
    new_password = fields.Str(
        required=True, 
        validate=validate.Length(min=6), 
        description="Nueva contraseña (mínimo 6 caracteres)",
        example="newpassword456"
    )
    confirm_password = fields.Str(
        required=True, 
        description="Confirmación de la nueva contraseña",
        example="newpassword456"
    )

class UserListSchema(Schema):
    """Esquema para respuesta de lista de usuarios"""
    users = fields.Nested(
        UserSchema, 
        many=True, 
        description="Lista de usuarios"
    )
    total = fields.Int(
        description="Total de usuarios en la base de datos"
    )
    active_count = fields.Int(
        description="Cantidad de usuarios activos"
    )
    inactive_count = fields.Int(
        description="Cantidad de usuarios inactivos"
    )

class UserSearchSchema(Schema):
    """Esquema para búsqueda y filtrado de usuarios"""
    username = fields.Str(
        description="Buscar por nombre de usuario (búsqueda parcial)",
        example="juan"
    )
    email = fields.Str(
        description="Buscar por email (búsqueda parcial)",
        example="juan@"
    )
    first_name = fields.Str(
        description="Buscar por nombre (búsqueda parcial)",
        example="Juan"
    )
    last_name = fields.Str(
        description="Buscar por apellido (búsqueda parcial)",
        example="Pérez"
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']),
        description="Filtrar por rol específico",
        example="manager"
    )
    is_active = fields.Bool(
        description="Filtrar por estado de actividad",
        example=True
    )
    created_after = fields.Date(
        description="Filtrar usuarios creados después de esta fecha",
        example="2024-01-01"
    )
    created_before = fields.Date(
        description="Filtrar usuarios creados antes de esta fecha",
        example="2024-12-31"
    )

class UserProfileSchema(Schema):
    """Esquema para perfil de usuario (sin información sensible)"""
    id = fields.Int(
        dump_only=True, 
        description="ID único del usuario"
    )
    username = fields.Str(
        dump_only=True, 
        description="Nombre de usuario"
    )
    email = fields.Str(
        dump_only=True, 
        description="Email del usuario"
    )
    first_name = fields.Str(
        dump_only=True, 
        description="Nombre del usuario"
    )
    last_name = fields.Str(
        dump_only=True, 
        description="Apellido del usuario"
    )
    role = fields.Str(
        dump_only=True, 
        description="Rol del usuario"
    )
    is_active = fields.Bool(
        dump_only=True, 
        description="Estado de actividad del usuario"
    )
    last_login = fields.DateTime(
        dump_only=True, 
        description="Último inicio de sesión"
    )
    created_at = fields.DateTime(
        dump_only=True, 
        description="Fecha de creación"
    )
