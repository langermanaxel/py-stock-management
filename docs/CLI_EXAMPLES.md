# 🖥️ Ejemplos de Uso del Sistema CLI Unificado

## 🚀 Inicio Rápido

### Ver Ayuda General
```bash
python manage.py --help
```

**Salida esperada:**
```
Usage: manage.py [OPTIONS] COMMAND [ARGS]...

  Sistema de Gestión Unificado para Stock Management

Options:
  --config TEXT  Configuración a usar (development/production)  [default: development]
  --version      Show the version and exit.
  --help         Show this message and exit.

Commands:
  db     Operaciones de base de datos
  seed   Operaciones de seeding de datos
  shell  Abrir shell interactivo de Flask
  status Mostrar estado actual de la aplicación
  user   Operaciones de usuarios
```

## 🌱 Seeding de Datos

### Cargar Datos de Demostración
```bash
python manage.py seed --demo
```

**Salida esperada:**
```
🌱 Cargando datos de demostración...
  ✅ Categoría creada: Electrónicos
  ✅ Categoría creada: Ropa
  ✅ Categoría creada: Hogar
  ✅ Categoría creada: Deportes
  ✅ Categoría creada: Libros
  ✅ Producto creado: Laptop HP
  ✅ Producto creado: Smartphone Samsung
  ✅ Producto creado: Camiseta Básica
  ✅ Producto creado: Jeans Clásicos
  ✅ Producto creado: Sofá 3 Plazas
  ✅ Producto creado: Mesa de Centro
  ✅ Producto creado: Pelota de Fútbol
  ✅ Producto creado: Raqueta de Tenis
  ✅ Producto creado: Python para Principiantes
  ✅ Producto creado: Historia del Arte
  ✅ Stock creado: Laptop HP - 50 unidades
  ✅ Stock creado: Smartphone Samsung - 50 unidades
  ✅ Stock creado: Camiseta Básica - 100 unidades
  ✅ Stock creado: Jeans Clásicos - 100 unidades
  ✅ Stock creado: Sofá 3 Plazas - 100 unidades
  ✅ Stock creado: Mesa de Centro - 100 unidades
  ✅ Stock creado: Pelota de Fútbol - 100 unidades
  ✅ Stock creado: Raqueta de Tenis - 100 unidades
  ✅ Stock creado: Python para Principiantes - 100 unidades
  ✅ Stock creado: Historia del Arte - 100 unidades
🎉 Datos de demostración cargados exitosamente!
```

### Cargar Productos Personalizados
```bash
python manage.py seed --custom
```

**Salida esperada:**
```
🎨 Cargando productos personalizados...
  ✅ Producto personalizado creado: Auriculares Bluetooth
  ✅ Producto personalizado creado: Reloj Inteligente
  ✅ Producto personalizado creado: Zapatillas Running
  ✅ Producto personalizado creado: Mochila Escolar
  ✅ Producto personalizado creado: Cafetera Express
🎉 Productos personalizados cargados exitosamente!
```

### Cargar Todos los Datos
```bash
python manage.py seed --all
```

**Salida esperada:**
```
🚀 Cargando todos los datos...
🌱 Cargando datos de demostración...
  ✅ Categoría creada: Electrónicos
  # ... (más categorías y productos)
🎉 Datos de demostración cargados exitosamente!
🎨 Cargando productos personalizados...
  ✅ Producto personalizado creado: Auriculares Bluetooth
  # ... (más productos personalizados)
🎉 Productos personalizados cargados exitosamente!
🎉 Todos los datos han sido cargados exitosamente!
```

## 🗄️ Gestión de Base de Datos

### Inicializar Base de Datos
```bash
python manage.py db init
```

**Salida esperada:**
```
🗄️  Inicializando base de datos...
✅ Base de datos inicializada exitosamente!
```

### Ver Ayuda de Base de Datos
```bash
python manage.py db --help
```

**Salida esperada:**
```
Usage: manage.py db [OPTIONS] COMMAND [ARGS]...

  Operaciones de base de datos

Options:
  --help  Show this message and exit.

Commands:
  init     Inicializar base de datos
  migrate  Crear nueva migración
  upgrade  Aplicar migraciones pendientes
```

## 👥 Gestión de Usuarios

### Crear Usuario Administrador
```bash
python manage.py user create-admin
```

**Salida esperada (con prompts interactivos):**
```
👑 Creando usuario administrador...
Nombre de usuario: admin
Email: admin@example.com
Password: 
Repeat for confirmation: 
Nombre: Administrador
Apellido: Sistema
✅ Usuario administrador 'admin' creado exitosamente!
```

### Crear Usuarios de Muestra
```bash
python manage.py user create-sample
```

**Salida esperada:**
```
👥 Creando usuarios de muestra...
  ✅ Usuario creado: manager1 (manager)
  ✅ Usuario creado: user1 (user)
  ✅ Usuario creado: viewer1 (viewer)
🎉 Usuarios de muestra creados exitosamente!
```

### Ver Ayuda de Usuarios
```bash
python manage.py user --help
```

**Salida esperada:**
```
Usage: manage.py user [OPTIONS] COMMAND [ARGS]...

  Operaciones de usuarios

Options:
  --help  Show this message and exit.

Commands:
  create-admin   Crear usuario administrador
  create-sample  Crear usuarios de muestra
```

## 📊 Utilidades

### Ver Estado de la Aplicación
```bash
python manage.py status
```

**Salida esperada:**
```
📊 Estado de la aplicación:
========================================
📁 Categorías: 5
📦 Productos: 15
📊 Stock: 15
👥 Usuarios: 4
🛒 Órdenes de venta: 0
📋 Órdenes de compra: 0
🗄️  Base de datos: ✅ Conectada
⚙️  Entorno: development
🔐 JWT habilitado: ✅
📚 API docs: ✅
```

### Abrir Shell Interactivo
```bash
python manage.py shell
```

**Salida esperada:**
```
🐍 Abriendo shell interactivo...
   Variables disponibles: app, db, User, Category, Product, Stock, Order, PurchaseOrder
Python 3.11.0 (main, Oct 24 2022, 18:26:48) 
[GCC 11.2.0] on linux
Type "help", "copyright", "credits" or "license" for more information.
(InteractiveConsole)
>>> 
```

## 🔧 Configuración Avanzada

### Usar Configuración de Producción
```bash
python manage.py --config production status
```

### Combinar Comandos
```bash
# Inicializar DB y cargar datos en un solo comando
python manage.py db init && python manage.py seed --demo

# Crear admin y usuarios de muestra
python manage.py user create-admin && python manage.py user create-sample
```

## 🚨 Solución de Problemas

### Error: "Click no está instalado"
```bash
pip install click
```

### Error: "manage.py no encontrado"
```bash
# Asegúrate de estar en el directorio raíz del proyecto
ls manage.py
```

### Error: "Base de datos no conectada"
```bash
# Verifica que la base de datos esté configurada
python manage.py status
```

### Error: "Permisos insuficientes"
```bash
# En Linux/Mac, asegúrate de que manage.py sea ejecutable
chmod +x manage.py
```

## 📚 Casos de Uso Comunes

### 🆕 Configuración Inicial del Proyecto
```bash
# 1. Inicializar base de datos
python manage.py db init

# 2. Cargar datos de demostración
python manage.py seed --demo

# 3. Crear usuario administrador
python manage.py user create-admin

# 4. Verificar estado
python manage.py status
```

### 🔄 Desarrollo Diario
```bash
# Ver estado actual
python manage.py status

# Cargar datos adicionales
python manage.py seed --custom

# Abrir shell para debugging
python manage.py shell
```

### 🚀 Preparación para Producción
```bash
# Usar configuración de producción
python manage.py --config production db init
python manage.py --config production seed --demo
python manage.py --config production user create-admin
```

## 🎯 Consejos y Mejores Prácticas

1. **Siempre verifica el estado antes de operaciones críticas:**
   ```bash
   python manage.py status
   ```

2. **Usa la ayuda integrada para descubrir comandos:**
   ```bash
   python manage.py --help
   python manage.py seed --help
   ```

3. **Combina comandos para automatizar flujos de trabajo:**
   ```bash
   python manage.py db init && python manage.py seed --all
   ```

4. **Usa el shell interactivo para debugging:**
   ```bash
   python manage.py shell
   ```

5. **Mantén backups antes de operaciones masivas:**
   ```bash
   # Hacer backup de la base de datos antes de seeding
   cp instance/stock_management.db instance/backup_$(date +%Y%m%d_%H%M%S).db
   python manage.py seed --all
   ```

## 🔗 Comandos Relacionados

- **Flask CLI:** `flask db migrate`, `flask db upgrade`
- **Pytest:** `pytest tests/`
- **Docker:** `docker-compose up`, `docker-compose down`
- **Git:** `git status`, `git commit`, `git push`

---

💡 **¿Necesitas más ayuda?** Ejecuta `python manage.py --help` para ver todos los comandos disponibles.
