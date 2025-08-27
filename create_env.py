#!/usr/bin/env python3
"""
Script para crear un archivo .env completo con todas las variables necesarias
"""

def create_env_file():
    """Crea un archivo .env completo"""
    
    env_content = """# 🔒 Variables de Entorno - Sistema de Gestión de Inventario

# =============================================================================
# 🗄️ CONFIGURACIÓN DE BASE DE DATOS
# =============================================================================
DATABASE_URL=sqlite:///instance/stock_management.db

# =============================================================================
# 🔐 CONFIGURACIÓN DE SEGURIDAD
# =============================================================================
SECRET_KEY=clave-super-secreta-para-desarrollo-cambiala-en-produccion
JWT_SECRET_KEY=clave-jwt-super-secreta-para-desarrollo-cambiala-en-produccion

# =============================================================================
# 🌐 CONFIGURACIÓN FLASK
# =============================================================================
FLASK_ENV=development
DEBUG=True
FLASK_RUN_HOST=127.0.0.1
FLASK_RUN_PORT=5000

# =============================================================================
# 🔧 CONFIGURACIÓN SQLALCHEMY
# =============================================================================
SQLALCHEMY_TRACK_MODIFICATIONS=False

# =============================================================================
# 📝 CONFIGURACIÓN CORS (CRÍTICO PARA EL FRONTEND)
# =============================================================================
CORS_ORIGINS=http://localhost:5000,http://127.0.0.1:5000,http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000
CORS_SUPPORTS_CREDENTIALS=True
CORS_EXPOSE_HEADERS=Set-Cookie,Authorization

# =============================================================================
# 🔐 CONFIGURACIÓN JWT/AUTENTICACIÓN
# =============================================================================
JWT_ACCESS_TOKEN_EXPIRES=3600
JWT_REFRESH_TOKEN_EXPIRES=2592000

# =============================================================================
# 📊 CONFIGURACIÓN DE LOGS
# =============================================================================
LOG_LEVEL=INFO
LOG_FILE=logs/app.log
"""
    
    try:
        with open('.env', 'w', encoding='utf-8') as f:
            f.write(env_content)
        
        print("✅ Archivo .env creado exitosamente")
        print("🔐 Variables de seguridad configuradas")
        print("🌐 CORS configurado para puertos 5000 y 8080")
        return True
        
    except Exception as e:
        print(f"❌ Error creando archivo .env: {e}")
        return False

def main():
    """Función principal"""
    
    print("🔧 CREADOR DE ARCHIVO .ENV")
    print("="*40)
    
    if create_env_file():
        print("\n💡 Ahora puedes ejecutar:")
        print("   python start_backend.py")
    else:
        print("\n❌ No se pudo crear el archivo .env")

if __name__ == "__main__":
    main()
