# Sistema de Permisos para Usuarios

## 📋 Descripción General

El sistema de gestión de usuarios implementa un control de acceso basado en roles (RBAC) que determina qué operaciones puede realizar cada usuario según su nivel de autorización en la administración del sistema de usuarios.

## 🔐 Roles y Permisos

### 1. **Administrador (Admin)**
- **Nivel de acceso**: Máximo
- **Permisos**:
  - ✅ Ver todos los usuarios del sistema
  - ✅ Crear nuevos usuarios
  - ✅ Editar usuarios existentes
  - ✅ Eliminar usuarios (con restricciones de seguridad)
  - ✅ Activar/desactivar usuarios
  - ✅ Ver estadísticas del sistema
  - ✅ Acceso completo al sistema de usuarios

### 2. **Gerente (Manager)**
- **Nivel de acceso**: Medio
- **Permisos**:
  - ❌ Sin acceso al sistema de usuarios
  - ✅ Solo puede ver y editar su propio perfil
  - ✅ Acceso a otras funcionalidades del sistema

### 3. **Supervisor (Supervisor)**
- **Nivel de acceso**: Medio
- **Permisos**:
  - ❌ Sin acceso al sistema de usuarios
  - ✅ Solo puede ver y editar su propio perfil
  - ✅ Acceso a otras funcionalidades del sistema

### 4. **Usuario (User)**
- **Nivel de acceso**: Básico
- **Permisos**:
  - ❌ Sin acceso al sistema de usuarios
  - ✅ Solo puede ver y editar su propio perfil
  - ✅ Acceso limitado a otras funcionalidades

## 🛡️ Implementación de Seguridad

### Decoradores de Permisos

```python
# Gestión completa de usuarios (solo admin)
@roles_required('admin')

# Perfil de usuario (todos los roles autenticados)
@roles_required('admin', 'manager', 'supervisor', 'user')
```

### Validación en Frontend

```javascript
// Permisos basados en rol del usuario
get canCreateUsers() {
    return ['admin'].includes(this.user.role);
},

get canEditUsers() {
    return ['admin'].includes(this.user.role);
},

get canDeleteUsers() {
    return ['admin'].includes(this.user.role);
},

get canViewUsers() {
    return ['admin'].includes(this.user.role);
},

get canToggleUserStatus() {
    return ['admin'].includes(this.user.role);
}
```

## 🔄 Operaciones Disponibles

### 1. **Listar Usuarios**
- **Endpoint**: `GET /api/users/`
- **Permisos**: Solo Admin
- **Respuesta**: Lista de usuarios con detalles completos

### 2. **Ver Usuario Específico**
- **Endpoint**: `GET /api/users/{id}`
- **Permisos**: Solo Admin
- **Respuesta**: Detalles completos del usuario

### 3. **Crear Usuario**
- **Endpoint**: `POST /api/users/`
- **Permisos**: Solo Admin
- **Datos requeridos**: 
  ```json
  {
    "username": "nuevo_usuario",
    "password": "contraseña123",
    "first_name": "Nombre",
    "last_name": "Apellido",
    "email": "email@ejemplo.com",
    "role": "user"
  }
  ```

### 4. **Editar Usuario**
- **Endpoint**: `PUT /api/users/{id}`
- **Permisos**: Solo Admin
- **Datos opcionales**: Cualquier campo del usuario

### 5. **Eliminar Usuario**
- **Endpoint**: `DELETE /api/users/{id}`
- **Permisos**: Solo Admin
- **Restricciones**: 
  - No se puede eliminar el propio usuario
  - No se puede eliminar el último administrador

### 6. **Cambiar Estado de Usuario**
- **Endpoint**: `PUT /api/users/{id}/toggle-status`
- **Permisos**: Solo Admin
- **Restricciones**: 
  - No se puede desactivar el propio usuario
  - No se puede desactivar el último administrador

### 7. **Ver Perfil de Usuario**
- **Endpoint**: `GET /api/users/profile`
- **Permisos**: Todos los roles autenticados
- **Respuesta**: Perfil del usuario actual

### 8. **Editar Perfil de Usuario**
- **Endpoint**: `PUT /api/users/profile`
- **Permisos**: Todos los roles autenticados
- **Datos permitidos**: Solo campos del perfil personal

### 9. **Estadísticas de Usuarios**
- **Endpoint**: `GET /api/users/stats`
- **Permisos**: Solo Admin
- **Respuesta**: Estadísticas del sistema de usuarios

## 🎯 Características del Frontend

### Interfaz Adaptativa
- Los botones y acciones se muestran/ocultan según los permisos del usuario
- Navegación condicional basada en roles
- Mensajes de error apropiados para permisos insuficientes

### Componentes de Seguridad
- Validación de permisos en tiempo real
- Modales condicionales para crear/editar
- Confirmaciones para acciones destructivas
- Filtros de rol y estado adaptativos

### Experiencia de Usuario
- Indicadores visuales del rol actual
- Mensajes informativos sobre permisos
- Interfaz consistente con el resto del sistema
- Gestión dinámica de formularios de usuario

## 🧪 Pruebas del Sistema

### Archivo de Pruebas
```bash
python test_users_permissions.py
```

### Casos de Prueba
1. **Login con diferentes roles**
2. **Acceso a listar usuarios**
3. **Creación de usuarios**
4. **Edición de usuarios**
5. **Eliminación de usuarios**
6. **Cambio de estado de usuarios**
7. **Acceso a perfil de usuario**
8. **Acceso a estadísticas**

### Validación de Permisos
- Verificar que solo los roles autorizados puedan realizar cada operación
- Confirmar que los roles sin permisos reciban errores 403
- Validar que las operaciones autorizadas funcionen correctamente
- Probar el flujo completo de creación a eliminación

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
- Tabla `users` con roles, permisos y estados
- Campos de seguridad: password_hash, is_active
- Relaciones con otras entidades del sistema
- Índices en campos de búsqueda frecuente

## 🚀 Uso del Sistema

### 1. **Acceso a la Página**
```bash
# Navegar a /users
http://localhost:5000/users
```

### 2. **Operaciones Disponibles**
- **Ver usuarios**: Solo Admin
- **Crear usuario**: Solo Admin
- **Editar usuario**: Solo Admin
- **Eliminar usuario**: Solo Admin
- **Cambiar estado**: Solo Admin
- **Ver perfil**: Todos los roles autenticados

### 3. **Navegación**
- Barra de navegación adaptativa según permisos
- Menú de usuario con información del rol
- Enlaces condicionales a otras secciones

## 📊 Monitoreo y Logs

### Logs de Seguridad
- Intentos de acceso no autorizado
- Operaciones de creación/edición/eliminación
- Cambios en permisos de usuario
- Cambios en estado de usuarios

### Métricas
- Uso del sistema por rol
- Operaciones más frecuentes
- Errores de permisos
- Distribución de roles en el sistema

## 🔒 Consideraciones de Seguridad

### 1. **Validación de Tokens**
- Verificación JWT en cada endpoint
- Renovación automática de tokens
- Logout seguro

### 2. **Sanitización de Datos**
- Validación de entrada en frontend y backend
- Prevención de inyección SQL
- Escape de caracteres especiales
- Validación de roles y permisos

### 3. **Auditoría**
- Registro de todas las operaciones
- Trazabilidad de cambios
- Historial de modificaciones
- Log de cambios de estado

### 4. **Restricciones de Seguridad**
- No auto-eliminación
- Protección del último administrador
- Validación de roles válidos
- Verificación de permisos en cascada

## 🐛 Solución de Problemas

### Errores Comunes

#### Error 403 - Permisos Insuficientes
```json
{
  "message": "Permisos insuficientes",
  "detail": "Rol 'manager' no tiene acceso a este recurso",
  "required_roles": ["admin"]
}
```

#### Error 401 - No Autenticado
```json
{
  "message": "Error de autenticación"
}
```

#### Error 400 - Usuario No Puede Ser Eliminado
```json
{
  "error": "No puedes eliminar tu propio usuario"
}
```

#### Error 400 - Último Administrador
```json
{
  "error": "No se puede eliminar el último administrador"
}
```

### Verificación de Permisos
1. Confirmar que el usuario esté autenticado
2. Verificar que el token JWT sea válido
3. Comprobar que el rol del usuario tenga los permisos necesarios
4. Validar que la base de datos contenga la información correcta

## 📈 Mejoras Futuras

### Funcionalidades Planificadas
- [ ] Sistema de auditoría avanzado para cambios de usuarios
- [ ] Historial de cambios con rollback
- [ ] Notificaciones de cambios importantes
- [ ] Exportación de datos con filtros de permisos
- [ ] Dashboard de usuarios para administradores
- [ ] Sistema de aprobaciones para cambios críticos

### Optimizaciones Técnicas
- [ ] Caché de permisos en Redis
- [ ] Validación de permisos en middleware
- [ ] Sistema de auditoría avanzado
- [ ] API de permisos para integraciones externas
- [ ] Validación en tiempo real de permisos

## 📞 Soporte

### Documentación Adicional
- [README principal](../README.md)
- [Sistema de autenticación](AUTH_SYSTEM_README.md)
- [Sistema de categorías](CATEGORIES_PERMISSIONS_README.md)
- [Sistema de compras](PURCHASES_PERMISSIONS_README.md)
- [Reglas de negocio](BUSINESS_RULES_README.md)
- [API documentation](API_DOCUMENTATION.md)

### Contacto
- Crear un issue en el repositorio
- Revisar la documentación existente
- Consultar los ejemplos de código
- Verificar la configuración de permisos

## 🔐 Matriz de Permisos

| Operación | Admin | Manager | Supervisor | User |
|-----------|-------|---------|------------|------|
| Ver usuarios | ✅ | ❌ | ❌ | ❌ |
| Crear usuarios | ✅ | ❌ | ❌ | ❌ |
| Editar usuarios | ✅ | ❌ | ❌ | ❌ |
| Eliminar usuarios | ✅ | ❌ | ❌ | ❌ |
| Cambiar estado | ✅ | ❌ | ❌ | ❌ |
| Ver perfil propio | ✅ | ✅ | ✅ | ✅ |
| Editar perfil propio | ✅ | ✅ | ✅ | ✅ |
| Ver estadísticas | ✅ | ❌ | ❌ | ❌ |

## 🚨 Restricciones de Seguridad

### Protecciones Implementadas
1. **Auto-protección**: Los usuarios no pueden eliminarse o desactivarse a sí mismos
2. **Protección de administradores**: No se puede eliminar el último administrador del sistema
3. **Validación de roles**: Solo se permiten roles predefinidos y válidos
4. **Sanitización de datos**: Todos los campos de entrada son validados y sanitizados
5. **Auditoría completa**: Todas las operaciones son registradas para trazabilidad
