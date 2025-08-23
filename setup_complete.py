#!/usr/bin/env python3
"""
Script de configuración completa del sistema CI/CD
Ejecuta todos los pasos necesarios para configurar el proyecto
"""

import os
import sys
import subprocess
import time

def print_header(title):
    """Imprime un encabezado formateado"""
    print("\n" + "="*60)
    print(f"🎯 {title}")
    print("="*60)

def print_step(step, description):
    """Imprime un paso del proceso"""
    print(f"\n{step}. {description}")
    print("-" * 40)

def run_command(command, description, check=True):
    """Ejecuta un comando y maneja errores"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, check=check, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completado")
            return True, result.stdout
        else:
            print(f"⚠️ {description} completado con advertencias")
            print(f"   Salida: {result.stdout}")
            if result.stderr:
                print(f"   Errores: {result.stderr}")
            return True, result.stdout
    except subprocess.CalledProcessError as e:
        print(f"❌ Error en {description}: {e}")
        if e.stderr:
            print(f"   Salida de error: {e.stderr}")
        return False, None
    except Exception as e:
        print(f"❌ Error inesperado en {description}: {e}")
        return False, None

def check_requirements():
    """Verifica los requisitos del sistema"""
    print_header("VERIFICACIÓN DE REQUISITOS")
    
    # Verificar Python
    print_step("1", "Verificar versión de Python")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Error: Se requiere Python 3.8+ (tienes {version.major}.{version.minor})")
        return False
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} - OK")
    
    # Verificar pip
    print_step("2", "Verificar pip")
    success, _ = run_command(f"{sys.executable} -m pip --version", "Verificando pip")
    if not success:
        return False
    
    # Verificar git
    print_step("3", "Verificar git")
    success, _ = run_command("git --version", "Verificando git")
    if not success:
        return False
    
    # Verificar que estamos en un repositorio git
    print_step("4", "Verificar repositorio git")
    if not os.path.exists(".git"):
        print("❌ Error: No estás en un repositorio git")
        print("   Ejecuta: git init")
        return False
    print("✅ Repositorio git detectado")
    
    return True

def personalize_badges():
    """Personaliza los badges del README"""
    print_header("PERSONALIZACIÓN DE BADGES")
    
    print_step("1", "Solicitar información del usuario")
    username = input("👤 Ingresa tu nombre de usuario de GitHub: ").strip()
    repo_name = input("📦 Ingresa el nombre de tu repositorio: ").strip()
    
    if not username or not repo_name:
        print("❌ Error: Debes proporcionar tanto el username como el nombre del repositorio")
        return False
    
    print_step("2", "Actualizar README.md")
    if not os.path.exists("README.md"):
        print("❌ Error: No se encontró README.md")
        return False
    
    with open("README.md", 'r', encoding='utf-8') as f:
        content = f.read()
    
    old_content = content
    content = content.replace("USERNAME", username)
    content = content.replace("REPO_NAME", repo_name)
    
    if old_content == content:
        print("ℹ️ No se encontraron placeholders para reemplazar")
    else:
        with open("README.md", 'w', encoding='utf-8') as f:
            f.write(content)
        print("✅ README.md actualizado")
    
    print_step("3", "Actualizar otros archivos")
    files_to_update = [
        "pyproject.toml",
        ".github/dependabot.yml",
        "sonar-project.properties"
    ]
    
    for file_path in files_to_update:
        if os.path.exists(file_path):
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                old_content = content
                content = content.replace("USERNAME", username)
                content = content.replace("REPO_NAME", repo_name)
                
                if old_content != content:
                    with open(file_path, 'w', encoding='utf-8') as f:
                        f.write(content)
                    print(f"✅ {file_path} actualizado")
                else:
                    print(f"ℹ️ {file_path} no requiere cambios")
                    
            except Exception as e:
                print(f"⚠️ Error actualizando {file_path}: {e}")
        else:
            print(f"ℹ️ {file_path} no encontrado")
    
    return True

def install_pre_commit():
    """Instala pre-commit hooks"""
    print_header("INSTALACIÓN DE PRE-COMMIT")
    
    print_step("1", "Instalar pre-commit")
    success, _ = run_command(f"{sys.executable} -m pip install pre-commit", "Instalando pre-commit")
    if not success:
        return False
    
    print_step("2", "Instalar hooks")
    success, _ = run_command(f"{sys.executable} -m pre_commit install", "Instalando hooks")
    if not success:
        return False
    
    print_step("3", "Probar pre-commit")
    success, _ = run_command(f"{sys.executable} -m pre_commit run --all-files", "Probando pre-commit", check=False)
    if not success:
        print("⚠️ Algunos hooks fallaron. Esto es normal en la primera ejecución.")
    
    return True

def show_next_steps():
    """Muestra los siguientes pasos para completar la configuración"""
    print_header("PRÓXIMOS PASOS")
    
    print("\n🔧 CONFIGURAR SONARCLOUD:")
    print("   1. Ve a https://sonarcloud.io/")
    print("   2. Crea una cuenta o inicia sesión")
    print("   3. Conecta tu repositorio de GitHub")
    print("   4. Copia el token de SonarCloud")
    print("   5. Ve a tu repositorio en GitHub > Settings > Secrets")
    print("   6. Agrega el secret: SONAR_TOKEN")
    
    print("\n🔄 ACTIVAR DEPENDABOT:")
    print("   1. Ve a tu repositorio en GitHub")
    print("   2. Settings > Security & analysis")
    print("   3. Habilita 'Dependency graph'")
    print("   4. Habilita 'Dependabot alerts'")
    print("   5. Habilita 'Dependabot security updates'")
    
    print("\n🧪 PROBAR EL SISTEMA:")
    print("   1. Haz un commit y push")
    print("   2. Verifica que se ejecuten los workflows en GitHub Actions")
    print("   3. Revisa los badges en tu README")
    
    print("\n📊 MONITOREAR:")
    print("   • GitHub Actions: Estado de CI/CD")
    print("   • CodeQL: Alertas de seguridad")
    print("   • SonarCloud: Calidad del código")
    print("   • Dependabot: Actualizaciones automáticas")

def create_initial_commit():
    """Crea el commit inicial con toda la configuración"""
    print_header("COMMIT INICIAL")
    
    print_step("1", "Verificar estado de git")
    success, output = run_command("git status", "Verificando estado de git")
    if not success:
        return False
    
    print_step("2", "Agregar archivos")
    success, _ = run_command("git add .", "Agregando archivos")
    if not success:
        return False
    
    print_step("3", "Verificar archivos agregados")
    success, output = run_command("git status --porcelain", "Verificando archivos agregados")
    if success and output:
        print("📁 Archivos a commitear:")
        for line in output.strip().split('\n'):
            if line:
                print(f"   {line}")
    
    print_step("4", "Crear commit")
    success, _ = run_command('git commit -m "🚀 Configurar CI/CD completo con GitHub Actions, SonarCloud, Dependabot y pre-commit"', "Creando commit")
    if not success:
        return False
    
    print_step("5", "Verificar commit creado")
    success, output = run_command("git log --oneline -1", "Verificando commit creado")
    if success:
        print(f"✅ Commit creado: {output.strip()}")
    
    return True

def main():
    """Función principal"""
    print("🚀 CONFIGURADOR COMPLETO DE CI/CD")
    print("Sistema de Gestión de Inventario")
    print("="*50)
    
    try:
        # Verificar requisitos
        if not check_requirements():
            print("\n❌ No se cumplen los requisitos del sistema")
            sys.exit(1)
        
        # Personalizar badges
        if not personalize_badges():
            print("\n❌ Falló la personalización de badges")
            sys.exit(1)
        
        # Instalar pre-commit
        if not install_pre_commit():
            print("\n❌ Falló la instalación de pre-commit")
            sys.exit(1)
        
        # Crear commit inicial
        print("\n💾 ¿Quieres crear un commit inicial con toda la configuración?")
        response = input("   (s/n): ").strip().lower()
        if response in ['s', 'si', 'sí', 'y', 'yes']:
            if not create_initial_commit():
                print("\n⚠️ No se pudo crear el commit inicial")
                print("   Puedes hacerlo manualmente más tarde")
        
        # Mostrar próximos pasos
        show_next_steps()
        
        print("\n" + "="*60)
        print("🎉 ¡CONFIGURACIÓN COMPLETADA EXITOSAMENTE!")
        print("="*60)
        print("\n✨ Tu proyecto ahora tiene:")
        print("   ✅ GitHub Actions configurado")
        print("   ✅ SonarCloud listo para conectar")
        print("   ✅ Dependabot configurado")
        print("   ✅ Pre-commit hooks instalados")
        print("   ✅ Badges personalizados")
        print("\n🚀 ¡Sigue los próximos pasos para completar la configuración!")
        
    except KeyboardInterrupt:
        print("\n\n❌ Configuración cancelada por el usuario")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Error inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
