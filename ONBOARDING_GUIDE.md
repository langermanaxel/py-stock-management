# 🚀 Guía de Onboarding - Sistema de Gestión de Inventario

## 📋 Resumen del Proyecto

**Sistema de Gestión de Inventario** es una aplicación web completa desarrollada con Flask que permite gestionar productos, categorías, stock y órdenes de compra/venta de manera eficiente y profesional.

### ✨ Características Principales
- 🗄️ **Gestión de Inventario** - Productos, categorías, stock
- 👥 **Sistema de Usuarios** - Roles y permisos
- 📊 **Reportes y Analytics** - Dashboard interactivo
- 🔐 **Autenticación JWT** - Seguridad robusta
- 📱 **Interfaz Responsiva** - Compatible con móviles
- 🧪 **Tests Automatizados** - CI/CD completo
- 🐳 **Docker Ready** - Despliegue fácil

---

## 🎯 Requisitos Previos

### 🐍 Python
- **Versión**: 3.8 o superior
- **Verificar**: `python --version`

### 📦 Gestor de Paquetes
- **pip**: Incluido con Python 3.4+
- **Verificar**: `pip --version`

### 🔧 Git
- **Versión**: 2.0 o superior
- **Verificar**: `git --version`

### 🌐 Navegador Web
- **Chrome**, **Firefox**, **Safari** o **Edge** (versión moderna)

---

## 🚀 Configuración Inicial

### 1. 📥 Clonar el Repositorio

```bash
# Clonar el repositorio
git clone https://github.com/USERNAME/stock_management.git

# Entrar al directorio
cd stock_management

# Verificar contenido
ls -la
```

### 2. 🔧 Configurar Variables de Entorno

#### Opción A: Configuración Automática (Recomendada)
```bash
# Ejecutar script de configuración
python setup_env.py

# El script te guiará paso a paso para configurar:
# - Base de datos
# - Claves secretas
# - Entorno Flask
# - Configuración CORS y JWT
```

#### Opción B: Configuración Manual
```bash
# Copiar archivo de ejemplo
cp env.example .env

# Editar .env con tus valores
nano .env  # o usar tu editor preferido
```

### 3. 🌍 Crear Entorno Virtual

```bash
# Crear entorno virtual
python -m venv env

# Activar entorno virtual
# Windows
env\Scripts\activate

# Linux/Mac
source env/bin/activate

# Verificar activación
which python  # Debe mostrar ruta dentro de env/
```

### 4. 📦 Instalar Dependencias

```bash
# Actualizar pip
pip install --upgrade pip

# Instalar dependencias del proyecto
pip install -r requirements.txt

# Verificar instalación
pip list
```

---

## 🗄️ Configuración de Base de Datos

### 🐘 SQLite (Desarrollo - Recomendado para empezar)

**Ventajas:**
- ✅ No requiere instalación adicional
- ✅ Archivo único, fácil de respaldar
- ✅ Perfecto para desarrollo y testing

**Configuración:**
```bash
# En .env
DATABASE_URL=sqlite:///instance/stock_management.db
```

### 🐘 PostgreSQL (Producción)

**Ventajas:**
- ✅ Robusto y escalable
- ✅ Soporte avanzado para JSON
- ✅ Mejor rendimiento con grandes volúmenes

**Instalación:**
```bash
# Ubuntu/Debian
sudo apt-get install postgresql postgresql-contrib

# macOS
brew install postgresql

# Windows
# Descargar desde https://www.postgresql.org/download/windows/
```

**Configuración:**
```bash
# En .env
DATABASE_URL=postgresql://usuario:password@localhost:5432/stock_management
```

### 🐘 MySQL (Alternativa)

**Instalación:**
```bash
# Ubuntu/Debian
sudo apt-get install mysql-server

# macOS
brew install mysql

# Windows
# Descargar desde https://dev.mysql.com/downloads/mysql/
```

**Configuración:**
```bash
# En .env
DATABASE_URL=mysql://usuario:password@localhost:3306/stock_management
```

---

## 🔐 Configuración de Seguridad

### 🔑 Claves Secretas

**Generar automáticamente:**
```bash
python setup_env.py  # Las genera por ti
```

**Generar manualmente:**
```bash
# SECRET_KEY
python -c "import secrets; print(secrets.token_hex(32))"

# JWT_SECRET_KEY
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 🔐 Configuración JWT

**Variables en .env:**
```bash
JWT_SECRET_KEY=tu-clave-jwt-super-secreta
JWT_ACCESS_TOKEN_EXPIRES=3600        # 1 hora
JWT_REFRESH_TOKEN_EXPIRES=2592000    # 30 días
```

---

## 🚀 Inicialización del Proyecto

### 1. 🗄️ Inicializar Base de Datos

```bash
# Inicializar repositorio de migraciones
python manage.py db init

# Crear primera migración
python manage.py db migrate -m "Migración inicial"

# Aplicar migración
python manage.py db upgrade
```

### 2. 👥 Crear Usuario Administrador

```bash
# Crear usuario admin
python manage.py user create-admin

# Seguir las instrucciones para configurar:
# - Email
# - Password
# - Nombre completo
```

### 3. 🌱 Cargar Datos de Ejemplo (Opcional)

```bash
# Cargar categorías y productos de ejemplo
python seed_data.py

# O usar el CLI
python manage.py data seed
```

---

## 🧪 Ejecutar Tests

### 🧪 Tests Básicos

```bash
# Ejecutar todos los tests
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=app --cov-report=html

# Tests específicos
pytest tests/test_crud.py -v
```

### 🔍 Linting y Formateo

```bash
# Verificar formato con Black
black --check .

# Verificar imports con isort
isort --check-only .

# Verificar estilo con Flake8
flake8 .

# Verificar tipos con MyPy
mypy app/
```

---

## 🚀 Ejecutar la Aplicación

### 🏃‍♂️ Modo Desarrollo

```bash
# Ejecutar directamente
python run.py

# O usar Flask CLI
flask run

# O usar el script de gestión
python manage.py run
```

### 🐳 Con Docker (¡Recomendado!)

**🚀 ¡Levanta en 1 comando!**

```bash
# Opción 1: Script automático (Linux/Mac)
chmod +x start-docker.sh
./start-docker.sh

# Opción 2: Script automático (Windows PowerShell)
.\start-docker.ps1

# Opción 3: Comando manual
docker-compose up -d
```

**📋 Comandos útiles:**
```bash
# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener
docker-compose down

# Reiniciar
docker-compose restart
```

**🌐 Acceso:**
- **Aplicación**: http://localhost:5000
- **API Docs**: http://localhost:5000/swagger-ui

**📖 Ver [DOCKER_QUICKSTART.md](DOCKER_QUICKSTART.md) para más detalles.**

---

## 📱 Acceder a la Aplicación

### 🌐 Navegador Web

1. **Abrir navegador**
2. **Ir a**: `http://localhost:5000`
3. **Login con usuario admin** creado anteriormente

### 📱 API REST

**Base URL**: `http://localhost:5000/api/v1`

**Endpoints principales:**
- `GET /api/v1/products` - Listar productos
- `POST /api/v1/products` - Crear producto
- `GET /api/v1/categories` - Listar categorías
- `POST /api/v1/auth/login` - Login de usuario

---

## 🔧 Comandos Útiles

### 🗄️ Base de Datos

```bash
# Ver estado de migraciones
python manage.py db current

# Ver historial de migraciones
python manage.py db history

# Crear nueva migración
python manage.py db migrate -m "Descripción del cambio"

# Aplicar migraciones
python manage.py db upgrade

# Revertir migración
python manage.py db downgrade
```

### 👥 Usuarios

```bash
# Crear usuario admin
python manage.py user create-admin

# Crear usuario normal
python manage.py user create

# Listar usuarios
python manage.py user list

# Cambiar password
python manage.py user change-password
```

### 📊 Datos

```bash
# Cargar datos de ejemplo
python manage.py data seed

# Verificar datos
python manage.py data verify

# Limpiar datos
python manage.py data clear
```

### 🧪 Testing

```bash
# Tests con coverage
pytest tests/ --cov=app --cov-report=html

# Tests específicos
pytest tests/test_crud.py::test_create_product -v

# Tests con reporte detallado
pytest tests/ -v --tb=long
```

---

## 🚨 Troubleshooting Común

### ❌ Error: "No module named 'flask'"

**Solución:**
```bash
# Activar entorno virtual
source env/bin/activate  # Linux/Mac
env\Scripts\activate     # Windows

# Instalar dependencias
pip install -r requirements.txt
```

### ❌ Error: "Database not found"

**Solución:**
```bash
# Verificar DATABASE_URL en .env
cat .env | grep DATABASE_URL

# Inicializar base de datos
python manage.py db init
python manage.py db migrate
python manage.py db upgrade
```

### ❌ Error: "Port already in use"

**Solución:**
```bash
# Cambiar puerto en .env
FLASK_RUN_PORT=5001

# O matar proceso en puerto 5000
lsof -ti:5000 | xargs kill -9  # Linux/Mac
netstat -ano | findstr :5000    # Windows
```

### ❌ Error: "Permission denied"

**Solución:**
```bash
# Verificar permisos de archivos
ls -la

# Dar permisos de ejecución
chmod +x *.py

# Verificar permisos de directorios
chmod 755 app/ templates/ static/
```

---

## 📚 Recursos Adicionales

### 📖 Documentación

- **README.md** - Documentación principal del proyecto
- **CI_CD_GUIDE.md** - Guía de CI/CD y GitHub Actions
- **SETUP_CI_CD.md** - Configuración paso a paso de CI/CD
- **CLI_EXAMPLES.md** - Ejemplos de uso del CLI
- **DEPLOY_CLOUD.md** - Guía de despliegue en la nube

### 🔗 Enlaces Útiles

- **Flask**: [flask.palletsprojects.com](https://flask.palletsprojects.com/)
- **SQLAlchemy**: [docs.sqlalchemy.org](https://docs.sqlalchemy.org/)
- **Pytest**: [docs.pytest.org](https://docs.pytest.org/)
- **GitHub Actions**: [docs.github.com/en/actions](https://docs.github.com/en/actions)

### 🆘 Obtener Ayuda

1. **Revisar logs** en `logs/app.log`
2. **Verificar configuración** en `.env`
3. **Ejecutar tests** para identificar problemas
4. **Revisar documentación** del proyecto
5. **Crear issue** en GitHub si persiste el problema

---

## 🎉 ¡Onboarding Completado!

### ✅ Checklist de Verificación

- [ ] ✅ Repositorio clonado
- [ ] ✅ Variables de entorno configuradas
- [ ] ✅ Entorno virtual creado y activado
- [ ] ✅ Dependencias instaladas
- [ ] ✅ Base de datos inicializada
- [ ] ✅ Usuario admin creado
- [ ] ✅ Aplicación ejecutándose
- [ ] ✅ Acceso desde navegador
- [ ] ✅ Tests ejecutándose
- [ ] ✅ Linting sin errores

### 🚀 Próximos Pasos

1. **Explorar la aplicación** - Navegar por todas las funcionalidades
2. **Revisar el código** - Entender la estructura del proyecto
3. **Ejecutar tests** - Familiarizarse con el sistema de testing
4. **Hacer cambios** - Experimentar con el código
5. **Contribuir** - Reportar bugs o sugerir mejoras

### 🎯 Objetivos de Aprendizaje

- **Flask**: Framework web y sus extensiones
- **SQLAlchemy**: ORM y migraciones de base de datos
- **Testing**: Pytest y testing automatizado
- **CI/CD**: GitHub Actions y workflows
- **Docker**: Contenerización y despliegue
- **Frontend**: HTML, CSS, JavaScript y Bootstrap

**¡Bienvenido al proyecto! 🎉**

Si tienes alguna pregunta o necesitas ayuda, no dudes en:
- Revisar la documentación
- Ejecutar los tests
- Crear un issue en GitHub
- Contactar al equipo de desarrollo
