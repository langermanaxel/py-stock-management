#!/usr/bin/env python3
"""
Script para configurar automáticamente el archivo .env
Guía al usuario a través de la configuración de variables de entorno
"""

import os
import secrets
import sys
from pathlib import Path

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step, description):
    """Imprime un paso del proceso"""
    print(f"\n{step}. {description}")
    print("-" * 40)

def generate_secret_key():
    """Genera una clave secreta segura"""
    return secrets.token_hex(32)

def generate_jwt_key():
    """Genera una clave JWT segura"""
    return secrets.token_urlsafe(32)

def get_user_input(prompt, default="", required=True):
    """Obtiene entrada del usuario con validación"""
    while True:
        if default:
            user_input = input(f"{prompt} [{default}]: ").strip()
            if not user_input:
                user_input = default
        else:
            user_input = input(f"{prompt}: ").strip()
        
        if required and not user_input:
            print("❌ Este campo es obligatorio. Intenta de nuevo.")
            continue
        
        return user_input

def get_database_choice():
    """Obtiene la elección de base de datos del usuario"""
    print("\n🗄️ Selecciona tu base de datos:")
    print("1. SQLite (recomendado para desarrollo)")
    print("2. PostgreSQL (recomendado para producción)")
    print("3. MySQL")
    print("4. Personalizada")
    
    while True:
        choice = input("Elige una opción (1-4): ").strip()
        
        if choice == "1":
            return "sqlite:///instance/stock_management.db"
        elif choice == "2":
            host = get_user_input("Host de PostgreSQL", "localhost")
            port = get_user_input("Puerto de PostgreSQL", "5432")
            database = get_user_input("Nombre de la base de datos", "stock_management")
            username = get_user_input("Usuario de PostgreSQL", "postgres")
            password = get_user_input("Password de PostgreSQL", "")
            return f"postgresql://{username}:{password}@{host}:{port}/{database}"
        elif choice == "3":
            host = get_user_input("Host de MySQL", "localhost")
            port = get_user_input("Puerto de MySQL", "3306")
            database = get_user_input("Nombre de la base de datos", "stock_management")
            username = get_user_input("Usuario de MySQL", "root")
            password = get_user_input("Password de MySQL", "")
            return f"mysql://{username}:{password}@{host}:{port}/{database}"
        elif choice == "4":
            return get_user_input("URL de conexión personalizada")
        else:
            print("❌ Opción inválida. Elige 1, 2, 3 o 4.")

def get_environment_choice():
    """Obtiene la elección de entorno del usuario"""
    print("\n🌐 Selecciona tu entorno:")
    print("1. Desarrollo (development)")
    print("2. Testing")
    print("3. Producción (production)")
    
    while True:
        choice = input("Elige una opción (1-3): ").strip()
        
        if choice == "1":
            return "development", True
        elif choice == "2":
            return "testing", False
        elif choice == "3":
            return "production", False
        else:
            print("❌ Opción inválida. Elige 1, 2 o 3.")

def create_env_file():
    """Crea el archivo .env con la configuración del usuario"""
    print_header("CONFIGURACIÓN DE VARIABLES DE ENTORNO")
    
    # Verificar si ya existe .env
    if os.path.exists(".env"):
        print("⚠️ El archivo .env ya existe.")
        overwrite = input("¿Quieres sobrescribirlo? (s/n): ").strip().lower()
        if overwrite not in ['s', 'si', 'sí', 'y', 'yes']:
            print("❌ Configuración cancelada.")
            return False
    
    print_step("1", "Configuración de Base de Datos")
    database_url = get_database_choice()
    
    print_step("2", "Configuración de Seguridad")
    print("🔐 Generando claves secretas seguras...")
    secret_key = generate_secret_key()
    jwt_secret_key = generate_jwt_key()
    
    print_step("3", "Configuración del Entorno")
    flask_env, debug_mode = get_environment_choice()
    
    print_step("4", "Configuración del Servidor")
    host = get_user_input("Host del servidor", "127.0.0.1")
    port = get_user_input("Puerto del servidor", "5000")
    
    print_step("5", "Configuración CORS")
    cors_origins = get_user_input("Orígenes CORS permitidos", "http://localhost:3000,http://127.0.0.1:5000")
    
    print_step("6", "Configuración JWT")
    access_expires = get_user_input("Expiración token acceso (segundos)", "3600")
    refresh_expires = get_user_input("Expiración token refresh (segundos)", "2592000")
    
    print_step("7", "Configuración de Logs")
    log_level = get_user_input("Nivel de logging", "INFO")
    log_file = get_user_input("Archivo de logs", "logs/app.log")
    
    # Crear directorio de logs si no existe
    log_dir = Path(log_file).parent
    log_dir.mkdir(parents=True, exist_ok=True)
    
    print_step("8", "Configuración de Email (opcional)")
    use_email = input("¿Quieres configurar email? (s/n): ").strip().lower()
    email_config = ""
    
    if use_email in ['s', 'si', 'sí', 'y', 'yes']:
        mail_server = get_user_input("Servidor SMTP", "smtp.gmail.com")
        mail_port = get_user_input("Puerto SMTP", "587")
        mail_username = get_user_input("Usuario de email", "")
        mail_password = get_user_input("Password de aplicación", "")
        
        email_config = f"""
# 📧 Configuración de Email
MAIL_SERVER={mail_server}
MAIL_PORT={mail_port}
MAIL_USE_TLS=True
MAIL_USERNAME={mail_username}
MAIL_PASSWORD={mail_password}"""
    
    # Crear contenido del archivo .env
    env_content = f"""# 🔒 Variables de Entorno - Sistema de Gestión de Inventario
# Archivo generado automáticamente por setup_env.py
# ⚠️ NUNCA subas este archivo al repositorio

# =============================================================================
# 🗄️ CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================
DATABASE_URL={database_url}

# =============================================================================
# 🔐 CONFIGURACIÓN DE SEGURIDAD
# =============================================================================
SECRET_KEY={secret_key}
JWT_SECRET_KEY={jwt_secret_key}

# =============================================================================
# 🌐 CONFIGURACIÓN FLASK
# =============================================================================
FLASK_ENV={flask_env}
DEBUG={str(debug_mode)}
FLASK_RUN_HOST={host}
FLASK_RUN_PORT={port}

# =============================================================================
# 🔧 CONFIGURACIÓN SQLALCHEMY
# =============================================================================
SQLALCHEMY_TRACK_MODIFICATIONS=False

# =============================================================================
# 📝 CONFIGURACIÓN CORS
# =============================================================================
CORS_ORIGINS={cors_origins}

# =============================================================================
# 🔐 CONFIGURACIÓN JWT/AUTENTICACIÓN
# =============================================================================
JWT_ACCESS_TOKEN_EXPIRES={access_expires}
JWT_REFRESH_TOKEN_EXPIRES={refresh_expires}

# =============================================================================
# 📊 CONFIGURACIÓN DE LOGS
# =============================================================================
LOG_LEVEL={log_level}
LOG_FILE={log_file}

# =============================================================================
# ⚠️ IMPORTANTE - SEGURIDAD
# =============================================================================
# 1. NUNCA subas este archivo al repositorio
# 2. Cambia todas las claves secretas en producción
# 3. Usa variables de entorno del sistema en producción
# 4. Rota las claves JWT regularmente
# 5. Usa HTTPS en producción{email_config}
"""
    
    # Escribir archivo .env
    try:
        with open(".env", "w", encoding="utf-8") as f:
            f.write(env_content)
        
        print("\n✅ Archivo .env creado exitosamente!")
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def show_next_steps():
    """Muestra los siguientes pasos después de crear .env"""
    print_header("PRÓXIMOS PASOS")
    
    print("\n🔧 CONFIGURACIÓN COMPLETADA:")
    print("   ✅ Archivo .env creado")
    print("   ✅ Variables de entorno configuradas")
    print("   ✅ Claves secretas generadas")
    
    print("\n🚀 PARA INICIAR EL PROYECTO:")
    print("   1. Instalar dependencias: pip install -r requirements.txt")
    print("   2. Inicializar base de datos: python manage.py db init")
    print("   3. Crear migración: python manage.py db migrate")
    print("   4. Aplicar migración: python manage.py db upgrade")
    print("   5. Crear usuario admin: python manage.py user create-admin")
    print("   6. Ejecutar aplicación: python run.py")
    
    print("\n🧪 PARA EJECUTAR TESTS:")
    print("   pytest tests/ -v")
    
    print("\n🔍 PARA VERIFICAR CONFIGURACIÓN:")
    print("   python -c \"from dotenv import load_dotenv; load_dotenv(); import os; print('DATABASE_URL:', os.getenv('DATABASE_URL'))\"")
    
    print("\n⚠️ RECORDATORIOS DE SEGURIDAD:")
    print("   • El archivo .env ya está en .gitignore")
    print("   • Cambia las claves secretas en producción")
    print("   • Usa HTTPS en producción")
    print("   • Rota las claves JWT regularmente")

def main():
    """Función principal"""
    print("🔧 CONFIGURADOR AUTOMÁTICO DE VARIABLES DE ENTORNO")
    print("Sistema de Gestión de Inventario")
    print("="*50)
    
    try:
        # Verificar si existe env.example
        if not os.path.exists("env.example"):
            print("❌ Error: No se encontró env.example")
            print("   Asegúrate de estar en el directorio raíz del proyecto")
            sys.exit(1)
        
        # Crear archivo .env
        if create_env_file():
            show_next_steps()
            
            print("\n" + "="*60)
            print("🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
            print("="*60)
            print("\n✨ Tu archivo .env está listo para usar")
            print("🚀 ¡Puedes continuar con la instalación del proyecto!")
        else:
            print("\n❌ No se pudo crear el archivo .env")
            print("   Revisa los errores e intenta de nuevo")
            sys.exit(1)
        
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
