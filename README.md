# 📦 Sistema de Gestión de Inventario

[![CI/CD Pipeline](https://github.com/USERNAME/REPO_NAME/workflows/🚀%20CI%2FCD%20Pipeline/badge.svg)](https://github.com/USERNAME/REPO_NAME/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/USERNAME/REPO_NAME/actions/workflows/ci.yml)
[![Code Quality](https://img.shields.io/badge/code%20quality-A%2B-brightgreen)](https://github.com/USERNAME/REPO_NAME/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-blue)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Un sistema completo de gestión de inventario desarrollado con Flask que permite gestionar productos, categorías, stock y órdenes de compra/venta de manera eficiente y profesional.

## ✨ Características Principales

### 🎯 Funcionalidades Core
- **📁 Gestión de Categorías**: Crear, editar, eliminar y organizar categorías
- **🛍️ Gestión de Productos**: CRUD completo con asociación a categorías y precios
- **📊 Control de Stock**: Monitoreo en tiempo real con alertas de stock bajo
- **🛒 Órdenes de Venta**: Sistema completo con múltiples productos por orden
- **📋 Órdenes de Compra**: Gestión de reabastecimiento de inventario
- **📈 Dashboard**: Vista general con métricas y estadísticas del negocio
- **📱 Interfaz Responsiva**: Diseño moderno que se adapta a cualquier dispositivo

### 🔐 Funcionalidades de Seguridad
- **🔑 Autenticación Dual**: Sesiones para frontend + JWT para API
- **👥 Gestión de Usuarios**: Crear, editar y gestionar cuentas de usuario
- **🛡️ Sistema de Roles**: 4 niveles de acceso (Admin, Gerente, Usuario, Viewer)
- **🔒 Control de Permisos**: Acceso granular por funcionalidad (read, write, delete, manage_users, admin)
- **📝 Auditoría**: Logs completos de todas las acciones de usuario
- **🔐 Hashing Seguro**: Contraseñas protegidas con bcrypt
- **🛡️ Protección de Rutas**: Todas las operaciones de escritura requieren autenticación

### 📚 Documentación de API
- **🌐 OpenAPI 3.0**: Especificación completa de la API
- **📖 Swagger UI**: Interfaz interactiva para probar endpoints
- **🔍 Esquemas Validados**: Marshmallow schemas con validación automática
- **📋 Documentación Automática**: Generada automáticamente desde el código

### ✅ Sistema de Validaciones Centralizado
- **🛡️ Validaciones de Stock**: No-negativo, disponibilidad, integridad
- **📋 Validaciones de Órdenes**: Completitud, stock disponible, estructura
- **🔄 Validaciones Transaccionales**: Commit/rollback automático
- **🧪 Tests Completos**: Cobertura de todos los casos de uso

### 🔄 Flujo de Trabajo Optimizado

1. **⚙️ Configuración Inicial**:
   - Crear categorías de productos
   - Agregar productos al catálogo
   - Configurar stock inicial con niveles mínimos

2. **📦 Gestión de Órdenes**:
   - **Sección Órdenes**: Crear y gestionar órdenes de compra pendientes
   - **Sección Compras**: Visualizar historial de órdenes completadas
   - **Sección Ventas**: Procesar órdenes de venta con descuento automático de stock

3. **📊 Monitoreo**:
   - Dashboard con métricas en tiempo real
   - Alertas automáticas de stock bajo
   - Seguimiento completo de todas las transacciones

## 🛠️ Stack Tecnológico

- **🐍 Backend**: Flask 3.0.0 (Python) con arquitectura modular
- **🗄️ Base de Datos**: SQLite con SQLAlchemy ORM + Flask-Migrate
- **🎨 Frontend**: HTML5, CSS3, JavaScript Vanilla
- **🎭 UI/UX**: CSS personalizado con variables y sistema responsivo
- **🎯 Iconos**: Font Awesome para interfaz moderna
- **🔄 API**: RESTful con validación de datos y CORS configurado
- **📚 OpenAPI**: Documentación automática con flask-smorest
- **⚙️ Configuración**: Variables de entorno con python-dotenv
- **🔐 Seguridad**: JWT, bcrypt, middleware de autenticación

### 📦 Dependencias con Versiones Específicas
- **Flask==3.0.0**: Framework web principal
- **Flask-SQLAlchemy==3.1.1**: ORM para manejo de base de datos
- **Flask-CORS==4.0.0**: Manejo de CORS para API
- **Flask-Migrate==4.0.5**: Sistema de migraciones de base de datos
- **python-dotenv==1.0.0**: Carga de variables de entorno
- **flask-smorest==0.42.0**: Documentación automática de API
- **marshmallow==3.20.1**: Serialización y validación de datos

## 📋 Requisitos del Sistema

- Python 3.7 o superior
- Flask 2.0+
- SQLAlchemy 1.4+
- Navegador web moderno

## 🔧 Configuración de Variables de Entorno

### 📋 Opción 1: Configuración Automática (Recomendada)

Ejecuta el script de configuración automática:
```bash
python setup_env.py
```

Este script te guiará paso a paso para configurar:
- 🗄️ Base de datos (SQLite, PostgreSQL, MySQL)
- 🔐 Claves secretas (generadas automáticamente)
- 🌐 Entorno Flask (desarrollo, testing, producción)
- 📝 Configuración CORS
- 🔐 Configuración JWT
- 📊 Configuración de logs
- 📧 Configuración de email (opcional)

### 📋 Opción 2: Configuración Manual

1. **Copia el archivo de ejemplo**:
   ```bash
   cp env.example .env
   ```

2. **Configura las variables según tu entorno**:
   ```bash
   # 🗄️ Base de Datos
   DATABASE_URL=sqlite:///instance/stock_management.db
   
   # 🌐 Configuración Flask
   SECRET_KEY=tu-clave-secreta-super-segura-aqui
   FLASK_ENV=development
   DEBUG=True
   
   # 📝 CORS
   CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5000
   ```

### 🔍 Variables Disponibles

| Variable | Descripción | Valor por Defecto |
|----------|-------------|-------------------|
| `DATABASE_URL` | URI de conexión a la base de datos | `sqlite:///instance/stock_management.db` |
| `SECRET_KEY` | Clave secreta de Flask | Auto-generada |
| `DEBUG` | Modo debug | `True` |
| `FLASK_ENV` | Entorno de Flask | `development` |
| `CORS_ORIGINS` | Orígenes permitidos para CORS | `localhost:3000,127.0.0.1:5000` |

### 🗄️ Configuración de Base de Datos

**Para SQLite (recomendado para desarrollo):**
```bash
DATABASE_URL=sqlite:///instance/stock_management.db
```

**Para PostgreSQL (producción):**
```bash
DATABASE_URL=postgresql://usuario:password@localhost:5432/stock_management
```

**Para MySQL:**
```bash
DATABASE_URL=mysql://usuario:password@localhost:3306/stock_management
```

### 🔐 Configuración de Seguridad

**JWT (JSON Web Tokens):**
```bash
JWT_SECRET_KEY=clave-jwt-super-secreta-y-muy-larga-para-produccion
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000
```

**⚠️ IMPORTANTE:** Cambia la clave JWT_SECRET_KEY en producción por una clave segura y única.

### 🔑 Generar Claves Secretas Seguras

**Para generar claves secretas manualmente:**

```bash
# Generar SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# Generar JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"

# Verificar variables de entorno
python -c "from dotenv import load_dotenv; load_dotenv(); import os; print('DATABASE_URL:', os.getenv('DATABASE_URL'))"
```

## 🚀 Instalación Rápida

### 1. 📥 Clonar el repositorio
   ```bash
git clone https://github.com/tu-usuario/stock_management.git
cd stock_management
```

### 2. 🔧 Configurar entorno virtual
```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# Windows
env\Scripts\activate
# Linux/Mac
source env/bin/activate
```

### 3. 📦 Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. 🗄️ Inicializar la base de datos con migraciones

#### Configurar Flask-Migrate
```bash
# Inicializar el repositorio de migraciones
flask db init

# Crear la primera migración
flask db migrate -m "Migración inicial"

# Aplicar la migración
flask db upgrade
```

#### 📝 Comandos de Migración Útiles
```bash
# Crear nueva migración después de cambios en modelos
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones pendientes
flask db upgrade

# Ver historial de migraciones
flask db history

# Revertir a migración anterior
flask db downgrade
```

### 5. 🔐 Configurar Sistema de Autenticación

#### Crear Usuario Administrador
```bash
# Usar el nuevo sistema CLI unificado
python manage.py user create-admin
```

**Credenciales por defecto:**
- 🔐 **Admin**: `admin` / `Admin123!`
- 👔 **Gerente**: `gerente` / `Gerente123!`
- 👤 **Usuario**: `usuario` / `Usuario123!`
- 👁️ **Viewer**: `viewer` / `Viewer123!`

**⚠️ IMPORTANTE:** Cambia las contraseñas después del primer login.

#### Configurar Flask-Migrate
```bash
# Inicializar el repositorio de migraciones
flask db init

# Crear la primera migración
flask db migrate -m "Migración inicial"

# Aplicar la migración
flask db upgrade
```

#### 📝 Comandos de Migración Útiles
```bash
# Crear nueva migración después de cambios en modelos
flask db migrate -m "Descripción del cambio"

# Aplicar migraciones pendientes
flask db upgrade

# Ver historial de migraciones
flask db history

# Revertir a migración anterior
flask db downgrade
```

#### 📊 Cargar datos de ejemplo (opcional)
```bash
python load_sample_data.py
```

### 6. 🔐 Sistema de Roles y Permisos

#### 👑 Roles Disponibles
- **🔐 Administrador**: Acceso completo al sistema
  - Gestionar usuarios y roles
  - Acceso total a stock, órdenes y compras
  - Configuración del sistema
  
- **👔 Gerente**: Gestión operativa
  - Gestionar stock y órdenes
  - Crear y modificar productos
  - Acceso a reportes completos
  
- **👤 Usuario**: Operaciones básicas
  - Ver y crear órdenes
  - Consultar stock
  - Acceso limitado a funciones
  
- **👁️ Viewer**: Solo lectura
  - Consultar información
  - Sin permisos de modificación

#### 🛡️ Seguridad Implementada
- **JWT Tokens**: Autenticación segura con expiración
- **Hashing de Contraseñas**: bcrypt para máxima seguridad
- **Middleware de Autenticación**: Protección de todas las rutas
- **Control de Acceso**: Verificación de permisos por operación
- **Logs de Auditoría**: Registro de todas las acciones de usuario

### 5. 🚀 Ejecutar la aplicación
```bash
python run.py
```

**🌐 La aplicación estará disponible en:** `http://localhost:5000`

### 6. 📚 Acceder a la Documentación de la API

Una vez ejecutando, accede a:

- **🌐 Swagger UI**: `http://localhost:5000/swagger-ui`
- **📄 OpenAPI JSON**: `http://localhost:5000/api-spec.json`
- **📄 OpenAPI YAML**: `http://localhost:5000/api-spec.yaml`

**🔐 Para probar endpoints protegidos:**
1. Usa el botón "Authorize" en Swagger UI
2. Ingresa tu token JWT: `Bearer <tu-token>`
3. ¡Listo para probar todos los endpoints!

## 🏗️ Arquitectura del Proyecto

```
stock_management/
├── 📁 app/                      # Aplicación principal
│   ├── 🐍 __init__.py          # Factory de la aplicación Flask
│   ├── ⚙️ config.py            # Configuración centralizada
│   ├── 🗄️ database.py          # Configuración de base de datos
│   ├── 📁 models/              # Modelos de datos (SQLAlchemy)
│   │   ├── 📂 category.py      # Modelo de categorías
│   │   ├── 🛍️ product.py       # Modelo de productos
│   │   ├── 📊 stock.py         # Modelo de inventario
│   │   ├── 🛒 order.py         # Modelo de órdenes de venta
│   │   └── 📋 purchase_order.py # Modelo de órdenes de compra
│   └── 📁 routes/              # Endpoints de la API REST
│       ├── 📂 categories.py    # API de categorías
│       ├── 🛍️ products.py      # API de productos
│       ├── 📊 stock.py         # API de stock
│       ├── 🛒 orders.py        # API de órdenes de venta
│       └── 📋 purchases.py     # API de órdenes de compra
├── 📁 static/                  # Recursos estáticos
│   ├── 🎨 css/style.css       # Estilos principales
│   └── ⚡ js/app.js           # JavaScript principal
├── 📁 templates/               # Templates HTML
│   └── 🏠 index.html          # Aplicación SPA
├── 📁 instance/                # Base de datos SQLite
├── 📄 requirements.txt         # Dependencias Python
├── 🚀 run.py                  # Punto de entrada
├── 🔒 .gitignore              # Archivos ignorados por Git
└── 📖 README.md               # Documentación del proyecto
```

## 🌐 Documentación de la API

### 📖 Acceso a la Documentación

Una vez que la aplicación esté ejecutándose, puedes acceder a:

- **🌐 Swagger UI**: `http://localhost:5000/swagger-ui`
- **📄 OpenAPI JSON**: `http://localhost:5000/api-spec.json`
- **📄 OpenAPI YAML**: `http://localhost:5000/api-spec.yaml`

### ✨ Características de la Documentación

- **🎨 Interfaz moderna**: Swagger UI 5.9.0 con tema personalizado
- **🔍 Búsqueda y filtrado**: Encuentra endpoints rápidamente
- **📱 Responsive**: Funciona perfectamente en dispositivos móviles
- **🎯 Ejemplos interactivos**: Prueba endpoints directamente desde la interfaz
- **🔒 Autenticación integrada**: Botón Authorize para tokens JWT
- **📊 Respuestas detalladas**: Ejemplos de éxito y error para cada endpoint
- **🏷️ Organización por tags**: Endpoints agrupados por funcionalidad

### 🔐 Autenticación

La API utiliza JWT (JSON Web Tokens) para autenticación:

1. **Login**: `POST /api/auth/login` con `username` y `password`
2. **Usar Token**: Incluir `Authorization: Bearer <token>` en headers
3. **Refresh**: `POST /api/auth/refresh` para renovar tokens

### 📚 Endpoints Principales

#### 🔐 Autenticación (`/api/auth`)
- **Login/Logout**: Gestión de sesiones
- **Registro**: Crear nuevos usuarios
- **Perfil**: Gestionar información del usuario
- **Cambio de contraseña**: Actualizar credenciales

#### 🛍️ Productos (`/api/products`)
- **CRUD completo**: Crear, leer, actualizar, eliminar
- **Búsqueda avanzada**: Filtros por nombre, categoría, precio, stock
- **Validaciones**: Prevención de productos duplicados
- **Stock integrado**: Información de inventario incluida

#### 📂 Categorías (`/api/categories`)
- **Gestión completa**: Organización de productos
- **Búsqueda**: Filtrar por nombre y productos
- **Relaciones**: Productos asociados automáticamente

#### 📊 Stock (`/api/stock`)
- **Control de inventario**: Cantidades y alertas
- **Ajustes**: Incrementos y decrementos con validaciones
- **Validaciones de negocio**: Stock nunca negativo
- **Reportes**: Productos con stock bajo y agotado

#### 🛒 Órdenes (`/api/orders`)
- **Gestión de ventas**: Crear y gestionar órdenes
- **Validaciones**: Stock disponible y reglas de negocio
- **Estados**: Pendiente, completada, cancelada
- **Transaccional**: Operaciones seguras con rollback

#### 📋 Compras (`/api/purchases`)
- **Órdenes de compra**: Reposición de inventario
- **Actualización automática**: Stock se actualiza al completar
- **Seguimiento**: Estado y progreso de las compras

### 🧪 Testing Interactivo

Puedes probar todos los endpoints directamente desde Swagger UI:

1. **Endpoints Públicos**: Prueba directamente
2. **Endpoints Protegidos**: 
   - Haz clic en "Authorize" (🔒)
   - Ingresa tu token JWT: `Bearer <tu-token>`
   - ¡Listo para probar!

### 📖 Documentación Detallada

Para información completa sobre la API, consulta:
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)**: Guía completa de la API
- **Swagger UI**: Interfaz interactiva con ejemplos
- **OpenAPI Spec**: Especificación técnica en JSON/YAML

## 🎨 Características de la Interfaz

### 📈 Dashboard Inteligente
- 📊 Estadísticas en tiempo real
- ⚠️ Alertas de productos con stock bajo
- 📈 Métricas de órdenes pendientes
- 💰 Resumen de ventas y compras

### 🛍️ Gestión de Productos
- 🔍 Filtrado por categoría
- 🔎 Búsqueda en tiempo real
- ✏️ Edición rápida
- 🔗 Asociación automática con stock

### 📦 Sistema de Órdenes Avanzado
- 🛒 Múltiples productos por orden
- ✅ Validación de stock en tiempo real
- 🏷️ Estados de seguimiento (pendiente, completada)
- 📜 Historial completo de transacciones
- 🎯 Flujo optimizado para crear órdenes

### 📱 Diseño Responsivo
- 💻 Adaptable para escritorio, tablet y móvil
- 🍔 Menú de navegación hamburguesa
- 📋 Tablas responsivas con scroll horizontal
- 🎨 Interfaz moderna y limpia

## ⚙️ Configuración Avanzada

### 🔐 Variables de Entorno
Crea un archivo `.env` para configuraciones personalizadas:
```env
DATABASE_URL=sqlite:///instance/stock_management.db
SECRET_KEY=tu-clave-secreta-aqui
DEBUG=True
FLASK_ENV=development
```

### 🗄️ Configuración de Base de Datos
La aplicación usa SQLite por defecto. Para usar PostgreSQL:

1. 📦 Instalar psycopg2: `pip install psycopg2-binary`
2. ⚙️ Modificar `SQLALCHEMY_DATABASE_URI` en `app/config.py`
3. 🔄 Ejecutar migraciones si es necesario

## 🧪 Testing y Validación

### 🔍 Archivos de Prueba Incluidos
- `test_api.py` - 🧪 Pruebas de endpoints de API
- `test_crud.py` - 📝 Pruebas de operaciones CRUD
- `test_frontend.py` - 🎨 Pruebas de interfaz
- `verify_data.py` - ✅ Verificación de integridad de datos
- `test_validations.py` - ✅ Pruebas de validaciones centralizadas

### ✅ Sistema de Validaciones

#### 🛡️ Validaciones de Stock
- **Cantidad no-negativa**: Previene stock negativo
- **Stock mínimo válido**: Niveles de alerta apropiados
- **Disponibilidad**: Verifica stock antes de operaciones
- **Integridad**: Previene duplicados y inconsistencias

#### 📋 Validaciones de Órdenes
- **Completitud**: Verifica que todos los campos requeridos estén presentes
- **Stock disponible**: Confirma disponibilidad antes de crear/completar
- **Estructura válida**: Valida formato de items y cantidades
- **Estados permitidos**: Solo operaciones válidas por estado

#### 🔄 Validaciones Transaccionales
- **Commit automático**: Operaciones exitosas se confirman
- **Rollback automático**: Errores revierten cambios
- **Consistencia**: Base de datos siempre en estado válido
- **Atomicidad**: Operaciones completas o nada

#### 🐛 Casos de Uso Cubiertos
- ✅ **"Crear orden con producto ya agregado"** - Funciona correctamente
- ✅ **"Orden incompleta"** - Falla con mensaje claro
- ✅ **"Stock insuficiente"** - Previene sobreventa
- ✅ **"Cantidades inválidas"** - Valida números positivos
- ✅ **"Productos inexistentes"** - Verifica existencia

### 🚀 Ejecutar Pruebas
```bash
# Probar API
python test_api.py

# Verificar datos
python verify_data.py

# Probar operaciones CRUD
python test_crud.py

# Probar documentación de la API
python test_api_docs.py

# Probar validaciones centralizadas
python -m pytest tests/test_validations.py -v
```

## 🖥️ Sistema CLI Unificado

### 🚀 Comandos Principales

El proyecto incluye un sistema CLI unificado para todas las operaciones de gestión:

```bash
# Ver ayuda general
python manage.py --help

# Ver ayuda específica
python manage.py seed --help
python manage.py db --help
python manage.py user --help
```

### 🌱 Seeding de Datos

```bash
# Cargar datos de demostración completos
python manage.py seed --demo

# Cargar productos personalizados
python manage.py seed --custom

# Cargar todos los datos
python manage.py seed --all
```

### 🗄️ Gestión de Base de Datos

```bash
# Inicializar base de datos
python manage.py db init

# Crear migración (requiere Flask-Migrate)
python manage.py db migrate

# Aplicar migraciones
python manage.py db upgrade
```

### 👥 Gestión de Usuarios

```bash
# Crear usuario administrador
python manage.py user create-admin

# Crear usuarios de muestra
python manage.py user create-sample
```

### 📊 Utilidades

```bash
# Ver estado de la aplicación
python manage.py status

# Abrir shell interactivo
python manage.py shell
```

### 🔄 Migración desde Scripts Antiguos

Si tienes scripts antiguos (`init_sample_data.py`, `load_sample_data.py`, etc.), puedes migrar fácilmente:

```bash
# Ejecutar script de migración
python migrate_to_cli.py

# Esto creará backup y guía de migración
```

## 📚 Documentación Completa

### 🚀 Guías Principales
- **[ONBOARDING_GUIDE.md](ONBOARDING_GUIDE.md)** - 🚀 **Guía completa de onboarding para nuevos desarrolladores**
- **[CI_CD_GUIDE.md](CI_CD_GUIDE.md)** - Guía completa del sistema CI/CD con GitHub Actions
- **[SETUP_CI_CD.md](SETUP_CI_CD.md)** - Configuración paso a paso de CI/CD

### 🔧 Guías de Desarrollo
- **[CLI_EXAMPLES.md](CLI_EXAMPLES.md)** - Ejemplos de uso del CLI de gestión
- **[MIGRATION_CLI.md](MIGRATION_CLI.md)** - Guía de migración del CLI
- **[MIGRATION_POSTGRESQL.md](MIGRATION_POSTGRESQL.md)** - Migración a PostgreSQL
- **[VALIDATIONS.md](VALIDATIONS.md)** - Sistema de validaciones del proyecto

### 🚀 Guías de Despliegue
- **[DEPLOY_CLOUD.md](DEPLOY_CLOUD.md)** - Guía completa de despliegue en la nube
- **[README_DOCKER.md](README_DOCKER.md)** - Guía de Docker y contenerización
- **[DEPLOY_GITHUB.md](DEPLOY_GITHUB.md)** - Despliegue en GitHub Pages

### 🎨 Guías de Funcionalidades
- **[TOAST_SYSTEM.md](TOAST_SYSTEM.md)** - Sistema de notificaciones toast
- **[README_CLI.md](README_CLI.md)** - Documentación del CLI de gestión
- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - 📚 **Documentación completa de la API con Swagger/OpenAPI**
- **[AUTH_SYSTEM_README.md](AUTH_SYSTEM_README.md)** - 🔐 **Sistema completo de autenticación y autorización**

### 🐳 Guías de Docker
- **[DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md)** - 🚀 **Inicio rápido con Docker en 1 comando**
- **[README_DOCKER.md](README_DOCKER.md)** - Guía completa de Docker y contenerización

### 📋 Scripts de Configuración
- **[setup_complete.py](setup_complete.py)** - Configuración automática completa de CI/CD
- **[setup_env.py](setup_env.py)** - Configuración automática de variables de entorno
- **[personalize_badges.py](personalize_badges.py)** - Personalización de badges del README
- **[install_pre_commit.py](install_pre_commit.py)** - Instalación de pre-commit hooks

## 🤝 Contribución

¡Las contribuciones son bienvenidas! Para contribuir:

1. 🍴 Fork el proyecto
2. 🌿 Crea una rama: `git checkout -b feature/nueva-caracteristica`
3. 💾 Commit cambios: `git commit -m 'Agregar nueva característica'`
4. 📤 Push a la rama: `git push origin feature/nueva-caracteristica`
5. 🔄 Abre un Pull Request

### 📝 Guías de Contribución
- ✅ Seguir las convenciones de código existentes
- 🧪 Agregar tests para nuevas características
- 📖 Actualizar documentación cuando sea necesario
- 🔍 Asegurar que todas las pruebas pasen

## 📄 Licencia

Este proyecto está bajo la **Licencia MIT**. Ver el archivo `LICENSE` para más detalles.

## 🆘 Soporte y Ayuda

### 🔧 Solución de Problemas Comunes

#### ❌ **Problema: Spinner infinito en login (puerto 8080)**
**Síntomas:** El spinner de login se queda "pensando" sin redirigir
**Causa:** Problema de CORS entre puertos diferentes (frontend en 8080, backend en 5000)

**Solución rápida:**
```bash
# 1. Ejecutar el configurador automático
python setup_cors.py

# 2. Iniciar el backend (puerto 5000)
python start_backend.py

# 3. Probar la API
python test_api_cors.py
```

**Solución manual:**
1. Crear archivo `.env` con:
   ```
   CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000,http://localhost:8080,http://127.0.0.1:8080
   CORS_SUPPORTS_CREDENTIALS=True
   ```
2. **IMPORTANTE:** El backend debe ejecutarse en puerto 5000, no en 8080
3. Reiniciar el backend: `python run.py` (puerto 5000)
4. Verificar que el frontend use `credentials: 'include'`

**⚠️ NOTA CRÍTICA:** 
- Backend: Puerto 5000 (http://127.0.0.1:5000)
- Frontend: Puerto 8080 (http://localhost:8080)
- El archivo `run.py` debe tener `port=5000`, NO `port=8080`

#### ❌ **Problema: Error "Subject must be a string" en JWT**
**Síntomas:** Error 500 en login, spinner infinito
**Causa:** JWT recibe ID numérico en lugar de string
**Estado:** ✅ **SOLUCIONADO** en `app/routes/auth.py`

#### ❌ **Problema: Cookies de sesión no se establecen**
**Síntomas:** Usuario se desloguea al recargar la página
**Causa:** CORS no permite credenciales o configuración incorrecta
**Solución:** Verificar `supports_credentials=True` en CORS

#### ❌ **Problema: Frontend no puede conectar al backend**
**Síntomas:** Errores de red en consola del navegador
**Causa:** URL incorrecta o puerto diferente
**Solución:** Frontend detecta automáticamente puerto 8080 y usa 127.0.0.1:5000

### 🧪 **Diagnóstico Automático**
```bash
# Probar API y CORS
python test_api_cors.py

# Configurar entorno automáticamente
python setup_cors.py
```

### �� ¿Necesitas ayuda?
1. 📖 Revisa esta documentación
2. 🔍 Busca en [issues existentes](../../issues)
3. ❓ Crea un [nuevo issue](../../issues/new) con detalles

### 🐛 Reportar Bugs
Al reportar un bug, incluye:
- 🖥️ Sistema operativo y versión de Python
- 📝 Pasos para reproducir el error
- 📋 Mensaje de error completo
- 📸 Capturas de pantalla si es relevante

## 🗺️ Roadmap de Desarrollo

### 🚀 Próximas Características
- [x] 👤 Sistema de usuarios y autenticación ✅
- [ ] 📊 Reportes y gráficos avanzados
- [ ] 📤 Exportación de datos (CSV, PDF)
- [ ] 📧 Notificaciones por email
- [x] 📋 API REST documentada con Swagger/OpenAPI ✅
- [ ] 🌙 Modo oscuro/claro
- [ ] 💾 Backup automático de base de datos
- [ ] 🔔 Sistema de notificaciones push

### 🛠️ Mejoras Técnicas
- [ ] 🧪 Tests automatizados completos
- [ ] 🔄 CI/CD con GitHub Actions
- [ ] 🐳 Dockerización completa
- [ ] ☁️ Deploy automático en cloud
- [ ] 📊 Monitoreo y logs centralizados
- [ ] ⚡ Cache con Redis
- [x] 🔒 Seguridad mejorada con JWT ✅

### 🎯 Optimizaciones
- [ ] ⚡ Mejoras de rendimiento
- [ ] 📱 PWA (Progressive Web App)
- [ ] 🌐 Internacionalización (i18n)
- [ ] ♿ Mejoras de accesibilidad
- [ ] 📊 Analytics integrado

## 🎉 Características Destacadas

### 🧠 Gestión Inteligente de Stock
- 🚨 Alertas automáticas de stock bajo
- 💡 Sugerencias de reabastecimiento
- 📈 Historial completo de movimientos
- 🎯 Niveles de stock personalizables

### 📋 Sistema de Órdenes Robusto
- 🛒 Órdenes multi-producto
- 🏷️ Estados de seguimiento detallados
- ✅ Validación automática de disponibilidad
- 🔄 Actualización automática de inventario

### 📊 Dashboard Informativo
- 📈 Métricas en tiempo real
- 📊 Gráficos de tendencias
- ⚠️ Alertas importantes
- 📋 Resumen ejecutivo completo

---

### 💝 ¿Te gusta este proyecto?

⭐ **¡Dale una estrella si te ha sido útil!** ⭐

🐛 **¿Encontraste un bug?** [Repórtalo aquí](../../issues/new)

💡 **¿Tienes una idea?** [Compártela con nosotros](../../discussions)

🤝 **¿Quieres contribuir?** [Lee nuestra guía de contribución](#-contribución)

---

*Desarrollado con ❤️ para la comunidad*