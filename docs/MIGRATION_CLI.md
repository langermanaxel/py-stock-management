# Guía de Migración a CLI Unificado

## Cambios Realizados

Los siguientes scripts han sido reemplazados por el nuevo sistema CLI unificado:

- `init_sample_data.py` → `python seed_data.py --demo`
- `load_sample_data.py` → `python seed_data.py --demo`
- `add_custom_products.py` → `python seed_data.py --custom`
- `create_admin_user.py` → `python manage.py user create-admin` (cuando esté disponible)

## Nuevos Comandos Disponibles

### Seeding de Datos (Script Simplificado)
```bash
# Cargar datos de demostración
python seed_data.py --demo

# Cargar productos personalizados
python seed_data.py --custom

# Cargar todos los datos
python seed_data.py --all
```

### CLI Completo (cuando esté disponible)
```bash
# Ver ayuda general
python manage.py --help

# Ver ayuda específica
python manage.py seed --help
python manage.py db --help
python manage.py user --help
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
- `python seed_data.py --help`
- `python manage.py --help` (cuando esté disponible)
