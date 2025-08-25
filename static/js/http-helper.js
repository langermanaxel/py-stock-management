// ========================================
// HELPER HTTP CENTRALIZADO PARA LA API
// ========================================

class HTTPHelper {
    constructor(baseURL = '/api') {
        this.baseURL = baseURL;
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
     * Realiza una petición HTTP con manejo robusto de errores
     * @param {string} endpoint - Endpoint de la API (sin /api)
     * @param {Object} options - Opciones de fetch
     * @returns {Promise<Object>} Respuesta parseada
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        
        try {
            const response = await fetch(url, {
                ...options,
                headers: {
                    'Content-Type': 'application/json',
                    ...options.headers
                }
            });

            // Si la respuesta no es exitosa, parsear el error
            if (!response.ok) {
                const error = await this.parseErrorResponse(response);
                throw error;
            }

            // Intentar parsear la respuesta exitosa
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
     * Realiza una petición GET
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} headers - Headers adicionales
     * @returns {Promise<Object>} Respuesta
     */
    async get(endpoint, headers = {}) {
        return this.request(endpoint, {
            method: 'GET',
            headers
        });
    }

    /**
     * Realiza una petición POST
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} data - Datos a enviar
     * @param {Object} headers - Headers adicionales
     * @returns {Promise<Object>} Respuesta
     */
    async post(endpoint, data = null, headers = {}) {
        return this.request(endpoint, {
            method: 'POST',
            body: data ? JSON.stringify(data) : undefined,
            headers
        });
    }

    /**
     * Realiza una petición PUT
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} data - Datos a enviar
     * @param {Object} headers - Headers adicionales
     * @returns {Promise<Object>} Respuesta
     */
    async put(endpoint, data = null, headers = {}) {
        return this.request(endpoint, {
            method: 'PUT',
            body: data ? JSON.stringify(data) : undefined,
            headers
        });
    }

    /**
     * Realiza una petición DELETE
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} headers - Headers adicionales
     * @returns {Promise<Object>} Respuesta
     */
    async delete(endpoint, headers = {}) {
        return this.request(endpoint, {
            method: 'DELETE',
            headers
        });
    }

    /**
     * Realiza una petición PATCH
     * @param {string} endpoint - Endpoint de la API
     * @param {Object} data - Datos a enviar
     * @param {Object} headers - Headers adicionales
     * @returns {Promise<Object>} Respuesta
     */
    async patch(endpoint, data = null, headers = {}) {
        return this.request(endpoint, {
            method: 'PATCH',
            body: data ? JSON.stringify(data) : undefined,
            headers
        });
    }
}

// Instancia global del helper HTTP
window.httpHelper = new HTTPHelper();

// Función de utilidad para mostrar errores de manera consistente
window.showError = function(error, title = 'Error') {
    console.error(`${title}:`, error);
    
    let message = 'Ha ocurrido un error inesperado';
    
    if (error.message) {
        message = error.message;
    } else if (typeof error === 'string') {
        message = error;
    }
    
    // Usar Alpine.js toast si está disponible
    if (window.toastManager && window.toastManager.showError) {
        window.toastManager.showError(message);
    } else {
        // Fallback a alert si no hay toast
        alert(`${title}: ${message}`);
    }
};

// Función de utilidad para mostrar mensajes de éxito
window.showSuccess = function(message, title = 'Éxito') {
    console.log(`${title}:`, message);
    
    // Usar Alpine.js toast si está disponible
    if (window.toastManager && window.toastManager.showSuccess) {
        window.toastManager.showSuccess(message);
    } else {
        // Fallback a alert si no hay toast
        alert(`${title}: ${message}`);
    }
};
