#!/usr/bin/env python3
"""
Script para personalizar automáticamente los badges del README
Reemplaza USERNAME y REPO_NAME con los valores reales de tu repositorio
"""

import re
import os

def personalize_badges():
    """Personaliza los badges del README con tu información real"""
    
    print("🔧 Personalizando badges del README...")
    
    # Solicitar información del usuario
    username = input("👤 Ingresa tu nombre de usuario de GitHub: ").strip()
    repo_name = input("📦 Ingresa el nombre de tu repositorio: ").strip()
    
    if not username or not repo_name:
        print("❌ Error: Debes proporcionar tanto el username como el nombre del repositorio")
        return
    
    # Leer el README actual
    readme_path = "README.md"
    if not os.path.exists(readme_path):
        print(f"❌ Error: No se encontró el archivo {readme_path}")
        return
    
    with open(readme_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Reemplazar placeholders
    old_content = content
    content = content.replace("USERNAME", username)
    content = content.replace("REPO_NAME", repo_name)
    
    # Verificar si hubo cambios
    if old_content == content:
        print("ℹ️ No se encontraron placeholders para reemplazar")
        return
    
    # Escribir el README actualizado
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print("✅ Badges personalizados exitosamente!")
    print(f"👤 Username: {username}")
    print(f"📦 Repositorio: {repo_name}")
    print("\n🔗 URLs de los badges:")
    print(f"   CI/CD: https://github.com/{username}/{repo_name}/actions/workflows/ci.yml")
    print(f"   Tests: https://github.com/{username}/{repo_name}/actions/workflows/ci.yml")
    print(f"   Quality: https://github.com/{username}/{repo_name}/actions/workflows/ci.yml")
    
    # También actualizar otros archivos que contengan USERNAME/REPO_NAME
    update_other_files(username, repo_name)

def update_other_files(username, repo_name):
    """Actualiza otros archivos que contengan USERNAME/REPO_NAME"""
    
    files_to_update = [
        "pyproject.toml",
        ".github/dependabot.yml",
        "sonar-project.properties"
    ]
    
    print("\n🔄 Actualizando otros archivos...")
    
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

def show_next_steps():
    """Muestra los siguientes pasos para completar la configuración"""
    
    print("\n" + "="*60)
    print("🎯 PRÓXIMOS PASOS PARA COMPLETAR LA CONFIGURACIÓN")
    print("="*60)
    
    print("\n1. 🔧 CONFIGURAR SONARCLOUD:")
    print("   • Ve a https://sonarcloud.io/")
    print("   • Crea una cuenta o inicia sesión")
    print("   • Conecta tu repositorio de GitHub")
    print("   • Copia el token de SonarCloud")
    print("   • Ve a tu repositorio en GitHub > Settings > Secrets")
    print("   • Agrega el secret: SONAR_TOKEN")
    
    print("\n2. 🔄 ACTIVAR DEPENDABOT:")
    print("   • Ve a tu repositorio en GitHub")
    print("   • Settings > Security & analysis")
    print("   • Habilita 'Dependency graph'")
    print("   • Habilita 'Dependabot alerts'")
    print("   • Habilita 'Dependabot security updates'")
    
    print("\n3. 🪝 INSTALAR PRE-COMMIT HOOKS:")
    print("   • Ejecuta: pip install pre-commit")
    print("   • Ejecuta: pre-commit install")
    print("   • Ejecuta: pre-commit run --all-files")
    
    print("\n4. 🧪 PROBAR EL SISTEMA:")
    print("   • Haz un commit y push")
    print("   • Verifica que se ejecuten los workflows en GitHub Actions")
    print("   • Revisa los badges en tu README")
    
    print("\n5. 📊 MONITOREAR:")
    print("   • GitHub Actions: Estado de CI/CD")
    print("   • CodeQL: Alertas de seguridad")
    print("   • SonarCloud: Calidad del código")
    print("   • Dependabot: Actualizaciones automáticas")

if __name__ == "__main__":
    print("🚀 Personalizador de Badges para CI/CD")
    print("="*50)
    
    try:
        personalize_badges()
        show_next_steps()
    except KeyboardInterrupt:
        print("\n\n❌ Operación cancelada por el usuario")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n✨ ¡Configuración completada!")
