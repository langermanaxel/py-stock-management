/**
 * Feedback and loading states management
 */

class FeedbackManager {
    constructor() {
        this.toastContainer = null;
        this.init();
    }

    init() {
        this.createToastContainer();
        this.setupGlobalErrorHandling();
    }

    /**
     * Create toast container if it doesn't exist
     */
    createToastContainer() {
        if (!document.getElementById('toast-container')) {
            this.toastContainer = document.createElement('div');
            this.toastContainer.id = 'toast-container';
            this.toastContainer.className = 'toast-container';
            document.body.appendChild(this.toastContainer);
        } else {
            this.toastContainer = document.getElementById('toast-container');
        }
    }

    /**
     * Show toast notification
     */
    showToast(type, title, message, duration = 5000) {
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        
        const icon = this.getToastIcon(type);
        
        toast.innerHTML = `
            <div class="toast-icon">
                ${icon}
            </div>
            <div class="toast-content">
                <div class="toast-title">${title}</div>
                <div class="toast-message">${message}</div>
            </div>
            <button class="toast-close" onclick="this.parentElement.remove()" aria-label="Cerrar notificación">
                <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <line x1="18" y1="6" x2="6" y2="18"></line>
                    <line x1="6" y1="6" x2="18" y2="18"></line>
                </svg>
            </button>
        `;

        this.toastContainer.appendChild(toast);

        // Trigger animation
        setTimeout(() => toast.classList.add('show'), 100);

        // Auto remove
        if (duration > 0) {
            setTimeout(() => {
                toast.classList.remove('show');
                setTimeout(() => toast.remove(), 300);
            }, duration);
        }

        return toast;
    }

    /**
     * Get appropriate icon for toast type
     */
    getToastIcon(type) {
        const icons = {
            success: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M22 11.08V12a10 10 0 1 1-5.93-9.14"></path>
                <polyline points="22,4 12,14.01 9,11.01"></polyline>
            </svg>`,
            error: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="15" y1="9" x2="9" y2="15"></line>
                <line x1="9" y1="9" x2="15" y2="15"></line>
            </svg>`,
            warning: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10.29 3.86L1.82 18a2 2 0 0 0 1.71 3h16.94a2 2 0 0 0 1.71-3L13.71 3.86a2 2 0 0 0-3.42 0z"></path>
                <line x1="12" y1="9" x2="12" y2="13"></line>
                <line x1="12" y1="17" x2="12.01" y2="17"></line>
            </svg>`,
            info: `<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="12" cy="12" r="10"></circle>
                <line x1="12" y1="16" x2="12" y2="12"></line>
                <line x1="12" y1="8" x2="12.01" y2="8"></line>
            </svg>`
        };
        return icons[type] || icons.info;
    }

    /**
     * Show success toast
     */
    success(title, message, duration) {
        return this.showToast('success', title, message, duration);
    }

    /**
     * Show error toast
     */
    error(title, message, duration) {
        return this.showToast('error', title, message, duration);
    }

    /**
     * Show warning toast
     */
    warning(title, message, duration) {
        return this.showToast('warning', title, message, duration);
    }

    /**
     * Show info toast
     */
    info(title, message, duration) {
        return this.showToast('info', title, message, duration);
    }

    /**
     * Set button loading state
     */
    setButtonLoading(button, loading = true) {
        if (loading) {
            button.classList.add('btn-loading');
            button.disabled = true;
            button.setAttribute('aria-busy', 'true');
        } else {
            button.classList.remove('btn-loading');
            button.disabled = false;
            button.removeAttribute('aria-busy');
        }
    }

    /**
     * Show skeleton loading for table
     */
    showTableSkeleton(tableContainer, rows = 5) {
        const skeleton = document.createElement('div');
        skeleton.className = 'skeleton-table';
        skeleton.innerHTML = `
            <table class="w-full">
                <thead>
                    <tr>
                        <th class="text-left py-3 px-4 border-b border-gray-200">
                            <div class="skeleton skeleton-text"></div>
                        </th>
                        <th class="text-left py-3 px-4 border-b border-gray-200">
                            <div class="skeleton skeleton-text"></div>
                        </th>
                        <th class="text-left py-3 px-4 border-b border-gray-200">
                            <div class="skeleton skeleton-text"></div>
                        </th>
                        <th class="text-left py-3 px-4 border-b border-gray-200">
                            <div class="skeleton skeleton-text"></div>
                        </th>
                        <th class="text-left py-3 px-4 border-b border-gray-200">
                            <div class="skeleton skeleton-text"></div>
                        </th>
                    </tr>
                </thead>
                <tbody>
                    ${Array.from({ length: rows }, () => `
                        <tr>
                            <td class="py-3 px-4 border-b border-gray-200">
                                <div class="skeleton skeleton-text"></div>
                            </td>
                            <td class="py-3 px-4 border-b border-gray-200">
                                <div class="skeleton skeleton-text"></div>
                            </td>
                            <td class="py-3 px-4 border-b border-gray-200">
                                <div class="skeleton skeleton-text"></div>
                            </td>
                            <td class="py-3 px-4 border-b border-gray-200">
                                <div class="skeleton skeleton-text"></div>
                            </td>
                            <td class="py-3 px-4 border-b border-gray-200">
                                <div class="skeleton skeleton-text"></div>
                            </td>
                        </tr>
                    `).join('')}
                </tbody>
            </table>
        `;
        
        tableContainer.innerHTML = '';
        tableContainer.appendChild(skeleton);
    }

    /**
     * Show empty state
     */
    showEmptyState(container, options = {}) {
        const {
            icon = 'box',
            title = 'No hay elementos',
            description = 'No se encontraron elementos para mostrar.',
            actionText = 'Agregar nuevo',
            actionCallback = null
        } = options;

        const emptyState = document.createElement('div');
        emptyState.className = 'empty-state';
        
        const iconSvg = this.getEmptyStateIcon(icon);
        
        emptyState.innerHTML = `
            <div class="empty-state-icon">
                ${iconSvg}
            </div>
            <h3 class="empty-state-title">${title}</h3>
            <p class="empty-state-description">${description}</p>
            ${actionCallback ? `
                <div class="empty-state-action">
                    <button class="btn-primary" onclick="${actionCallback}">
                        ${actionText}
                    </button>
                </div>
            ` : ''}
        `;

        container.innerHTML = '';
        container.appendChild(emptyState);
    }

    /**
     * Show error state
     */
    showErrorState(container, options = {}) {
        const {
            title = 'Error al cargar',
            description = 'Ocurrió un error al cargar los datos.',
            actionText = 'Reintentar',
            actionCallback = null
        } = options;

        const errorState = document.createElement('div');
        errorState.className = 'error-state';
        
        errorState.innerHTML = `
            <div class="error-state-icon">
                <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                    <circle cx="12" cy="12" r="10"></circle>
                    <line x1="15" y1="9" x2="9" y2="15"></line>
                    <line x1="9" y1="9" x2="15" y2="15"></line>
                </svg>
            </div>
            <h3 class="error-state-title">${title}</h3>
            <p class="error-state-description">${description}</p>
            ${actionCallback ? `
                <div class="error-state-action">
                    <button class="btn-primary" onclick="${actionCallback}">
                        ${actionText}
                    </button>
                </div>
            ` : ''}
        `;

        container.innerHTML = '';
        container.appendChild(errorState);
    }

    /**
     * Get empty state icon
     */
    getEmptyStateIcon(type) {
        const icons = {
            box: `<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                <polyline points="3.27,6.96 12,12.01 20.73,6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>`,
            users: `<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path>
                <circle cx="9" cy="7" r="4"></circle>
                <path d="M23 21v-2a4 4 0 0 0-3-3.87"></path>
                <path d="M16 3.13a4 4 0 0 1 0 7.75"></path>
            </svg>`,
            shopping: `<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <circle cx="9" cy="21" r="1"></circle>
                <circle cx="20" cy="21" r="1"></circle>
                <path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"></path>
            </svg>`,
            package: `<svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1.5">
                <line x1="16.5" y1="9.4" x2="7.5" y2="4.21"></line>
                <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path>
                <polyline points="3.27,6.96 12,12.01 20.73,6.96"></polyline>
                <line x1="12" y1="22.08" x2="12" y2="12"></line>
            </svg>`
        };
        return icons[type] || icons.box;
    }

    /**
     * Setup global error handling
     */
    setupGlobalErrorHandling() {
        // Handle fetch errors
        const originalFetch = window.fetch;
        window.fetch = async (...args) => {
            try {
                const response = await originalFetch(...args);
                if (!response.ok) {
                    throw new Error(`HTTP ${response.status}: ${response.statusText}`);
                }
                return response;
            } catch (error) {
                console.error('Fetch error:', error);
                this.error('Error de conexión', 'No se pudo conectar con el servidor. Verifica tu conexión a internet.');
                throw error;
            }
        };

        // Handle unhandled promise rejections
        window.addEventListener('unhandledrejection', (event) => {
            console.error('Unhandled promise rejection:', event.reason);
            this.error('Error inesperado', 'Ocurrió un error inesperado. Por favor, recarga la página.');
        });
    }

    /**
     * Handle authentication errors with specific messages
     */
    handleAuthError(error) {
        const errorMessages = {
            'invalid_credentials': {
                title: 'Credenciales inválidas',
                message: 'El usuario o contraseña son incorrectos. Verifica tus datos e intenta nuevamente.'
            },
            'session_expired': {
                title: 'Sesión expirada',
                message: 'Tu sesión ha expirado. Por favor, inicia sesión nuevamente.'
            },
            'access_denied': {
                title: 'Acceso denegado',
                message: 'No tienes permisos para realizar esta acción.'
            },
            'account_locked': {
                title: 'Cuenta bloqueada',
                message: 'Tu cuenta ha sido bloqueada. Contacta al administrador.'
            }
        };

        const errorType = error.type || 'unknown';
        const errorInfo = errorMessages[errorType] || {
            title: 'Error de autenticación',
            message: error.message || 'Ocurrió un error al autenticarte. Intenta nuevamente.'
        };

        this.error(errorInfo.title, errorInfo.message);
    }

    /**
     * Show loading overlay
     */
    showLoadingOverlay(message = 'Cargando...') {
        const overlay = document.createElement('div');
        overlay.id = 'loading-overlay';
        overlay.className = 'fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50';
        overlay.innerHTML = `
            <div class="bg-white rounded-lg p-6 flex items-center space-x-3">
                <div class="loading-spinner"></div>
                <span class="text-gray-700">${message}</span>
            </div>
        `;
        document.body.appendChild(overlay);
    }

    /**
     * Hide loading overlay
     */
    hideLoadingOverlay() {
        const overlay = document.getElementById('loading-overlay');
        if (overlay) {
            overlay.remove();
        }
    }
}

// Initialize feedback manager when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    window.feedbackManager = new FeedbackManager();
});

// Export for use in other modules
if (typeof module !== 'undefined' && module.exports) {
    module.exports = FeedbackManager;
}
