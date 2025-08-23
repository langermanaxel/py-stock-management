#!/usr/bin/env python3
"""
Esquemas de Marshmallow para Autenticación
"""

from marshmallow import Schema, fields, validate

class LoginSchema(Schema):
    """Esquema para inicio de sesión"""
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
    remember_me = fields.Bool(
        description="Recordar sesión del usuario",
        example=False
    )

class LoginResponseSchema(Schema):
    """Esquema para respuesta de inicio de sesión exitoso"""
    access_token = fields.Str(
        description="Token de acceso JWT para autenticación",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    refresh_token = fields.Str(
        description="Token de renovación JWT",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    token_type = fields.Str(
        description="Tipo de token (siempre 'bearer')",
        example="bearer"
    )
    expires_in = fields.Int(
        description="Tiempo de expiración del token en segundos",
        example=3600
    )
    user = fields.Nested(
        'UserProfileSchema', 
        description="Información del perfil del usuario"
    )

class RefreshTokenSchema(Schema):
    """Esquema para renovación de token"""
    refresh_token = fields.Str(
        required=True, 
        description="Token de renovación JWT",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )

class RefreshTokenResponseSchema(Schema):
    """Esquema para respuesta de renovación de token"""
    access_token = fields.Str(
        description="Nuevo token de acceso JWT",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )
    token_type = fields.Str(
        description="Tipo de token (siempre 'bearer')",
        example="bearer"
    )
    expires_in = fields.Int(
        description="Tiempo de expiración del nuevo token en segundos",
        example=3600
    )

class LogoutSchema(Schema):
    """Esquema para cierre de sesión"""
    refresh_token = fields.Str(
        required=True, 
        description="Token de renovación a invalidar",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )

class LogoutResponseSchema(Schema):
    """Esquema para respuesta de cierre de sesión"""
    message = fields.Str(
        description="Mensaje de confirmación",
        example="Sesión cerrada exitosamente"
    )
    logged_out_at = fields.DateTime(
        description="Fecha y hora del cierre de sesión"
    )

class PasswordResetRequestSchema(Schema):
    """Esquema para solicitar restablecimiento de contraseña"""
    email = fields.Email(
        required=True, 
        description="Email del usuario para restablecer contraseña",
        example="juan.perez@empresa.com"
    )

class PasswordResetRequestResponseSchema(Schema):
    """Esquema para respuesta de solicitud de restablecimiento"""
    message = fields.Str(
        description="Mensaje de confirmación",
        example="Se ha enviado un email con instrucciones para restablecer la contraseña"
    )
    reset_token_expires_in = fields.Int(
        description="Tiempo de expiración del token de restablecimiento en segundos",
        example=3600
    )

class PasswordResetSchema(Schema):
    """Esquema para restablecer contraseña"""
    reset_token = fields.Str(
        required=True, 
        description="Token de restablecimiento de contraseña",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
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

class PasswordResetResponseSchema(Schema):
    """Esquema para respuesta de restablecimiento de contraseña"""
    message = fields.Str(
        description="Mensaje de confirmación",
        example="Contraseña restablecida exitosamente"
    )
    password_changed_at = fields.DateTime(
        description="Fecha y hora del cambio de contraseña"
    )

class ChangePasswordSchema(Schema):
    """Esquema para cambio de contraseña (usuario autenticado)"""
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

class ChangePasswordResponseSchema(Schema):
    """Esquema para respuesta de cambio de contraseña"""
    message = fields.Str(
        description="Mensaje de confirmación",
        example="Contraseña cambiada exitosamente"
    )
    password_changed_at = fields.DateTime(
        description="Fecha y hora del cambio de contraseña"
    )

class VerifyTokenSchema(Schema):
    """Esquema para verificación de token"""
    token = fields.Str(
        required=True, 
        description="Token JWT a verificar",
        example="eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
    )

class VerifyTokenResponseSchema(Schema):
    """Esquema para respuesta de verificación de token"""
    valid = fields.Bool(
        description="Indica si el token es válido",
        example=True
    )
    user_id = fields.Int(
        description="ID del usuario del token (si es válido)",
        example=1
    )
    username = fields.Str(
        description="Nombre de usuario del token (si es válido)",
        example="juan.perez"
    )
    role = fields.Str(
        description="Rol del usuario del token (si es válido)",
        example="manager"
    )
    expires_at = fields.DateTime(
        description="Fecha y hora de expiración del token (si es válido)"
    )

class AuthErrorSchema(Schema):
    """Esquema para errores de autenticación"""
    error = fields.Str(
        description="Tipo de error de autenticación",
        example="invalid_credentials"
    )
    message = fields.Str(
        description="Descripción del error",
        example="Credenciales inválidas"
    )
    details = fields.Dict(
        description="Detalles adicionales del error"
    )
    timestamp = fields.DateTime(
        description="Fecha y hora del error"
    )
