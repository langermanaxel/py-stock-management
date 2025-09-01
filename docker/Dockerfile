# Dockerfile mínimo para Sistema de Gestión de Inventario
# ¡Levanta en 1 comando con: docker-compose up!

FROM python:3.11-slim

# Instalar dependencias mínimas
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Directorio de trabajo
WORKDIR /app

# Copiar dependencias e instalar
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar aplicación
COPY . .

# Crear directorio para base de datos
RUN mkdir -p instance logs

# Exponer puerto
EXPOSE 5000

# Variables de entorno por defecto
ENV FLASK_APP=run.py
ENV FLASK_ENV=development
ENV DEBUG=true
ENV DATABASE_URL=sqlite:///instance/stock_management.db

# Comando de inicio
CMD ["python", "run.py"]
