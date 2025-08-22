# Dockerfile para Sistema de Gestión de Inventario
# Multi-stage build para optimizar el tamaño final

# =============================================================================
# STAGE 1: Build dependencies
# =============================================================================
FROM python:3.11-slim as builder

# Instalar dependencias del sistema necesarias para compilar
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Crear directorio de trabajo
WORKDIR /app

# Copiar archivos de dependencias
COPY requirements.txt .

# Crear entorno virtual e instalar dependencias
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
RUN pip install --no-cache-dir --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt

# =============================================================================
# STAGE 2: Runtime image
# =============================================================================
FROM python:3.11-slim

# Instalar dependencias del sistema para runtime
RUN apt-get update && apt-get install -y \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && apt-get clean

# Crear usuario no-root para seguridad
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Crear directorio de trabajo
WORKDIR /app

# Copiar entorno virtual desde el stage de build
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copiar código de la aplicación
COPY app/ ./app/
COPY templates/ ./templates/
COPY static/ ./static/
COPY run.py .
COPY app.py .

# Crear directorio para la base de datos
RUN mkdir -p instance && chown -R appuser:appuser instance

# Cambiar al usuario no-root
USER appuser

# Exponer puerto
EXPOSE 5000

# Variables de entorno por defecto
ENV FLASK_APP=run.py
ENV FLASK_ENV=production
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Comando por defecto
CMD ["python", "run.py"]
