// Sistema de Autenticación JWT para el Frontend
class JWTAuthManager {
    constructor() {
        this.token = localStorage.getItem('jwt_token');
        this.refreshToken = localStorage.getItem('jwt_refresh_token');
        this.user = JSON.parse(localStorage.getItem('user_info') || 'null');
        this.baseURL = '/api';
    }

    // Verificar si el usuario está autenticado
    isAuthenticated() {
        return this.token && this.user;
    }

    // Obtener el token actual
    getToken() {
        return this.token;
    }

    // Obtener información del usuario
    getUser() {
        return this.user;
    }

    // Obtener el rol del usuario
    getUserRole() {
        return this.user?.role || null;
    }

    // Verificar si el usuario tiene un rol específico
    hasRole(role) {
        return this.user?.role === role;
    }

    // Verificar si el usuario tiene uno de los roles permitidos
    hasAnyRole(roles) {
        if (!Array.isArray(roles)) {
            roles = [roles];
        }
        return roles.includes(this.user?.role);
    }

    // Verificar permisos específicos
    hasPermission(permission) {
        return this.user?.permissions?.includes(permission) || false;
    }

    // Login del usuario
    async login(username, password) {
        try {
            const response = await fetch(`${this.baseURL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password })
            });

            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Error en el login');
            }

            const data = await response.json();
            
            // Guardar tokens y información del usuario
            this.token = data.access_token;
            this.refreshToken = data.refresh_token;
            this.user = data.user;
            
            localStorage.setItem('jwt_token', this.token);
            localStorage.setItem('jwt_refresh_token', this.refreshToken);
            localStorage.setItem('user_info', JSON.stringify(this.user));
            
            return { success: true, user: this.user };
        } catch (error) {
            console.error('Error en login:', error);
            return { success: false, error: error.message };
        }
    }

    // Logout del usuario
    logout() {
        this.token = null;
        this.refreshToken = null;
        this.user = null;
        
        localStorage.removeItem('jwt_token');
        localStorage.removeItem('jwt_refresh_token');
        localStorage.removeItem('user_info');
        
        // Redirigir al login
        window.location.href = '/login';
    }

    // Refrescar token
    async refreshAccessToken() {
        if (!this.refreshToken) {
            this.logout();
            return false;
        }

        try {
            const response = await fetch(`${this.baseURL}/auth/refresh`, {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${this.refreshToken}`
                }
            });

            if (!response.ok) {
                throw new Error('Error al refrescar token');
            }

            const data = await response.json();
            this.token = data.access_token;
            localStorage.setItem('jwt_token', this.token);
            return true;
        } catch (error) {
            console.error('Error al refrescar token:', error);
            this.logout();
            return false;
        }
    }

    // Hacer petición HTTP con autenticación automática
    async authenticatedRequest(url, options = {}) {
        if (!this.token) {
            this.logout();
            return null;
        }

        // Agregar headers de autenticación
        const headers = {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${this.token}`,
            ...options.headers
        };

        try {
            const response = await fetch(url, {
                ...options,
                headers
            });

            // Si el token expiró, intentar refrescarlo
            if (response.status === 401) {
                const refreshed = await this.refreshAccessToken();
                if (refreshed) {
                    // Reintentar la petición con el nuevo token
                    headers.Authorization = `Bearer ${this.token}`;
                    const retryResponse = await fetch(url, {
                        ...options,
                        headers
                    });
                    return retryResponse;
                }
            }

            return response;
        } catch (error) {
            console.error('Error en petición autenticada:', error);
            return null;
        }
    }

    // Verificar si el token está próximo a expirar
    isTokenExpiringSoon() {
        if (!this.token) return true;
        
        try {
            const payload = JSON.parse(atob(this.token.split('.')[1]));
            const now = Math.floor(Date.now() / 1000);
            const timeUntilExpiry = payload.exp - now;
            
            // Si expira en menos de 5 minutos, refrescar
            return timeUntilExpiry < 300;
        } catch (error) {
            return true;
        }
    }

    // Inicializar el manager (verificar token y refrescar si es necesario)
    async initialize() {
        if (this.isAuthenticated() && this.isTokenExpiringSoon()) {
            await this.refreshAccessToken();
        }
    }
}

// Instancia global del manager de autenticación
const authManager = new JWTAuthManager();

// Función para mostrar/ocultar elementos según el rol del usuario
function updateUIForUserRole() {
    const user = authManager.getUser();
    if (!user) return;

    // Ocultar/mostrar botones según el rol
    const role = user.role;
    
    // Elementos que solo pueden ver usuarios con rol 'user' o superior
    if (role === 'viewer') {
        hideElementsByRole('user');
        hideElementsByRole('manager');
        hideElementsByRole('admin');
    } else if (role === 'user') {
        hideElementsByRole('manager');
        hideElementsByRole('admin');
    } else if (role === 'manager') {
        hideElementsByRole('admin');
    }
}

// Ocultar elementos según el rol
function hideElementsByRole(role) {
    const elements = document.querySelectorAll(`[data-role="${role}"]`);
    elements.forEach(el => {
        el.style.display = 'none';
    });
}

// Función para crear botones con permisos según el rol
function createActionButton(action, text, icon, role = 'user') {
    const button = document.createElement('button');
    button.innerHTML = `<i class="${icon}"></i> ${text}`;
    button.className = 'action-btn';
    button.setAttribute('data-role', role);
    
    // Solo mostrar si el usuario tiene el rol necesario
    if (!authManager.hasAnyRole([role, 'admin'])) {
        button.style.display = 'none';
    }
    
    return button;
}

// Función para verificar permisos antes de ejecutar acciones
function checkPermission(action, requiredRole = 'user') {
    if (!authManager.isAuthenticated()) {
        showToast('error', 'Error', 'Debes iniciar sesión para realizar esta acción');
        return false;
    }
    
    if (!authManager.hasAnyRole(requiredRole)) {
        showToast('error', 'Error', 'No tienes permisos para realizar esta acción');
        return false;
    }
    
    return true;
}

// Exportar para uso global
window.authManager = authManager;
window.updateUIForUserRole = updateUIForUserRole;
window.createActionButton = createActionButton;
window.checkPermission = checkPermission;
