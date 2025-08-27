#!/usr/bin/env python3
"""
Paquete de decoradores de autorización
"""

from .role_decorators import (
    roles_required,
    admin_required,
    gerente_or_admin_required,
    usuario_or_above_required,
    viewer_or_above_required,
    active_user_required
)

__all__ = [
    'roles_required',
    'admin_required', 
    'gerente_or_admin_required',
    'usuario_or_above_required',
    'viewer_or_above_required',
    'active_user_required'
]
