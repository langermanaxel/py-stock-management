# 🌐 Configuración CORS - Sistema de Gestión de Inventario

## 📋 **Descripción**

Este documento describe la configuración completa de CORS (Cross-Origin Resource Sharing) implementada en el sistema para permitir que el frontend se comunique correctamente con el backend desde diferentes orígenes.

## 🚨 **Problema Identificado**

- **Frontend y Backend en puertos diferentes**: El frontend puede estar corriendo en un puerto diferente al backend
- **Headers de autorización**: El header `Authorization: Bearer <token>` debe estar permitido
- **Peticiones preflight**: Las peticiones OPTIONS deben manejarse correctamente
- **Credenciales**: El frontend debe poder enviar cookies y headers de autenticación

## ✅ **Solución Implementada**

### **1. Configuración CORS en Flask**

```python
# app/__init__.py
CORS(app, 
     resources={r"/*": {"origins": app.config["CORS_ORIGINS"]}},
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS', 'PATCH'])
```

**Características:**
- **`resources={r"/*"}`**: Aplica CORS a todas las rutas
- **`supports_credentials=True`**: Permite envío de credenciales
- **`allow_headers`**: Incluye `Authorization` para JWT
- **`methods`**: Todos los métodos HTTP necesarios

### **2. Orígenes Permitidos**

```python
# app/config.py
CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 
    'http://localhost:5000,http://127.0.0.1:5000,http://localhost:8080,http://127.0.0.1:8080').split(',')
```

**Puertos incluidos:**
- `5000`: Puerto típico de desarrollo Flask
- `8080`: Puerto alternativo para desarrollo
- `127.0.0.1`: Localhost IPv4
- `localhost`: Localhost por nombre

### **3. Configuración del Frontend**

```javascript
// static/js/auth.js
const response = await fetch(url, {
    ...options,
    headers,
    credentials: 'same-origin',
    mode: 'cors'
});
```

**Configuración:**
- **`credentials: 'same-origin'`**: Envía credenciales al mismo origen
- **`mode: 'cors'`**: Habilita modo CORS
- **Headers personalizados**: Incluye `Authorization` y `Content-Type`

## 🔧 **Archivos de Configuración**

### **Backend**

| Archivo | Propósito |
|---------|-----------|
| `app/__init__.py` | Configuración principal de CORS |
| `app/config.py` | Orígenes permitidos |
| `app/middleware/cors_middleware.py` | Middleware personalizado para CORS |
| `app/decorators/cors_decorators.py` | Decoradores para endpoints de la API |

### **Frontend**

| Archivo | Propósito |
|---------|-----------|
| `static/js/auth.js` | Configuración CORS en peticiones autenticadas |
| `static/js/config.js` | Configuración global de CORS |
| `static/js/http-helper.js` | Helper HTTP con configuración CORS |

## 🧪 **Pruebas de CORS**

### **1. Script de Prueba Automatizada**

```bash
python test_cors.py
```

**Pruebas incluidas:**
- ✅ Peticiones OPTIONS (preflight)
- ✅ Headers CORS en respuestas
- ✅ Orígenes permitidos
- ✅ Métodos HTTP permitidos
- ✅ Headers de autorización

### **2. Pruebas Manuales en el Navegador**

**Consola del Navegador:**
```javascript
// Probar petición OPTIONS
fetch('/api/categories/', { method: 'OPTIONS' })
  .then(response => console.log('Status:', response.status))
  .catch(error => console.error('Error:', error));

// Probar petición GET
fetch('/api/categories/', { 
  headers: { 'Authorization': 'Bearer test-token' } 
})
  .then(response => console.log('Status:', response.status))
  .catch(error => console.error('Error:', error));
```

## 🔍 **Verificación de Headers CORS**

### **Headers Requeridos**

```http
Access-Control-Allow-Origin: *
Access-Control-Allow-Methods: GET, POST, PUT, DELETE, OPTIONS, PATCH
Access-Control-Allow-Headers: Content-Type, Authorization, X-Requested-With
Access-Control-Allow-Credentials: true
Access-Control-Max-Age: 86400
```

### **Verificación en el Navegador**

1. **Abrir DevTools** (F12)
2. **Ir a la pestaña Network**
3. **Hacer una petición a la API**
4. **Verificar que los headers CORS estén presentes**

## 🚀 **Configuración por Entorno**

### **Desarrollo Local**

```bash
# .env
CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000,http://localhost:8080,http://127.0.0.1:8080
FLASK_RUN_PORT=8080
```

### **Producción**

```bash
# .env
CORS_ORIGINS=https://tu-dominio.com,https://www.tu-dominio.com
FLASK_RUN_PORT=5000
```

## 🔧 **Solución de Problemas Comunes**

### **1. Error: "No 'Access-Control-Allow-Origin' header"**

**Causa:** El origen del frontend no está en `CORS_ORIGINS`
**Solución:** Agregar el origen a la configuración

### **2. Error: "Authorization header not allowed"**

**Causa:** El header `Authorization` no está en `allow_headers`
**Solución:** Verificar que `Authorization` esté incluido

### **3. Error: "Method not allowed"**

**Causa:** El método HTTP no está en `methods`
**Solución:** Verificar que todos los métodos necesarios estén incluidos

### **4. Error: "Credentials not supported"**

**Causa:** `supports_credentials` no está habilitado
**Solución:** Verificar que `supports_credentials=True`

## 📋 **Checklist de Verificación**

- [ ] **Backend corriendo** en el puerto correcto
- [ ] **CORS habilitado** en `app/__init__.py`
- [ ] **Orígenes permitidos** incluyen el puerto del frontend
- [ ] **Headers de autorización** permitidos
- [ ] **Peticiones OPTIONS** devuelven 200
- [ ] **Frontend configurado** con `credentials: 'same-origin'`
- [ ] **No errores CORS** en la consola del navegador
- [ ] **Headers CORS** presentes en todas las respuestas

## 🎯 **Beneficios de la Configuración**

- **✅ Sin errores CORS**: El frontend puede comunicarse con el backend
- **✅ Autenticación JWT**: Los tokens se envían correctamente
- **✅ Peticiones preflight**: Las peticiones OPTIONS funcionan
- **✅ Múltiples orígenes**: Soporte para diferentes puertos de desarrollo
- **✅ Seguridad**: Solo orígenes permitidos pueden acceder
- **✅ Credenciales**: Soporte para cookies y headers de auth

## 🔗 **Enlaces Útiles**

- **Documentación Flask-CORS**: https://flask-cors.readthedocs.io/
- **MDN CORS**: https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS
- **Script de Prueba**: `test_cors.py`
- **Configuración**: `app/__init__.py` y `app/config.py`

---

**🎯 Con esta configuración CORS, tu frontend debería poder comunicarse correctamente con el backend sin errores de CORS!**
