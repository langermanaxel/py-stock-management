# Manejo Robusto de Errores JSON - Frontend

## Problema Resuelto

El backend puede devolver errores en diferentes formatos:
- `{"msg": "Mensaje de error"}`
- `{"message": "Mensaje de error"}`
- `{"detail": "Mensaje de error"}`
- `{"error": "Mensaje de error"}`
- `{"description": "Mensaje de error"}`

Pero el frontend asumía siempre `{error: ...}`, causando que los mensajes no se mostraran y pareciera "misterioso".

## Solución Implementada

### 1. Parser Robusto de Errores (`http-helper.js`)

```javascript
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
```

### 2. Funciones de Utilidad Globales

```javascript
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
```

### 3. Integración en `auth.js`

El `JWTAuthManager` también incluye el parser robusto para manejar errores de autenticación:

```javascript
async parseErrorResponse(response, fallbackMessage = 'Error en la petición') {
    // Misma lógica que en http-helper.js
}

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
```

### 4. Uso en `app.js`

Todas las funciones de carga de datos y envío de formularios ahora usan el manejo robusto de errores:

```javascript
// Función para cargar categorías
async function loadCategories() {
    try {
        if (!authManager.isAuthenticated()) {
            console.warn('Usuario no autenticado, saltando carga de categorías');
            return;
        }

        const categories = await authManager.authenticatedRequest('/api/categories');
        if (categories && Array.isArray(categories)) {
            window.categories = categories;
            updateCategoryFilter();
            updateCategoryTable();
        }
    } catch (error) {
        showError(error, 'Error cargando categorías');
    }
}

// Función para crear categoría
async function submitCategory(event) {
    event.preventDefault();
    
    try {
        const formData = new FormData(event.target);
        const categoryData = {
            name: formData.get('name'),
            description: formData.get('description')
        };

        const response = await authManager.authenticatedRequest('/api/categories', {
            method: 'POST',
            body: JSON.stringify(categoryData)
        });

        showSuccess('Categoría creada exitosamente');
        event.target.reset();
        await loadCategories();
        
        // Cerrar modal si existe
        const modal = document.querySelector('#categoryModal');
        if (modal && window.bootstrap) {
            const bootstrapModal = window.bootstrap.Modal.getInstance(modal);
            if (bootstrapModal) {
                bootstrapModal.hide();
            }
        }
    } catch (error) {
        showError(error, 'Error creando categoría');
    }
}
```

## Características del Sistema

### 1. **Parsing Inteligente**
- Detecta automáticamente el tipo de contenido (JSON vs texto)
- Busca mensajes de error en múltiples campos comunes
- Maneja respuestas HTML y extrae solo el texto útil

### 2. **Manejo de Errores de Red**
- Distingue entre errores del backend y errores de red
- Crea errores descriptivos para problemas de conectividad
- Preserva información original del error

### 3. **Consistencia en la UI**
- Funciones globales `showError()` y `showSuccess()`
- Integración automática con Alpine.js toast si está disponible
- Fallback a `alert()` si no hay sistema de notificaciones

### 4. **Información Detallada**
- Incluye status code, URL y detalles adicionales
- Preserva la respuesta original para debugging
- Logging consistente en consola

### 5. **Manejo de Respuestas Exitosas**
- Detecta automáticamente si la respuesta es JSON o texto
- Maneja casos donde no hay contenido
- Proporciona respuestas por defecto cuando es necesario

## Beneficios

1. **Mensajes de Error Claros**: Los usuarios ven exactamente qué salió mal
2. **Debugging Mejorado**: Los desarrolladores tienen información completa del error
3. **Consistencia**: Todas las funciones manejan errores de la misma manera
4. **Robustez**: Funciona con diferentes formatos de respuesta del backend
5. **Mantenibilidad**: Un solo lugar para actualizar la lógica de manejo de errores

## Casos de Uso

### Error del Backend (JSON)
```javascript
// Backend devuelve: {"msg": "Categoría ya existe"}
// Frontend muestra: "Categoría ya existe"
```

### Error del Backend (HTML)
```javascript
// Backend devuelve: <html><body>Internal Server Error</body></html>
// Frontend muestra: "Internal Server Error"
```

### Error de Red
```javascript
// Sin conexión a internet
// Frontend muestra: "Error de red: Failed to fetch"
```

### Respuesta Exitosa
```javascript
// Backend devuelve: {"success": true, "data": [...]}
// Frontend procesa normalmente
```

## Archivos Modificados

1. **`static/js/http-helper.js`** - Parser robusto y funciones HTTP
2. **`static/js/auth.js`** - Manejo de errores en autenticación
3. **`static/js/app.js`** - Integración del nuevo sistema de errores

## Próximos Pasos

1. **Testing**: Probar con diferentes tipos de errores del backend
2. **Personalización**: Ajustar mensajes por defecto según necesidades
3. **Internacionalización**: Preparar para múltiples idiomas
4. **Métricas**: Agregar tracking de errores para análisis
