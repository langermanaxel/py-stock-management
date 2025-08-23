# 🚀 Guía de Configuración CI/CD - Paso a Paso

## 📋 Resumen de lo que vamos a configurar

✅ **GitHub Actions** - CI/CD automático  
✅ **SonarCloud** - Análisis de calidad del código  
✅ **Dependabot** - Actualizaciones automáticas de dependencias  
✅ **Pre-commit hooks** - Validación antes de cada commit  
✅ **Badges personalizados** - Estado del proyecto en el README  

---

## 🎯 PASO 1: Personalizar Badges del README

### 🔧 Opción Automática (Recomendada)
```bash
# Ejecutar el script de personalización
python personalize_badges.py
```

### 🔧 Opción Manual
1. **Editar README.md** - Reemplazar:
   - `USERNAME` → Tu nombre de usuario de GitHub
   - `REPO_NAME` → Nombre de tu repositorio

2. **Ejemplo de cambio**:
   ```markdown
   # Antes
   [![CI/CD Pipeline](https://github.com/USERNAME/REPO_NAME/workflows/🚀%20CI%2FCD%20Pipeline/badge.svg)]
   
   # Después
   [![CI/CD Pipeline](https://github.com/tu-usuario/stock_management/workflows/🚀%20CI%2FCD%20Pipeline/badge.svg)]
   ```

---

## 🔧 PASO 2: Configurar SonarCloud

### 1. 🌐 Crear cuenta en SonarCloud
- Ve a [https://sonarcloud.io/](https://sonarcloud.io/)
- Haz clic en "Log in" → "Log in with GitHub"
- Autoriza la aplicación

### 2. 🔗 Conectar tu repositorio
- Haz clic en "Create new organization" (si es tu primera vez)
- Selecciona tu organización de GitHub
- Haz clic en "Set Up" en tu repositorio

### 3. 🔑 Obtener token de SonarCloud
- Ve a tu perfil → "My Account" → "Security"
- Genera un nuevo token
- **Copia el token** (lo necesitarás en el siguiente paso)

### 4. 🔐 Agregar token a GitHub Secrets
- Ve a tu repositorio en GitHub
- **Settings** → **Secrets and variables** → **Actions**
- Haz clic en **"New repository secret"**
- **Name**: `SONAR_TOKEN`
- **Value**: Pega el token de SonarCloud
- Haz clic en **"Add secret"**

### 5. ✅ Verificar configuración
- El workflow `sonarcloud.yml` se ejecutará automáticamente
- Ve a la pestaña **Actions** para ver el progreso
- Los resultados aparecerán en [SonarCloud](https://sonarcloud.io/)

---

## 🔄 PASO 3: Activar Dependabot

### 1. ⚙️ Ir a Settings del repositorio
- Ve a tu repositorio en GitHub
- Haz clic en **Settings** (pestaña)

### 2. 🔒 Security & analysis
- En el menú lateral, haz clic en **Security & analysis**
- Verás varias opciones para habilitar

### 3. ✅ Habilitar funcionalidades
- **Dependency graph**: ✅ **Enable**
- **Dependabot alerts**: ✅ **Enable**
- **Dependabot security updates**: ✅ **Enable**

### 4. 🔄 Configuración automática
- Dependabot usará el archivo `.github/dependabot.yml`
- Los PRs se crearán automáticamente los lunes
- Revisa y mergea según sea necesario

---

## 🪝 PASO 4: Instalar Pre-commit Hooks

### 🔧 Opción Automática (Recomendada)
```bash
# Ejecutar el script de instalación
python install_pre_commit.py
```

### 🔧 Opción Manual
```bash
# 1. Instalar pre-commit
pip install pre-commit

# 2. Instalar hooks
pre-commit install

# 3. Ejecutar en todos los archivos (opcional)
pre-commit run --all-files
```

### ✅ Verificar instalación
```bash
# Ver hooks instalados
pre-commit --version

# Ver hooks configurados
pre-commit run --all-files
```

---

## 🧪 PASO 5: Probar el Sistema

### 1. 💾 Hacer commit y push
```bash
# Agregar cambios
git add .

# Hacer commit (pre-commit se ejecutará automáticamente)
git commit -m "Configurar CI/CD completo"

# Push a GitHub
git push origin main
```

### 2. 🔍 Verificar GitHub Actions
- Ve a la pestaña **Actions** en tu repositorio
- Deberías ver workflows ejecutándose:
  - 🚀 CI/CD Pipeline
  - 🔒 CodeQL Security Analysis
  - 🔍 SonarCloud Analysis

### 3. 📊 Verificar badges
- Los badges en tu README deberían mostrar el estado actual
- Haz clic en ellos para ver detalles

---

## 📊 PASO 6: Monitorear y Mantener

### 🔍 GitHub Actions
- **Estado**: ✅/❌ en cada push/PR
- **Tiempo**: < 10 minutos por workflow
- **Logs**: Detalles completos en cada ejecución

### 🔒 CodeQL
- **Análisis**: Diario a las 2:00 AM UTC
- **Alertas**: En la pestaña Security
- **Vulnerabilidades**: 0 críticas/altas

### 🔍 SonarCloud
- **Calidad**: Quality Gate en cada análisis
- **Coverage**: Mínimo 80%
- **Duplicación**: Máximo 3%

### 🔄 Dependabot
- **Actualizaciones**: Semanales los lunes
- **PRs**: Automáticos con tests
- **Seguridad**: Alertas inmediatas

---

## 🚨 Troubleshooting Común

### ❌ Workflow falla
1. **Revisar logs** en GitHub Actions
2. **Verificar sintaxis YAML** en los workflows
3. **Comprobar secrets** configurados
4. **Revisar permisos** del repositorio

### ❌ SonarCloud no funciona
1. **Verificar SONAR_TOKEN** en GitHub Secrets
2. **Comprobar configuración** en sonar-project.properties
3. **Revisar logs** del workflow sonarcloud.yml

### ❌ Pre-commit falla
1. **Ejecutar manualmente**: `pre-commit run --all-files`
2. **Verificar configuración** en `.pre-commit-config.yaml`
3. **Revisar versiones** de las herramientas

### ❌ Dependabot no crea PRs
1. **Verificar configuración** en `.github/dependabot.yml`
2. **Comprobar permisos** del repositorio
3. **Revisar Settings** → Security & analysis

---

## 🎯 Comandos Útiles

### 🔧 Pre-commit
```bash
# Instalar hooks
pre-commit install

# Ejecutar en todos los archivos
pre-commit run --all-files

# Ejecutar en archivos específicos
pre-commit run --files archivo.py

# Actualizar hooks
pre-commit autoupdate

# Ver hooks instalados
pre-commit --version
```

### 🧪 Testing
```bash
# Ejecutar tests
pytest tests/ -v

# Con coverage
pytest tests/ -v --cov=app --cov-report=html

# Linting
flake8 .
black --check .
isort --check-only .
```

### 🔒 Seguridad
```bash
# Análisis de seguridad
bandit -r app/
safety check
pip-audit
```

---

## 📚 Recursos Adicionales

- **GitHub Actions**: [docs.github.com/en/actions](https://docs.github.com/en/actions)
- **SonarCloud**: [docs.sonarcloud.io](https://docs.sonarcloud.io/)
- **Dependabot**: [docs.github.com/en/dependabot](https://docs.github.com/en/dependabot)
- **Pre-commit**: [pre-commit.com](https://pre-commit.com/)

---

## 🎉 ¡Configuración Completada!

Con estos pasos tendrás:
- ✅ **CI/CD automático** en cada push/PR
- ✅ **Análisis de calidad** continuo
- ✅ **Actualizaciones automáticas** de dependencias
- ✅ **Validación automática** antes de cada commit
- ✅ **Badges informativos** en tu README

**¡Tu proyecto ahora tiene un sistema de CI/CD profesional!** 🚀
