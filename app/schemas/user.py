#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Usuarios
"""

from marshmallow import Schema, fields, validate

class UserSchema(Schema):
    """Esquema para Usuario"""
    id = fields.Int(dump_only=True, description="ID único del usuario")
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80), 
                          description="Nombre de usuario")
    email = fields.Email(required=True, description="Email del usuario")
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50), 
                           description="Nombre del usuario")
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50), 
                          description="Apellido del usuario")
    role = fields.Str(validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
                     description="Rol del usuario")
    is_active = fields.Bool(description="Indica si el usuario está activo")
    last_login = fields.DateTime(dump_only=True, description="Fecha del último login")
    created_at = fields.DateTime(dump_only=True, description="Fecha de creación")
    updated_at = fields.DateTime(dump_only=True, description="Fecha de última actualización")
    
    # Campos relacionados
    permissions = fields.List(fields.Str(), description="Permisos del usuario")

class UserCreateSchema(Schema):
    """Esquema para crear usuario"""
    username = fields.Str(required=True, validate=validate.Length(min=3, max=80), 
                          description="Nombre de usuario")
    email = fields.Email(required=True, description="Email del usuario")
    password = fields.Str(required=True, validate=validate.Length(min=6), 
                         description="Contraseña del usuario")
    first_name = fields.Str(required=True, validate=validate.Length(min=1, max=50), 
                           description="Nombre del usuario")
    last_name = fields.Str(required=True, validate=validate.Length(min=1, max=50), 
                          description="Apellido del usuario")
    role = fields.Str(validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
                     description="Rol del usuario")

class UserUpdateSchema(Schema):
    """Esquema para actualizar usuario"""
    first_name = fields.Str(validate=validate.Length(min=1, max=50), 
                           description="Nombre del usuario")
    last_name = fields.Str(validate=validate.Length(min=1, max=50), 
                          description="Apellido del usuario")
    email = fields.Email(description="Email del usuario")
    role = fields.Str(validate=validate.OneOf(['admin', 'manager', 'user', 'viewer']), 
                     description="Rol del usuario")
    is_active = fields.Bool(description="Indica si el usuario está activo")

class UserLoginSchema(Schema):
    """Esquema para login de usuario"""
    username = fields.Str(required=True, description="Nombre de usuario")
    password = fields.Str(required=True, description="Contraseña")

class UserListSchema(Schema):
    """Esquema para lista de usuarios"""
    users = fields.Nested(UserSchema, many=True, description="Lista de usuarios")
    total = fields.Int(description="Total de usuarios")
    active_count = fields.Int(description="Cantidad de usuarios activos")
