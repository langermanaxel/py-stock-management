#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Usuarios
"""

from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """Esquema completo para Usuario"""
    id = fields.Int(
        dump_only=True, 
        
    )
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=80), 
        
        
    )
    email = fields.Email(
        required=True, 
        
        
    )
    first_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        
        
    )
    last_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        
        
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
        
        
    )
    is_active = fields.Bool(
        
        
    )
    last_login = fields.DateTime(
        dump_only=True, 
        
    )
    created_at = fields.DateTime(
        dump_only=True, 
        
    )
    updated_at = fields.DateTime(
        dump_only=True, 
        
    )
    
    # Campos relacionados
    permissions = fields.List(
        fields.Str(), 
        
    )
    
    # Campos calculados
    full_name = fields.Str(
        dump_only=True, 
        
    )
    can_login = fields.Bool(
        dump_only=True, 
        
    )

class UserCreateSchema(Schema):
    """Esquema para crear un nuevo usuario"""
    username = fields.Str(
        required=True, 
        validate=validate.Length(min=3, max=80), 
        
        
    )
    email = fields.Email(
        required=True, 
        
        
    )
    password = fields.Str(
        required=True, 
        validate=validate.Length(min=6), 
        
        
    )
    first_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        
        
    )
    last_name = fields.Str(
        required=True, 
        validate=validate.Length(min=1, max=50), 
        
        
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
        
        
    )
    is_active = fields.Bool(
        
        
    )

class UserUpdateSchema(Schema):
    """Esquema para actualizar un usuario existente"""
    first_name = fields.Str(
        validate=validate.Length(min=1, max=50), 
        
        
    )
    last_name = fields.Str(
        validate=validate.Length(min=1, max=50), 
        
        
    )
    email = fields.Email(
        
        
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
        
        
    )
    is_active = fields.Bool(
        
        
    )

class UserLoginSchema(Schema):
    """Esquema para inicio de sesión de usuario"""
    username = fields.Str(
        required=True, 
        
        
    )
    password = fields.Str(
        required=True, 
        
        
    )

class UserPasswordChangeSchema(Schema):
    """Esquema para cambio de contraseña"""
    current_password = fields.Str(
        required=True, 
        
        
    )
    new_password = fields.Str(
        required=True, 
        validate=validate.Length(min=6), 
        
        
    )
    confirm_password = fields.Str(
        required=True, 
        
        
    )

class UserListSchema(Schema):
    """Esquema para respuesta de lista de usuarios"""
    users = fields.Nested(
        UserSchema, 
        many=True, 
        
    )
    total = fields.Int(
        
    )
    active_count = fields.Int(
        
    )
    inactive_count = fields.Int(
        
    )

class UserSearchSchema(Schema):
    """Esquema para búsqueda y filtrado de usuarios"""
    username = fields.Str(
        
        
    )
    email = fields.Str(
        
        
    )
    first_name = fields.Str(
        
        
    )
    last_name = fields.Str(
        
        
    )
    role = fields.Str(
        validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']),
        
        
    )
    is_active = fields.Bool(
        
        
    )
    created_after = fields.Date(
        
        
    )
    created_before = fields.Date(
        
        
    )

class UserProfileSchema(Schema):
    """Esquema para perfil de usuario (sin información sensible)"""
    id = fields.Int(
        dump_only=True, 
        
    )
    username = fields.Str(
        dump_only=True, 
        
    )
    email = fields.Str(
        dump_only=True, 
        
    )
    first_name = fields.Str(
        dump_only=True, 
        
    )
    last_name = fields.Str(
        dump_only=True, 
        
    )
    role = fields.Str(
        dump_only=True, 
        
    )
    is_active = fields.Bool(
        dump_only=True, 
        
    )
    last_login = fields.DateTime(
        dump_only=True, 
        
    )
    created_at = fields.DateTime(
        dump_only=True, 
        
    )
