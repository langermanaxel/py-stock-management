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
    CORS_ORIGINS = os.environ.get('CORS_ORIGINS', 'http://localhost:3000,http://127.0.0.1:5000').split(',')
    
    # Configuración de logs
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    LOG_FILE = os.environ.get('LOG_FILE', 'logs/app.log')