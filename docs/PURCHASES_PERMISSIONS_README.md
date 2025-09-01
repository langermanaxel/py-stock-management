# Sistema de Permisos para Compras

## 📋 Descripción General

El sistema de gestión de compras implementa un control de acceso basado en roles (RBAC) que determina qué operaciones puede realizar cada usuario según su nivel de autorización en la gestión de órdenes de compra e inventario.

## 🔐 Roles y Permisos

### 1. **Administrador (Admin)**
- **Nivel de acceso**: Máximo
- **Permisos**:
  - ✅ Ver todas las órdenes de compra
  - ✅ Crear nuevas órdenes de compra
  - ✅ Editar órdenes de compra existentes
  - ✅ Eliminar órdenes de compra (solo pendientes)
  - ✅ Completar órdenes de compra
  - ✅ Acceso completo al sistema de compras

### 2. **Gerente (Manager)**
- **Nivel de acceso**: Alto
- **Permisos**:
  - ✅ Ver todas las órdenes de compra
  - ✅ Crear nuevas órdenes de compra
  - ✅ Editar órdenes de compra existentes
  - ❌ Eliminar órdenes de compra
  - ✅ Completar órdenes de compra
  - ✅ Gestión completa del flujo de compras

### 3. **Supervisor (Supervisor)**
- **Nivel de acceso**: Medio
- **Permisos**:
  - ✅ Ver todas las órdenes de compra
  - ❌ Crear nuevas órdenes de compra
  - ❌ Editar órdenes de compra existentes
  - ❌ Eliminar órdenes de compra
  - ❌ Completar órdenes de compra
  - ✅ Monitoreo y supervisión del proceso

### 4. **Usuario (User)**
- **Nivel de acceso**: Básico
- **Permisos**:
  - ❌ Sin acceso al sistema de compras
  - ✅ Solo puede crear órdenes de venta
  - ✅ Acceso limitado a otras funcionalidades

## 🛡️ Implementación de Seguridad

### Decoradores de Permisos

```python
# Ver compras (admin, manager, supervisor)
@roles_required('admin', 'manager', 'supervisor')

# Crear/Editar/Completar compras (admin y manager)
@roles_required('admin', 'manager')

# Eliminar compras (solo admin)
@roles_required('admin')
```

### Validación en Frontend

```javascript
// Permisos basados en rol del usuario
get canCreatePurchases() {
    return ['admin', 'manager'].includes(this.user.role);
},

get canEditPurchases() {
    return ['admin', 'manager'].includes(this.user.role);
},

get canDeletePurchases() {
    return ['admin'].includes(this.user.role);
},

get canViewPurchases() {
    return ['admin', 'manager', 'supervisor'].includes(this.user.role);
},

get canCompletePurchases() {
    return ['admin', 'manager'].includes(this.user.role);
}
```

## 🔄 Operaciones Disponibles

### 1. **Listar Órdenes de Compra**
- **Endpoint**: `GET /api/purchases/`
- **Permisos**: Admin, Manager, Supervisor
- **Respuesta**: Lista de órdenes con detalles completos

### 2. **Ver Orden de Compra Individual**
- **Endpoint**: `GET /api/purchases/{id}`
- **Permisos**: Admin, Manager, Supervisor
- **Respuesta**: Detalles completos de la orden

### 3. **Crear Orden de Compra**
- **Endpoint**: `POST /api/purchases/`
- **Permisos**: Admin y Manager
- **Datos requeridos**: 
  ```json
  {
    "items": [
      {"product_id": 1, "quantity": 5},
      {"product_id": 2, "quantity": 3}
    ]
  }
  ```

### 4. **Editar Orden de Compra**
- **Endpoint**: `PUT /api/purchases/{id}`
- **Permisos**: Admin y Manager
- **Datos requeridos**: `{"status": "completed"}`

### 5. **Eliminar Orden de Compra**
- **Endpoint**: `DELETE /api/purchases/{id}`
- **Permisos**: Solo Admin
- **Restricciones**: Solo se pueden eliminar órdenes pendientes

### 6. **Completar Orden de Compra**
- **Endpoint**: `PUT /api/purchases/{id}/complete`
- **Permisos**: Admin y Manager
- **Funcionalidad**: Actualiza el stock automáticamente

## 🎯 Características del Frontend

### Interfaz Adaptativa
- Los botones y acciones se muestran/ocultan según los permisos del usuario
- Navegación condicional basada en roles
- Mensajes de error apropiados para permisos insuficientes

### Componentes de Seguridad
- Validación de permisos en tiempo real
- Modales condicionales para crear/editar
- Confirmaciones para acciones destructivas
- Filtros de estado adaptativos

### Experiencia de Usuario
- Indicadores visuales del rol actual
- Mensajes informativos sobre permisos
- Interfaz consistente con el resto del sistema
- Gestión dinámica de productos en órdenes

## 🧪 Pruebas del Sistema

### Archivo de Pruebas
```bash
python test_purchases_permissions.py
```

### Casos de Prueba
1. **Login con diferentes roles**
2. **Acceso a listar compras**
3. **Creación de órdenes de compra**
4. **Edición de órdenes de compra**
5. **Eliminación de órdenes de compra**
6. **Completar órdenes de compra**
7. **Acceso a órdenes individuales**

### Validación de Permisos
- Verificar que solo los roles autorizados puedan realizar cada operación
- Confirmar que los roles sin permisos reciban errores 403
- Validar que las operaciones autorizadas funcionen correctamente
- Probar el flujo completo de creación a completado

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
- Tabla `purchase_orders` con estados y fechas
- Tabla `purchase_order_items` con productos y cantidades
- Relación con `products` y `stock`
- Índices en campos de búsqueda frecuente

## 🚀 Uso del Sistema

### 1. **Acceso a la Página**
```bash
# Navegar a /purchases
http://localhost:5000/purchases
```

### 2. **Operaciones Disponibles**
- **Ver compras**: Admin, Manager, Supervisor
- **Crear orden**: Solo Admin y Manager
- **Editar orden**: Solo Admin y Manager
- **Completar orden**: Solo Admin y Manager
- **Eliminar orden**: Solo Admin

### 3. **Navegación**
- Barra de navegación adaptativa según permisos
- Menú de usuario con información del rol
- Enlaces condicionales a otras secciones

## 📊 Monitoreo y Logs

### Logs de Seguridad
- Intentos de acceso no autorizado
- Operaciones de creación/edición/eliminación
- Cambios en permisos de usuario
- Completado de órdenes de compra

### Métricas
- Uso de compras por rol
- Operaciones más frecuentes
- Errores de permisos
- Tiempo de procesamiento de órdenes

## 🔒 Consideraciones de Seguridad

### 1. **Validación de Tokens**
- Verificación JWT en cada endpoint
- Renovación automática de tokens
- Logout seguro

### 2. **Sanitización de Datos**
- Validación de entrada en frontend y backend
- Prevención de inyección SQL
- Escape de caracteres especiales
- Validación de cantidades y productos

### 3. **Auditoría**
- Registro de todas las operaciones
- Trazabilidad de cambios
- Historial de modificaciones
- Log de actualizaciones de stock

## 🐛 Solución de Problemas

### Errores Comunes

#### Error 403 - Permisos Insuficientes
```json
{
  "message": "Permisos insuficientes",
  "detail": "Rol 'user' no tiene acceso a este recurso",
  "required_roles": ["admin", "manager", "supervisor"]
}
```

#### Error 401 - No Autenticado
```json
{
  "message": "Error de autenticación"
}
```

#### Error 400 - Orden No Pendiente
```json
{
  "error": "Solo se pueden eliminar órdenes de compra pendientes"
}
```

### Verificación de Permisos
1. Confirmar que el usuario esté autenticado
2. Verificar que el token JWT sea válido
3. Comprobar que el rol del usuario tenga los permisos necesarios
4. Validar que la base de datos contenga la información correcta

## 📈 Mejoras Futuras

### Funcionalidades Planificadas
- [ ] Sistema de aprobaciones para órdenes grandes
- [ ] Historial de cambios con rollback
- [ ] Notificaciones de cambios importantes
- [ ] Exportación de datos con filtros de permisos
- [ ] Dashboard de compras para supervisores

### Optimizaciones Técnicas
- [ ] Caché de permisos en Redis
- [ ] Validación de permisos en middleware
- [ ] Sistema de auditoría avanzado
- [ ] API de permisos para integraciones externas
- [ ] Validación en tiempo real de stock disponible

## 📞 Soporte

### Documentación Adicional
- [README principal](../README.md)
- [Sistema de autenticación](AUTH_SYSTEM_README.md)
- [Sistema de categorías](CATEGORIES_PERMISSIONS_README.md)
- [Reglas de negocio](BUSINESS_RULES_README.md)
- [API documentation](API_DOCUMENTATION.md)

### Contacto
- Crear un issue en el repositorio
- Revisar la documentación existente
- Consultar los ejemplos de código
- Verificar la configuración de permisos
