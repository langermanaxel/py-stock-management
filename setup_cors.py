#!/usr/bin/env python3
"""
Script para configurar automáticamente CORS y variables de entorno
para resolver problemas de autenticación entre puertos diferentes.
"""

import os
import shutil
from pathlib import Path

def setup_environment():
    """Configura el archivo .env con la configuración correcta de CORS"""
    
    print("🔧 Configurando entorno para resolver problemas de CORS...")
    
    # Verificar si existe .env
    env_file = Path('.env')
    env_example = Path('env.example')
    
    if not env_example.exists():
        print("❌ No se encontró env.example")
        return False
    
    # Crear .env desde env.example si no existe
    if not env_file.exists():
        print("📝 Creando archivo .env desde env.example...")
        shutil.copy(env_example, env_file)
        print("✅ Archivo .env creado")
    else:
        print("📝 Archivo .env ya existe, actualizando configuración...")
    
    # Leer el contenido actual
    with open(env_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Actualizar configuración de CORS
    cors_origins = "http://localhost:5000,http://127.0.0.1:5000,http://localhost:8080,http://127.0.0.1:8080,http://localhost:3000"
    
    # Buscar y reemplazar CORS_ORIGINS
    if 'CORS_ORIGINS=' in content:
        # Reemplazar línea existente
        lines = content.split('\n')
        for i, line in enumerate(lines):
            if line.startswith('CORS_ORIGINS='):
                lines[i] = f'CORS_ORIGINS={cors_origins}'
                break
        content = '\n'.join(lines)
    else:
        # Agregar si no existe
        content += f'\n# Configuración CORS para desarrollo\nCORS_ORIGINS={cors_origins}\n'
    
    # Agregar configuraciones adicionales de CORS
    cors_configs = [
        'CORS_SUPPORTS_CREDENTIALS=True',
        'CORS_EXPOSE_HEADERS=Set-Cookie,Authorization'
    ]
    
    for config in cors_configs:
        if config not in content:
            content += f'\n{config}\n'
    
    # Escribir archivo actualizado
    with open(env_file, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Configuración de CORS actualizada")
    print(f"🌐 Orígenes permitidos: {cors_origins}")
    print("🔐 Credenciales habilitadas para CORS")
    
    return True

def show_next_steps():
    """Muestra los siguientes pasos para el usuario"""
    
    print("\n" + "="*60)
    print("🚀 PRÓXIMOS PASOS PARA RESOLVER EL PROBLEMA:")
    print("="*60)
    
    print("\n1️⃣ REINICIAR EL BACKEND:")
    print("   - Detén el servidor Flask (Ctrl+C)")
    print("   - Ejecuta: python run.py")
    
    print("\n2️⃣ VERIFICAR CONFIGURACIÓN:")
    print("   - El backend debe estar en: http://127.0.0.1:5000")
    print("   - El frontend debe estar en: http://localhost:8080")
    
    print("\n3️⃣ PROBAR CONEXIÓN:")
    print("   - Abre http://localhost:8080 en tu navegador")
    print("   - Intenta hacer login con credenciales válidas")
    
    print("\n4️⃣ VERIFICAR EN CONSOLA DEL NAVEGADOR:")
    print("   - F12 → Console → Buscar errores de CORS")
    print("   - Network → Ver si las peticiones llegan al backend")
    
    print("\n5️⃣ SI SIGUE EL PROBLEMA:")
    print("   - Verifica que el backend esté ejecutándose")
    print("   - Revisa los logs del backend")
    print("   - Ejecuta: curl -X POST http://127.0.0.1:5000/api/auth/login")
    
    print("\n" + "="*60)

def main():
    """Función principal"""
    
    print("🔧 CONFIGURADOR DE CORS PARA STOCK MANAGEMENT")
    print("="*50)
    
    try:
        if setup_environment():
            show_next_steps()
        else:
            print("❌ Error al configurar el entorno")
            
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Intenta ejecutar el script manualmente")

if __name__ == "__main__":
    main()
