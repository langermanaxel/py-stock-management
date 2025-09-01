# 🚀 Frontend Actualizado con JWT - Sistema de Gestión de Stock

## 📋 Resumen de Cambios

El frontend ha sido completamente actualizado para usar **JWT (JSON Web Tokens)** en lugar de sesiones de Flask, y se ha implementado un **sistema de roles robusto** que se adapta automáticamente según los permisos del usuario.

## 🔐 Sistema de Autenticación JWT

### **Características Principales:**

- ✅ **Autenticación basada en JWT** - Sin dependencia de sesiones del servidor
- ✅ **Tokens de acceso y refresh** - Renovación automática de tokens
- ✅ **Almacenamiento local seguro** - Tokens guardados en localStorage
- ✅ **Verificación automática de expiración** - Renovación proactiva de tokens
- ✅ **Manejo de errores 401** - Redirección automática al login

### **Flujo de Autenticación:**

1. **Usuario ingresa credenciales** en `/login`
2. **Frontend envía petición** a `/api/auth/login`
3. **Backend valida credenciales** y devuelve tokens JWT
4. **Frontend almacena tokens** en localStorage
5. **Todas las peticiones posteriores** incluyen el token en el header `Authorization`
6. **Token expirado** → Frontend intenta renovar automáticamente
7. **Renovación fallida** → Usuario es redirigido al login

## 👥 Sistema de Roles y Permisos

### **Roles Implementados:**

| Rol | Nivel | Permisos | Descripción |
|-----|-------|----------|-------------|
| **👑 Admin** | 4 | `all` | Acceso completo a todas las funcionalidades |
| **🏢 Manager** | 3 | `read`, `create`, `update` | Gestión de inventario (sin eliminar) |
| **👤 User** | 2 | `read`, `create_orders` | Visualización y creación de órdenes |
| **👁️ Viewer** | 1 | `read_limited` | Acceso muy limitado, solo lectura |

### **Control de Acceso por Endpoint:**

| Funcionalidad | Admin | Manager | User | Viewer |
|---------------|-------|---------|------|--------|
| **Ver Dashboard** | ✅ | ✅ | ✅ | ✅ |
| **Ver Categorías** | ✅ | ✅ | ✅ | ❌ |
| **Crear Categorías** | ✅ | ✅ | ❌ | ❌ |
| **Editar Categorías** | ✅ | ✅ | ❌ | ❌ |
| **Eliminar Categorías** | ✅ | ❌ | ❌ | ❌ |
| **Ver Productos** | ✅ | ✅ | ✅ | ❌ |
| **Crear Productos** | ✅ | ✅ | ❌ | ❌ |
| **Editar Productos** | ✅ | ✅ | ❌ | ❌ |
| **Eliminar Productos** | ✅ | ❌ | ❌ | ❌ |
| **Ver Stock** | ✅ | ✅ | ✅ | ❌ |
| **Gestionar Stock** | ✅ | ✅ | ❌ | ❌ |

## 🎨 Características de la UI

### **Adaptación Automática:**

- **Elementos se ocultan/muestran** según el rol del usuario
- **Botones de acción** aparecen solo si el usuario tiene permisos
- **Navegación** se adapta a los permisos disponibles
- **Formularios** se muestran solo a usuarios autorizados

### **Atributos de Rol:**

```html
<!-- Solo visible para usuarios con rol 'manager' o superior -->
<div data-role="manager">
    <h3>Agregar Categoría</h3>
    <form>...</form>
</div>

<!-- Solo visible para administradores -->
<button data-role="admin" onclick="deleteCategory(id)">
    <i class="fas fa-trash"></i> Eliminar
</button>
```

## 📁 Archivos del Frontend

### **JavaScript Principal:**

- **`static/js/config.js`** - Configuración global y credenciales de demo
- **`static/js/auth.js`** - Sistema de autenticación JWT
- **`static/js/app.js`** - Lógica principal de la aplicación

### **Templates HTML:**

- **`templates/login.html`** - Página de login con JWT
- **`templates/index.html`** - Dashboard principal con control de roles
- **`templates/profile.html`** - Perfil de usuario
- **`templates/change_password.html`** - Cambio de contraseña

## 🚀 Cómo Usar

### **1. Acceder al Sistema:**

```bash
# Navegar al login
http://localhost:8080/login
```

### **2. Credenciales de Demo:**

| Usuario | Contraseña | Rol | Acceso |
|---------|------------|-----|--------|
| `admin` | `Admin123!` | Administrador | Completo |
| `gerente` | `Gerente123!` | Manager | Gestión |
| `usuario` | `Usuario123!` | User | Visualización |
| `viewer` | `Viewer123!` | Viewer | Limitado |

### **3. Navegación Automática:**

- **Login exitoso** → Redirección automática al dashboard
- **Token expirado** → Renovación automática o redirección al login
- **Sin permisos** → Elementos se ocultan automáticamente

## 🔧 Funciones Disponibles

### **Autenticación:**

```javascript
// Verificar si el usuario está autenticado
authManager.isAuthenticated()

// Obtener información del usuario
authManager.getUser()

// Verificar rol específico
authManager.hasRole('admin')

// Verificar múltiples roles
authManager.hasAnyRole(['admin', 'manager'])

// Hacer petición autenticada
authManager.authenticatedRequest('/api/categories/')
```

### **Control de Permisos:**

```javascript
// Verificar permisos antes de ejecutar acciones
checkPermission('delete_category', 'admin')

// Crear botones con permisos
createActionButton('edit', 'Editar', 'fas fa-edit', 'manager')

// Actualizar UI según el rol
updateUIForUserRole()
```

## 🧪 Testing del Sistema

### **1. Probar Diferentes Roles:**

1. **Login con `admin`** → Verificar acceso completo
2. **Login con `gerente`** → Verificar gestión sin eliminación
3. **Login con `usuario`** → Verificar solo visualización
4. **Login con `viewer`** → Verificar acceso limitado

### **2. Verificar Control de Acceso:**

- **Elementos ocultos** para roles sin permisos
- **Botones de acción** aparecen según el rol
- **Formularios** se muestran solo a usuarios autorizados
- **Mensajes de error** claros para acciones no permitidas

### **3. Probar Expiración de Tokens:**

- **Token válido** → Acceso normal
- **Token próximo a expirar** → Renovación automática
- **Token expirado** → Redirección al login

## 🚨 Consideraciones de Seguridad

### **Frontend:**

- ✅ **Tokens JWT** almacenados en localStorage
- ✅ **Verificación de permisos** en cada acción
- ✅ **Ocultación de elementos** según el rol
- ✅ **Validación de entrada** en formularios

### **Backend:**

- ✅ **Endpoints protegidos** con decoradores de roles
- ✅ **Validación de tokens** en cada petición
- ✅ **Manejo de errores** consistente
- ✅ **Respuestas JSON** estandarizadas

## 🔄 Migración desde Sesiones

### **Cambios Realizados:**

1. **Eliminación de `@login_required`** en rutas del frontend
2. **Reemplazo de `session`** por JWT en el frontend
3. **Actualización de funciones** para usar `authManager.authenticatedRequest()`
4. **Implementación de control de roles** en la UI
5. **Adaptación de templates** para mostrar/ocultar elementos

### **Beneficios de la Migración:**

- **Escalabilidad** - Sin dependencia del estado del servidor
- **Flexibilidad** - Autenticación desde cualquier cliente
- **Seguridad** - Tokens con expiración y renovación
- **Mantenibilidad** - Código más limpio y organizado

## 📝 Próximos Pasos

### **Funcionalidades Pendientes:**

- [ ] **Edición de entidades** (categorías, productos, stock)
- [ ] **Gestión de órdenes** y compras
- [ ] **Reportes y estadísticas** por rol
- [ ] **Perfil de usuario** completo
- [ ] **Cambio de contraseña** via API

### **Mejoras Futuras:**

- [ ] **Refresh automático** de datos
- [ ] **Notificaciones en tiempo real**
- [ ] **Modo offline** con cache local
- [ ] **Temas personalizables** por usuario
- [ ] **Accesibilidad** mejorada

---

**🎉 El frontend está completamente actualizado y listo para usar con el nuevo sistema de autenticación JWT y control de roles!**
