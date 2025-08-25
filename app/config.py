from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    # Configuración de la aplicación
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'clave-super-secreta-para-desarrollo'
    
    # Configuración de la base de datos
    # Prioriza DATABASE_URL del entorno, si no usa SQLite por defecto
    basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    database_path = os.path.join(basedir, 'instance', 'stock_management.db')
    
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or f"sqlite:///{database_path}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configuración de Flask
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # Configuración de CORS
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:5000,http://127.0.0.1:5000,http://localhost:8080,http://127.0.0.1:8080').split(',')
    
    # Configuración de logs
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')
    
    # 🔐 Configuración JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'clave-jwt-super-secreta-para-desarrollo'
    JWT_ACCESS_TOKEN_EXPIRES = int(os.environ.get('JWT_ACCESS_TOKEN_EXPIRES', 3600))  # 1 hora
    JWT_REFRESH_TOKEN_EXPIRES = int(os.environ.get('JWT_REFRESH_TOKEN_EXPIRES', 2592000))  # 30 días
    
    # 📚 Configuración de la API
    API_TITLE = os.environ.get('API_TITLE', 'Sistema de Gestión de Inventario API')
    API_VERSION = os.environ.get('API_VERSION', 'v1')
    OPENAPI_VERSION = os.environ.get('OPENAPI_VERSION', '3.0.2')