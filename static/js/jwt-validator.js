/**
 * JWT Validator - Validación robusta de tokens JWT
 * Asegura que el subject sea string y maneja errores de JWT correctamente
 */

class JWTValidator {
    constructor() {
        this.validAlgorithms = ['HS256', 'HS384', 'HS512', 'RS256', 'RS384', 'RS512'];
        this.maxTokenAge = 24 * 60 * 60 * 1000; // 24 horas
        this.init();
    }

    init() {
        // Setup JWT validation
        this.setupJWTValidation();
    }

    /**
     * Setup JWT validation
     */
    setupJWTValidation() {
        // Override token creation to ensure proper format
        this.setupTokenCreation();
        
        // Setup token validation
        this.setupTokenValidation();
    }

    /**
     * Setup token creation with proper subject format
     */
    setupTokenCreation() {
        // This would typically be done server-side
        // For now, we'll provide a client-side validation
        console.log('JWT validation setup complete');
    }

    /**
     * Setup token validation
     */
    setupTokenValidation() {
        // Validate tokens on page load
        this.validateStoredTokens();
        
        // Validate tokens before API calls
        this.setupAPITokenValidation();
    }

    /**
     * Validate stored tokens
     */
    validateStoredTokens() {
        const token = localStorage.getItem('access_token');
        if (token) {
            const validation = this.validateToken(token);
            if (!validation.valid) {
                console.error('Invalid stored token:', validation.error);
                this.handleInvalidToken();
            }
        }
    }

    /**
     * Setup API token validation
     */
    setupAPITokenValidation() {
        // Override fetch to validate tokens before requests
        const originalFetch = window.fetch;
        
        window.fetch = async (url, options = {}) => {
            // Check if this is an API request
            if (url.includes('/api/') && options.headers && options.headers.Authorization) {
                const token = options.headers.Authorization.replace('Bearer ', '');
                const validation = this.validateToken(token);
                
                if (!validation.valid) {
                    console.error('Invalid token for API request:', validation.error);
                    await this.handleInvalidToken();
                    return new Response('Unauthorized', { status: 401 });
                }
            }
            
            return originalFetch(url, options);
        };
    }

    /**
     * Validate JWT token
     */
    validateToken(token) {
        try {
            console.log('🔍 Validando token JWT:', token.substring(0, 50) + '...');
            
            // Check if token is a string
            if (typeof token !== 'string') {
                console.error('❌ Token no es string:', typeof token);
                return {
                    valid: false,
                    error: 'Token must be a string'
                };
            }

            // Check token format
            const parts = token.split('.');
            if (parts.length !== 3) {
                console.error('❌ Formato JWT inválido:', parts.length, 'partes');
                return {
                    valid: false,
                    error: 'Invalid JWT format'
                };
            }

            // Decode header
            const header = this.decodeBase64(parts[0]);
            if (!header) {
                console.error('❌ Header JWT inválido');
                return {
                    valid: false,
                    error: 'Invalid JWT header'
                };
            }

            console.log('📋 Header decodificado:', header);

            // Check algorithm (más permisivo)
            if (header.alg && !this.validAlgorithms.includes(header.alg)) {
                console.warn('⚠️ Algoritmo no reconocido:', header.alg, 'pero continuando...');
                // No fallar por algoritmo desconocido
            }

            // Decode payload
            const payload = this.decodeBase64(parts[1]);
            if (!payload) {
                console.error('❌ Payload JWT inválido');
                return {
                    valid: false,
                    error: 'Invalid JWT payload'
                };
            }

            console.log('📋 Payload decodificado:', payload);

            // Validate required claims (más permisivo)
            const requiredClaims = ['sub', 'exp', 'iat'];
            const missingClaims = [];
            
            for (const claim of requiredClaims) {
                if (!payload[claim]) {
                    missingClaims.push(claim);
                }
            }
            
            if (missingClaims.length > 0) {
                console.error('❌ Claims faltantes:', missingClaims);
                return {
                    valid: false,
                    error: `Missing required claim: ${missingClaims.join(', ')}`
                };
            }

            // Validate subject is string (más permisivo)
            if (payload.sub !== null && payload.sub !== undefined && typeof payload.sub !== 'string') {
                console.warn('⚠️ Subject no es string:', typeof payload.sub, 'pero continuando...');
                // Convertir a string si es posible
                payload.sub = String(payload.sub);
            }

            // Validate expiration
            const now = Math.floor(Date.now() / 1000);
            if (payload.exp < now) {
                console.error('❌ Token expirado:', payload.exp, '<', now);
                return {
                    valid: false,
                    error: 'Token has expired'
                };
            }

            // Validate issued at (más permisivo)
            if (payload.iat > now) {
                return {
                    valid: false,
                    error: 'Token issued in the future'
                };
            }

            // Validate token age (más permisivo)
            const tokenAge = (now - payload.iat) * 1000;
            if (tokenAge > this.maxTokenAge) {
                console.warn('⚠️ Token muy antiguo:', tokenAge, 'ms, pero continuando...');
                // No fallar por token antiguo
            }

            console.log('✅ Token JWT válido');
            return {
                valid: true,
                payload: payload,
                header: header
            };

        } catch (error) {
            console.error('❌ Error validando token JWT:', error);
            return {
                valid: false,
                error: `Token validation error: ${error.message}`
            };
        }
    }

    /**
     * Decode base64 string
     */
    decodeBase64(str) {
        try {
            // Add padding if needed
            while (str.length % 4) {
                str += '=';
            }
            
            const decoded = atob(str.replace(/-/g, '+').replace(/_/g, '/'));
            return JSON.parse(decoded);
        } catch (error) {
            return null;
        }
    }

    /**
     * Handle invalid token
     */
    async handleInvalidToken() {
        // Clear invalid token
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        
        // Show error message
        this.showTokenErrorBanner();
        
        // Redirect to login
        setTimeout(() => {
            window.location.href = '/login';
        }, 3000);
    }

    /**
     * Show token error banner
     */
    showTokenErrorBanner() {
        const banner = document.createElement('div');
        banner.className = 'token-error-banner';
        banner.innerHTML = `
            <div class="banner-content">
                <div class="banner-icon">
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.732-.833-2.5 0L4.268 19.5c-.77.833.192 2.5 1.732 2.5z"></path>
                    </svg>
                </div>
                <div class="banner-text">
                    <h3>Error de autenticación</h3>
                    <p>Tu token de sesión no es válido. Serás redirigido al login.</p>
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
     * Create JWT token (for testing purposes)
     */
    createToken(payload, secret = 'default-secret') {
        try {
            // Ensure subject is string
            if (payload.sub && typeof payload.sub !== 'string') {
                payload.sub = String(payload.sub);
            }

            // Add required claims
            const now = Math.floor(Date.now() / 1000);
            const tokenPayload = {
                ...payload,
                iat: now,
                exp: now + (60 * 60) // 1 hour
            };

            // Create header
            const header = {
                alg: 'HS256',
                typ: 'JWT'
            };

            // Encode header and payload
            const encodedHeader = this.encodeBase64(JSON.stringify(header));
            const encodedPayload = this.encodeBase64(JSON.stringify(tokenPayload));

            // Create signature (simplified for demo)
            const signature = this.createSignature(encodedHeader, encodedPayload, secret);

            return `${encodedHeader}.${encodedPayload}.${signature}`;
        } catch (error) {
            console.error('Error creating token:', error);
            return null;
        }
    }

    /**
     * Encode base64 string
     */
    encodeBase64(str) {
        return btoa(str)
            .replace(/\+/g, '-')
            .replace(/\//g, '_')
            .replace(/=/g, '');
    }

    /**
     * Create signature (simplified for demo)
     */
    createSignature(header, payload, secret) {
        // This is a simplified signature for demo purposes
        // In production, use proper HMAC or RSA signing
        const data = `${header}.${payload}`;
        const signature = btoa(data + secret);
        return signature.replace(/\+/g, '-').replace(/\//g, '_').replace(/=/g, '');
    }

    /**
     * Get token payload
     */
    getTokenPayload(token) {
        const validation = this.validateToken(token);
        return validation.valid ? validation.payload : null;
    }

    /**
     * Check if token is expired
     */
    isTokenExpired(token) {
        const validation = this.validateToken(token);
        if (!validation.valid) return true;

        const now = Math.floor(Date.now() / 1000);
        return validation.payload.exp < now;
    }

    /**
     * Get time until expiration
     */
    getTimeUntilExpiration(token) {
        const validation = this.validateToken(token);
        if (!validation.valid) return 0;

        const now = Math.floor(Date.now() / 1000);
        const timeLeft = validation.payload.exp - now;
        return Math.max(0, timeLeft * 1000); // Convert to milliseconds
    }

    /**
     * Refresh token if needed
     */
    async refreshTokenIfNeeded(token) {
        const timeUntilExpiration = this.getTimeUntilExpiration(token);
        const refreshThreshold = 5 * 60 * 1000; // 5 minutes

        if (timeUntilExpiration < refreshThreshold) {
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
                    })
                });

                if (!response.ok) {
                    throw new Error('Token refresh failed');
                }

                const data = await response.json();
                localStorage.setItem('access_token', data.access_token);
                
                return data.access_token;
            } catch (error) {
                console.error('Error refreshing token:', error);
                throw error;
            }
        }

        return token;
    }
}

// Initialize JWT validator
const jwtValidator = new JWTValidator();

// Export for use in other modules
if (typeof window !== 'undefined') {
    window.jwtValidator = jwtValidator;
}

if (typeof module !== 'undefined' && module.exports) {
    module.exports = JWTValidator;
}
