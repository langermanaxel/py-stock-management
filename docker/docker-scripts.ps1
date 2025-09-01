# Scripts de Docker para Sistema de Gestión de Inventario (PowerShell)
# Incluye comandos útiles para desarrollo y producción en Windows

param(
    [Parameter(Position=0)]
    [string]$Command = "help",
    
    [Parameter(Position=1)]
    [string]$Service = "web",
    
    [Parameter(Position=2)]
    [string]$ExecCommand = "bash"
)

# Configuración de colores para PowerShell
$Red = "Red"
$Green = "Green"
$Yellow = "Yellow"
$Blue = "Blue"
$White = "White"

# Función para imprimir mensajes con colores
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor $Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARNING] $Message" -ForegroundColor $Yellow
}

function Write-Error {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor $Red
}

function Write-Header {
    param([string]$Message)
    Write-Host "========================================" -ForegroundColor $Blue
    Write-Host $Message -ForegroundColor $Blue
    Write-Host "========================================" -ForegroundColor $Blue
}

# =============================================================================
# FUNCIONES PRINCIPALES
# =============================================================================

# Construir imagen de Docker
function Build-Image {
    Write-Header "Construyendo imagen de Docker"
    docker build -t stock-management:latest .
    Write-Info "Imagen construida exitosamente"
}

# Ejecutar en modo desarrollo
function Start-DevEnvironment {
    Write-Header "Iniciando entorno de desarrollo"
    
    # Crear directorios necesarios
    if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" | Out-Null }
    if (!(Test-Path "instance")) { New-Item -ItemType Directory -Path "instance" | Out-Null }
    
    # Iniciar servicios de desarrollo
    docker-compose -f docker-compose.dev.yml up -d
    
    Write-Info "Entorno de desarrollo iniciado"
    Write-Info "Aplicación disponible en: http://localhost:5000"
    Write-Info "Adminer disponible en: http://localhost:8080"
    Write-Info "Redis disponible en: localhost:6379"
}

# Ejecutar en modo producción
function Start-ProdEnvironment {
    Write-Header "Iniciando entorno de producción"
    
    # Crear directorios necesarios
    if (!(Test-Path "logs")) { New-Item -ItemType Directory -Path "logs" | Out-Null }
    if (!(Test-Path "instance")) { New-Item -ItemType Directory -Path "instance" | Out-Null }
    
    # Iniciar servicios de producción
    docker-compose up -d
    
    Write-Info "Entorno de producción iniciado"
    Write-Info "Aplicación disponible en: http://localhost:5000"
}

# Detener todos los servicios
function Stop-AllServices {
    Write-Header "Deteniendo todos los servicios"
    
    # Detener servicios de desarrollo
    try { docker-compose -f docker-compose.dev.yml down } catch { }
    
    # Detener servicios de producción
    try { docker-compose down } catch { }
    
    Write-Info "Todos los servicios detenidos"
}

# Ver logs de la aplicación
function Show-Logs {
    param([string]$ServiceName = "web")
    Write-Header "Mostrando logs del servicio: $ServiceName"
    
    if (docker-compose ps | Select-String -Pattern $ServiceName) {
        docker-compose logs -f $ServiceName
    }
    elseif (docker-compose -f docker-compose.dev.yml ps | Select-String -Pattern $ServiceName) {
        docker-compose -f docker-compose.dev.yml logs -f $ServiceName
    }
    else {
        Write-Error "Servicio $ServiceName no encontrado"
        exit 1
    }
}

# Ejecutar comandos dentro del contenedor
function Invoke-ContainerCommand {
    param(
        [string]$ServiceName = "web",
        [string]$Command = "bash"
    )
    
    Write-Header "Ejecutando comando en $ServiceName: $Command"
    
    if (docker-compose ps | Select-String -Pattern $ServiceName) {
        docker-compose exec $ServiceName $Command
    }
    elseif (docker-compose -f docker-compose.dev.yml ps | Select-String -Pattern $ServiceName) {
        docker-compose -f docker-compose.dev.yml exec $ServiceName $Command
    }
    else {
        Write-Error "Servicio $ServiceName no encontrado"
        exit 1
    }
}

# Inicializar base de datos
function Initialize-Database {
    Write-Header "Inicializando base de datos"
    
    # Crear usuario administrador
    Invoke-ContainerCommand -ServiceName "web" -Command "python create_admin_user.py"
    
    # Cargar datos de ejemplo
    Invoke-ContainerCommand -ServiceName "web" -Command "python load_sample_data.py"
    
    Write-Info "Base de datos inicializada exitosamente"
}

# Ejecutar tests
function Run-Tests {
    Write-Header "Ejecutando tests"
    
    Invoke-ContainerCommand -ServiceName "web" -Command "python -m pytest tests/ -v"
    
    Write-Info "Tests completados"
}

# Limpiar recursos de Docker
function Cleanup-Docker {
    Write-Header "Limpiando recursos de Docker"
    
    # Detener y eliminar contenedores
    Stop-AllServices
    
    # Eliminar imágenes no utilizadas
    docker image prune -f
    
    # Eliminar volúmenes no utilizados
    docker volume prune -f
    
    # Eliminar redes no utilizadas
    docker network prune -f
    
    Write-Info "Limpieza completada"
}

# Ver estado de los servicios
function Show-Status {
    Write-Header "Estado de los servicios"
    
    Write-Host "Servicios de desarrollo:" -ForegroundColor $Blue
    try { docker-compose -f docker-compose.dev.yml ps } catch { Write-Host "No hay servicios de desarrollo ejecutándose" }
    
    Write-Host "`nServicios de producción:" -ForegroundColor $Blue
    try { docker-compose ps } catch { Write-Host "No hay servicios de producción ejecutándose" }
    
    Write-Host "`nImágenes de Docker:" -ForegroundColor $Blue
    docker images | Select-String "stock-management"
}

# Mostrar ayuda
function Show-Help {
    Write-Header "Comandos disponibles"
    
    Write-Host "Uso: .\docker-scripts.ps1 [COMANDO] [SERVICIO] [COMANDO_EXEC]" -ForegroundColor $White
    Write-Host ""
    Write-Host "Comandos:" -ForegroundColor $White
    Write-Host "  build          - Construir imagen de Docker" -ForegroundColor $White
    Write-Host "  dev-up         - Iniciar entorno de desarrollo" -ForegroundColor $White
    Write-Host "  prod-up        - Iniciar entorno de producción" -ForegroundColor $White
    Write-Host "  stop           - Detener todos los servicios" -ForegroundColor $White
    Write-Host "  logs [SERVICE] - Ver logs de un servicio (default: web)" -ForegroundColor $White
    Write-Host "  exec [SERVICE] [COMMAND] - Ejecutar comando en contenedor" -ForegroundColor $White
    Write-Host "  init-db        - Inicializar base de datos" -ForegroundColor $White
    Write-Host "  test           - Ejecutar tests" -ForegroundColor $White
    Write-Host "  cleanup        - Limpiar recursos de Docker" -ForegroundColor $White
    Write-Host "  status         - Ver estado de los servicios" -ForegroundColor $White
    Write-Host "  help           - Mostrar esta ayuda" -ForegroundColor $White
    Write-Host ""
    Write-Host "Ejemplos:" -ForegroundColor $White
    Write-Host "  .\docker-scripts.ps1 dev-up                    # Iniciar desarrollo" -ForegroundColor $White
    Write-Host "  .\docker-scripts.ps1 logs web                  # Ver logs de la app" -ForegroundColor $White
    Write-Host "  .\docker-scripts.ps1 exec web python --version # Ver versión de Python" -ForegroundColor $White
    Write-Host "  .\docker-scripts.ps1 cleanup                   # Limpiar todo" -ForegroundColor $White
}

# =============================================================================
# SCRIPT PRINCIPAL
# =============================================================================

switch ($Command.ToLower()) {
    "build" {
        Build-Image
    }
    "dev-up" {
        Start-DevEnvironment
    }
    "prod-up" {
        Start-ProdEnvironment
    }
    "stop" {
        Stop-AllServices
    }
    "logs" {
        Show-Logs -ServiceName $Service
    }
    "exec" {
        Invoke-ContainerCommand -ServiceName $Service -Command $ExecCommand
    }
    "init-db" {
        Initialize-Database
    }
    "test" {
        Run-Tests
    }
    "cleanup" {
        Cleanup-Docker
    }
    "status" {
        Show-Status
    }
    "help" {
        Show-Help
    }
    default {
        Write-Warning "Comando '$Command' no reconocido"
        Show-Help
    }
}
