# 📚 Documentación de la API - Sistema de Gestión de Inventario

## 🌐 Acceso a la Documentación Interactiva

Una vez que la aplicación esté ejecutándose, puedes acceder a la documentación interactiva de la API:

- **🌐 Swagger UI**: `http://localhost:5000/swagger-ui`
- **📄 OpenAPI JSON**: `http://localhost:5000/api-spec.json`
- **📄 OpenAPI YAML**: `http://localhost:5000/api-spec.yaml`

## 🚀 Características de la Documentación

### ✨ Interfaz Swagger UI Mejorada

La documentación incluye:

- **🎨 Interfaz moderna**: Swagger UI 5.9.0 con tema personalizado
- **🔍 Búsqueda y filtrado**: Encuentra endpoints rápidamente
- **📱 Responsive**: Funciona perfectamente en dispositivos móviles
- **🎯 Ejemplos interactivos**: Prueba endpoints directamente desde la interfaz
- **🔒 Autenticación integrada**: Botón Authorize para tokens JWT
- **📊 Respuestas detalladas**: Ejemplos de éxito y error para cada endpoint

### 📋 Organización por Tags

Los endpoints están organizados en categorías lógicas:

1. **🔐 Autenticación** - Login, logout, gestión de usuarios
2. **🛍️ Productos** - CRUD de productos y categorías
3. **📊 Stock** - Control de inventario y alertas
4. **🛒 Órdenes** - Gestión de ventas con validaciones
5. **📋 Compras** - Gestión de compras y reposición
6. **📈 Reportes** - Estadísticas y análisis

## 🔐 Autenticación y Autorización

### JWT Tokens

La API utiliza JWT (JSON Web Tokens) para autenticación:

1. **Login**: `POST /api/auth/login`
2. **Autorización**: Incluir `Authorization: Bearer <token>` en headers
3. **Refresh**: `POST /api/auth/refresh` para renovar tokens

### Cómo Usar la Autenticación en Swagger UI

1. Haz clic en el botón **"Authorize"** (🔒) en la parte superior
2. Ingresa tu token JWT en el formato: `Bearer <tu-token>`
3. Haz clic en **"Authorize"**
4. ¡Listo! Ahora puedes probar todos los endpoints protegidos

## 📚 Endpoints Principales

### 🔐 Autenticación (`/api/auth`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `POST` | `/login` | Iniciar sesión con credenciales |
| `POST` | `/refresh` | Renovar token de acceso |
| `POST` | `/logout` | Cerrar sesión |
| `POST` | `/register` | Registrar nuevo usuario |
| `GET` | `/profile` | Obtener perfil del usuario |
| `PUT` | `/profile` | Actualizar perfil del usuario |
| `PUT` | `/change-password` | Cambiar contraseña |

### 🛍️ Productos (`/api/products`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Listar todos los productos |
| `POST` | `/` | Crear nuevo producto |
| `GET` | `/<id>` | Obtener producto por ID |
| `PUT` | `/<id>` | Actualizar producto |
| `DELETE` | `/<id>` | Eliminar producto |
| `GET` | `/search` | Buscar y filtrar productos |
| `GET` | `/<id>/stock` | Obtener stock del producto |

### 📂 Categorías (`/api/categories`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Listar todas las categorías |
| `POST` | `/` | Crear nueva categoría |
| `GET` | `/<id>` | Obtener categoría por ID |
| `PUT` | `/<id>` | Actualizar categoría |
| `DELETE` | `/<id>` | Eliminar categoría |
| `GET` | `/search` | Buscar categorías |

### 📊 Stock (`/api/stock`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Consultar inventario completo |
| `POST` | `/` | Crear registro de stock |
| `PUT` | `/<id>` | Actualizar stock |
| `DELETE` | `/<id>` | Eliminar registro de stock |
| `GET` | `/low-stock` | Productos con stock bajo |
| `GET` | `/out-of-stock` | Productos sin stock |
| `POST` | `/<id>/adjust` | Ajustar stock (incremento/decremento) |
| `GET` | `/validate` | Validar reglas de negocio |

### 🛒 Órdenes (`/api/orders`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Listar órdenes de venta |
| `POST` | `/` | Crear nueva orden |
| `GET` | `/<id>` | Obtener orden por ID |
| `PUT` | `/<id>` | Actualizar orden |
| `DELETE` | `/<id>` | Eliminar orden |
| `POST` | `/<id>/complete` | Completar orden (transaccional) |
| `POST` | `/<id>/cancel` | Cancelar orden |
| `GET` | `/<id>/items` | Obtener items de la orden |
| `POST` | `/<id>/items` | Agregar item a la orden |

### 📋 Compras (`/api/purchases`)

| Método | Endpoint | Descripción |
|--------|----------|-------------|
| `GET` | `/` | Listar órdenes de compra |
| `POST` | `/` | Crear nueva orden de compra |
| `GET` | `/<id>` | Obtener orden de compra por ID |
| `PUT` | `/<id>` | Actualizar orden de compra |
| `DELETE` | `/<id>` | Eliminar orden de compra |
| `POST` | `/<id>/complete` | Completar orden (actualiza stock) |

## 🧪 Testing de la API

### Probar Endpoints desde Swagger UI

1. **Endpoints Públicos**: Puedes probarlos directamente
2. **Endpoints Protegidos**: 
   - Haz clic en "Authorize" y ingresa tu token
   - O copia el token desde la respuesta de login
3. **Ejecutar Requests**: 
   - Haz clic en "Try it out"
   - Completa los parámetros requeridos
   - Haz clic en "Execute"

### Ejemplo de Login

```bash
curl -X POST "http://localhost:5000/api/auth/login" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "admin",
    "password": "admin123"
  }'
```

### Ejemplo de Request Autenticado

```bash
curl -X GET "http://localhost:5000/api/products" \
  -H "Authorization: Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
```

## 📊 Códigos de Respuesta

| Código | Descripción | Ejemplo |
|--------|-------------|---------|
| **200** | Operación exitosa | Producto obtenido correctamente |
| **201** | Recurso creado | Producto creado exitosamente |
| **204** | Sin contenido | Producto eliminado correctamente |
| **400** | Error de validación | Datos incorrectos o duplicados |
| **401** | No autorizado | Token JWT inválido o expirado |
| **403** | Prohibido | Sin permisos suficientes |
| **404** | No encontrado | Producto no existe |
| **500** | Error interno | Error de base de datos |

## 🔍 Búsqueda y Filtrado

### Búsqueda de Productos

```http
GET /api/products/search?name=laptop&category_id=1&min_price=100&max_price=2000&in_stock=true
```

**Parámetros disponibles:**
- `name`: Búsqueda por nombre (parcial)
- `category_id`: Filtrar por categoría
- `min_price`: Precio mínimo
- `max_price`: Precio máximo
- `in_stock`: Solo productos con stock

### Búsqueda de Órdenes

```http
GET /api/orders/search?customer_name=juan&status=pending&date_from=2024-01-01&date_to=2024-12-31
```

**Parámetros disponibles:**
- `customer_name`: Búsqueda por cliente
- `status`: Filtrar por estado
- `date_from`: Fecha desde
- `date_to`: Fecha hasta
- `product_id`: Filtrar por producto

## 📈 Ejemplos de Uso

### Crear un Producto

```json
POST /api/products
{
  "name": "Laptop Dell XPS 13",
  "description": "Laptop ultrabook de 13 pulgadas con procesador Intel i7",
  "price": 1299.99,
  "category_id": 1,
  "min_stock": 5
}
```

### Crear una Orden

```json
POST /api/orders
{
  "customer_name": "Juan Pérez",
  "customer_email": "juan.perez@email.com",
  "customer_phone": "+34 123 456 789",
  "notes": "Entregar en horario de mañana",
  "items": [
    {
      "product_id": 1,
      "quantity": 2
    },
    {
      "product_id": 3,
      "quantity": 1
    }
  ]
}
```

### Ajustar Stock

```json
POST /api/stock/1/adjust
{
  "adjustment_type": "increment",
  "quantity": 10,
  "reason": "Reposición de inventario",
  "allow_negative": false
}
```

## 🚨 Validaciones de Negocio

### Reglas Implementadas

1. **Stock nunca negativo**: El sistema previene stock negativo
2. **Ventas no exceden stock**: No se pueden vender más unidades de las disponibles
3. **Operaciones transaccionales**: Las operaciones críticas usan commit/rollback
4. **Validación de datos**: Todos los campos tienen validaciones apropiadas

### Ejemplos de Validación

```json
// ❌ Error: Stock insuficiente
{
  "message": "Stock insuficiente para el producto 'Laptop Dell XPS 13'. Disponible: 5, Solicitado: 10"
}

// ❌ Error: Producto duplicado
{
  "message": "Ya existe un producto con ese nombre"
}

// ❌ Error: Cantidad inválida
{
  "message": "La cantidad debe ser mayor a 0"
}
```

## 🔧 Configuración Avanzada

### Personalizar Swagger UI

Puedes modificar la configuración en `app/api.py`:

```python
app.config["OPENAPI_SWAGGER_UI_CONFIG"] = {
    "docExpansion": "list",  # Expandir todos los endpoints
    "filter": True,           # Habilitar filtrado
    "tryItOutEnabled": True,  # Habilitar "Try it out"
    "syntaxHighlight.theme": "monokai"  # Tema de sintaxis
}
```

### Agregar Nuevos Endpoints

1. Crear el esquema en `app/schemas/`
2. Crear el endpoint en `app/api/`
3. Registrar en `app/api.py`
4. La documentación se genera automáticamente

## 🆘 Solución de Problemas

### Problemas Comunes

1. **Token expirado**: Usa `/api/auth/refresh` para renovar
2. **Permisos insuficientes**: Verifica el rol del usuario
3. **Validación fallida**: Revisa el esquema y los datos enviados
4. **Error de base de datos**: Verifica la conexión y estructura

### Logs y Debugging

- Los errores se registran en la consola del servidor
- Usa el modo debug para más información
- Revisa los logs de la aplicación

## 📚 Recursos Adicionales

- **README del Proyecto**: Documentación general del sistema
- **Guía de Onboarding**: Para nuevos desarrolladores
- **Guía de CI/CD**: Configuración de integración continua
- **Guía de Docker**: Ejecución con contenedores
- **Guía de Reglas de Negocio**: Validaciones implementadas

## 🤝 Contribuir

Para mejorar la documentación de la API:

1. Actualiza los esquemas con mejores descripciones
2. Agrega ejemplos más claros
3. Mejora la configuración de Swagger UI
4. Documenta nuevos endpoints
5. Agrega casos de uso y ejemplos

---

**🎯 Objetivo**: Proporcionar una documentación clara, completa y fácil de usar para que cualquier desarrollador pueda integrar y usar la API de manera eficiente.
