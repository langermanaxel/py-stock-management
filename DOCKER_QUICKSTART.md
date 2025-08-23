# 🐳 Docker Quick Start - Sistema de Gestión de Inventario

## 🚀 ¡Levanta en 1 Comando!

### 📋 Requisitos Previos
- **Docker Desktop** instalado y ejecutándose
- **Docker Compose** (incluido con Docker Desktop)

### 🎯 Inicio Rápido

#### 🌟 Opción 1: Script Automático (Recomendado)

**Linux/Mac:**
```bash
chmod +x start-docker.sh
./start-docker.sh
```

**Windows (PowerShell):**
```powershell
.\start-docker.ps1
```

#### 🌟 Opción 2: Comando Manual

```bash
# 1. Crear directorios necesarios
mkdir -p instance logs

# 2. Construir y levantar
docker-compose up -d

# 3. Ver logs (opcional)
docker-compose logs -f
```

### 🌐 Acceso a la Aplicación

Una vez ejecutándose:
- **🌐 Aplicación**: http://localhost:5000
- **📚 API Docs**: http://localhost:5000/swagger-ui

### 📋 Comandos Útiles

```bash
# Ver estado
docker-compose ps

# Ver logs
docker-compose logs -f

# Detener aplicación
docker-compose down

# Reiniciar
docker-compose restart

# Reconstruir imagen
docker-compose build --no-cache
docker-compose up -d
```

### 🗄️ Persistencia de Datos

- **Base de datos**: `./instance/` → `/app/instance`
- **Logs**: `./logs/` → `/app/logs`

Los datos se mantienen entre reinicios del contenedor.

### 🔧 Configuración

El `docker-compose.yml` incluye:
- ✅ Puerto 5000 expuesto
- ✅ Volúmenes persistentes
- ✅ Variables de entorno por defecto
- ✅ Reinicio automático

### 🚨 Troubleshooting

#### ❌ Puerto 5000 ocupado
```bash
# Cambiar puerto en docker-compose.yml
ports:
  - "5001:5000"  # Cambiar 5000 por 5001
```

#### ❌ Error de permisos
```bash
# En Linux/Mac
sudo chown -R $USER:$USER instance logs
```

#### ❌ Docker no ejecutándose
- Inicia Docker Desktop
- Verifica que el servicio esté activo

### 🎉 ¡Listo!

Tu Sistema de Gestión de Inventario está ejecutándose en Docker con:
- 🐳 Contenedor optimizado
- 💾 Datos persistentes
- 🔄 Reinicio automático
- 📊 Logs accesibles

**¡Disfruta tu aplicación!** 🚀
