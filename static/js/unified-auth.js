/**
 * Sistema de Autenticación Unificado
 * Maneja JWT de acceso en headers y refresh token también en headers.
 * - Rutas por defecto: /auth/login, /auth/refresh, /auth/validate, /auth/logout
 * - Si tu backend usa /api/auth/*, cambia this.baseAuthPath en el constructor.
 */

class UnifiedAuthManager {
    constructor() {
      /** Ruta base del blueprint de autenticación en el backend */
      this.baseAuthPath = '/api/auth'; // Endpoint correcto para la API
  
      this.token = null;           // access_token en memoria
      this.user = null;            // usuario actual
      this.isInitialized = false;
  
      /** Timeout por inactividad (ms) */
      this.sessionTimeout = 30 * 60 * 1000; // 30 minutos
      /** Umbral de refresh (ms) antes de expirar el access token */
      this.refreshThreshold = 5 * 60 * 1000; // 5 minutos
  
      /** Flag para evitar refrescos simultáneos entre pestañas */
      this._refreshInFlight = null;
  
      this.init();
    }
  
    /**
     * Inicializar el sistema de autenticación
     */
    init() {
      console.log('🔐 Inicializando sistema de autenticación unificado...');
  
      // Cargar datos del storage
      this.loadStoredData();
  
      // Listeners de interacción y sincronización entre pestañas
      this.setupEventListeners();
  
      // Verificar sesión inicial
      this.checkInitialSession();
  
      // Programar refresh automático dinámico
      this.setupAutomaticRefresh();
  
      this.isInitialized = true;
      console.log('✅ Sistema de autenticación inicializado');
    }
  
    /**
     * Cargar datos almacenados en localStorage
     */
    loadStoredData() {
      this.token = localStorage.getItem('access_token');
      this.user = JSON.parse(localStorage.getItem('user') || 'null');
  
      if (this.token && this.user) {
        console.log('📱 Sesión cargada:', {
          user: this.user.username,
          role: this.user.role,
          tokenLength: this.token.length,
        });
      }
    }
  
    /**
     * Event listeners: storage (multitab), interacción (actividad), login/logout
     */
    setupEventListeners() {
      // Mantener sincronizadas las pestañas
      window.addEventListener('storage', (e) => {
        if (e.key === 'access_token' || e.key === 'user' || e.key === 'refresh_token') {
          this.loadStoredData();
        }
      });
  
      // Marcar actividad del usuario
      ['click', 'keydown', 'mousemove', 'touchstart', 'visibilitychange'].forEach((evt) => {
        window.addEventListener(evt, () => this.updateLastActivity(), { passive: true });
      });
  
      // Eventos de login/logout disparados por la app
      window.addEventListener('userLoggedIn', (e) => {
        this.user = e.detail;
        this.loadStoredData();
      });
  
      window.addEventListener('userLoggedOut', () => {
        this.clearSession();
      });
    }
  
    /**
     * Verificar sesión al iniciar
     */
    async checkInitialSession() {
      try {
        if (!this.token || !this.user) {
          console.log('🔍 No hay sesión activa');
          this.handleNoSession();
          return;
        }
  
        console.log('🔍 Verificando sesión inicial...');
  
        // Renovar si el token está expirado
        if (this.isTokenExpired(this.token)) {
          console.log('⏰ Token expirado, intentando renovar...');
          const refreshed = await this.refreshToken();
          if (!refreshed) {
            this.handleSessionExpired();
            return;
          }
        }
  
        // Validar contra el servidor (y sincronizar user si viene en la respuesta)
        const isValid = await this.validateWithServer();
        if (!isValid) {
          console.log('❌ Sesión inválida según el servidor');
          this.handleSessionExpired();
          return;
        }
  
        // A falta de marca previa, no expulsar por inactividad
        if (!localStorage.getItem('last_activity')) {
          this.updateLastActivity();
        }
  
        console.log('✅ Sesión válida');
      } catch (error) {
        console.error('❌ Error verificando sesión inicial:', error);
        this.handleSessionExpired();
      }
    }
  
    /**
     * Chequeos periódicos: refresh e inactividad
     */
    async checkSession() {
      try {
        if (!this.token || !this.user) return;
  
        // ¿Necesita refresh?
        if (this.needsRefresh()) {
          console.log('🔄 Token cerca de expirar, intentando refresh...');
          const refreshed = await this.refreshToken();
          if (!refreshed) {
            this.handleSessionExpired();
            return;
          }
        }
  
        // ¿Expirada por inactividad?
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
  
        const response = await fetch(`${this.baseAuthPath}/login`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          // No usamos cookies httpOnly en este flujo; todo va por headers
          body: JSON.stringify({ username, password }),
        });
  
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
          throw new Error(data.message || 'Error en el login');
        }
  
        // Guardar tokens y usuario
        this.token = data.access_token;
        this.user = data.user;
  
        localStorage.setItem('access_token', this.token);
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
        localStorage.setItem('user', JSON.stringify(this.user));
  
        console.log('✅ Login exitoso:', { user: this.user.username, role: this.user.role });
  
        // Notificar a la app
        window.dispatchEvent(new CustomEvent('userLoggedIn', { detail: this.user }));
  
        // Marcar actividad
        this.updateLastActivity();
  
        // Reprogramar refresco dinámico
        this.setupAutomaticRefresh(true);
  
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
  
        if (this.token) {
          try {
            await fetch(`${this.baseAuthPath}/logout`, {
              method: 'POST',
              headers: { Authorization: `Bearer ${this.token}` },
            });
          } catch (error) {
            console.warn('⚠️ Error llamando endpoint de logout:', error);
          }
        }
  
        this.clearSession();
        window.dispatchEvent(new CustomEvent('userLoggedOut'));
  
        console.log('✅ Logout exitoso');
      } catch (error) {
        console.error('❌ Error en logout:', error);
        this.clearSession();
      }
    }
  
    /**
     * Renovar access token usando refresh token (en headers)
     * - Usa guard para evitar llamadas simultáneas
     */
    async refreshToken() {
      if (this._refreshInFlight) return this._refreshInFlight;
      this._refreshInFlight = this._doRefresh().finally(() => (this._refreshInFlight = null));
      return this._refreshInFlight;
    }
  
    async _doRefresh() {
      const refreshToken = localStorage.getItem('refresh_token');
      if (!refreshToken) return false;
  
      try {
        console.log('🔄 Renovando token...');
        const response = await fetch(`${this.baseAuthPath}/refresh`, {
          method: 'POST',
          headers: { Authorization: `Bearer ${refreshToken}` },
        });
  
        if (!response.ok) return false;
  
        const data = await response.json().catch(() => ({}));
        if (!data.access_token) return false;
  
        // Actualizar tokens
        this.token = data.access_token;
        localStorage.setItem('access_token', this.token);
        if (data.refresh_token) {
          localStorage.setItem('refresh_token', data.refresh_token);
        }
  
        // Mantener sesión activa por interacción "implícita"
        this.updateLastActivity();
  
        console.log('✅ Token renovado exitosamente');
  
        // Reprogramar refresco dinámico
        this.setupAutomaticRefresh(true);
  
        return true;
      } catch (error) {
        console.error('❌ Error renovando token:', error);
        return false;
      }
    }
  
    /**
     * Validar token actual con el servidor y sincronizar usuario si viene en la respuesta
     */
    async validateWithServer() {
      try {
        if (!this.token) return false;
  
        const response = await this.authFetch(`${this.baseAuthPath}/validate`, {
          method: 'GET',
        });
  
        if (!response.ok) return false;
  
        const data = await response.json().catch(() => null);
        if (data?.user) {
          this.user = data.user;
          localStorage.setItem('user', JSON.stringify(this.user));
        }
  
        return true;
      } catch (error) {
        console.error('❌ Error validando con servidor:', error);
        return false;
      }
    }
  
    /**
     * Fetch con Authorization y retry automático en 401 (intenta 1 refresh)
     */
    async authFetch(input, init = {}) {
      const withAuth = {
        ...init,
        headers: {
          ...(init.headers || {}),
          ...this.getAuthHeaders(),
        },
      };
  
      let res = await fetch(input, withAuth);
      if (res.status === 401) {
        const refreshed = await this.refreshToken();
        if (!refreshed) {
          this.handleSessionExpired();
          return res;
        }
        // Reintento con token fresco
        withAuth.headers = { ...(init.headers || {}), ...this.getAuthHeaders() };
        res = await fetch(input, withAuth);
      }
      return res;
    }
  
    /**
     * ¿Está expirado el token?
     */
    isTokenExpired(token) {
      try {
        const payload = this.decodeJWT(token);
        if (!payload || !payload.exp) return true;
        const now = Math.floor(Date.now() / 1000);
        return payload.exp < now;
      } catch (error) {
        console.error('❌ Error decodificando token:', error);
        return true;
      }
    }
  
    /**
     * ¿Necesita refresh según el umbral?
     */
    needsRefresh() {
      if (!this.token) return false;
      try {
        const payload = this.decodeJWT(this.token);
        if (!payload || !payload.exp) return true;
        const now = Math.floor(Date.now() / 1000);
        const timeUntilExpiry = (payload.exp - now) * 1000;
        return timeUntilExpiry < this.refreshThreshold;
      } catch (error) {
        console.error('❌ Error verificando refresh:', error);
        return true;
      }
    }
  
    /**
     * ¿Expiró la sesión por inactividad?
     * Si no hay marca de actividad, NO expulsar (se marca en login/validate/inicio de interacción)
     */
    isSessionTimedOut() {
      const lastActivity = localStorage.getItem('last_activity');
      if (!lastActivity) return false;
      const now = Date.now();
      const timeSinceActivity = now - parseInt(lastActivity, 10);
      return timeSinceActivity > this.sessionTimeout;
    }
  
    /**
     * Actualizar última actividad (marca milisegundos)
     */
    updateLastActivity() {
      localStorage.setItem('last_activity', Date.now().toString());
    }
  
    /**
     * Decodificar JWT (base64url + padding)
     */
    decodeJWT(token) {
      try {
        const parts = token.split('.');
        if (parts.length !== 3) return null;
        const base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
        const padded = base64 + '='.repeat((4 - (base64.length % 4)) % 4);
        const decoded = atob(padded);
        return JSON.parse(decoded);
      } catch (error) {
        console.error('❌ Error decodificando JWT:', error);
        return null;
      }
    }
  
    /**
     * Limpiar sesión (storage + memoria)
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
     * Manejar falta de sesión (redirigir si corresponde)
     */
    handleNoSession() {
      const currentPath = window.location.pathname;
      const protectedPaths = ['/dashboard', '/index']; // OJO: no proteger '/' si es home público
      if (protectedPaths.includes(currentPath)) {
        console.log('🔒 Página protegida sin sesión, redirigiendo al login');
        window.location.href = '/login';
      }
    }
  
    /**
     * Manejar sesión expirada (mensaje + redirect)
     */
    handleSessionExpired() {
      console.log('⏰ Sesión expirada, limpiando datos y redirigiendo');
      this.clearSession();
      this.showSessionExpiredMessage();
      setTimeout(() => {
        window.location.href = '/login';
      }, 2000);
    }
  
    /**
     * Banner visual de sesión expirada
     */
    showSessionExpiredMessage() {
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
      banner.style.cssText = `
        position: fixed; top: 20px; right: 20px;
        background: #ff6b6b; color: white;
        padding: 15px 20px; border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        z-index: 10000; max-width: 400px;
        animation: slideIn 0.3s ease-out;
      `;
      const style = document.createElement('style');
      style.textContent = `
        @keyframes slideIn {
          from { transform: translateX(100%); opacity: 0; }
          to   { transform: translateX(0);   opacity: 1; }
        }
      `;
      document.head.appendChild(style);
      document.body.appendChild(banner);
      setTimeout(() => banner.remove(), 5000);
    }
  
    /**
     * Refresh automático dinámico: programa un timeout hasta el umbral,
     * luego verifica sesión (que puede refrescar) y vuelve a programar.
     * Si forceReplan=true, reprograma sin esperar al timeout anterior.
     */
    setupAutomaticRefresh(forceReplan = false) {
      if (forceReplan && this._refreshTimer) {
        clearTimeout(this._refreshTimer);
        this._refreshTimer = null;
      }
      const schedule = () => {
        if (!this.token) {
          this._refreshTimer = setTimeout(schedule, 60_000);
          return;
        }
        const payload = this.decodeJWT(this.token);
        if (!payload || !payload.exp) {
          this._refreshTimer = setTimeout(schedule, 60_000);
          return;
        }
        const now = Math.floor(Date.now() / 1000);
        const msToExpiry = (payload.exp - now) * 1000;
        const msToThreshold = Math.max(0, msToExpiry - this.refreshThreshold);
        const delay = Math.min(msToThreshold, this.sessionTimeout); // seguridad
  
        this._refreshTimer = setTimeout(async () => {
          await this.checkSession();
          schedule(); // reprogramar
        }, delay);
      };
      schedule();
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
     * ¿Está autenticado?
     */
    isAuthenticated() {
      return !!(this.token && this.user && !this.isTokenExpired(this.token));
    }
  
    /**
     * Headers de autorización
     */
    getAuthHeaders() {
      if (!this.token) return {};
      return { Authorization: `Bearer ${this.token}` };
    }
  }
  
  // Instancia global
  window.unifiedAuth = new UnifiedAuthManager();
  // Export para otros módulos (si no usás bundler)
  window.UnifiedAuthManager = UnifiedAuthManager;
  