// ========================================
// UTILIDADES DE PÁGINA - GUARDIAS Y DETECCIÓN
// ========================================

// Detector de página actual
class PageDetector {
    constructor() {
        this.currentPage = this.detectCurrentPage();
    }

    // Detectar la página actual basándose en la URL y elementos del DOM
    detectCurrentPage() {
        const path = window.location.pathname;
        
        // Detectar por URL
        if (path === '/login' || path.includes('login')) {
            return 'login';
        }
        
        if (path === '/profile' || path.includes('profile')) {
            return 'profile';
        }
        
        if (path === '/change-password' || path.includes('change-password')) {
            return 'change-password';
        }
        
        if (path === '/' || path === '/index' || path.includes('dashboard')) {
            return 'dashboard';
        }
        
        // Detectar por elementos específicos del DOM
        if (document.getElementById('loginForm')) {
            return 'login';
        }
        
        if (document.getElementById('dashboard')) {
            return 'dashboard';
        }
        
        if (document.getElementById('profileForm')) {
            return 'profile';
        }
        
        if (document.getElementById('changePasswordForm')) {
            return 'change-password';
        }
        
        // Página por defecto
        return 'unknown';
    }

    // Verificar si estamos en una página específica
    isPage(pageName) {
        return this.currentPage === pageName;
    }

    // Verificar si estamos en el dashboard
    isDashboard() {
        return this.currentPage === 'dashboard';
    }

    // Verificar si estamos en el login
    isLogin() {
        return this.currentPage === 'login';
    }

    // Verificar si estamos en el perfil
    isProfile() {
        return this.currentPage === 'profile';
    }

    // Verificar si estamos en cambio de contraseña
    isChangePassword() {
        return this.currentPage === 'change-password';
    }

    // Obtener la página actual
    getCurrentPage() {
        return this.currentPage;
    }
}

// Sistema de guardias para elementos del DOM
class DOMGuard {
    constructor() {
        this.pageDetector = new PageDetector();
    }

    // Verificar si un elemento existe antes de usarlo
    elementExists(selector) {
        return document.querySelector(selector) !== null;
    }

    // Verificar si múltiples elementos existen
    elementsExist(selectors) {
        return selectors.every(selector => this.elementExists(selector));
    }

    // Ejecutar función solo si el elemento existe
    safeExecute(selector, callback, fallback = null) {
        const element = document.querySelector(selector);
        if (element) {
            return callback(element);
        } else if (fallback) {
            return fallback();
        }
        return null;
    }

    // Agregar event listener de forma segura
    safeAddEventListener(selector, event, callback, options = {}) {
        const element = document.querySelector(selector);
        if (element) {
            element.addEventListener(event, callback, options);
            return true;
        }
        return false;
    }

    // Agregar múltiples event listeners de forma segura
    safeAddEventListeners(selectors, event, callback, options = {}) {
        let addedCount = 0;
        selectors.forEach(selector => {
            if (this.safeAddEventListener(selector, event, callback, options)) {
                addedCount++;
            }
        });
        return addedCount;
    }

    // Ejecutar código solo en páginas específicas
    executeOnPage(pageName, callback) {
        if (this.pageDetector.isPage(pageName)) {
            return callback();
        }
        return null;
    }

    // Ejecutar código solo en el dashboard
    executeOnDashboard(callback) {
        return this.executeOnPage('dashboard', callback);
    }

    // Ejecutar código solo en el login
    executeOnLogin(callback) {
        return this.executeOnPage('login', callback);
    }

    // Ejecutar código solo en el perfil
    executeOnProfile(callback) {
        return this.executeOnPage('profile', callback);
    }

    // Ejecutar código solo en cambio de contraseña
    executeOnChangePassword(callback) {
        return this.executeOnPage('change-password', callback);
    }

    // Ejecutar código en múltiples páginas
    executeOnPages(pageNames, callback) {
        if (pageNames.includes(this.pageDetector.getCurrentPage())) {
            return callback();
        }
        return null;
    }

    // Ejecutar código en todas las páginas excepto las especificadas
    executeOnPagesExcept(excludedPages, callback) {
        if (!excludedPages.includes(this.pageDetector.getCurrentPage())) {
            return callback();
        }
        return null;
    }
}

// Función helper para inicialización segura
function safeInitialize(initializers) {
    const guard = new DOMGuard();
    
    initializers.forEach(initializer => {
        if (initializer.condition && initializer.condition(guard)) {
            try {
                initializer.callback(guard);
            } catch (error) {
                console.warn(`Error en inicialización de ${initializer.name}:`, error);
            }
        }
    });
}

// Exportar para uso global
window.PageDetector = PageDetector;
window.DOMGuard = DOMGuard;
window.safeInitialize = safeInitialize;
