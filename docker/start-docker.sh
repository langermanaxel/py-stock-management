#!/bin/bash

# Script de inicio rápido para Docker
# ¡Levanta el Sistema de Gestión de Inventario en 1 comando!

echo "🚀 Iniciando Sistema de Gestión de Inventario con Docker..."
echo "=================================================="

# Verificar si Docker está instalado
if ! command -v docker &> /dev/null; then
    echo "❌ Error: Docker no está instalado"
    echo "   Instala Docker desde: https://docs.docker.com/get-docker/"
    exit 1
fi

# Verificar si Docker Compose está instalado
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Error: Docker Compose no está instalado"
    echo "   Instala Docker Compose desde: https://docs.docker.com/compose/install/"
    exit 1
fi

# Verificar si Docker está ejecutándose
if ! docker info &> /dev/null; then
    echo "❌ Error: Docker no está ejecutándose"
    echo "   Inicia Docker Desktop o el servicio de Docker"
    exit 1
fi

echo "✅ Docker y Docker Compose verificados"

# Crear directorios necesarios si no existen
echo "📁 Creando directorios necesarios..."
mkdir -p instance logs

# Construir y levantar la aplicación
echo "🔨 Construyendo imagen Docker..."
docker-compose build

echo "🚀 Levantando aplicación..."
docker-compose up -d

# Esperar a que la aplicación esté lista
echo "⏳ Esperando a que la aplicación esté lista..."
sleep 10

# Verificar estado
echo "🔍 Verificando estado de la aplicación..."
if curl -s http://localhost:5000 > /dev/null; then
    echo "✅ ¡Aplicación iniciada exitosamente!"
    echo ""
    echo "🌐 Accede a la aplicación en: http://localhost:5000"
    echo "📚 Documentación de la API en: http://localhost:5000/swagger-ui"
    echo ""
    echo "📋 Comandos útiles:"
    echo "   Ver logs: docker-compose logs -f"
    echo "   Detener: docker-compose down"
    echo "   Reiniciar: docker-compose restart"
    echo "   Estado: docker-compose ps"
else
    echo "⚠️ La aplicación puede estar aún iniciando..."
    echo "   Revisa los logs con: docker-compose logs -f"
    echo "   O espera unos segundos más y verifica: http://localhost:5000"
fi

echo ""
echo "🎉 ¡Listo! Tu Sistema de Gestión de Inventario está ejecutándose en Docker."
