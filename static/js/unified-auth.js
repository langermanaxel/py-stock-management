/**
 * Sistema de Autenticación Unificado
 * Maneja tanto JWT como sesiones de manera consistente
 */

class UnifiedAuthManager {
    constructor() {
        this.token = null;
        this.user = null;
        this.isInitialized = false;
        this.sessionTimeout = 30 * 60 * 1000; // 30 minutos
        this.refreshThreshold = 5 * 60 * 1000; // 5 minutos antes de expirar
        
        this.init();
    }

    /**
     * Inicializar el sistema de autenticación
     */
    init() {
        console.log('🔐 Inicializando sistema de autenticación unificado...');
        
        // Cargar datos del localStorage
        this.loadStoredData();
        
        // Configurar listeners
        this.setupEventListeners();
        
        // Verificar sesión inicial
        this.checkInitialSession();
        
        // Configurar refresh automático
        this.setupAutomaticRefresh();
        
        this.isInitialized = true;
        console.log('✅ Sistema de autenticación inicializado');
    }

    /**
     * Cargar datos almacenados
     */
    loadStoredData() {
        this.token = localStorage.getItem('access_token');
        this.user = JSON.parse(localStorage.getItem('user') || 'null');
        
        if (this.token && this.user) {
            console.log('📱 Datos de sesión cargados:', {
                user: this.user.username,
                role: this.user.role,
                tokenLength: this.token.length
            });
        }
    }

    /**
     * Configurar event listeners
     */
    setupEventListeners() {
        // Escuchar cambios en el localStorage
        window.addEventListener('storage', (e) => {
            if (e.key === 'access_token' || e.key === 'user') {
                this.loadStoredData();
            }
        });

        // Escuchar eventos de login/logout
        window.addEventListener('userLoggedIn', (e) => {
            this.user = e.detail;
            this.loadStoredData();
        });

        window.addEventListener('userLoggedOut', () => {
            this.clearSession();
        });
    }

    /**
     * Verificar sesión inicial
     */
    async checkInitialSession() {
        try {
            if (!this.token || !this.user) {
                console.log('🔍 No hay sesión activa');
                this.handleNoSession();
                return;
            }

            console.log('🔍 Verificando sesión inicial...');
            
            // Verificar si el token está expirado
            if (this.isTokenExpired(this.token)) {
                console.log('⏰ Token expirado, intentando renovar...');
                const refreshed = await this.refreshToken();
                if (!refreshed) {
                    this.handleSessionExpired();
                    return;
                }
            }

            // Verificar con el servidor
            const isValid = await this.validateWithServer();
            if (!isValid) {
                console.log('❌ Sesión inválida según el servidor');
                this.handleSessionExpired();
                return;
            }

            console.log('✅ Sesión válida');
            this.updateLastActivity();
            
        } catch (error) {
            console.error('❌ Error verificando sesión inicial:', error);
            this.handleSessionExpired();
        }
    }

    /**
     * Verificar sesión periódicamente
     */
    async checkSession() {
        try {
            if (!this.token || !this.user) {
                return;
            }

            // Verificar si necesita refresh
            if (this.needsRefresh()) {
                console.log('🔄 Token necesita renovación...');
                const refreshed = await this.refreshToken();
                if (!refreshed) {
                    this.handleSessionExpired();
                    return;
                }
            }

            // Verificar actividad
            if (this.isSessionTimedOut()) {
                console.log('⏰ Sesión expirada por inactividad');
                this.handleSessionExpired();
                return;
            }

        } catch (error) {
            console.error('❌ Error verificando sesión:', error);
            this.handleSessionExpired();
        }
    }

    /**
     * Login de usuario
     */
    async login(username, password) {
        try {
            console.log('🔐 Iniciando login para:', username);
            
            const response = await fetch('/api/auth/login', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ username, password }),
                credentials: 'include'
            });

            const data = await response.json();

            if (!response.ok) {
                throw new Error(data.message || 'Error en el login');
            }

            // Almacenar datos
            this.token = data.access_token;
            this.user = data.user;
            
            localStorage.setItem('access_token', this.token);
            localStorage.setItem('refresh_token', data.refresh_token);
            localStorage.setItem('user', JSON.stringify(this.user));

            console.log('✅ Login exitoso:', {
                user: this.user.username,
                role: this.user.role
            });

            // Emitir evento
            window.dispatchEvent(new CustomEvent('userLoggedIn', { detail: this.user }));
            
            // Actualizar actividad
            this.updateLastActivity();

            return data;

        } catch (error) {
            console.error('❌ Error en login:', error);
            throw error;
        }
    }

    /**
     * Logout de usuario
     */
    async logout() {
        try {
            console.log('🚪 Iniciando logout...');
            
            // Llamar al endpoint de logout si existe
            if (this.token) {
                try {
                    await fetch('/api/auth/logout', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${this.token}`
                        }
                    });
                } catch (error) {
                    console.warn('⚠️ Error llamando endpoint de logout:', error);
                }
            }

            // Limpiar datos locales
            this.clearSession();

            // Emitir evento
            window.dispatchEvent(new CustomEvent('userLoggedOut'));

            console.log('✅ Logout exitoso');

        } catch (error) {
            console.error('❌ Error en logout:', error);
            // Limpiar datos locales aunque falle el logout del servidor
            this.clearSession();
        }
    }

    /**
     * Renovar token
     */
    async refreshToken() {
        try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
                return false;
            }

            console.log('🔄 Renovando token...');
            
            const response = await fetch('/api/auth/refresh', {
                method: 'POST',
                headers: {
                    'Authorization': `Bearer ${refreshToken}`
                }
            });

            if (!response.ok) {
                return false;
            }

            const data = await response.json();
            
            // Actualizar tokens
            this.token = data.access_token;
            localStorage.setItem('access_token', this.token);
            
            if (data.refresh_token) {
                localStorage.setItem('refresh_token', data.refresh_token);
            }

            console.log('✅ Token renovado exitosamente');
            return true;

        } catch (error) {
            console.error('❌ Error renovando token:', error);
            return false;
        }
    }

    /**
     * Validar con el servidor
     */
    async validateWithServer() {
        try {
            if (!this.token) {
                return false;
            }

            const response = await fetch('/api/auth/validate', {
                method: 'GET',
                headers: {
                    'Authorization': `Bearer ${this.token}`
                }
            });

            return response.ok;

        } catch (error) {
            console.error('❌ Error validando con servidor:', error);
            return false;
        }
    }

    /**
     * Verificar si el token está expirado
     */
    isTokenExpired(token) {
        try {
            const payload = this.decodeJWT(token);
            if (!payload || !payload.exp) {
                return true;
            }

            const now = Math.floor(Date.now() / 1000);
            return payload.exp < now;

        } catch (error) {
            console.error('❌ Error decodificando token:', error);
            return true;
        }
    }

    /**
     * Verificar si necesita refresh
     */
    needsRefresh() {
        if (!this.token) {
            return false;
        }

        try {
            const payload = this.decodeJWT(this.token);
            if (!payload || !payload.exp) {
                return true;
            }

            const now = Math.floor(Date.now() / 1000);
            const timeUntilExpiry = (payload.exp - now) * 1000;
            
            return timeUntilExpiry < this.refreshThreshold;

        } catch (error) {
            console.error('❌ Error verificando refresh:', error);
            return true;
        }
    }

    /**
     * Verificar si la sesión ha expirado por inactividad
     */
    isSessionTimedOut() {
        const lastActivity = localStorage.getItem('last_activity');
        if (!lastActivity) {
            return true;
        }

        const now = Date.now();
        const timeSinceActivity = now - parseInt(lastActivity);
        
        return timeSinceActivity > this.sessionTimeout;
    }

    /**
     * Actualizar última actividad
     */
    updateLastActivity() {
        localStorage.setItem('last_activity', Date.now().toString());
    }

    /**
     * Decodificar JWT
     */
    decodeJWT(token) {
        try {
            const parts = token.split('.');
            if (parts.length !== 3) {
                return null;
            }

            const payload = parts[1];
            const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
            return JSON.parse(decoded);

        } catch (error) {
            console.error('❌ Error decodificando JWT:', error);
            return null;
        }
    }

    /**
     * Limpiar sesión
     */
    clearSession() {
        this.token = null;
        this.user = null;
        
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
        localStorage.removeItem('last_activity');
    }

    /**
     * Manejar falta de sesión
     */
    handleNoSession() {
        const currentPath = window.location.pathname;
        const protectedPaths = ['/dashboard', '/', '/index'];

        if (protectedPaths.includes(currentPath)) {
            console.log('🔒 Página protegida sin sesión, redirigiendo al login');
            window.location.href = '/login';
        }
    }

    /**
     * Manejar sesión expirada
     */
    handleSessionExpired() {
        console.log('⏰ Sesión expirada, limpiando datos y redirigiendo');
        this.clearSession();
        
        // Mostrar mensaje de sesión expirada
        this.showSessionExpiredMessage();
        
        // Redirigir al login
        setTimeout(() => {
            window.location.href = '/login';
        }, 2000);
    }

    /**
     * Mostrar mensaje de sesión expirada
     */
    showSessionExpiredMessage() {
        // Crear banner de sesión expirada
        const banner = document.createElement('div');
        banner.className = 'session-expired-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <div class="banner-icon">⚠️</div>
                <div class="banner-text">
                    <h3>Sesión Expirada</h3>
                    <p>Tu sesión ha expirado por seguridad. Serás redirigido al login.</p>
                </div>
            </div>
        `;

        // Estilos
        banner.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            background: #ff6b6b;
            color: white;
            padding: 15px 20px;
            border-radius: 8px;
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
            z-index: 10000;
            max-width: 400px;
            animation: slideIn 0.3s ease-out;
        `;

        // Agregar animación
        const style = document.createElement('style');
        style.textContent = `
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
        `;
        document.head.appendChild(style);

        document.body.appendChild(banner);

        // Auto-remover después de 5 segundos
        setTimeout(() => {
            if (banner.parentNode) {
                banner.remove();
            }
        }, 5000);
    }

    /**
     * Configurar refresh automático
     */
    setupAutomaticRefresh() {
        // Verificar cada 5 minutos
        setInterval(() => {
            this.checkSession();
        }, 5 * 60 * 1000);
    }

    /**
     * Obtener token actual
     */
    getToken() {
        return this.token;
    }

    /**
     * Obtener usuario actual
     */
    getUser() {
        return this.user;
    }

    /**
     * Verificar si está autenticado
     */
    isAuthenticated() {
        return !!(this.token && this.user && !this.isTokenExpired(this.token));
    }

    /**
     * Obtener headers de autorización
     */
    getAuthHeaders() {
        if (!this.token) {
            return {};
        }

        return {
            'Authorization': `Bearer ${this.token}`
        };
    }
}

// Crear instancia global
window.unifiedAuth = new UnifiedAuthManager();

// Exportar para uso en otros módulos
window.UnifiedAuthManager = UnifiedAuthManager;
