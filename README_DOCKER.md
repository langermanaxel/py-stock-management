# 🐳 Docker para Sistema de Gestión de Inventario

## 📋 Resumen

Configuración completa de Docker para el Sistema de Gestión de Inventario, incluyendo entornos de desarrollo y producción, con volúmenes persistentes para la base de datos.

## ✨ Características

- 🐳 **Multi-stage Dockerfile** optimizado para producción
- 🚀 **Docker Compose** para desarrollo y producción
- 📦 **Volúmenes persistentes** para base de datos SQLite
- 🔧 **Scripts automatizados** para gestión de contenedores
- 🌍 **Multi-plataforma** (Windows, macOS, Linux)
- 📱 **Responsive** y optimizado para diferentes dispositivos

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                    Docker Host                              │
├─────────────────────────────────────────────────────────────┤
│  ┌─────────────────┐    ┌─────────────────┐               │
│  │   Web Service   │    │  Redis (Dev)    │               │
│  │   Port: 5000    │    │   Port: 6379    │               │
│  └─────────────────┘    └─────────────────┘               │
│           │                       │                        │
│           ▼                       ▼                        │
│  ┌─────────────────┐    ┌─────────────────┐               │
│  │   Adminer       │    │   Volume Mount  │               │
│  │   Port: 8080    │    │   ./instance/   │               │
│  └─────────────────┘    └─────────────────┘               │
└─────────────────────────────────────────────────────────────┘
```

## 🚀 Inicio Rápido

### **1. Clonar y Preparar**
```bash
# Clonar repositorio
git clone https://github.com/tu-usuario/stock_management.git
cd stock_management

# Crear directorios necesarios
mkdir -p logs instance
```

### **2. Desarrollo (Recomendado para empezar)**
```bash
# Usando script de Docker
./docker-scripts.sh dev-up

# O manualmente
docker-compose -f docker-compose.dev.yml up -d
```

### **3. Producción**
```bash
# Usando script de Docker
./docker-scripts.sh prod-up

# O manualmente
docker-compose up -d
```

### **4. Verificar**
```bash
# Ver estado de servicios
./docker-scripts.sh status

# Ver logs
./docker-scripts.sh logs web

# Abrir en navegador
open http://localhost:5000  # macOS
start http://localhost:5000  # Windows
xdg-open http://localhost:5000  # Linux
```

## 🐳 Archivos de Docker

### **Dockerfile**
- **Multi-stage build** para optimizar tamaño
- **Python 3.11-slim** como base
- **Usuario no-root** para seguridad
- **Health check** integrado
- **Optimizado** para producción

### **docker-compose.yml**
- **Servicio web** principal
- **Volumen persistente** para base de datos
- **Variables de entorno** configurables
- **Health checks** y restart policies
- **Límites de recursos** configurados

### **docker-compose.dev.yml**
- **Hot reload** habilitado
- **Volúmenes montados** para desarrollo
- **Redis** para cache (opcional)
- **Adminer** para gestión de BD
- **Debug** y logging detallado

## 🔧 Scripts de Gestión

### **Linux/macOS**
```bash
# Dar permisos de ejecución
chmod +x docker-scripts.sh

# Ver comandos disponibles
./docker-scripts.sh help

# Comandos principales
./docker-scripts.sh dev-up      # Iniciar desarrollo
./docker-scripts.sh prod-up     # Iniciar producción
./docker-scripts.sh stop        # Detener servicios
./docker-scripts.sh logs web    # Ver logs
./docker-scripts.sh cleanup     # Limpiar recursos
```

### **Windows PowerShell**
```powershell
# Ver comandos disponibles
.\docker-scripts.ps1 help

# Comandos principales
.\docker-scripts.ps1 dev-up     # Iniciar desarrollo
.\docker-scripts.ps1 prod-up    # Iniciar producción
.\docker-scripts.ps1 stop       # Detener servicios
.\docker-scripts.ps1 logs web   # Ver logs
.\docker-scripts.ps1 cleanup    # Limpiar recursos
```

## 📊 Comandos de Docker

### **Construir Imagen**
```bash
# Construir imagen
docker build -t stock-management:latest .

# Construir sin cache
docker build --no-cache -t stock-management:latest .

# Construir con tag específico
docker build -t stock-management:v1.0.0 .
```

### **Ejecutar Contenedor**
```bash
# Ejecutar en modo detached
docker run -d -p 5000:5000 --name stock-app stock-management:latest

# Ejecutar con volúmenes
docker run -d -p 5000:5000 \
  -v $(pwd)/instance:/app/instance \
  -v $(pwd)/logs:/app/logs \
  --name stock-app stock-management:latest

# Ejecutar interactivo
docker run -it --rm stock-management:latest bash
```

### **Gestionar Contenedores**
```bash
# Ver contenedores ejecutándose
docker ps

# Ver todos los contenedores
docker ps -a

# Ver logs de un contenedor
docker logs stock-app

# Ver logs en tiempo real
docker logs -f stock-app

# Ejecutar comando en contenedor
docker exec -it stock-app python --version

# Detener contenedor
docker stop stock-app

# Eliminar contenedor
docker rm stock-app
```

### **Gestionar Imágenes**
```bash
# Ver imágenes
docker images

# Eliminar imagen
docker rmi stock-management:latest

# Eliminar imágenes no utilizadas
docker image prune -f

# Ver historial de imagen
docker history stock-management:latest
```

### **Gestionar Volúmenes**
```bash
# Ver volúmenes
docker volume ls

# Eliminar volumen
docker volume rm stock_management_stock_data

# Eliminar volúmenes no utilizados
docker volume prune -f

# Ver información del volumen
docker volume inspect stock_management_stock_data
```

## 🌍 Variables de Entorno

### **Variables Obligatorias**
```bash
# Configuración de la aplicación
SECRET_KEY=tu-clave-secreta-super-segura-aqui
JWT_SECRET_KEY=tu-clave-jwt-super-segura-aqui
FLASK_ENV=production
DEBUG=false

# Configuración de base de datos
SQLALCHEMY_DATABASE_URI=sqlite:///instance/stock_management.db
SQLALCHEMY_TRACK_MODIFICATIONS=false
```

### **Variables Opcionales**
```bash
# Configuración JWT
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=86400

# Configuración de la API
API_TITLE=Stock Management API
API_VERSION=1.0.0
OPENAPI_VERSION=3.0.2

# Configuración de logging
LOG_LEVEL=INFO
LOG_FILE=logs/app.log

# Configuración de CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:5000
```

## 🔍 Troubleshooting

### **Problemas Comunes**

#### **Error: "Port already in use"**
```bash
# Verificar qué está usando el puerto
lsof -i :5000  # macOS/Linux
netstat -ano | findstr :5000  # Windows

# Cambiar puerto en docker-compose
ports:
  - "8000:5000"  # Puerto 8000 en host, 5000 en contenedor
```

#### **Error: "Permission denied"**
```bash
# Verificar permisos de directorios
ls -la instance/
ls -la logs/

# Crear directorios con permisos correctos
mkdir -p instance logs
chmod 755 instance logs
```

#### **Error: "Database locked"**
```bash
# Detener todos los servicios
docker-compose down

# Eliminar archivo de base de datos corrupto
rm instance/stock_management.db

# Reiniciar servicios
docker-compose up -d
```

#### **Error: "Container won't start"**
```bash
# Ver logs del contenedor
docker logs stock_management_web

# Verificar configuración
docker-compose config

# Reconstruir imagen
docker-compose build --no-cache
```

### **Comandos de Diagnóstico**
```bash
# Ver estado de servicios
docker-compose ps

# Ver logs de todos los servicios
docker-compose logs

# Ver logs de un servicio específico
docker-compose logs web

# Ver logs en tiempo real
docker-compose logs -f web

# Ver configuración compilada
docker-compose config

# Ver uso de recursos
docker stats

# Ver información del sistema
docker system df
```

## 📈 Performance y Optimización

### **Configuración de Recursos**
```yaml
# docker-compose.yml
deploy:
  resources:
    limits:
      memory: 512M
      cpus: '0.5'
    reservations:
      memory: 256M
      cpus: '0.25'
```

### **Optimización de Imagen**
```dockerfile
# Dockerfile optimizado
FROM python:3.11-slim as builder
# ... build stage

FROM python:3.11-slim
# ... runtime stage
# Solo copiar lo necesario
COPY --from=builder /opt/venv /opt/venv
```

### **Volúmenes Optimizados**
```yaml
# docker-compose.yml
volumes:
  stock_data:
    driver: local
    driver_opts:
      type: none
      o: bind
      device: ./instance
```

## 🔐 Seguridad

### **Usuario No-Root**
```dockerfile
# Dockerfile
RUN groupadd -r appuser && useradd -r -g appuser appuser
USER appuser
```

### **Health Checks**
```yaml
# docker-compose.yml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### **Variables de Entorno Seguras**
```bash
# NUNCA committear estas variables
SECRET_KEY=clave-super-secreta
JWT_SECRET_KEY=clave-jwt-super-secreta
DATABASE_URL=url-de-conexion-secreta
```

## 🚀 Despliegue en Producción

### **1. Preparar Imagen**
```bash
# Construir imagen de producción
docker build -t stock-management:prod .

# Etiquetar para registro
docker tag stock-management:prod tu-registro/stock-management:v1.0.0

# Subir a registro
docker push tu-registro/stock-management:v1.0.0
```

### **2. Desplegar en Servidor**
```bash
# Copiar archivos al servidor
scp docker-compose.yml usuario@servidor:/app/
scp .env usuario@servidor:/app/

# En el servidor
cd /app
docker-compose pull
docker-compose up -d
```

### **3. Configurar Reverse Proxy**
```nginx
# nginx.conf
server {
    listen 80;
    server_name tu-dominio.com;
    
    location / {
        proxy_pass http://localhost:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## 📊 Monitoreo

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

### **Logs Estructurados**
```python
# app/config.py
import logging
from logging.handlers import RotatingFileHandler

if not app.debug:
    file_handler = RotatingFileHandler(
        'logs/app.log', 
        maxBytes=10240, 
        backupCount=10
    )
    app.logger.addHandler(file_handler)
```

### **Métricas de Docker**
```bash
# Ver estadísticas en tiempo real
docker stats

# Ver uso de recursos
docker system df

# Ver información del sistema
docker info
```

## 🔄 CI/CD

### **GitHub Actions**
```yaml
# .github/workflows/docker.yml
name: Docker Build and Push

on:
  push:
    branches: [ main ]
    tags: [ 'v*' ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Build and push Docker image
        uses: docker/build-push-action@v4
        with:
          context: .
          push: true
          tags: tu-registro/stock-management:latest
```

### **Docker Hub**
```bash
# Login a Docker Hub
docker login

# Subir imagen
docker push tu-usuario/stock-management:latest

# Subir con tag específico
docker tag stock-management:latest tu-usuario/stock-management:v1.0.0
docker push tu-usuario/stock-management:v1.0.0
```

## 📚 Recursos Adicionales

### **Documentación Oficial**
- [Docker Documentation](https://docs.docker.com/)
- [Docker Compose](https://docs.docker.com/compose/)
- [Docker Best Practices](https://docs.docker.com/develop/dev-best-practices/)

### **Tutoriales y Ejemplos**
- [Docker for Python Developers](https://docs.docker.com/language/python/)
- [Flask with Docker](https://flask.palletsprojects.com/en/2.3.x/deploying/docker/)
- [Multi-stage Docker Builds](https://docs.docker.com/develop/dev-best-practices/dockerfile_best-practices/#use-multi-stage-builds)

### **Herramientas Útiles**
- [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- [Portainer](https://www.portainer.io/) - Gestión visual de Docker
- [Docker Compose UI](https://github.com/francescou/docker-compose-ui)

## 🤝 Contribuir

### **Reportar Issues**
1. Verificar que no sea un problema de configuración local
2. Incluir logs de Docker: `docker-compose logs web`
3. Incluir versión de Docker: `docker --version`
4. Incluir sistema operativo y versión

### **Sugerir Mejoras**
1. Crear issue con etiqueta "enhancement"
2. Describir el caso de uso
3. Proponer solución si es posible

### **Pull Requests**
1. Fork del repositorio
2. Crear rama para la feature
3. Incluir tests si es posible
4. Actualizar documentación

---

**Última actualización**: Diciembre 2024  
**Versión**: 1.0.0  
**Autor**: Sistema de Gestión de Inventario  
**Compatibilidad**: Docker 20.10+, Docker Compose 2.0+
