"""
Módulo core del sistema de gestión de stock
Contiene funcionalidades centralizadas como permisos y configuración
"""

from .permissions import (
    PermissionManager,
    Permission,
    Role,
    PermissionLevel,
    require_permission,
    require_role,
    require_any_role,
    admin_required,
    manager_or_above_required,
    supervisor_or_above_required,
    user_or_above_required,
    viewer_or_above_required
)

__all__ = [
    'PermissionManager',
    'Permission',
    'Role',
    'PermissionLevel',
    'require_permission',
    'require_role',
    'require_any_role',
    'admin_required',
    'manager_or_above_required',
    'supervisor_or_above_required',
    'user_or_above_required',
    'viewer_or_above_required'
]
