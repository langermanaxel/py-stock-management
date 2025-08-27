// Sistema de Autenticación JWT para el Frontend
class JWTAuthManager {
    constructor() {
        this.token = localStorage.getItem('jwt_token');
        this.refreshToken = localStorage.getItem('jwt_refresh_token');
        this.user = JSON.parse(localStorage.getItem('user_info') || 'null');
        
        // Configuración de URL base
        // Como Flask sirve tanto el frontend como la API desde el mismo puerto (5000)
        // siempre usamos rutas relativas
        this.baseURL = '/api';
        
        console.log('🔧 Auth Manager inicializado con baseURL:', this.baseURL);
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

    /**
     * Realiza una petición autenticada a la API
     * @param {string} url - URL completa de la API
     * @param {Object} options - Opciones de fetch
     * @returns {Promise<Object>} Respuesta de la API
     */
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
                headers,
                credentials: 'include', // Cambiar a 'include' para CORS con cookies
                mode: 'cors'
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

    /**
     * Parsea respuestas de error del backend en diferentes formatos
     * @param {Response} response - Objeto Response de fetch
     * @param {string} fallbackMessage - Mensaje por defecto si no se puede parsear
     * @returns {Error} Error con mensaje extraído del backend
     */
    async parseErrorResponse(response, fallbackMessage = 'Error en la petición') {
        let errorMessage = fallbackMessage;
        let errorDetails = null;

        try {
            // Intentar parsear como JSON primero
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                const errorData = await response.json();
                
                // Buscar mensaje en diferentes campos comunes del backend
                if (errorData.msg) {
                    errorMessage = errorData.msg;
                } else if (errorData.message) {
                    errorMessage = errorData.message;
                } else if (errorData.detail) {
                    errorMessage = errorData.detail;
                } else if (errorData.error) {
                    errorMessage = errorData.error;
                } else if (errorData.description) {
                    errorMessage = errorData.description;
                } else if (typeof errorData === 'string') {
                    errorMessage = errorData;
                } else if (errorData && typeof errorData === 'object') {
                    // Si es un objeto, buscar el primer valor string
                    const firstStringValue = Object.values(errorData).find(val => typeof val === 'string');
                    if (firstStringValue) {
                        errorMessage = firstStringValue;
                    }
                }

                // Guardar detalles adicionales si existen
                if (errorData.details) {
                    errorDetails = errorData.details;
                } else if (errorData.errors) {
                    errorDetails = errorData.errors;
                }
            } else {
                // Si no es JSON, intentar leer como texto
                try {
                    const textResponse = await response.text();
                    if (textResponse && textResponse.trim()) {
                        // Buscar contenido HTML y extraer solo el texto útil
                        if (textResponse.includes('<html') || textResponse.includes('<body')) {
                            // Es HTML, extraer solo el texto del body
                            const tempDiv = document.createElement('div');
                            tempDiv.innerHTML = textResponse;
                            const bodyText = tempDiv.textContent || tempDiv.innerText || '';
                            if (bodyText.trim()) {
                                errorMessage = bodyText.trim().substring(0, 200); // Limitar longitud
                            }
                        } else {
                            errorMessage = textResponse.trim();
                        }
                    }
                } catch (textError) {
                    console.warn('No se pudo leer respuesta como texto:', textError);
                }
            }
        } catch (parseError) {
            console.warn('Error parseando respuesta de error:', parseError);
            // Mantener el mensaje por defecto
        }

        // Crear error con información completa
        const error = new Error(errorMessage);
        error.status = response.status;
        error.statusText = response.statusText;
        error.url = response.url;
        error.details = errorDetails;
        error.response = response;

        return error;
    }

    /**
     * Parsea respuestas exitosas del backend
     * @param {Response} response - Objeto Response de fetch
     * @returns {Promise<Object>} Respuesta parseada
     */
    async parseResponse(response) {
        try {
            const contentType = response.headers.get('content-type');
            if (contentType && contentType.includes('application/json')) {
                return await response.json();
            } else {
                // Si no es JSON, devolver el texto
                return await response.text();
            }
        } catch (parseError) {
            console.warn('Error parseando respuesta exitosa:', parseError);
            return { success: true, message: 'Operación completada' };
        }
    }

    /**
     * Inicia sesión del usuario
     * @param {string} username - Nombre de usuario
     * @param {string} password - Contraseña
     * @returns {Promise<Object>} Respuesta del servidor
     */
    async login(username, password) {
        try {
            const response = await fetch(`${this.baseURL}/auth/login`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include', // Cambiar a 'include' para CORS con cookies
                mode: 'cors'
            });

            if (!response.ok) {
                const error = await this.parseErrorResponse(response);
                throw error;
            }

            const data = await this.parseResponse(response);
            
            if (data.access_token) {
                this.token = data.access_token;
                this.refreshToken = data.refresh_token;
                this.user = data.user;
                
                // Guardar en localStorage
                localStorage.setItem('jwt_token', this.token);
                localStorage.setItem('jwt_refresh_token', this.refreshToken);
                localStorage.setItem('user_info', JSON.stringify(this.user));
                
                // Emitir evento de login exitoso
                window.dispatchEvent(new CustomEvent('userLoggedIn', { detail: this.user }));
                
                return data;
            } else {
                throw new Error('Respuesta del servidor inválida: token no encontrado');
            }

        } catch (error) {
            // Si ya es un error parseado, re-lanzarlo
            if (error.status) {
                throw error;
            }
            
            // Si es un error de red, crear uno más descriptivo
            const networkError = new Error(`Error de red: ${error.message}`);
            networkError.isNetworkError = true;
            networkError.originalError = error;
            throw networkError;
        }
    }

    /**
     * Refresca el token de acceso usando el refresh token
     * @returns {Promise<Object>} Respuesta del servidor
     */
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
                },
                credentials: 'include', // Cambiar a 'include' para CORS con cookies
                mode: 'cors'
            });

            if (!response.ok) {
                const error = await this.parseErrorResponse(response);
                throw error;
            }

            const data = await this.parseResponse(response);
            
            if (data.access_token) {
                this.token = data.access_token;
                localStorage.setItem('jwt_token', this.token);
                return true;
            } else {
                throw new Error('Respuesta del servidor inválida: nuevo token no encontrado');
            }

        } catch (error) {
            // Si ya es un error parseado, re-lanzarlo
            if (error.status) {
                throw error;
            }
            
            // Si es un error de red, crear uno más descriptivo
            const networkError = new Error(`Error de red: ${error.message}`);
            networkError.isNetworkError = true;
            networkError.originalError = error;
            throw networkError;
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
