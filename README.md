# 📦 Sistema de Gestión de Inventario

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

- **🐍 Backend**: Flask (Python) con arquitectura modular
- **🗄️ Base de Datos**: SQLite con SQLAlchemy ORM
- **🎨 Frontend**: HTML5, CSS3, JavaScript Vanilla
- **🎭 UI/UX**: CSS personalizado con variables y sistema responsivo
- **🎯 Iconos**: Font Awesome para interfaz moderna
- **🔄 API**: RESTful con validación de datos

## 📋 Requisitos del Sistema

- Python 3.7 o superior
- Flask 2.0+
- SQLAlchemy 1.4+
- Navegador web moderno

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

### 4. 🗄️ Inicializar base de datos
```bash
# Crear las tablas
python -c "from app import create_app; app = create_app(); app.app_context().push(); from app.database import db; db.create_all()"

# Cargar datos de ejemplo (opcional)
python load_sample_data.py
```

### 5. 🚀 Ejecutar la aplicación
```bash
python run.py
```

**🌐 La aplicación estará disponible en:** `http://localhost:5000`

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

### 📂 Categorías
```http
GET    /api/categories/        # 📋 Listar todas las categorías
POST   /api/categories/        # ➕ Crear nueva categoría
PUT    /api/categories/<id>    # ✏️ Actualizar categoría
DELETE /api/categories/<id>    # 🗑️ Eliminar categoría
```

### 🛍️ Productos
```http
GET    /api/products/          # 📋 Listar todos los productos
POST   /api/products/          # ➕ Crear nuevo producto
PUT    /api/products/<id>      # ✏️ Actualizar producto
DELETE /api/products/<id>      # 🗑️ Eliminar producto
```

### 📊 Stock
```http
GET    /api/stock/             # 📋 Consultar inventario
POST   /api/stock/             # ➕ Crear registro de stock
PUT    /api/stock/<id>         # ✏️ Actualizar stock
```

### 🛒 Órdenes de Venta
```http
GET    /api/orders/            # 📋 Listar órdenes de venta
POST   /api/orders/            # ➕ Crear nueva orden
PUT    /api/orders/<id>/complete # ✅ Completar orden
DELETE /api/orders/<id>        # 🗑️ Eliminar orden
```

### 📋 Órdenes de Compra
```http
GET    /api/purchases/         # 📋 Listar órdenes de compra
POST   /api/purchases/         # ➕ Crear nueva orden
PUT    /api/purchases/<id>/complete # ✅ Completar orden (actualiza stock)
DELETE /api/purchases/<id>     # 🗑️ Eliminar orden
```

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

### 🚀 Ejecutar Pruebas
```bash
# Probar API
python test_api.py

# Verificar datos
python verify_data.py

# Probar operaciones CRUD
python test_crud.py
```

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

### 🔍 ¿Necesitas ayuda?
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
- [ ] 👤 Sistema de usuarios y autenticación
- [ ] 📊 Reportes y gráficos avanzados
- [ ] 📤 Exportación de datos (CSV, PDF)
- [ ] 📧 Notificaciones por email
- [ ] 📋 API REST documentada con Swagger
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
- [ ] 🔒 Seguridad mejorada con JWT

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