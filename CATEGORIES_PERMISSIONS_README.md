# Sistema de Permisos para Categorías

## 📋 Descripción General

El sistema de gestión de categorías implementa un control de acceso basado en roles (RBAC) que determina qué operaciones puede realizar cada usuario según su nivel de autorización.

## 🔐 Roles y Permisos

### 1. **Administrador (Admin)**
- **Nivel de acceso**: Máximo
- **Permisos**:
  - ✅ Ver todas las categorías
  - ✅ Crear nuevas categorías
  - ✅ Editar categorías existentes
  - ✅ Eliminar categorías (si no tienen productos asociados)
  - ✅ Ver productos por categoría
  - ✅ Acceso completo al sistema

### 2. **Gerente (Manager)**
- **Nivel de acceso**: Alto
- **Permisos**:
  - ✅ Ver todas las categorías
  - ✅ Crear nuevas categorías
  - ✅ Editar categorías existentes
  - ❌ Eliminar categorías
  - ✅ Ver productos por categoría
  - ✅ Gestión de productos y stock

### 3. **Supervisor (Supervisor)**
- **Nivel de acceso**: Medio
- **Permisos**:
  - ✅ Ver todas las categorías
  - ❌ Crear nuevas categorías
  - ❌ Editar categorías existentes
  - ❌ Eliminar categorías
  - ✅ Ver productos por categoría
  - ✅ Gestión básica de stock

### 4. **Usuario (User)**
- **Nivel de acceso**: Básico
- **Permisos**:
  - ✅ Ver todas las categorías
  - ❌ Crear nuevas categorías
  - ❌ Editar categorías existentes
  - ❌ Eliminar categorías
  - ✅ Ver productos por categoría
  - ✅ Crear órdenes

## 🛡️ Implementación de Seguridad

### Decoradores de Permisos

```python
# Ver categorías (todos los roles)
@roles_required('admin', 'manager', 'supervisor', 'user')

# Crear/Editar categorías (admin y manager)
@roles_required('admin', 'manager')

# Eliminar categorías (solo admin)
@roles_required('admin')
```

### Validación en Frontend

```javascript
// Permisos basados en rol del usuario
get canCreateCategories() {
    return ['admin', 'manager'].includes(this.user.role);
},

get canEditCategories() {
    return ['admin', 'manager'].includes(this.user.role);
},

get canDeleteCategories() {
    return ['admin'].includes(this.user.role);
},

get canViewCategories() {
    return ['admin', 'manager', 'supervisor', 'user'].includes(this.user.role);
}
```

## 🔄 Operaciones Disponibles

### 1. **Listar Categorías**
- **Endpoint**: `GET /api/categories/`
- **Permisos**: Todos los roles
- **Respuesta**: Lista de categorías con conteo de productos

### 2. **Ver Categoría Individual**
- **Endpoint**: `GET /api/categories/{id}`
- **Permisos**: Todos los roles
- **Respuesta**: Detalles de la categoría con conteo de productos

### 3. **Crear Categoría**
- **Endpoint**: `POST /api/categories/`
- **Permisos**: Admin y Manager
- **Datos requeridos**: `{"name": "Nombre de la categoría"}`

### 4. **Editar Categoría**
- **Endpoint**: `PUT /api/categories/{id}`
- **Permisos**: Admin y Manager
- **Datos requeridos**: `{"name": "Nuevo nombre"}`

### 5. **Eliminar Categoría**
- **Endpoint**: `DELETE /api/categories/{id}`
- **Permisos**: Solo Admin
- **Restricciones**: No se puede eliminar si tiene productos asociados

### 6. **Ver Productos por Categoría**
- **Endpoint**: `GET /api/categories/{id}/products`
- **Permisos**: Todos los roles
- **Respuesta**: Lista de productos en la categoría

## 🎯 Características del Frontend

### Interfaz Adaptativa
- Los botones y acciones se muestran/ocultan según los permisos del usuario
- Navegación condicional basada en roles
- Mensajes de error apropiados para permisos insuficientes

### Componentes de Seguridad
- Validación de permisos en tiempo real
- Modales condicionales para crear/editar
- Confirmaciones para acciones destructivas

### Experiencia de Usuario
- Indicadores visuales del rol actual
- Mensajes informativos sobre permisos
- Interfaz consistente con el resto del sistema

## 🧪 Pruebas del Sistema

### Archivo de Pruebas
```bash
python test_categories_permissions.py
```

### Casos de Prueba
1. **Login con diferentes roles**
2. **Acceso a listar categorías**
3. **Creación de categorías**
4. **Edición de categorías**
5. **Eliminación de categorías**
6. **Acceso a productos por categoría**

### Validación de Permisos
- Verificar que solo los roles autorizados puedan realizar cada operación
- Confirmar que los roles sin permisos reciban errores 403
- Validar que las operaciones autorizadas funcionen correctamente

## 🔧 Configuración

### Variables de Entorno
```bash
# Configuración de JWT
JWT_SECRET_KEY=tu_clave_secreta
JWT_ACCESS_TOKEN_EXPIRES=15m
JWT_REFRESH_TOKEN_EXPIRES=30d

# Configuración de base de datos
DATABASE_URL=sqlite:///instance/stock_management.db
```

### Base de Datos
- Tabla `users` con campo `role`
- Tabla `categories` con relación a `products`
- Índices en campos de búsqueda frecuente

## 🚀 Uso del Sistema

### 1. **Acceso a la Página**
```bash
# Navegar a /categories
http://localhost:5000/categories
```

### 2. **Operaciones Disponibles**
- **Ver categorías**: Disponible para todos los usuarios autenticados
- **Crear categoría**: Solo Admin y Manager
- **Editar categoría**: Solo Admin y Manager
- **Eliminar categoría**: Solo Admin

### 3. **Navegación**
- Barra de navegación adaptativa según permisos
- Menú de usuario con información del rol
- Enlaces condicionales a otras secciones

## 📊 Monitoreo y Logs

### Logs de Seguridad
- Intentos de acceso no autorizado
- Operaciones de creación/edición/eliminación
- Cambios en permisos de usuario

### Métricas
- Uso de categorías por rol
- Operaciones más frecuentes
- Errores de permisos

## 🔒 Consideraciones de Seguridad

### 1. **Validación de Tokens**
- Verificación JWT en cada endpoint
- Renovación automática de tokens
- Logout seguro

### 2. **Sanitización de Datos**
- Validación de entrada en frontend y backend
- Prevención de inyección SQL
- Escape de caracteres especiales

### 3. **Auditoría**
- Registro de todas las operaciones
- Trazabilidad de cambios
- Historial de modificaciones

## 🐛 Solución de Problemas

### Errores Comunes

#### Error 403 - Permisos Insuficientes
```json
{
  "message": "Permisos insuficientes",
  "detail": "Rol 'user' no tiene acceso a este recurso",
  "required_roles": ["admin", "manager"]
}
```

#### Error 401 - No Autenticado
```json
{
  "message": "Error de autenticación"
}
```

### Verificación de Permisos
1. Confirmar que el usuario esté autenticado
2. Verificar que el token JWT sea válido
3. Comprobar que el rol del usuario tenga los permisos necesarios
4. Validar que la base de datos contenga la información correcta

## 📈 Mejoras Futuras

### Funcionalidades Planificadas
- [ ] Sistema de permisos granulares por categoría
- [ ] Historial de cambios con rollback
- [ ] Notificaciones de cambios importantes
- [ ] Exportación de datos con filtros de permisos
- [ ] Dashboard de permisos para administradores

### Optimizaciones Técnicas
- [ ] Caché de permisos en Redis
- [ ] Validación de permisos en middleware
- [ ] Sistema de auditoría avanzado
- [ ] API de permisos para integraciones externas

## 📞 Soporte

### Documentación Adicional
- [README principal](../README.md)
- [Sistema de autenticación](AUTH_SYSTEM_README.md)
- [Reglas de negocio](BUSINESS_RULES_README.md)
- [API documentation](API_DOCUMENTATION.md)

### Contacto
- Crear un issue en el repositorio
- Revisar la documentación existente
- Consultar los ejemplos de código
