// Configuración del Frontend
const APP_CONFIG = {
    // URLs de la API
    API_BASE_URL: '/api',
    
    // Configuración CORS
    CORS: {
        credentials: 'same-origin',
        mode: 'cors',
        headers: {
            'Content-Type': 'application/json',
            'X-Requested-With': 'XMLHttpRequest'
        }
    },
    
    // Credenciales de Demo
    DEMO_CREDENTIALS: {
        admin: {
            username: 'admin',
            password: 'Admin123!',
            role: 'admin',
            description: 'Acceso completo a todas las funcionalidades'
        },
        gerente: {
            username: 'gerente',
            password: 'Gerente123!',
            role: 'manager',
            description: 'Gestión de inventario (sin eliminar)'
        },
        usuario: {
            username: 'usuario',
            password: 'Usuario123!',
            role: 'user',
            description: 'Visualización y creación de órdenes'
        },
        viewer: {
            username: 'viewer',
            password: 'Viewer123!',
            role: 'viewer',
            description: 'Acceso muy limitado, solo lectura'
        }
    },
    
    // Roles y permisos
    ROLES: {
        admin: {
            name: 'Administrador',
            level: 4,
            permissions: ['all']
        },
        manager: {
            name: 'Gerente',
            level: 3,
            permissions: ['read', 'create', 'update']
        },
        user: {
            name: 'Usuario',
            level: 2,
            permissions: ['read', 'create_orders']
        },
        viewer: {
            name: 'Viewer',
            level: 1,
            permissions: ['read_limited']
        }
    },
    
    // Configuración de la UI
    UI: {
        // Tiempo de expiración de tokens (en minutos)
        TOKEN_EXPIRY_WARNING: 5,
        
        // Duración de los toasts (en milisegundos)
        TOAST_DURATION: 5000,
        
        // Colores por tipo de mensaje
        MESSAGE_COLORS: {
            success: '#28a745',
            error: '#dc3545',
            warning: '#ffc107',
            info: '#17a2b8'
        }
    },
    
    // Endpoints de la API
    ENDPOINTS: {
        auth: {
            login: '/auth/login',
            refresh: '/auth/refresh',
            logout: '/auth/logout'
        },
        data: {
            categories: '/categories/',
            products: '/products/',
            stock: '/stock/',
            orders: '/orders/',
            purchases: '/purchases/'
        }
    }
};

// Función para obtener credenciales de demo
function getDemoCredentials() {
    return APP_CONFIG.DEMO_CREDENTIALS;
}

// Función para obtener información de un rol
function getRoleInfo(role) {
    return APP_CONFIG.ROLES[role] || null;
}

// Función para verificar si un rol tiene un permiso específico
function hasRolePermission(role, permission) {
    const roleInfo = getRoleInfo(role);
    if (!roleInfo) return false;
    
    if (roleInfo.permissions.includes('all')) return true;
    return roleInfo.permissions.includes(permission);
}

// Función para obtener el nivel de un rol
function getRoleLevel(role) {
    const roleInfo = getRoleInfo(role);
    return roleInfo ? roleInfo.level : 0;
}

// Función para verificar si un rol es superior o igual a otro
function isRoleSuperiorOrEqual(role1, role2) {
    return getRoleLevel(role1) >= getRoleLevel(role2);
}

// Exportar para uso global
window.APP_CONFIG = APP_CONFIG;
window.getDemoCredentials = getDemoCredentials;
window.getRoleInfo = getRoleInfo;
window.hasRolePermission = hasRolePermission;
window.getRoleLevel = getRoleLevel;
window.isRoleSuperiorOrEqual = isRoleSuperiorOrEqual;
