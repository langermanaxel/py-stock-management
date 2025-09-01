# 📦 Sistema de Gestión de Inventario

[![CI/CD Pipeline](https://github.com/USERNAME/REPO_NAME/workflows/🚀%20CI%2FCD%20Pipeline/badge.svg)](https://github.com/USERNAME/REPO_NAME/actions/workflows/ci.yml)
[![Tests](https://img.shields.io/badge/tests-passing-brightgreen)](https://github.com/USERNAME/REPO_NAME/actions/workflows/ci.yml)
[![Code Quality](https://img.shields.io/badge/code%20quality-A%2B-brightgreen)](https://github.com/USERNAME/REPO_NAME/actions/workflows/ci.yml)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/flask-3.0.0-blue)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

Un sistema completo de gestión de inventario desarrollado con Flask que permite gestionar productos, categorías, stock y órdenes de compra/venta de manera eficiente y profesional.

## 🚀 Inicio Rápido

### 1. Configuración Inicial
```bash
# Clonar el repositorio
git clone https://github.com/USERNAME/stock_management.git
cd stock_management

# Configurar entorno
python scripts/setup_env.py

# Crear base de datos
python scripts/create_working_database.py

# Ejecutar aplicación
python run.py
```

### 2. Acceso a la Aplicación
- **🌐 Aplicación Web**: `http://localhost:5000`
- **📚 API Docs**: `http://localhost:5000/swagger-ui`
- **🔐 Login Demo**: admin / admin123

## 📁 Estructura del Proyecto

```
stock_management/
├── 📁 app/                    # Aplicación principal Flask
│   ├── 📁 api/               # Endpoints de API REST
│   ├── 📁 models/            # Modelos de base de datos
│   ├── 📁 routes/            # Rutas del frontend
│   ├── 📁 schemas/           # Esquemas de validación
│   ├── 📁 validators/        # Validadores de negocio
│   ├── 📁 decorators/        # Decoradores personalizados
│   ├── 📁 middleware/        # Middleware de la aplicación
│   └── 📄 config.py          # Configuración de la app
├── 📁 scripts/               # Scripts de utilidad y configuración
│   ├── setup_*.py           # Scripts de configuración
│   ├── create_*.py          # Scripts de creación de datos
│   ├── manage.py            # CLI de gestión
│   └── demo_*.py            # Scripts de demostración
├── 📁 docs/                  # Documentación completa
│   ├── README.md            # Documentación principal
│   ├── API_DOCUMENTATION.md # Documentación de API
│   ├── AUTH_SYSTEM_README.md # Sistema de autenticación
│   └── *.md                 # Otra documentación
├── 📁 tests/                 # Tests automatizados
│   ├── test_*.py            # Tests unitarios e integración
│   └── conftest.py          # Configuración de pytest
├── 📁 docker/                # Configuración Docker
│   ├── Dockerfile           # Imagen de contenedor
│   ├── docker-compose.yml   # Orquestación de servicios
│   └── docker-scripts.*     # Scripts de Docker
├── 📁 deployment/            # Archivos de despliegue
│   └── Procfile             # Configuración Heroku
├── 📁 config/                # Archivos de configuración
│   └── env.example          # Variables de entorno ejemplo
├── 📁 static/                # Archivos estáticos (CSS, JS)
├── 📁 templates/             # Plantillas HTML
├── 📁 instance/              # Base de datos SQLite
└── 📄 run.py                 # Punto de entrada de la aplicación
```

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
- **🔒 Control de Permisos**: Acceso granular por funcionalidad
- **📝 Auditoría**: Logs completos de todas las acciones de usuario
- **🔐 Hashing Seguro**: Contraseñas protegidas con bcrypt

## 🛠️ Stack Tecnológico

- **🐍 Backend**: Flask 3.0.0 (Python) con arquitectura modular
- **🗄️ Base de Datos**: SQLite con SQLAlchemy ORM + Flask-Migrate
- **🎨 Frontend**: HTML5, CSS3, JavaScript Vanilla
- **🎭 UI/UX**: CSS personalizado con variables y sistema responsivo
- **🎯 Iconos**: Font Awesome para interfaz moderna
- **🔄 API**: RESTful con validación de datos y CORS configurado
- **📚 OpenAPI**: Documentación automática con flask-smorest

## 📚 Documentación

- **[📖 Documentación Completa](docs/README.md)** - Guía detallada del sistema
- **[🔐 Sistema de Autenticación](docs/AUTH_SYSTEM_README.md)** - Configuración de seguridad
- **[🌐 Documentación de API](docs/API_DOCUMENTATION.md)** - Endpoints y ejemplos
- **[🐳 Docker](docs/README_DOCKER.md)** - Configuración de contenedores
- **[🚀 Despliegue](docs/DEPLOY_CLOUD.md)** - Guías de despliegue
- **[🧪 Tests](docs/)** - Documentación de testing

## 🧪 Testing

```bash
# Ejecutar todos los tests
pytest

# Tests con cobertura
pytest --cov=app

# Tests específicos
pytest tests/test_auth.py
```

## 🐳 Docker

```bash
# Construir imagen
docker build -f docker/Dockerfile -t stock-management .

# Ejecutar con docker-compose
docker-compose -f docker/docker-compose.yml up
```

## 🤝 Contribución

1. Fork el proyecto
2. Crea una rama para tu feature (`git checkout -b feature/AmazingFeature`)
3. Commit tus cambios (`git commit -m 'Add some AmazingFeature'`)
4. Push a la rama (`git push origin feature/AmazingFeature`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver el archivo [LICENSE](LICENSE) para detalles.

## 🆘 Soporte

Si tienes problemas o preguntas:

1. Revisa la [documentación](docs/)
2. Busca en los [issues existentes](https://github.com/USERNAME/stock_management/issues)
3. Crea un [nuevo issue](https://github.com/USERNAME/stock_management/issues/new)

---

**Desarrollado con ❤️ usando Flask y Python**
