# Script de inicio rápido para Docker (Windows PowerShell)
# ¡Levanta el Sistema de Gestión de Inventario en 1 comando!

Write-Host "🚀 Iniciando Sistema de Gestión de Inventario con Docker..." -ForegroundColor Green
Write-Host "==================================================" -ForegroundColor Cyan

# Verificar si Docker está instalado
try {
    $dockerVersion = docker --version
    Write-Host "✅ Docker encontrado: $dockerVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker no está instalado" -ForegroundColor Red
    Write-Host "   Instala Docker Desktop desde: https://docs.docker.com/desktop/install/windows/" -ForegroundColor Yellow
    exit 1
}

# Verificar si Docker Compose está instalado
try {
    $composeVersion = docker-compose --version
    Write-Host "✅ Docker Compose encontrado: $composeVersion" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker Compose no está instalado" -ForegroundColor Red
    Write-Host "   Instala Docker Compose desde: https://docs.docker.com/compose/install/" -ForegroundColor Yellow
    exit 1
}

# Verificar si Docker está ejecutándose
try {
    docker info | Out-Null
    Write-Host "✅ Docker está ejecutándose" -ForegroundColor Green
} catch {
    Write-Host "❌ Error: Docker no está ejecutándose" -ForegroundColor Red
    Write-Host "   Inicia Docker Desktop desde el menú de inicio" -ForegroundColor Yellow
    exit 1
}

Write-Host "✅ Docker y Docker Compose verificados" -ForegroundColor Green

# Crear directorios necesarios si no existen
Write-Host "📁 Creando directorios necesarios..." -ForegroundColor Cyan
if (!(Test-Path "instance")) { New-Item -ItemType Directory -Name "instance" }
if (!(Test-Path "logs")) { New-Item -ItemType Directory -Name "logs" }

# Construir y levantar la aplicación
Write-Host "🔨 Construyendo imagen Docker..." -ForegroundColor Cyan
docker-compose build

Write-Host "🚀 Levantando aplicación..." -ForegroundColor Cyan
docker-compose up -d

# Esperar a que la aplicación esté lista
Write-Host "⏳ Esperando a que la aplicación esté lista..." -ForegroundColor Yellow
Start-Sleep -Seconds 10

# Verificar estado
Write-Host "🔍 Verificando estado de la aplicación..." -ForegroundColor Cyan
try {
    $response = Invoke-WebRequest -Uri "http://localhost:5000" -TimeoutSec 5 -ErrorAction Stop
    if ($response.StatusCode -eq 200) {
        Write-Host "✅ ¡Aplicación iniciada exitosamente!" -ForegroundColor Green
        Write-Host ""
        Write-Host "🌐 Accede a la aplicación en: http://localhost:5000" -ForegroundColor Cyan
        Write-Host "📚 Documentación de la API en: http://localhost:5000/swagger-ui" -ForegroundColor Cyan
        Write-Host ""
        Write-Host "📋 Comandos útiles:" -ForegroundColor Yellow
        Write-Host "   Ver logs: docker-compose logs -f" -ForegroundColor White
        Write-Host "   Detener: docker-compose down" -ForegroundColor White
        Write-Host "   Reiniciar: docker-compose restart" -ForegroundColor White
        Write-Host "   Estado: docker-compose ps" -ForegroundColor White
    }
} catch {
    Write-Host "⚠️ La aplicación puede estar aún iniciando..." -ForegroundColor Yellow
    Write-Host "   Revisa los logs con: docker-compose logs -f" -ForegroundColor White
    Write-Host "   O espera unos segundos más y verifica: http://localhost:5000" -ForegroundColor White
}

Write-Host ""
Write-Host "🎉 ¡Listo! Tu Sistema de Gestión de Inventario está ejecutándose en Docker." -ForegroundColor Green
