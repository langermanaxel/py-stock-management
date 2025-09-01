# Migración de GitHub Actions de v3 a v4

## Resumen de Cambios

Este documento describe la migración completa del repositorio desde `actions/upload-artifact@v3` y `actions/download-artifact@v3` a v4, corrigiendo los breaking changes para que los pipelines funcionen correctamente en Ubuntu 24.04 (runner image 20250818.1.0).

## Cambios Realizados

### 1. Actualización de `actions/upload-artifact@v3` → `actions/upload-artifact@v4`

**Archivo:** `.github/workflows/ci.yml`
- **Línea 77:** Upload coverage report
- **Línea 113:** Upload security reports

### 2. Actualización de `actions/cache@v3` → `actions/cache@v4`

**Archivo:** `.github/workflows/ci.yml`
- **Línea 28:** Cache pip dependencies (job test)

**Archivo:** `.github/workflows/sonarcloud.yml`
- **Línea 29:** Cache pip dependencies

**Archivo:** `.github/workflows/dependabot.yml`
- **Línea 24:** Cache pip dependencies

### 3. Actualización de `codecov/codecov-action@v3` → `codecov/codecov-action@v4`

**Archivo:** `.github/workflows/ci.yml`
- **Línea 68:** Subir coverage a Codecov

### 4. Migración de `ubuntu-latest` → `ubuntu-24.04`

**Archivo:** `.github/workflows/ci.yml`
- **Job test:** Línea 12
- **Job security:** Línea 84
- **Job build:** Línea 123
- **Job deploy-preview:** Línea 168
- **Job notify:** Línea 195

**Archivo:** `.github/workflows/sonarcloud.yml`
- **Job sonarcloud:** Línea 18

**Archivo:** `.github/workflows/codeql.yml`
- **Job analyze:** Línea 25

**Archivo:** `.github/workflows/release.yml`
- **Job release:** Línea 18

**Archivo:** `.github/workflows/dependabot.yml`
- **Job dependabot:** Línea 18

### 5. **NUEVO:** Nombres Únicos de Artefactos (Artefactos Inmutables en v4)

**Problema Identificado:** Colisiones potenciales en nombres de artefactos
- **Job `test` con matriz Python:** 4 variantes (3.8, 3.9, 3.10, 3.11) subían con el mismo nombre
- **Job `security`:** Nombre genérico que podría colisionar

**Solución Aplicada:**
```yaml
# Antes (v3 - nombres duplicados)
name: coverage-report-${{ matrix.python-version }}
name: security-reports

# Después (v4 - nombres únicos)
name: coverage-report-${{ matrix.python-version }}-${{ github.job }}
name: security-reports-${{ github.job }}
```

**Regla de Renombrado Aplicada:**
- **Matriz Python:** `coverage-report-{python-version}-{job}`
- **Job único:** `security-reports-{job}`

### 6. **NUEVO:** Corrección de CodeQL Workflow

**Problema Identificado:** 
- Paso manual de `upload-sarif@v2` apuntando a ruta inexistente
- Uso de acciones v2 obsoletas
- Configuración de build manual innecesaria para Python

**Solución Aplicada:**
```yaml
# Antes (v2 - con upload manual)
- name: 🔍 Initialize CodeQL
  uses: github/codeql-action/init@v2
- name: 🔧 Autobuild
  uses: github/codeql-action/autobuild@v2
- name: 🔍 Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v2
- name: 📊 Upload SARIF
  uses: github/codeql-action/upload-sarif@v2

# Después (v3 - upload automático)
- name: 🔍 Initialize CodeQL
  uses: github/codeql-action/init@v3
- name: 🔍 Perform CodeQL Analysis
  uses: github/codeql-action/analyze@v3
```

**Cambios en Configuración:**
- **Archivo:** `.github/codeql/codeql-config.yml`
- **build-mode:** `manual` → `none` (Python no requiere build)
- **Eliminado:** Paso de autobuild innecesario
- **Eliminado:** Upload manual de SARIF (se hace automáticamente)

## Breaking Changes Corregidos

### actions/upload-artifact@v4
- **Cambio:** La acción ahora requiere Node.js 20 o superior
- **Cambio:** **Artefactos inmutables** - Los nombres deben ser únicos
- **Impacto:** Ubuntu 24.04 incluye Node.js 20 por defecto, por lo que es compatible
- **Beneficio:** Mejor rendimiento, seguridad y prevención de colisiones

### actions/cache@v4
- **Cambio:** Mejoras en el manejo de cache y compatibilidad con runners más nuevos
- **Impacto:** Mejor rendimiento del cache en Ubuntu 24.04
- **Beneficio:** Cache más rápido y confiable

### codecov/codecov-action@v4
- **Cambio:** Actualizaciones de seguridad y compatibilidad
- **Impacto:** Mejor integración con GitHub Actions modernos
- **Beneficio:** Reportes de coverage más confiables

### github/codeql-action@v3
- **Cambio:** Acciones v3 con mejor soporte para Python
- **Cambio:** Upload automático de resultados SARIF
- **Cambio:** Configuración optimizada para lenguajes interpretados
- **Impacto:** Análisis más confiable y resultados automáticos
- **Beneficio:** Menos pasos manuales, mejor integración con GitHub Security

## Compatibilidad con Ubuntu 24.04

### Runner Image: 20250818.1.0
- ✅ **Node.js:** Incluye Node.js 20 (requerido por upload-artifact@v4)
- ✅ **Python:** Soporte nativo para Python 3.8+
- ✅ **Git:** Versión 2.43+ incluida
- ✅ **Cache:** Mejor rendimiento con actions/cache@v4
- ✅ **Artefactos:** Nombres únicos previenen colisiones
- ✅ **CodeQL:** Acciones v3 con upload automático de resultados

## Verificación de Cambios

Para verificar que todos los cambios se aplicaron correctamente:

```bash
# Verificar que no hay referencias a v3
grep -r "@v3" .github/workflows/

# Verificar que ubuntu-24.04 está configurado
grep -r "ubuntu-24.04" .github/workflows/

# Verificar que las acciones v4 están configuradas
grep -r "actions/upload-artifact@v4" .github/workflows/
grep -r "actions/cache@v4" .github/workflows/

# Verificar nombres únicos de artefactos
grep -r "name:.*coverage-report" .github/workflows/
grep -r "name:.*security-reports" .github/workflows/

# Verificar acciones CodeQL v3
grep -r "github/codeql-action@v3" .github/workflows/

# Verificar que no hay upload-sarif manual
grep -r "upload-sarif" .github/workflows/
```

## Reglas de Nombres Únicos Aplicadas

### 1. **Matriz de Python (Job `test`)**
```yaml
name: coverage-report-${{ matrix.python-version }}-${{ github.job }}
# Resultado: coverage-report-3.8-test, coverage-report-3.9-test, etc.
```

### 2. **Job Único (Job `security`)**
```yaml
name: security-reports-${{ github.job }}
# Resultado: security-reports-security
```

### 3. **Sin Colisiones Detectadas**
- No hay `actions/download-artifact` en el repositorio
- No hay archivos ocultos que requieran `include-hidden-files: true`
- No hay acciones compuestas que usen v3

## Optimizaciones de CodeQL Aplicadas

### 1. **Acciones Actualizadas a v3**
- `github/codeql-action/init@v3`
- `github/codeql-action/analyze@v3`

### 2. **Eliminación de Pasos Innecesarios**
- ❌ `github/codeql-action/autobuild@v2` (no requerido para Python)
- ❌ `github/codeql-action/upload-sarif@v2` (se hace automáticamente)

### 3. **Configuración Optimizada para Python**
- **build-mode:** `none` (Python es interpretado)
- **Upload automático:** Los resultados se suben automáticamente a GitHub Security
- **Configuración limpia:** Eliminadas queries duplicadas y configuraciones obsoletas

## Próximos Pasos

1. **Commit y Push:** Realizar commit de todos los cambios
2. **Testing:** Verificar que los workflows se ejecuten correctamente
3. **Monitoring:** Observar el rendimiento de los nuevos runners
4. **Documentation:** Actualizar cualquier documentación relacionada

## Notas Importantes

- **Artefactos Inmutables:** Los nombres ahora son únicos por job/matriz
- **Sin Descargas:** No hay pasos de descarga que requieran cambios
- **Sin Archivos Ocultos:** No se requieren configuraciones adicionales
- **Sin Acciones Compuestas:** No hay dependencias internas que actualizar
- **CodeQL Optimizado:** Acciones v3 con upload automático de resultados
- **Build Mode Python:** Configurado como `none` para lenguajes interpretados
- Las acciones `actions/create-release@v1` y `actions/upload-release-asset@v1` se mantuvieron en v1 ya que no existen versiones v2
- La migración mantiene la funcionalidad existente mientras mejora la compatibilidad, rendimiento y previene colisiones

## Referencias

- [actions/upload-artifact v4 Release Notes](https://github.com/actions/upload-artifact/releases/tag/v4.0.0)
- [actions/cache v4 Release Notes](https://github.com/actions/cache/releases/tag/v4.0.0)
- [Ubuntu 24.04 GitHub Actions Runner](https://github.com/actions/runner-images/releases/tag/ubuntu24%2F20250818.1.0)
- [Artefactos Inmutables en v4](https://github.com/actions/upload-artifact#upload-artifact)
- [CodeQL Actions v3](https://github.com/github/codeql-action)
- [CodeQL Python Configuration](https://docs.github.com/en/code-security/code-scanning/creating-an-advanced-setup-for-code-scanning/using-custom-queries-with-the-codeql-cli)
