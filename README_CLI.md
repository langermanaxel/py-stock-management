# 🖥️ Sistema CLI Unificado para Stock Management

## 🎯 Objetivo

Este sistema unifica todos los scripts de datos antiguos (`init_sample_data.py`, `load_sample_data.py`, `add_custom_products.py`) en un solo comando CLI usando Click, proporcionando una **Developer Experience (DX) prolija** y profesional.

## 🚀 Comandos Disponibles

### 🌱 Seeding de Datos

```bash
# Cargar datos de demostración completos
python seed_data.py --demo

# Cargar productos personalizados adicionales
python seed_data.py --custom

# Cargar todos los datos (demo + personalizados)
python seed_data.py --all

# Ver ayuda
python seed_data.py --help
```

### 📊 Ver Estado

```bash
# Verificar conectividad y estado de la base de datos
python test_db.py
```

## 🔄 Migración desde Scripts Antiguos

### ✅ Scripts Reemplazados

| Script Antiguo | Nuevo Comando | Descripción |
|----------------|----------------|-------------|
| `init_sample_data.py` | `python seed_data.py --demo` | Datos de demostración básicos |
| `load_sample_data.py` | `python seed_data.py --demo` | Datos de demostración completos |
| `add_custom_products.py` | `python seed_data.py --custom` | Productos personalizados |

### 📦 Backup Automático

Los scripts antiguos han sido respaldados en:
```
backup_old_scripts/
├── init_sample_data.py
├── load_sample_data.py
├── add_custom_products.py
└── create_admin_user.py
```

## 🎨 Características del Nuevo Sistema

### ✨ Ventajas

1. **🔄 Unificado**: Un solo comando para todas las operaciones
2. **📚 Documentado**: Ayuda integrada con `--help`
3. **🛡️ Robusto**: Manejo de errores y transacciones
4. **🔧 Mantenible**: Código centralizado y organizado
5. **📱 Profesional**: Interfaz CLI estándar de la industria

### 🎯 Funcionalidades

- **Detección automática** de datos existentes
- **Transacciones seguras** con rollback automático
- **Logging detallado** de todas las operaciones
- **Manejo de errores** robusto y informativo
- **Compatibilidad** con SQLAlchemy 2.0+

## 🛠️ Instalación y Configuración

### 📋 Requisitos

```bash
pip install click==8.1.7 Flask-Migrate==4.0.5
```

### 🔧 Configuración

El sistema detecta automáticamente:
- Ruta de la base de datos SQLite
- Estructura de modelos existente
- Configuración de Flask

## 📖 Ejemplos de Uso

### 🆕 Configuración Inicial

```bash
# 1. Verificar base de datos
python test_db.py

# 2. Cargar datos de demostración
python seed_data.py --demo

# 3. Cargar productos personalizados
python seed_data.py --custom
```

### 🔄 Desarrollo Diario

```bash
# Cargar todos los datos
python seed_data.py --all

# Solo datos de demostración
python seed_data.py --demo

# Solo productos personalizados
python seed_data.py --custom
```

### 🧪 Testing y Debugging

```bash
# Verificar conectividad
python test_db.py

# Ver ayuda del CLI
python seed_data.py --help
```

## 🚨 Solución de Problemas

### ❌ Error: "Base de datos no encontrada"

```bash
# Verificar que la base de datos existe
ls instance/stock_management.db

# Ejecutar script de prueba
python test_db.py
```

### ❌ Error: "Modelo no encontrado"

```bash
# Verificar que los modelos están importados
python -c "from app.models import Category, Product, Stock; print('OK')"
```

### ❌ Error: "Transacción fallida"

```bash
# Verificar permisos de escritura
# Ejecutar con permisos de administrador si es necesario
```

## 🔮 Próximos Pasos

### 🎯 CLI Completo (Futuro)

```bash
# Comandos adicionales planeados
python manage.py db init          # Inicializar base de datos
python manage.py db migrate       # Crear migraciones
python manage.py user create-admin # Crear usuario administrador
python manage.py status           # Ver estado de la aplicación
```

### 🚀 Mejoras Planificadas

- [ ] Comando `db` para gestión de base de datos
- [ ] Comando `user` para gestión de usuarios
- [ ] Comando `status` para monitoreo
- [ ] Comando `shell` para debugging interactivo
- [ ] Integración con Flask-Migrate

## 📚 Documentación Relacionada

- `MIGRATION_CLI.md` - Guía de migración detallada
- `CLI_EXAMPLES.md` - Ejemplos de uso avanzados
- `README.md` - Documentación principal del proyecto

## 🤝 Contribución

Para contribuir al sistema CLI:

1. **📝 Crear feature branch**: `git checkout -b feature/nuevo-comando`
2. **🔧 Implementar funcionalidad**: Agregar nuevos comandos Click
3. **🧪 Agregar tests**: Verificar que funciona correctamente
4. **📚 Actualizar documentación**: README y ejemplos
5. **🔄 Crear Pull Request**: Con descripción detallada

## 📄 Licencia

Este sistema CLI está bajo la misma licencia MIT que el proyecto principal.

---

💡 **¿Necesitas ayuda?** Ejecuta `python seed_data.py --help` para ver todos los comandos disponibles.
