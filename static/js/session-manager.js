/**
 * Session Manager - Manejo unificado de sesiones web y JWT
 * Unifica expiraciones y manejo de errores 401
 */

class SessionManager {
    constructor() {
        this.sessionTimeout = 30 * 60 * 1000; // 30 minutos
        this.jwtTimeout = 60 * 60 * 1000; // 1 hora
        this.refreshThreshold = 5 * 60 * 1000; // 5 minutos
        this.sessionCheckInterval = null;
        this.lastActivity = Date.now();
        this.isSessionValid = true;
        this.init();
    }

    init() {
        // Setup session monitoring
        this.setupSessionMonitoring();
        
        // Setup activity tracking
        this.setupActivityTracking();
        
        // Setup unified error handling
        this.setupUnifiedErrorHandling();
        
        // Check initial session state
        this.checkInitialSession();
    }

    /**
     * Setup session monitoring
     */
    setupSessionMonitoring() {
        // Check session every minute
        this.sessionCheckInterval = setInterval(() => {
            this.checkSession();
        }, 60000);

        // Check session on page visibility change
        document.addEventListener('visibilitychange', () => {
            if (!document.hidden) {
                this.checkSession();
            }
        });

        // Check session on window focus
        window.addEventListener('focus', () => {
            this.checkSession();
        });
    }

    /**
     * Setup activity tracking
     */
    setupActivityTracking() {
        const events = ['mousedown', 'mousemove', 'keypress', 'scroll', 'touchstart', 'click'];
        
        events.forEach(event => {
            document.addEventListener(event, () => {
                this.updateLastActivity();
            }, true);
        });
    }

    /**
     * Update last activity timestamp
     */
    updateLastActivity() {
        this.lastActivity = Date.now();
    }

    /**
     * Setup unified error handling
     */
    setupUnifiedErrorHandling() {
        // Override fetch to handle 401 responses
        const originalFetch = window.fetch;
        
        window.fetch = async (url, options = {}) => {
            try {
                const response = await originalFetch(url, options);
                
                // Handle 401 Unauthorized
                if (response.status === 401) {
                    await this.handleUnauthorized();
                }
                
                return response;
            } catch (error) {
                // Handle network errors
                if (error.name === 'TypeError' && error.message.includes('fetch')) {
                    this.handleNetworkError();
                }
                throw error;
            }
        };
    }

    /**
     * Check initial session
     */
    async checkInitialSession() {
        try {
            // Check both session and JWT
            const sessionValid = await this.checkWebSession();
            const jwtValid = await this.checkJWTSession();
            
            if (!sessionValid || !jwtValid) {
                await this.handleSessionExpired();
            }
        } catch (error) {
            console.error('Error checking initial session:', error);
            await this.handleSessionExpired();
        }
    }

    /**
     * Check session
     */
    async checkSession() {
        try {
            // Check web session
            const sessionValid = await this.checkWebSession();
            
            // Check JWT session
            const jwtValid = await this.checkJWTSession();
            
            // Check activity timeout
            const activityValid = this.checkActivityTimeout();
            
            if (!sessionValid || !jwtValid || !activityValid) {
                await this.handleSessionExpired();
                return;
            }

            // Check if refresh is needed
            await this.checkRefreshNeeded();
            
        } catch (error) {
            console.error('Error checking session:', error);
            await this.handleSessionExpired();
        }
    }

    /**
     * Check web session
     */
    async checkWebSession() {
        try {
            const response = await fetch('/api/auth/session', {
                method: 'GET',
                credentials: 'include'
            });
            
            return response.ok;
        } catch (error) {
            console.error('Error checking web session:', error);
            return false;
        }
    }

    /**
     * Check JWT session
     */
    async checkJWTSession() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) return false;

            // Validate JWT token
            if (window.jwtValidator) {
                const validation = window.jwtValidator.validateToken(token);
                if (!validation.valid) {
                    return false;
                }
            }

            // Check expiration
            const payload = this.decodeJWT(token);
            if (!payload || !payload.exp) return false;

            const now = Math.floor(Date.now() / 1000);
            return payload.exp > now;
        } catch (error) {
            console.error('Error checking JWT session:', error);
            return false;
        }
    }

    /**
     * Check activity timeout
     */
    checkActivityTimeout() {
        const timeSinceActivity = Date.now() - this.lastActivity;
        return timeSinceActivity < this.sessionTimeout;
    }

    /**
     * Check if refresh is needed
     */
    async checkRefreshNeeded() {
        try {
            const token = localStorage.getItem('access_token');
            if (!token) return;

            const timeUntilExpiry = this.getTimeUntilExpiry(token);
            if (timeUntilExpiry < this.refreshThreshold) {
                await this.refreshTokens();
            }
        } catch (error) {
            console.error('Error checking refresh needed:', error);
        }
    }

    /**
     * Refresh tokens
     */
    async refreshTokens() {
        try {
            const refreshToken = localStorage.getItem('refresh_token');
            if (!refreshToken) {
                throw new Error('No refresh token available');
            }

            const response = await fetch('/api/auth/refresh', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({
                    refresh_token: refreshToken
                }),
                credentials: 'include'
            });

            if (!response.ok) {
                throw new Error('Token refresh failed');
            }

            const data = await response.json();
            
            // Update tokens
            localStorage.setItem('access_token', data.access_token);
            if (data.refresh_token) {
                localStorage.setItem('refresh_token', data.refresh_token);
            }

            // Update last activity
            this.updateLastActivity();

        } catch (error) {
            console.error('Error refreshing tokens:', error);
            await this.handleSessionExpired();
        }
    }

    /**
     * Handle unauthorized response (401)
     */
    async handleUnauthorized() {
        // Try to refresh tokens first
        try {
            await this.refreshTokens();
            return;
        } catch (error) {
            // If refresh fails, handle as expired
            await this.handleSessionExpired();
        }
    }

    /**
     * Handle session expired
     */
    async handleSessionExpired() {
        if (!this.isSessionValid) return; // Prevent multiple calls
        
        this.isSessionValid = false;
        
        // Clear tokens
        this.clearTokens();
        
        // Show session expired banner
        this.showSessionExpiredBanner();
        
        // Redirect to login after delay
        setTimeout(() => {
            this.redirectToLogin();
        }, 3000);
    }

    /**
     * Handle network error
     */
    handleNetworkError() {
        this.showNetworkErrorBanner();
    }

    /**
     * Show session expired banner
     */
    showSessionExpiredBanner() {
        const banner = document.createElement('div');
        banner.className = 'session-expired-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <div class="banner-icon">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 19.5c-.77.833.192 2.5 1.732 2.5z"></path>
                    </svg>
                </div>
                <div class="banner-text">
                    <h3>Tu sesión ha expirado</h3>
                    <p>Por seguridad, tu sesión ha expirado. Serás redirigido al login en unos segundos.</p>
                </div>
                <button class="banner-close" onclick="this.parentElement.parentElement.remove()">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;

        document.body.appendChild(banner);

        // Auto-remove after 5 seconds
        setTimeout(() => {
            if (banner.parentNode) {
                banner.remove();
            }
        }, 5000);
    }

    /**
     * Show network error banner
     */
    showNetworkErrorBanner() {
        const banner = document.createElement('div');
        banner.className = 'network-error-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <div class="banner-icon">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"></path>
                    </svg>
                </div>
                <div class="banner-text">
                    <h3>Error de conexión</h3>
                    <p>No se pudo conectar con el servidor. Verifica tu conexión a internet.</p>
                </div>
                <button class="banner-close" onclick="this.parentElement.parentElement.remove()">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"></path>
                    </svg>
                </button>
            </div>
        `;

        document.body.appendChild(banner);

        // Auto-remove after 10 seconds
        setTimeout(() => {
            if (banner.parentNode) {
                banner.remove();
            }
        }, 10000);
    }

    /**
     * Redirect to login
     */
    redirectToLogin() {
        const currentPath = window.location.pathname;
        const loginUrl = `/login?redirect=${encodeURIComponent(currentPath)}`;
        window.location.href = loginUrl;
    }

    /**
     * Decode JWT token
     */
    decodeJWT(token) {
        try {
            const parts = token.split('.');
            if (parts.length !== 3) return null;

            const payload = parts[1];
            const decoded = atob(payload.replace(/-/g, '+').replace(/_/g, '/'));
            return JSON.parse(decoded);
        } catch (error) {
            console.error('Error decoding JWT:', error);
            return null;
        }
    }

    /**
     * Get time until token expiry
     */
    getTimeUntilExpiry(token) {
        try {
            const payload = this.decodeJWT(token);
            if (!payload || !payload.exp) return 0;

            const now = Math.floor(Date.now() / 1000);
            return (payload.exp - now) * 1000; // Convert to milliseconds
        } catch (error) {
            console.error('Error getting time until expiry:', error);
            return 0;
        }
    }

    /**
     * Clear all tokens
     */
    clearTokens() {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        localStorage.removeItem('user');
    }

    /**
     * Get authenticated headers
     */
    getAuthHeaders() {
        const token = localStorage.getItem('access_token');
        if (!token) return {};

        return {
            'Authorization': `Bearer ${token}`
        };
    }

    /**
     * Make authenticated request
     */
    async makeAuthenticatedRequest(url, options = {}) {
        const headers = {
            ...this.getAuthHeaders(),
            ...options.headers
        };

        const response = await fetch(url, {
            ...options,
            headers,
            credentials: 'include' // Include cookies for web session
        });

        if (response.status === 401) {
            await this.handleUnauthorized();
        }

        return response;
    }

    /**
     * Check if user is authenticated
     */
    isAuthenticated() {
        const token = localStorage.getItem('access_token');
        if (!token) return false;

        try {
            const payload = this.decodeJWT(token);
            if (!payload) return false;

            const now = Math.floor(Date.now() / 1000);
            return payload.exp && payload.exp > now;
        } catch (error) {
            return false;
        }
    }

    /**
     * Get current user info
     */
    getCurrentUser() {
        try {
            const userStr = localStorage.getItem('user');
            return userStr ? JSON.parse(userStr) : null;
        } catch (error) {
            return null;
        }
    }

    /**
     * Logout user
     */
    async logout() {
        try {
            // Call logout endpoint
            await fetch('/api/auth/logout', {
                method: 'POST',
                headers: this.getAuthHeaders(),
                credentials: 'include'
            });
        } catch (error) {
            console.error('Error during logout:', error);
        } finally {
            // Clear tokens and redirect
            this.clearTokens();
            window.location.href = '/login';
        }
    }

    /**
     * Clean up resources
     */
    cleanup() {
        if (this.sessionCheckInterval) {
            clearInterval(this.sessionCheckInterval);
        }
    }
}

// Initialize session manager
const sessionManager = new SessionManager();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.sessionManager = sessionManager;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = SessionManager;
}
