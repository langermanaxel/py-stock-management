#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Autenticación
"""

from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    """Esquema para inicio de sesión"""
    username = fields.Str(
        required=True, 
        
    )
    password = fields.Str(
        required=True, 
        
    )
    remember_me = fields.Bool(
        
    )

class LoginResponseSchema(Schema):
    """Esquema para respuesta de inicio de sesión exitoso"""
    access_token = fields.Str(
        
    )
    refresh_token = fields.Str(
        
    )
    token_type = fields.Str(
        
    )
    expires_in = fields.Int(
        
    )
    user = fields.Nested(
        'UserProfileSchema'
    )

class RefreshTokenSchema(Schema):
    """Esquema para renovación de token"""
    refresh_token = fields.Str(
        required=True, 
        
        
    )

class RefreshTokenResponseSchema(Schema):
    """Esquema para respuesta de renovación de token"""
    access_token = fields.Str(
        
        
    )
    token_type = fields.Str(
        
        
    )
    expires_in = fields.Int(
        
        
    )

class LogoutSchema(Schema):
    """Esquema para cierre de sesión"""
    refresh_token = fields.Str(
        required=True, 
        
        
    )

class LogoutResponseSchema(Schema):
    """Esquema para respuesta de cierre de sesión"""
    message = fields.Str(
        
        
    )
    logged_out_at = fields.DateTime(
        
    )

class PasswordResetRequestSchema(Schema):
    """Esquema para solicitar restablecimiento de contraseña"""
    email = fields.Email(
        required=True, 
        
        
    )

class PasswordResetRequestResponseSchema(Schema):
    """Esquema para respuesta de solicitud de restablecimiento"""
    message = fields.Str(
        
        
    )
    reset_token_expires_in = fields.Int(
        
        
    )

class PasswordResetSchema(Schema):
    """Esquema para restablecer contraseña"""
    reset_token = fields.Str(
        required=True, 
        
        
    )
    new_password = fields.Str(
        required=True, 
        validate=validate.Length(min=6), 
        
        
    )
    confirm_password = fields.Str(
        required=True, 
        
        
    )

class PasswordResetResponseSchema(Schema):
    """Esquema para respuesta de restablecimiento de contraseña"""
    message = fields.Str(
        
        
    )
    password_changed_at = fields.DateTime(
        
    )

class ChangePasswordSchema(Schema):
    """Esquema para cambio de contraseña (usuario autenticado)"""
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

class ChangePasswordResponseSchema(Schema):
    """Esquema para respuesta de cambio de contraseña"""
    message = fields.Str(
        
        
    )
    password_changed_at = fields.DateTime(
        
    )

class VerifyTokenSchema(Schema):
    """Esquema para verificación de token"""
    token = fields.Str(
        required=True, 
        
        
    )

class VerifyTokenResponseSchema(Schema):
    """Esquema para respuesta de verificación de token"""
    valid = fields.Bool(
        
        
    )
    user_id = fields.Int(
        
        
    )
    username = fields.Str(
        
        
    )
    role = fields.Str(
        
        
    )
    expires_at = fields.DateTime(
        
    )

class AuthErrorSchema(Schema):
    """Esquema para errores de autenticación"""
    error = fields.Str(
        
        
    )
    message = fields.Str(
        
        
    )
    details = fields.Dict(
        
    )
    timestamp = fields.DateTime(
        
    )
