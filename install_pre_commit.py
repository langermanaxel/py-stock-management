#!/usr/bin/env python3
"""
Script para instalar y configurar pre-commit hooks automáticamente
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=True, capture_output=True, text=True)
        print(f"✅ {description} completado")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        print(f"   Salida de error: {e.stderr}")
        return None

def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Error: Se requiere Python 3.8+ (tienes {version.major}.{version.minor})")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    return True

def check_pip():
    """Verifica que pip esté disponible"""
    print("📦 Verificando pip...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True, check=True)
        print(f"✅ {result.stdout.strip()}")
        return True
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Error: pip no está disponible")
        return False

def install_pre_commit():
    """Instala pre-commit"""
    print("\n🪝 Instalando pre-commit...")
    
    # Verificar si ya está instalado
    try:
        result = subprocess.run([sys.executable, "-m", "pre_commit", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ pre-commit ya está instalado")
            return True
    except:
        pass
    
    # Instalar pre-commit
    result = run_command(f"{sys.executable} -m pip install pre-commit", "Instalando pre-commit")
    if result is None:
        return False
    
    print("✅ pre-commit instalado exitosamente")
    return True

def install_hooks():
    """Instala los hooks de pre-commit"""
    print("\n🔧 Instalando hooks de pre-commit...")
    
    # Verificar si existe el archivo de configuración
    if not os.path.exists(".pre-commit-config.yaml"):
        print("❌ Error: No se encontró .pre-commit-config.yaml")
        return False
    
    # Instalar hooks
    result = run_command(f"{sys.executable} -m pre_commit install", "Instalando hooks")
    if result is None:
        return False
    
    print("✅ Hooks instalados exitosamente")
    return True

def run_pre_commit():
    """Ejecuta pre-commit en todos los archivos"""
    print("\n🧪 Ejecutando pre-commit en todos los archivos...")
    
    result = run_command(f"{sys.executable} -m pre_commit run --all-files", "Ejecutando pre-commit")
    if result is None:
        print("⚠️ Algunos hooks fallaron. Esto es normal en la primera ejecución.")
        print("   Los hooks se ejecutarán automáticamente en el próximo commit.")
        return False
    
    print("✅ Todos los hooks pasaron exitosamente")
    return True

def show_manual_commands():
    """Muestra comandos para ejecutar manualmente si es necesario"""
    print("\n" + "="*60)
    print("📋 COMANDOS MANUALES (si los anteriores fallaron)")
    print("="*60)
    
    print("\n1. 🪝 Instalar pre-commit:")
    print("   pip install pre-commit")
    
    print("\n2. 🔧 Instalar hooks:")
    print("   pre-commit install")
    
    print("\n3. 🧪 Ejecutar en todos los archivos:")
    print("   pre-commit run --all-files")
    
    print("\n4. 🧪 Ejecutar en archivos específicos:")
    print("   pre-commit run --files archivo.py")
    
    print("\n5. 🔄 Actualizar hooks:")
    print("   pre-commit autoupdate")
    
    print("\n6. 📊 Ver hooks instalados:")
    print("   pre-commit --version")

def show_git_workflow():
    """Muestra el flujo de trabajo con Git y pre-commit"""
    print("\n" + "="*60)
    print("🚀 FLUJO DE TRABAJO CON PRE-COMMIT")
    print("="*60)
    
    print("\n1. 📝 Hacer cambios en el código")
    print("2. 💾 Agregar archivos: git add .")
    print("3. 🔄 Hacer commit: git commit -m 'Mensaje'")
    print("   → pre-commit se ejecutará automáticamente")
    print("4. 📤 Push: git push origin main")
    
    print("\n⚠️ IMPORTANTE:")
    print("   • Si pre-commit falla, corrige los errores")
    print("   • Vuelve a hacer git add . y git commit")
    print("   • Los hooks se ejecutarán nuevamente")
    
    print("\n🔧 HOOKS CONFIGURADOS:")
    print("   • Black - Formateo de código")
    print("   • isort - Ordenamiento de imports")
    print("   • Flake8 - Linting estático")
    print("   • MyPy - Type checking")
    print("   • Bandit - Análisis de seguridad")
    print("   • Safety - Verificación de dependencias")
    print("   • Prettier - Formateo de archivos")
    print("   • ESLint - Linting de JavaScript")

def main():
    """Función principal"""
    print("🚀 Instalador Automático de Pre-commit Hooks")
    print("="*50)
    
    # Verificaciones previas
    if not check_python_version():
        sys.exit(1)
    
    if not check_pip():
        sys.exit(1)
    
    # Instalación
    if not install_pre_commit():
        print("❌ Falló la instalación de pre-commit")
        show_manual_commands()
        sys.exit(1)
    
    if not install_hooks():
        print("❌ Falló la instalación de hooks")
        show_manual_commands()
        sys.exit(1)
    
    # Ejecutar pre-commit
    print("\n🧪 Probando pre-commit...")
    run_pre_commit()
    
    # Mostrar información adicional
    show_git_workflow()
    
    print("\n✨ ¡Instalación completada!")
    print("🎯 Los hooks se ejecutarán automáticamente en cada commit")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n❌ Instalación cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        show_manual_commands()
        sys.exit(1)
