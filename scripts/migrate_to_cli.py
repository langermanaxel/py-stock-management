#!/usr/bin/env python3
"""
Script de Migración a CLI Unificado
===================================

Este script ayuda a migrar desde los scripts individuales antiguos
hacia el nuevo sistema CLI unificado con `manage.py`.

Antes de ejecutar este script, asegúrate de:
1. Tener instalado `click`: pip install click
2. Tener el archivo `manage.py` en el directorio raíz
3. Hacer backup de tu base de datos actual

Uso:
    python migrate_to_cli.py
"""

import os
import shutil
import sys
from pathlib import Path

def backup_old_scripts():
    """Crear backup de los scripts antiguos"""
    backup_dir = Path("backup_old_scripts")
    backup_dir.mkdir(exist_ok=True)
    
    old_scripts = [
        "init_sample_data.py",
        "load_sample_data.py", 
        "add_custom_products.py",
        "create_admin_user.py"
    ]
    
    print("📦 Creando backup de scripts antiguos...")
    for script in old_scripts:
        if Path(script).exists():
            shutil.copy2(script, backup_dir / script)
            print(f"  ✅ Backup creado: {script}")
        else:
            print(f"  ℹ️  Script no encontrado: {script}")
    
    return backup_dir

def remove_old_scripts():
    """Eliminar scripts antiguos"""
    old_scripts = [
        "init_sample_data.py",
        "load_sample_data.py",
        "add_custom_products.py",
        "create_admin_user.py"
    ]
    
    print("\n🗑️  Eliminando scripts antiguos...")
    for script in old_scripts:
        if Path(script).exists():
            os.remove(script)
            print(f"  ✅ Eliminado: {script}")
        else:
            print(f"  ℹ️  No existía: {script}")

def create_migration_guide():
    """Crear guía de migración"""
    guide_content = """# Guía de Migración a CLI Unificado

## Cambios Realizados

Los siguientes scripts han sido reemplazados por el nuevo sistema CLI unificado:

- `init_sample_data.py` → `python manage.py seed --demo`
- `load_sample_data.py` → `python manage.py seed --demo`
- `add_custom_products.py` → `python manage.py seed --custom`
- `create_admin_user.py` → `python manage.py user create-admin`

## Nuevos Comandos Disponibles

### Seeding de Datos
```bash
# Cargar datos de demostración
python manage.py seed --demo

# Cargar productos personalizados
python manage.py seed --custom

# Cargar todos los datos
python manage.py seed --all
```

### Gestión de Base de Datos
```bash
# Inicializar base de datos
python manage.py db init

# Crear migración (requiere Flask-Migrate)
python manage.py db migrate

# Aplicar migraciones
python manage.py db upgrade
```

### Gestión de Usuarios
```bash
# Crear usuario administrador
python manage.py user create-admin

# Crear usuarios de muestra
python manage.py user create-sample
```

### Utilidades
```bash
# Ver estado de la aplicación
python manage.py status

# Abrir shell interactivo
python manage.py shell

# Ver ayuda completa
python manage.py --help
```

## Ventajas del Nuevo Sistema

1. **Unificado**: Un solo comando para todas las operaciones
2. **Consistente**: Interfaz CLI estándar con Click
3. **Extensible**: Fácil agregar nuevos comandos
4. **Documentado**: Ayuda integrada con `--help`
5. **Robusto**: Manejo de errores y validaciones
6. **Profesional**: Estándar de la industria para aplicaciones Flask

## Rollback

Si necesitas volver a los scripts antiguos, están disponibles en:
`backup_old_scripts/`

## Soporte

Para más información, consulta:
- `python manage.py --help`
- `python manage.py seed --help`
- `python manage.py db --help`
- `python manage.py user --help`
"""
    
    with open("MIGRATION_CLI.md", "w", encoding="utf-8") as f:
        f.write(guide_content)
    
    print("  ✅ Guía de migración creada: MIGRATION_CLI.md")

def test_new_cli():
    """Probar que el nuevo CLI funciona"""
    print("\n🧪 Probando nuevo CLI...")
    
    try:
        import click
        print("  ✅ Click instalado correctamente")
    except ImportError:
        print("  ❌ Click no está instalado. Ejecuta: pip install click")
        return False
    
    if not Path("manage.py").exists():
        print("  ❌ manage.py no encontrado")
        return False
    
    print("  ✅ manage.py encontrado")
    
    # Probar ejecución básica
    try:
        result = os.system("python manage.py --help > /dev/null 2>&1")
        if result == 0:
            print("  ✅ CLI ejecutándose correctamente")
            return True
        else:
            print("  ❌ Error al ejecutar CLI")
            return False
    except Exception as e:
        print(f"  ❌ Error: {e}")
        return False

def main():
    """Función principal de migración"""
    print("🚀 Iniciando migración a CLI unificado...")
    print("=" * 50)
    
    # Verificar que estamos en el directorio correcto
    if not Path("manage.py").exists():
        print("❌ Error: manage.py no encontrado en el directorio actual")
        print("   Ejecuta este script desde el directorio raíz del proyecto")
        sys.exit(1)
    
    # Crear backup
    backup_dir = backup_old_scripts()
    
    # Probar nuevo CLI
    if not test_new_cli():
        print("\n❌ El nuevo CLI no está funcionando correctamente")
        print("   Revisa los errores antes de continuar")
        sys.exit(1)
    
    # Crear guía de migración
    create_migration_guide()
    
    # Preguntar si eliminar scripts antiguos
    print(f"\n📋 Los scripts antiguos han sido respaldados en: {backup_dir}")
    
    try:
        remove_old = input("¿Deseas eliminar los scripts antiguos? (s/N): ").strip().lower()
        if remove_old in ['s', 'si', 'sí', 'y', 'yes']:
            remove_old_scripts()
            print("\n✅ Scripts antiguos eliminados")
        else:
            print("\nℹ️  Scripts antiguos conservados")
    except KeyboardInterrupt:
        print("\n\n⚠️  Operación cancelada por el usuario")
        print("   Los scripts antiguos han sido conservados")
    
    print("\n🎉 Migración completada exitosamente!")
    print("\n📚 Próximos pasos:")
    print("1. Lee MIGRATION_CLI.md para conocer los nuevos comandos")
    print("2. Prueba: python manage.py --help")
    print("3. Prueba: python manage.py seed --demo")
    print("4. Prueba: python manage.py status")
    print("\n💡 Para ayuda: python manage.py --help")

if __name__ == "__main__":
    main()
