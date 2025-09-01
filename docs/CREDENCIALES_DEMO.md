# 🔐 Credenciales de Demo - Sistema de Gestión de Stock

## 📋 Usuarios Disponibles

### 👑 **Administrador**
- **Username:** `admin`
- **Password:** `Admin123!`
- **Rol:** `admin`
- **Permisos:** Acceso completo a todas las funcionalidades
- **Funciones:** Gestión de usuarios, productos, categorías, stock, órdenes, compras, reportes

### 🏢 **Gerente**
- **Username:** `gerente`
- **Password:** `Gerente123!`
- **Rol:** `manager`
- **Permisos:** Gestión de productos, categorías, stock, órdenes, compras, reportes
- **Funciones:** Puede crear, actualizar y gestionar inventario, pero no puede eliminar ni gestionar usuarios

### 👤 **Usuario Normal**
- **Username:** `usuario`
- **Password:** `Usuario123!`
- **Rol:** `user`
- **Permisos:** Visualización de productos, stock y creación de órdenes
- **Funciones:** Puede ver información y crear órdenes, pero no puede modificar el inventario

### 👁️ **Viewer (Solo Lectura)**
- **Username:** `viewer`
- **Password:** `Viewer123!`
- **Rol:** `viewer`
- **Permisos:** Solo visualización limitada
- **Funciones:** Acceso muy restringido, solo puede ver información básica

## 🚀 Cómo Usar

### 1. **Login via API**
```bash
# Ejemplo con curl
curl -X POST http://localhost:8080/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username": "gerente", "password": "Gerente123!"}'
```

### 2. **Login via Frontend**
- Navegar a `http://localhost:8080/login`
- Usar cualquiera de las credenciales listadas arriba

### 3. **Usar Token JWT**
```bash
# Después del login, usar el token en el header Authorization
curl -H "Authorization: Bearer <TOKEN>" \
  http://localhost:8080/api/categories/
```

## 🔒 Matriz de Permisos por Endpoint

| Endpoint | Admin | Gerente | Usuario | Viewer |
|----------|-------|---------|---------|--------|
| **GET /categories** | ✅ | ✅ | ✅ | ❌ |
| **POST /categories** | ✅ | ✅ | ❌ | ❌ |
| **PUT /categories** | ✅ | ✅ | ❌ | ❌ |
| **DELETE /categories** | ✅ | ❌ | ❌ | ❌ |
| **GET /products** | ✅ | ✅ | ✅ | ❌ |
| **POST /products** | ✅ | ✅ | ❌ | ❌ |
| **PUT /products** | ✅ | ✅ | ❌ | ❌ |
| **DELETE /products** | ✅ | ❌ | ❌ | ❌ |
| **GET /stock** | ✅ | ✅ | ✅ | ❌ |
| **POST /stock** | ✅ | ✅ | ❌ | ❌ |
| **PUT /stock** | ✅ | ✅ | ❌ | ❌ |
| **DELETE /stock** | ✅ | ❌ | ❌ | ❌ |

## 📝 Notas Importantes

- **Todos los usuarios pueden hacer login** - No hay restricciones en la autenticación
- **La autorización se aplica después del login** - Según el rol del usuario
- **Los tokens JWT expiran** - Renovar cuando sea necesario
- **Los roles son jerárquicos** - Admin > Gerente > Usuario > Viewer

## 🧪 Testing

Para probar diferentes niveles de acceso:

1. **Login con cada usuario**
2. **Intentar acceder a endpoints protegidos**
3. **Verificar que los permisos se apliquen correctamente**
4. **Confirmar que los mensajes de error sean claros**

## 🔧 Crear Nuevos Usuarios

Si necesitas crear usuarios adicionales, usa el script:
```bash
python create_test_users.py
```

---

**⚠️ IMPORTANTE:** Estas credenciales son solo para desarrollo y testing. En producción, usar contraseñas seguras y únicas para cada usuario.
