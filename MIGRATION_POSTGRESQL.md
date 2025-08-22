# 🐘 Migración de SQLite a PostgreSQL

## 📋 Resumen

Guía completa para migrar el Sistema de Gestión de Inventario de **SQLite** (desarrollo) a **PostgreSQL** (producción), incluyendo configuración, migración de datos, y despliegue en diferentes plataformas cloud.

## 🎯 ¿Por qué Migrar a PostgreSQL?

### **SQLite (Desarrollo)**
- ✅ **Fácil de usar**: No requiere servidor separado
- ✅ **Portable**: Base de datos en un solo archivo
- ✅ **Rápido**: Para aplicaciones pequeñas y medianas
- ❌ **Limitaciones**: Concurrencia limitada, no escalable
- ❌ **Sin red**: No accesible desde múltiples servidores

### **PostgreSQL (Producción)**
- ✅ **Escalable**: Maneja múltiples conexiones simultáneas
- ✅ **Robusto**: ACID compliance, transacciones complejas
- ✅ **Funcionalidades avanzadas**: JSON, full-text search, GIS
- ✅ **Performance**: Optimizado para cargas de trabajo grandes
- ✅ **Cloud-ready**: Integración nativa con servicios cloud

## 🚀 **Paso 1: Preparar el Entorno**

### **Instalar Dependencias PostgreSQL**

```bash
# Instalar driver PostgreSQL
pip install psycopg2-binary==2.9.9

# Alternativa si psycopg2-binary no funciona
pip install psycopg2==2.9.9

# Actualizar requirements.txt
pip freeze > requirements.txt
```

### **Verificar Instalación**

```python
# test_postgresql.py
import psycopg2

try:
    # Intentar importar psycopg2
    print("✅ psycopg2 instalado correctamente")
    
    # Verificar versión
    print(f"Versión: {psycopg2.__version__}")
    
except ImportError as e:
    print(f"❌ Error al importar psycopg2: {e}")
    print("💡 Intenta: pip install psycopg2-binary")
```

## 🔧 **Paso 2: Configurar Conexión a PostgreSQL**

### **Variables de Entorno**

```bash
# .env
# Configuración para desarrollo local
DATABASE_URL=postgresql://stock_user:stock_password@localhost:5432/stock_management

# Configuración para producción (ejemplos)
# Railway
# DATABASE_URL=postgresql://postgres:password@containers-us-west-1.railway.app:5432/railway

# Render
# DATABASE_URL=postgresql://stock_user:password@dpg-abc123-a.frankfurt-postgres.render.com:5432/stock_management

# Heroku
# DATABASE_URL=postgresql://user:password@ec2-123-45-67-89.compute-1.amazonaws.com:5432/db123456

# DigitalOcean
# DATABASE_URL=postgresql://doadmin:password@db-postgresql-fra1-12345-do-user-67890-0.db.ondigitalocean.com:25060/defaultdb?sslmode=require
```

### **Configuración en app/config.py**

```python
# app/config.py
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
        'pool_size': 10,           # Conexiones en el pool
        'pool_timeout': 20,        # Timeout para obtener conexión
        'pool_recycle': -1,        # No reciclar conexiones
        'max_overflow': 0,         # No permitir overflow
        'echo': False,             # No mostrar SQL en logs
        'echo_pool': False         # No mostrar info del pool
    }
    
    # Configuración adicional para producción
    if os.getenv('FLASK_ENV') == 'production':
        SQLALCHEMY_ENGINE_OPTIONS.update({
            'pool_pre_ping': True,     # Verificar conexiones antes de usar
            'pool_reset_on_return': 'commit'  # Reset al devolver conexión
        })
```

## 🐳 **Paso 3: Configurar PostgreSQL con Docker**

### **docker-compose.postgresql.yml**

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
      - SECRET_KEY=your-secret-key-here
      - JWT_SECRET_KEY=your-jwt-secret-key-here
    depends_on:
      postgres:
        condition: service_healthy
    volumes:
      - ./logs:/app/logs
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s

  postgres:
    image: postgres:15-alpine
    container_name: stock_management_db
    environment:
      - POSTGRES_DB=stock_management
      - POSTGRES_USER=stock_user
      - POSTGRES_PASSWORD=stock_password
      - POSTGRES_INITDB_ARGS=--encoding=UTF-8 --lc-collate=C --lc-ctype=C
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./init.sql:/docker-entrypoint-initdb.d/init.sql
      - ./backups:/backups
    ports:
      - "5432:5432"
    restart: unless-stopped
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U stock_user -d stock_management"]
      interval: 10s
      timeout: 5s
      retries: 5
      start_period: 30s
    command: >
      postgres
      -c shared_preload_libraries=pg_stat_statements
      -c pg_stat_statements.track=all
      -c max_connections=100
      -c shared_buffers=256MB
      -c effective_cache_size=1GB
      -c maintenance_work_mem=64MB
      -c checkpoint_completion_target=0.9
      -c wal_buffers=16MB
      -c default_statistics_target=100
      -c random_page_cost=1.1
      -c effective_io_concurrency=200
      -c work_mem=4MB
      -c min_wal_size=1GB
      -c max_wal_size=4GB

  pgadmin:
    image: dpage/pgadmin4:latest
    container_name: stock_management_pgadmin
    environment:
      - PGADMIN_DEFAULT_EMAIL=admin@stockmanagement.com
      - PGADMIN_DEFAULT_PASSWORD=admin123
      - PGADMIN_CONFIG_SERVER_MODE=False
      - PGADMIN_CONFIG_MASTER_PASSWORD_REQUIRED=False
    ports:
      - "8080:80"
    depends_on:
      - postgres
    restart: unless-stopped
    volumes:
      - pgadmin_data:/var/lib/pgadmin

volumes:
  postgres_data:
    driver: local
  pgadmin_data:
    driver: local

networks:
  default:
    name: stock_management_network
```

### **Script de Inicialización PostgreSQL**

```sql
-- init.sql
-- Crear extensiones útiles
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";
CREATE EXTENSION IF NOT EXISTS "pg_stat_statements";

-- Configurar timezone
SET timezone = 'UTC';

-- Crear índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_products_category_id ON products(category_id);
CREATE INDEX IF NOT EXISTS idx_stock_product_id ON stock(product_id);
CREATE INDEX IF NOT EXISTS idx_users_username ON users(username);
CREATE INDEX IF NOT EXISTS idx_users_email ON users(email);
CREATE INDEX IF NOT EXISTS idx_orders_created_at ON orders(created_at);
CREATE INDEX IF NOT EXISTS idx_purchase_orders_created_at ON purchase_orders(created_at);

-- Crear índices para búsquedas de texto
CREATE INDEX IF NOT EXISTS idx_products_name_gin ON products USING gin(to_tsvector('english', name));
CREATE INDEX IF NOT EXISTS idx_products_description_gin ON products USING gin(to_tsvector('english', description));

-- Configurar estadísticas
ALTER TABLE products ALTER COLUMN price SET STATISTICS 1000;
ALTER TABLE stock ALTER COLUMN quantity SET STATISTICS 1000;

-- Crear vistas útiles
CREATE OR REPLACE VIEW low_stock_products AS
SELECT 
    p.name as product_name,
    p.description,
    s.quantity,
    s.min_stock,
    c.name as category_name
FROM stock s
JOIN products p ON s.product_id = p.id
JOIN categories c ON p.category_id = c.id
WHERE s.quantity <= s.min_stock;

-- Crear función para actualizar timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ language 'plpgsql';

-- Aplicar trigger a todas las tablas con updated_at
DO $$
DECLARE
    t text;
BEGIN
    FOR t IN 
        SELECT table_name 
        FROM information_schema.columns 
        WHERE column_name = 'updated_at' 
        AND table_schema = 'public'
    LOOP
        EXECUTE format('
            CREATE TRIGGER update_updated_at_%I 
            BEFORE UPDATE ON %I 
            FOR EACH ROW EXECUTE FUNCTION update_updated_at_column()
        ', t, t);
    END LOOP;
END;
$$ LANGUAGE plpgsql;
```

## 📊 **Paso 4: Migración de Datos**

### **Script de Migración SQLite → PostgreSQL**

```python
# migrate_to_postgresql.py
import sqlite3
import psycopg2
from psycopg2.extras import RealDictCursor
import os
from datetime import datetime
import sys

def get_sqlite_connection():
    """Conecta a la base de datos SQLite"""
    try:
        conn = sqlite3.connect('instance/stock_management.db')
        conn.row_factory = sqlite3.Row  # Para acceso por nombre de columna
        return conn
    except Exception as e:
        print(f"❌ Error conectando a SQLite: {e}")
        sys.exit(1)

def get_postgresql_connection():
    """Conecta a la base de datos PostgreSQL"""
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        return conn
    except Exception as e:
        print(f"❌ Error conectando a PostgreSQL: {e}")
        print("💡 Verifica que DATABASE_URL esté configurado correctamente")
        sys.exit(1)

def migrate_table(sqlite_cursor, pg_cursor, table_name, columns, data):
    """Migra una tabla específica"""
    print(f"  Migrando {len(data)} registros...")
    
    if not data:
        print(f"  ✅ Tabla {table_name} está vacía")
        return 0
    
    try:
        # Crear placeholders para la consulta INSERT
        placeholders = ', '.join(['%s'] * len(columns))
        columns_str = ', '.join(columns)
        
        # Insertar datos
        for row in data:
            pg_cursor.execute(f"""
                INSERT INTO {table_name} ({columns_str})
                VALUES ({placeholders})
                ON CONFLICT (id) DO NOTHING
            """, row)
        
        return len(data)
        
    except Exception as e:
        print(f"  ❌ Error migrando tabla {table_name}: {e}")
        raise

def migrate_sqlite_to_postgresql():
    """Migra datos de SQLite a PostgreSQL"""
    
    print("🚀 Iniciando migración de SQLite a PostgreSQL...")
    
    # Conectar a ambas bases de datos
    sqlite_conn = get_sqlite_connection()
    pg_conn = get_postgresql_connection()
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    # Definir tablas y columnas a migrar
    tables_config = {
        'categories': ['id', 'name', 'description', 'created_at', 'updated_at'],
        'products': ['id', 'name', 'description', 'price', 'category_id', 'created_at', 'updated_at'],
        'stock': ['id', 'product_id', 'quantity', 'min_stock', 'created_at', 'updated_at'],
        'users': ['id', 'username', 'email', 'password_hash', 'first_name', 'last_name', 'role', 'is_active', 'last_login', 'created_at', 'updated_at'],
        'orders': ['id', 'user_id', 'status', 'total', 'created_at', 'updated_at'],
        'order_items': ['id', 'order_id', 'product_id', 'quantity', 'unit_price', 'created_at', 'updated_at'],
        'purchase_orders': ['id', 'user_id', 'status', 'total', 'created_at', 'updated_at'],
        'purchase_order_items': ['id', 'purchase_order_id', 'product_id', 'quantity', 'unit_price', 'created_at', 'updated_at']
    }
    
    total_migrated = 0
    
    try:
        # Iniciar transacción
        pg_cursor.execute("BEGIN")
        
        for table_name, columns in tables_config.items():
            print(f"\n📋 Migrando tabla: {table_name}")
            
            try:
                # Obtener datos de SQLite
                sqlite_cursor.execute(f"SELECT {', '.join(columns)} FROM {table_name}")
                data = sqlite_cursor.fetchall()
                
                # Migrar tabla
                migrated_count = migrate_table(sqlite_cursor, pg_cursor, table_name, columns, data)
                total_migrated += migrated_count
                
                print(f"  ✅ {table_name}: {migrated_count} registros migrados")
                
            except Exception as e:
                print(f"  ❌ Error en tabla {table_name}: {e}")
                raise
        
        # Commit transacción
        pg_conn.commit()
        print(f"\n🎉 Migración completada exitosamente!")
        print(f"📊 Total de registros migrados: {total_migrated}")
        
    except Exception as e:
        # Rollback en caso de error
        pg_conn.rollback()
        print(f"\n❌ Error durante la migración: {e}")
        raise
    finally:
        # Cerrar conexiones
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()

def verify_migration():
    """Verifica que la migración se completó correctamente"""
    
    print("\n🔍 Verificando migración...")
    
    # Conectar a ambas bases de datos
    sqlite_conn = get_sqlite_connection()
    pg_conn = get_postgresql_connection()
    
    sqlite_cursor = sqlite_conn.cursor()
    pg_cursor = pg_conn.cursor()
    
    tables = ['categories', 'products', 'stock', 'users', 'orders', 'order_items', 'purchase_orders', 'purchase_order_items']
    
    all_ok = True
    
    for table in tables:
        try:
            # Contar registros en SQLite
            sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            sqlite_count = sqlite_cursor.fetchone()[0]
            
            # Contar registros en PostgreSQL
            pg_cursor.execute(f"SELECT COUNT(*) FROM {table}")
            pg_count = pg_cursor.fetchone()[0]
            
            status = "✅ OK" if sqlite_count == pg_count else "❌ ERROR"
            if sqlite_count != pg_count:
                all_ok = False
            
            print(f"  {table}: SQLite={sqlite_count}, PostgreSQL={pg_count} - {status}")
            
        except Exception as e:
            print(f"  {table}: ❌ Error - {e}")
            all_ok = False
    
    sqlite_cursor.close()
    sqlite_conn.close()
    pg_cursor.close()
    pg_conn.close()
    
    if all_ok:
        print("\n🎉 Verificación completada: TODAS las tablas están correctas")
    else:
        print("\n⚠️  Verificación completada: Hay problemas en algunas tablas")
    
    return all_ok

if __name__ == "__main__":
    try:
        # Ejecutar migración
        migrate_sqlite_to_postgresql()
        
        # Verificar migración
        verify_migration()
        
    except Exception as e:
        print(f"\n💥 Migración falló: {e}")
        sys.exit(1)
```

### **Ejecutar Migración**

```bash
# 1. Configurar variables de entorno
export DATABASE_URL="postgresql://stock_user:stock_password@localhost:5432/stock_management"

# 2. Verificar conexión a PostgreSQL
python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
print('✅ Conexión a PostgreSQL exitosa')
conn.close()
"

# 3. Ejecutar migración
python migrate_to_postgresql.py

# 4. Verificar datos migrados
python -c "
import psycopg2
conn = psycopg2.connect('$DATABASE_URL')
cur = conn.cursor()
cur.execute('SELECT COUNT(*) FROM products')
print(f'Productos migrados: {cur.fetchone()[0]}')
conn.close()
"
```

## 🔄 **Paso 5: Configurar Flask-Migrate**

### **Instalar Flask-Migrate**

```bash
pip install Flask-Migrate==4.0.5
pip freeze > requirements.txt
```

### **Configurar en app/__init__.py**

```python
# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

def create_app():
    app = Flask(__name__)
    
    # Configuración
    app.config.from_object('app.config.Config')
    
    # Inicializar extensiones
    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    CORS(app)
    
    # Registrar blueprints
    from app.routes import frontend_bp
    from app.api import api_bp
    
    app.register_blueprint(frontend_bp)
    app.register_blueprint(api_bp, url_prefix='/api')
    
    return app
```

### **Comandos de Migración**

```bash
# 1. Inicializar migraciones (solo la primera vez)
flask db init

# 2. Crear migración inicial
flask db migrate -m "Initial migration"

# 3. Aplicar migración
flask db upgrade

# 4. Ver historial de migraciones
flask db history

# 5. Ver estado actual
flask db current

# 6. Revertir última migración
flask db downgrade

# 7. Crear nueva migración después de cambios
flask db migrate -m "Add new field to products"

# 8. Aplicar nueva migración
flask db upgrade
```

## 🚀 **Paso 6: Despliegue en Producción**

### **Migración Automática en Diferentes Plataformas**

#### **Railway**
```bash
# Configurar variable de entorno DATABASE_URL en Railway dashboard
# Luego ejecutar:
railway run flask db upgrade
```

#### **Render**
```bash
# Configurar variable de entorno DATABASE_URL en Render dashboard
# Luego ejecutar:
render exec flask db upgrade
```

#### **Heroku**
```bash
# Configurar variable de entorno DATABASE_URL en Heroku dashboard
# Luego ejecutar:
heroku run flask db upgrade
```

#### **DigitalOcean**
```bash
# Configurar variable de entorno DATABASE_URL en DigitalOcean dashboard
# Luego ejecutar:
doctl apps run --app-id 12345 --command "flask db upgrade"
```

### **GitHub Actions para Migración Automática**

```yaml
# .github/workflows/deploy.yml
name: Deploy and Migrate

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
      
      - name: Wait for deployment
        run: sleep 30
      
      - name: Run database migration
        run: |
          curl -X POST \
            -H "Authorization: Bearer ${{ secrets.RAILWAY_TOKEN }}" \
            -H "Content-Type: application/json" \
            -d '{"command": "flask db upgrade"}' \
            "https://backboard.railway.app/gui/v1/services/${{ secrets.RAILWAY_SERVICE }}/exec"
```

## 🔍 **Paso 7: Verificación y Testing**

### **Script de Verificación Completa**

```python
# verify_postgresql_migration.py
import psycopg2
import sqlite3
import os
import sys
from datetime import datetime

def verify_migration():
    """Verifica que la migración se completó correctamente"""
    
    print("🔍 Verificando migración de SQLite a PostgreSQL...")
    
    # Verificar que DATABASE_URL esté configurado
    if not os.getenv('DATABASE_URL'):
        print("❌ DATABASE_URL no está configurado")
        return False
    
    try:
        # Conectar a ambas bases de datos
        sqlite_conn = sqlite3.connect('instance/stock_management.db')
        pg_conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        
        sqlite_cursor = sqlite_conn.cursor()
        pg_cursor = pg_conn.cursor()
        
        tables = [
            'categories', 'products', 'stock', 'users', 
            'orders', 'order_items', 'purchase_orders', 'purchase_order_items'
        ]
        
        all_ok = True
        total_sqlite = 0
        total_pg = 0
        
        print(f"\n{'Tabla':<25} {'SQLite':<10} {'PostgreSQL':<12} {'Estado':<10}")
        print("-" * 60)
        
        for table in tables:
            try:
                # Contar registros en SQLite
                sqlite_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                sqlite_count = sqlite_cursor.fetchone()[0]
                
                # Contar registros en PostgreSQL
                pg_cursor.execute(f"SELECT COUNT(*) FROM {table}")
                pg_count = pg_cursor.fetchone()[0]
                
                total_sqlite += sqlite_count
                total_pg += pg_count
                
                # Verificar estado
                if sqlite_count == pg_count:
                    status = "✅ OK"
                else:
                    status = "❌ ERROR"
                    all_ok = False
                
                print(f"{table:<25} {sqlite_count:<10} {pg_count:<12} {status:<10}")
                
            except Exception as e:
                print(f"{table:<25} {'ERROR':<10} {'ERROR':<12} ❌ {str(e)[:20]}")
                all_ok = False
        
        print("-" * 60)
        print(f"{'TOTAL':<25} {total_sqlite:<10} {total_pg:<12} {'✅ OK' if all_ok else '❌ ERROR':<10}")
        
        # Verificar integridad referencial
        print(f"\n🔗 Verificando integridad referencial...")
        
        try:
            # Verificar foreign keys
            pg_cursor.execute("""
                SELECT 
                    tc.table_name, 
                    kcu.column_name, 
                    ccu.table_name AS foreign_table_name,
                    ccu.column_name AS foreign_column_name 
                FROM 
                    information_schema.table_constraints AS tc 
                    JOIN information_schema.key_column_usage AS kcu
                      ON tc.constraint_name = kcu.constraint_name
                      AND tc.table_schema = kcu.table_schema
                    JOIN information_schema.constraint_column_usage AS ccu
                      ON ccu.constraint_name = tc.constraint_name
                      AND ccu.table_schema = tc.table_schema
                WHERE tc.constraint_type = 'FOREIGN KEY'
                ORDER BY tc.table_name, kcu.column_name;
            """)
            
            foreign_keys = pg_cursor.fetchall()
            print(f"  ✅ {len(foreign_keys)} foreign keys encontradas")
            
        except Exception as e:
            print(f"  ❌ Error verificando foreign keys: {e}")
            all_ok = False
        
        # Verificar índices
        print(f"\n📊 Verificando índices...")
        
        try:
            pg_cursor.execute("""
                SELECT 
                    schemaname,
                    tablename,
                    indexname,
                    indexdef
                FROM pg_indexes
                WHERE schemaname = 'public'
                ORDER BY tablename, indexname;
            """)
            
            indexes = pg_cursor.fetchall()
            print(f"  ✅ {len(indexes)} índices encontrados")
            
        except Exception as e:
            print(f"  ❌ Error verificando índices: {e}")
            all_ok = False
        
        sqlite_cursor.close()
        sqlite_conn.close()
        pg_cursor.close()
        pg_conn.close()
        
        if all_ok:
            print(f"\n🎉 Verificación completada: TODAS las tablas están correctas")
            print(f"📊 Total de registros: {total_pg}")
        else:
            print(f"\n⚠️  Verificación completada: Hay problemas en algunas tablas")
        
        return all_ok
        
    except Exception as e:
        print(f"❌ Error durante la verificación: {e}")
        return False

def test_postgresql_connection():
    """Prueba la conexión a PostgreSQL"""
    
    print("🔌 Probando conexión a PostgreSQL...")
    
    try:
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        
        # Prueba básica
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"  ✅ Conexión exitosa")
        print(f"  📊 Versión: {version.split(',')[0]}")
        
        # Prueba de consulta
        cursor.execute("SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public'")
        table_count = cursor.fetchone()[0]
        print(f"  📋 Tablas encontradas: {table_count}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error de conexión: {e}")
        return False

if __name__ == "__main__":
    print("🚀 Verificador de Migración PostgreSQL")
    print("=" * 50)
    
    # Probar conexión
    if not test_postgresql_connection():
        sys.exit(1)
    
    # Verificar migración
    if verify_migration():
        print("\n🎉 Migración verificada exitosamente!")
        sys.exit(0)
    else:
        print("\n💥 Hay problemas con la migración")
        sys.exit(1)
```

## 🔄 **Paso 8: Rollback (si es necesario)**

### **Script de Rollback a SQLite**

```python
# rollback_to_sqlite.py
import os
import sys
import shutil
from datetime import datetime

def rollback_to_sqlite():
    """Revierte la migración volviendo a SQLite"""
    
    print("⚠️  ADVERTENCIA: Esto eliminará la configuración de PostgreSQL")
    print("⚠️  La aplicación volverá a usar SQLite")
    print("⚠️  Los datos en PostgreSQL NO se eliminan, solo la configuración")
    
    confirm = input("\n¿Estás seguro? (escribe 'SI' para confirmar): ")
    
    if confirm != 'SI':
        print("Rollback cancelado")
        return
    
    try:
        # Hacer backup de la configuración actual
        backup_dir = f"backup_config_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        os.makedirs(backup_dir, exist_ok=True)
        
        # Backup de archivos de configuración
        config_files = ['.env', 'app/config.py']
        for file in config_files:
            if os.path.exists(file):
                shutil.copy2(file, backup_dir)
                print(f"  📁 Backup de {file} creado")
        
        # Restaurar configuración a SQLite
        print("\n🔄 Restaurando configuración a SQLite...")
        
        # Eliminar DATABASE_URL del entorno
        if 'DATABASE_URL' in os.environ:
            del os.environ['DATABASE_URL']
            print("  ✅ Variable DATABASE_URL eliminada del entorno")
        
        # Crear .env con configuración SQLite
        env_content = """# Configuración para SQLite (desarrollo)
FLASK_APP=run.py
FLASK_ENV=development
DEBUG=true
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-change-in-production
SQLALCHEMY_TRACK_MODIFICATIONS=true
LOG_LEVEL=DEBUG
"""
        
        with open('.env', 'w') as f:
            f.write(env_content)
        print("  ✅ Archivo .env recreado para SQLite")
        
        # Recrear base de datos SQLite
        print("\n🗄️  Recreando base de datos SQLite...")
        
        try:
            from app import create_app, db
            app = create_app()
            
            with app.app_context():
                db.drop_all()
                db.create_all()
                print("  ✅ Base de datos SQLite recreada")
                
        except Exception as e:
            print(f"  ⚠️  Error recreando base de datos: {e}")
            print("  💡 Puedes recrear manualmente ejecutando: python -c 'from app import create_app, db; app = create_app(); app.app_context().push(); db.create_all()'")
        
        print(f"\n🎉 Rollback completado exitosamente!")
        print(f"📁 Backup de configuración guardado en: {backup_dir}")
        print(f"🔄 La aplicación ahora usa SQLite")
        print(f"💡 Para volver a PostgreSQL, configura DATABASE_URL y ejecuta la migración")
        
    except Exception as e:
        print(f"❌ Error durante el rollback: {e}")
        raise

if __name__ == "__main__":
    rollback_to_sqlite()
```

## 📚 **Recursos Adicionales**

### **Documentación Oficial**
- [PostgreSQL Documentation](https://www.postgresql.org/docs/)
- [psycopg2 Documentation](https://www.psycopg.org/docs/)
- [Flask-Migrate Documentation](https://flask-migrate.readthedocs.io/)

### **Herramientas Útiles**
- [pgAdmin](https://www.pgadmin.org/) - Interfaz gráfica para PostgreSQL
- [DBeaver](https://dbeaver.io/) - Cliente universal de base de datos
- [PostgreSQL.app](https://postgresapp.com/) - PostgreSQL para macOS

### **Comandos Útiles de PostgreSQL**
```sql
-- Ver tablas
\dt

-- Ver estructura de una tabla
\d table_name

-- Ver índices
\di

-- Ver foreign keys
SELECT * FROM information_schema.table_constraints WHERE constraint_type = 'FOREIGN KEY';

-- Ver estadísticas de tablas
SELECT schemaname, tablename, attname, n_distinct, correlation 
FROM pg_stats 
WHERE schemaname = 'public';

-- Vacuum y analyze
VACUUM ANALYZE;

-- Ver conexiones activas
SELECT * FROM pg_stat_activity;
```

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0.0  
**Autor**: Sistema de Gestión de Inventario  
**Compatibilidad**: SQLite → PostgreSQL, Flask-Migrate, Docker
