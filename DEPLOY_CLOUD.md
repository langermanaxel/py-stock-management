# 🚀 Guía de Despliegue en Cloud

## 📋 Resumen

Guía completa para desplegar el Sistema de Gestión de Inventario en plataformas cloud modernas como **Railway**, **Render**, **Heroku** y **DigitalOcean**.

## 🎯 Plataformas Soportadas

### ✅ **Railway** (Recomendado)
- **Ventajas**: Despliegue automático, SSL gratuito, escalabilidad
- **Precio**: $5/mes para proyectos personales
- **URL**: [railway.app](https://railway.app)

### ✅ **Render**
- **Ventajas**: Despliegue automático, SSL gratuito, base de datos PostgreSQL
- **Precio**: Gratis para proyectos personales
- **URL**: [render.com](https://render.com)

### ✅ **Heroku**
- **Ventajas**: Ecosistema maduro, add-ons, escalabilidad
- **Precio**: $7/mes (Eliminado el plan gratuito)
- **URL**: [heroku.com](https://heroku.com)

### ✅ **DigitalOcean App Platform**
- **Ventajas**: Control total, integración con otros servicios DO
- **Precio**: $5/mes
- **URL**: [digitalocean.com](https://digitalocean.com)

## 🐳 Despliegue con Docker

### **1. Preparar la Aplicación**

```bash
# Asegurarse de que todos los archivos estén en el repositorio
git add .
git commit -m "Preparar para despliegue en cloud"
git push origin main
```

### **2. Verificar Archivos de Configuración**

- ✅ `Dockerfile` - Configuración de contenedor
- ✅ `docker-compose.yml` - Servicios de producción
- ✅ `Procfile` - Procesos para Railway/Render
- ✅ `requirements.txt` - Dependencias de Python
- ✅ `.env.example` - Variables de entorno de ejemplo

## 🚂 Despliegue en Railway

### **Paso 1: Crear Cuenta**
1. Ir a [railway.app](https://railway.app)
2. Iniciar sesión con GitHub
3. Crear nuevo proyecto

### **Paso 2: Conectar Repositorio**
1. Seleccionar "Deploy from GitHub repo"
2. Elegir el repositorio `stock_management`
3. Seleccionar la rama `main`

### **Paso 3: Configurar Variables de Entorno**
```bash
# Variables obligatorias
SECRET_KEY=tu-clave-secreta-super-segura-aqui
JWT_SECRET_KEY=tu-clave-jwt-super-segura-aqui
FLASK_ENV=production
DEBUG=false

# Variables de base de datos
SQLALCHEMY_DATABASE_URI=sqlite:///instance/stock_management.db
SQLALCHEMY_TRACK_MODIFICATIONS=false

# Variables JWT
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# Variables de la API
API_TITLE=Stock Management API
API_VERSION=1.0.0
OPENAPI_VERSION=3.0.2

# Variables de logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Variables de CORS
CORS_ORIGINS=https://tu-dominio.railway.app
```

### **Paso 4: Configurar Dominio Personalizado**
1. En la pestaña "Settings" del proyecto
2. Sección "Domains"
3. Agregar dominio personalizado
4. Configurar DNS según las instrucciones

### **Paso 5: Desplegar**
1. Railway detectará automáticamente el `Dockerfile`
2. Construirá la imagen automáticamente
3. Desplegará la aplicación
4. Proporcionará URL de acceso

## 🎨 Despliegue en Render

### **Paso 1: Crear Cuenta**
1. Ir a [render.com](https://render.com)
2. Iniciar sesión con GitHub
3. Crear nueva cuenta

### **Paso 2: Crear Web Service**
1. Click en "New +"
2. Seleccionar "Web Service"
3. Conectar repositorio GitHub

### **Paso 3: Configurar Servicio**
```yaml
# Configuración del servicio
Name: stock-management
Environment: Docker
Region: Frankfurt (EU Central)
Branch: main
Root Directory: ./
Docker Command: python run.py
Docker Context: ./
Dockerfile Path: Dockerfile

# Variables de entorno (Environment Variables)
SECRET_KEY=tu-clave-secreta-super-segura-aqui
JWT_SECRET_KEY=tu-clave-jwt-super-segura-aqui
FLASK_ENV=production
DEBUG=false
SQLALCHEMY_DATABASE_URI=sqlite:///instance/stock_management.db
```

### **Paso 4: Configurar Base de Datos PostgreSQL**
1. Crear "PostgreSQL" service
2. Configurar nombre y región
3. Copiar variables de conexión
4. Actualizar `SQLALCHEMY_DATABASE_URI` en el web service

### **Paso 5: Desplegar**
1. Click en "Create Web Service"
2. Render construirá y desplegará automáticamente
3. Proporcionará URL de acceso

## 🦸 Despliegue en Heroku

### **Paso 1: Instalar Heroku CLI**
```bash
# Windows
winget install --id=Heroku.HerokuCLI

# macOS
brew tap heroku/brew && brew install heroku

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

### **Paso 2: Login y Crear App**
```bash
# Login a Heroku
heroku login

# Crear nueva aplicación
heroku create stock-management-app

# Agregar remote de Heroku
heroku git:remote -a stock-management-app
```

### **Paso 3: Configurar Variables de Entorno**
```bash
# Variables obligatorias
heroku config:set SECRET_KEY="tu-clave-secreta-super-segura-aqui"
heroku config:set JWT_SECRET_KEY="tu-clave-jwt-super-segura-aqui"
heroku config:set FLASK_ENV="production"
heroku config:set DEBUG="false"

# Variables de base de datos
heroku config:set SQLALCHEMY_DATABASE_URI="sqlite:///instance/stock_management.db"
heroku config:set SQLALCHEMY_TRACK_MODIFICATIONS="false"

# Variables JWT
heroku config:set JWT_ACCESS_TOKEN_EXPIRES="3600"
heroku config:set JWT_REFRESH_TOKEN_EXPIRES="86400"
```

### **Paso 4: Desplegar**
```bash
# Desplegar a Heroku
git push heroku main

# Verificar logs
heroku logs --tail

# Abrir aplicación
heroku open
```

## 🐙 Despliegue en DigitalOcean App Platform

### **Paso 1: Crear Cuenta**
1. Ir a [digitalocean.com](https://digitalocean.com)
2. Crear cuenta y verificar email
3. Agregar método de pago

### **Paso 2: Crear App**
1. En el dashboard, click en "Create" → "Apps"
2. Conectar repositorio GitHub
3. Seleccionar rama `main`

### **Paso 3: Configurar App**
```yaml
# Configuración de la app
Name: stock-management
Environment: Docker
Source Directory: ./
Dockerfile Path: Dockerfile

# Variables de entorno
SECRET_KEY: tu-clave-secreta-super-segura-aqui
JWT_SECRET_KEY: tu-clave-jwt-super-segura-aqui
FLASK_ENV: production
DEBUG: false
```

### **Paso 4: Configurar Base de Datos**
1. Agregar "Database" component
2. Seleccionar PostgreSQL
3. Configurar nombre y versión
4. Conectar con la app

### **Paso 5: Desplegar**
1. Click en "Create Resources"
2. DigitalOcean construirá y desplegará
3. Proporcionará URL de acceso

## 🔧 Configuración de Base de Datos

### **SQLite (Desarrollo/Pruebas)**
```python
# app/config.py
SQLALCHEMY_DATABASE_URI = "sqlite:///instance/stock_management.db"
```

### **PostgreSQL (Producción)**
```python
# app/config.py
SQLALCHEMY_DATABASE_URI = os.getenv(
    'DATABASE_URL',
    'postgresql://user:password@localhost/stock_management'
)
```

### **Migración de Base de Datos**
```bash
# Crear migración inicial
flask db init
flask db migrate -m "Initial migration"
flask db upgrade

# En producción
heroku run flask db upgrade  # Heroku
railway run flask db upgrade  # Railway
```

## 🐘 Migración de SQLite a PostgreSQL

### **1. Configurar PostgreSQL**

#### **Variables de Entorno para PostgreSQL**
```bash
# URL de conexión PostgreSQL
DATABASE_URL=postgresql://username:password@host:port/database_name

# Ejemplos por plataforma:
# Railway
DATABASE_URL=postgresql://postgres:password@containers-us-west-1.railway.app:5432/railway

# Render
DATABASE_URL=postgresql://stock_user:password@dpg-abc123-a.frankfurt-postgres.render.com:5432/stock_management

# Heroku
DATABASE_URL=postgresql://user:password@ec2-123-45-67-89.compute-1.amazonaws.com:5432/db123456

# DigitalOcean
DATABASE_URL=postgresql://doadmin:password@db-postgresql-fra1-12345-do-user-67890-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require
```

#### **Configuración en app/config.py**
```python
import os
from urllib.parse import urlparse

def get_database_uri():
    """Obtiene la URI de base de datos según el entorno"""
    if os.getenv('DATABASE_URL'):
        # Parsear URL de PostgreSQL (Heroku, Railway, etc.)
        url = urlparse(os.getenv('DATABASE_URL'))
        return f"postgresql://{url.username}:{url.password}@{url.hostname}:{url.port}{url.path}"
    else:
        # Fallback a SQLite para desarrollo
        return "sqlite:///instance/stock_management.db"

# Configuración de base de datos
SQLALCHEMY_DATABASE_URI = get_database_uri()
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Configuración específica para PostgreSQL
if 'postgresql' in SQLALCHEMY_DATABASE_URI:
    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': 10,
        'pool_timeout': 20,
        'pool_recycle': -1,
        'max_overflow': 0
    }
```

### **2. Instalar Dependencias PostgreSQL**

#### **requirements.txt**
```txt
# Agregar estas dependencias para PostgreSQL
psycopg2-binary==2.9.9  # Driver PostgreSQL para Python
# O alternativamente:
# psycopg2==2.9.9  # Si psycopg2-binary no funciona
```

#### **Instalación**
```bash
# Instalar dependencias
pip install psycopg2-binary

# O si hay problemas con psycopg2-binary
pip install psycopg2

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### **3. Migración de Datos**

#### **Script de Migración SQLite → PostgreSQL**
```python
# migrate_to_postgresql.py
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime

def migrate_sqlite_to_postgresql():
    """Migra datos de SQLite a PostgreSQL"""
    
    # Conectar a SQLite
    sqlite_conn = sqlite3.connect('instance/stock_management.db')
    sqlite_cursor = sqlite_conn.cursor()
    
    # Conectar a PostgreSQL
    pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    pg_cursor = pg_conn.cursor()
    
    try:
        # Migrar categorías
        print("Migrando categorías...")
        sqlite_cursor.execute("SELECT * FROM categories")
        categories = sqlite_cursor.fetchall()
        
        for category in categories:
            pg_cursor.execute("""
                INSERT INTO categories (id, name, description, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, category)
        
        # Migrar productos
        print("Migrando productos...")
        sqlite_cursor.execute("SELECT * FROM products")
        products = sqlite_cursor.fetchall()
        
        for product in products:
            pg_cursor.execute("""
                INSERT INTO products (id, name, description, price, category_id, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, product)
        
        # Migrar stock
        print("Migrando stock...")
        sqlite_cursor.execute("SELECT * FROM stock")
        stock_items = sqlite_cursor.fetchall()
        
        for stock in stock_items:
            pg_cursor.execute("""
                INSERT INTO stock (id, product_id, quantity, min_stock, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, stock)
        
        # Migrar usuarios
        print("Migrando usuarios...")
        sqlite_cursor.execute("SELECT * FROM users")
        users = sqlite_cursor.fetchall()
        
        for user in users:
            pg_cursor.execute("""
                INSERT INTO users (id, username, email, password_hash, first_name, last_name, role, is_active, last_login, created_at, updated_at)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (id) DO NOTHING
            """, user)
        
        # Commit cambios
        pg_conn.commit()
        print("Migración completada exitosamente!")
        
    except Exception as e:
        pg_conn.rollback()
        print(f"Error durante la migración: {e}")
        raise
    finally:
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()

if __name__ == "__main__":
    migrate_sqlite_to_postgresql()
```

#### **Ejecutar Migración**
```bash
# Configurar variables de entorno
export DATABASE_URL="postgresql://user:password@localhost:5432/stock_management"

# Ejecutar migración
python migrate_to_postgresql.py

# Verificar datos migrados
python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM products')
print(f'Productos migrados: {cur.fetchone()[0]}')
conn.close()
"
```

### **4. Configuración de Docker para PostgreSQL**

#### **docker-compose.postgresql.yml**
```yaml
version: '3.8'

services:
  web:
    build: .
    container_name: stock_management_web
    ports:
      - "5000:5000"
    environment:
      - DATABASE_URL=postgresql://stock_user:stock_password@postgres:5432/stock_management
      - FLASK_ENV=production
      - DEBUG=false
    depends_on:
      - postgres
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped

  postgres:
    image: postgres:15-alpine
    container_name: stock_management_db
    environment:
      - POSTGRES_DB=stock_management
      - POSTGRES_USER=stock_user
      - POSTGRES_PASSWORD=stock_password
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U stock_user -d stock_management"]
      interval: 10s
      timeout: 5s
      retries: 5

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: stock_management_pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@stockmanagement.com
      - PGADMIN_DEFAULT_PASSWORD=admin123
    ports:
      - "8080:80"
    depends_on:
      - postgres
    restart: unless-stopped

volumes:
  postgres_data:
    driver: local

networks:
  default:
    name: stock_management_network
```

#### **Script de Inicialización PostgreSQL**
```sql
-- init.sql
-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";

-- Configurar timezone
SET timezone = 'UTC';

-- Crear índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_stock_product_id ON stock(product_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
```

### **5. Migración con Flask-Migrate**

#### **Configurar Flask-Migrate**
```python
# app/__init__.py
from flask_migrate import Migrate

# ... código existente ...

migrate = Migrate()

def create_app():
    app = Flask(__name__)
    # ... configuración existente ...
    
    # Inicializar Flask-Migrate
    migrate.init_app(app, db)
    
    return app
```

#### **Comandos de Migración**
```bash
# Inicializar migraciones (solo la primera vez)
flask db init

# Crear migración inicial
flask db migrate -m "Initial migration"

# Aplicar migración
flask db upgrade

# Ver historial de migraciones
flask db history

# Revertir última migración
flask db downgrade

# Ver estado actual
flask db current
```

#### **Migración Automática en Producción**
```bash
# Heroku
heroku run flask db upgrade

# Railway
railway run flask db upgrade

# Render
render exec flask db upgrade

# DigitalOcean
doctl apps run --app-id 12345 --command "flask db upgrade"
```

### **6. Verificación y Testing**

#### **Script de Verificación**
```python
# verify_migration.py
import psycopg2
import sqlite3
import os

def verify_migration():
    """Verifica que la migración se completó correctamente"""
    
    # Conectar a ambas bases de datos
    sqlite_conn = sqlite3.connect('instance/stock_management.db')
    pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    tables = ['categories', 'products', 'stock', 'users']
    
    for table in tables:
        print(f"\nVerificando tabla: {table}")
        
        # Contar registros en SQLite
        sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        sqlite_count = sqlite_cursor.fetchone()[0]
        
        # Contar registros en PostgreSQL
        pg_cursor.execute(f"SELECT COUNT(*) FROM {table}")
        pg_count = pg_cursor.fetchone()[0]
        
        print(f"  SQLite: {sqlite_count} registros")
        print(f"  PostgreSQL: {pg_count} registros")
        print(f"  Estado: {'✅ OK' if sqlite_count == pg_count else '❌ ERROR'}")
    
    sqlite_cursor.close()
    sqlite_conn.close()
    pg_cursor.close()
    pg_conn.close()

if __name__ == "__main__":
    verify_migration()
```

### **7. Rollback a SQLite (si es necesario)**

#### **Script de Rollback**
```python
# rollback_to_sqlite.py
import sqlite3
import psycopg2
import os

def rollback_to_sqlite():
    """Revierte la migración volviendo a SQLite"""
    
    print("⚠️  ADVERTENCIA: Esto eliminará la base de datos PostgreSQL")
    confirm = input("¿Estás seguro? (escribe 'SI' para confirmar): ")
    
    if confirm != 'SI':
        print("Rollback cancelado")
        return
    
    # Restaurar configuración a SQLite
    os.environ.pop('DATABASE_URL', None)
    
    # Recrear base de datos SQLite
    from app import create_app, db
    app = create_app()
    
    with app.app_context():
        db.drop_all()
        db.create_all()
        print("Base de datos SQLite recreada")
    
    print("Rollback completado. La aplicación ahora usa SQLite")

if __name__ == "__main__":
    rollback_to_sqlite()
```

## 🔐 Configuración de Seguridad

### **Variables de Entorno Críticas**
```bash
# NUNCA committear estas variables
SECRET_KEY=clave-super-secreta-para-flask
JWT_SECRET_KEY=clave-super-secreta-para-jwt
DATABASE_URL=url-de-conexion-a-base-de-datos
```

### **Generar Claves Seguras**
```python
# Generar claves seguras
import secrets
import string

def generate_secret_key(length=64):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))

# Generar claves
print(f"SECRET_KEY={generate_secret_key()}")
print(f"JWT_SECRET_KEY={generate_secret_key()}")
```

### **Configuración de CORS**
```python
# app/config.py
CORS_ORIGINS = os.getenv('CORS_ORIGINS', 'http://localhost:5000').split(',')
```

## 📊 Monitoreo y Logs

### **Health Check Endpoint**
```python
# app/routes/frontend.py
@app.route('/health')
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    })
```

### **Logging Configurado**
```python
# app/config.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    if not os.path.exists('logs'):
        os.mkdir('logs')
    file_handler = RotatingFileHandler('logs/app.log', maxBytes=10240, backupCount=10)
    file_handler.setFormatter(logging.Formatter(
        '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
    ))
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)
    app.logger.info('Stock Management startup')
```

## 🚀 Automatización de Despliegue

### **GitHub Actions para Despliegue Automático**
```yaml
# .github/workflows/deploy.yml
name: Deploy to Cloud

on:
  push:
    branches: [ main ]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@v1.0.0
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: ${{ secrets.RAILWAY_SERVICE }}
```

### **Configurar Secrets en GitHub**
1. Ir a Settings → Secrets and variables → Actions
2. Agregar `RAILWAY_TOKEN` y `RAILWAY_SERVICE`
3. Obtener token desde Railway dashboard

## 🔍 Troubleshooting Común

### **Error: "No module named 'flask'**
```bash
# Solución: Verificar requirements.txt
pip install -r requirements.txt

# En Docker
docker build --no-cache .
```

### **Error: "Database connection failed"**
```bash
# Verificar variables de entorno
echo $DATABASE_URL

# Verificar conectividad
ping tu-servidor-db.com
```

### **Error: "Port already in use"**
```bash
# Cambiar puerto en configuración
export PORT=8000
# O en docker-compose.yml
ports:
  - "8000:5000"
```

### **Error: "Permission denied"**
```bash
# En Docker, verificar usuario
USER appuser

# En cloud, verificar permisos de archivos
chmod +x run.py
```

## 📈 Escalabilidad y Performance

### **Configuración de Workers**
```python
# gunicorn.conf.py
bind = "0.0.0.0:5000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 50
timeout = 30
keepalive = 2
```

### **Cache con Redis**
```python
# app/extensions.py
from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'redis',
    'CACHE_REDIS_URL': os.getenv('REDIS_URL')
})
```

### **Load Balancer**
```nginx
# nginx.conf
upstream stock_management {
    server 127.0.0.1:5000;
    server 127.0.0.1:5001;
    server 127.0.0.1:5002;
}

server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://stock_management;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 💰 Costos Estimados

### **Railway**
- **Plan Personal**: $5/mes
- **Plan Pro**: $20/mes
- **Base de datos**: $5/mes adicional

### **Render**
- **Plan Gratuito**: $0/mes (con limitaciones)
- **Plan Personal**: $7/mes
- **PostgreSQL**: $7/mes

### **Heroku**
- **Plan Basic**: $7/mes
- **PostgreSQL**: $5/mes
- **Redis**: $15/mes

### **DigitalOcean**
- **App Platform**: $5/mes
- **PostgreSQL**: $15/mes
- **Load Balancer**: $12/mes

## 🎯 Recomendaciones por Caso de Uso

### **Proyecto Personal/Portfolio**
- **Recomendado**: Render (gratis) o Railway ($5/mes)
- **Razón**: Fácil de usar, bueno para aprender

### **Proyecto de Cliente**
- **Recomendado**: Railway o DigitalOcean
- **Razón**: Profesional, escalable, soporte

### **Aplicación Empresarial**
- **Recomendado**: DigitalOcean o AWS
- **Razón**: Control total, compliance, seguridad

## 📚 Recursos Adicionales

### **Documentación Oficial**
- [Railway Docs](https://docs.railway.app/)
- [Render Docs](https://render.com/docs)
- [Heroku Docs](https://devcenter.heroku.com/)
- [DigitalOcean Docs](https://docs.digitalocean.com/)

### **Tutoriales y Ejemplos**
- [Deploy Flask to Railway](https://railway.app/docs/tutorials/deploy-flask)
- [Deploy Python to Render](https://render.com/docs/deploy-python)
- [Deploy Python to Heroku](https://devcenter.heroku.com/articles/python)

### **Comunidad y Soporte**
- [Railway Discord](https://discord.gg/railway)
- [Render Community](https://community.render.com/)
- [Heroku Community](https://help.heroku.com/)

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0.0  
**Autor**: Sistema de Gestión de Inventario  
**Compatibilidad**: Railway, Render, Heroku, DigitalOcean
