#!/bin/bash

# Scripts de Docker para Sistema de Gestión de Inventario
# Incluye comandos útiles para desarrollo y producción

set -e  # Salir si hay algún error

# Colores para output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Función para imprimir mensajes con colores
print_message() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo -e "${BLUE}================================${NC}"
    echo -e "${BLUE}$1${NC}"
    echo -e "${BLUE}================================${NC}"
}

# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================

# Construir imagen de Docker
build_image() {
    print_header "Construyendo imagen de Docker"
    docker build -t stock-management:latest .
    print_message "Imagen construida exitosamente"
}

# Ejecutar en modo desarrollo
dev_up() {
    print_header "Iniciando entorno de desarrollo"
    
    # Crear directorios necesarios
    mkdir -p logs
    mkdir -p instance
    
    # Iniciar servicios de desarrollo
    docker-compose -f docker-compose.dev.yml up -d
    
    print_message "Entorno de desarrollo iniciado"
    print_message "Aplicación disponible en: http://localhost:5000"
    print_message "Adminer disponible en: http://localhost:8080"
    print_message "Redis disponible en: localhost:6379"
}

# Ejecutar en modo producción
prod_up() {
    print_header "Iniciando entorno de producción"
    
    # Crear directorios necesarios
    mkdir -p logs
    mkdir -p instance
    
    # Iniciar servicios de producción
    docker-compose up -d
    
    print_message "Entorno de producción iniciado"
    print_message "Aplicación disponible en: http://localhost:5000"
}

# Detener todos los servicios
stop_all() {
    print_header "Deteniendo todos los servicios"
    
    # Detener servicios de desarrollo
    docker-compose -f docker-compose.dev.yml down 2>/dev/null || true
    
    # Detener servicios de producción
    docker-compose down 2>/dev/null || true
    
    print_message "Todos los servicios detenidos"
}

# Ver logs de la aplicación
logs() {
    local service=${1:-web}
    print_header "Mostrando logs del servicio: $service"
    
    if docker-compose ps | grep -q "$service"; then
        docker-compose logs -f "$service"
    elif docker-compose -f docker-compose.dev.yml ps | grep -q "$service"; then
        docker-compose -f docker-compose.dev.yml logs -f "$service"
    else
        print_error "Servicio $service no encontrado"
        exit 1
    fi
}

# Ejecutar comandos dentro del contenedor
exec_command() {
    local service=${1:-web}
    local command=${2:-bash}
    
    print_header "Ejecutando comando en $service: $command"
    
    if docker-compose ps | grep -q "$service"; then
        docker-compose exec "$service" $command
    elif docker-compose -f docker-compose.dev.yml ps | grep -q "$service"; then
        docker-compose -f docker-compose.dev.yml exec "$service" $command
    else
        print_error "Servicio $service no encontrado"
        exit 1
    fi
}

# Inicializar base de datos
init_db() {
    print_header "Inicializando base de datos"
    
    # Crear usuario administrador
    exec_command web "python create_admin_user.py"
    
    # Cargar datos de ejemplo
    exec_command web "python load_sample_data.py"
    
    print_message "Base de datos inicializada exitosamente"
}

# Ejecutar tests
run_tests() {
    print_header "Ejecutando tests"
    
    exec_command web "python -m pytest tests/ -v"
    
    print_message "Tests completados"
}

# Limpiar recursos de Docker
cleanup() {
    print_header "Limpiando recursos de Docker"
    
    # Detener y eliminar contenedores
    stop_all
    
    # Eliminar imágenes no utilizadas
    docker image prune -f
    
    # Eliminar volúmenes no utilizados
    docker volume prune -f
    
    # Eliminar redes no utilizadas
    docker network prune -f
    
    print_message "Limpieza completada"
}

# Ver estado de los servicios
status() {
    print_header "Estado de los servicios"
    
    echo "Servicios de desarrollo:"
    docker-compose -f docker-compose.dev.yml ps 2>/dev/null || echo "No hay servicios de desarrollo ejecutándose"
    
    echo -e "\nServicios de producción:"
    docker-compose ps 2>/dev/null || echo "No hay servicios de producción ejecutándose"
    
    echo -e "\nImágenes de Docker:"
    docker images | grep stock-management
}

# Mostrar ayuda
show_help() {
    print_header "Comandos disponibles"
    
    echo "Uso: $0 [COMANDO]"
    echo ""
    echo "Comandos:"
    echo "  build          - Construir imagen de Docker"
    echo "  dev-up         - Iniciar entorno de desarrollo"
    echo "  prod-up        - Iniciar entorno de producción"
    echo "  stop           - Detener todos los servicios"
    echo "  logs [SERVICE] - Ver logs de un servicio (default: web)"
    echo "  exec [SERVICE] [COMMAND] - Ejecutar comando en contenedor"
    echo "  init-db        - Inicializar base de datos"
    echo "  test           - Ejecutar tests"
    echo "  cleanup        - Limpiar recursos de Docker"
    echo "  status         - Ver estado de los servicios"
    echo "  help           - Mostrar esta ayuda"
    echo ""
    echo "Ejemplos:"
    echo "  $0 dev-up                    # Iniciar desarrollo"
    echo "  $0 logs web                  # Ver logs de la app"
    echo "  $0 exec web python --version # Ver versión de Python"
    echo "  $0 cleanup                   # Limpiar todo"
}

# =============================================================================
# SCRIPT PRINCIPAL
# =============================================================================

case "${1:-help}" in
    "build")
        build_image
        ;;
    "dev-up")
        dev_up
        ;;
    "prod-up")
        prod_up
        ;;
    "stop")
        stop_all
        ;;
    "logs")
        logs "$2"
        ;;
    "exec")
        exec_command "$2" "${3:-bash}"
        ;;
    "init-db")
        init_db
        ;;
    "test")
        run_tests
        ;;
    "cleanup")
        cleanup
        ;;
    "status")
        status
        ;;
    "help"|*)
        show_help
        ;;
esac
