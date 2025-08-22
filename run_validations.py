#!/usr/bin/env python3
"""
Script para ejecutar validaciones rápidamente
"""

import subprocess
import sys
from pathlib import Path

def run_command(command, description):
    """Ejecutar comando y mostrar resultado"""
    print(f"\n🔧 {description}")
    print(f"   Comando: {command}")
    print("-" * 60)
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True,
            cwd=Path(__file__).parent
        )
        
        if result.returncode == 0:
            print("✅ ÉXITO")
            if result.stdout:
                print(result.stdout)
        else:
            print("❌ ERROR")
            if result.stderr:
                print(result.stderr)
            if result.stdout:
                print("STDOUT:", result.stdout)
                
        return result.returncode == 0
        
    except Exception as e:
        print(f"❌ ERROR EJECUTANDO COMANDO: {e}")
        return False

def main():
    """Función principal"""
    print("🚀 EJECUTOR RÁPIDO DE VALIDACIONES")
    print("=" * 60)
    
    # Verificar que estamos en el directorio correcto
    if not Path("app/validators").exists():
        print("❌ Error: No se encontró el directorio app/validators")
        print("   Asegúrate de ejecutar este script desde la raíz del proyecto")
        return
    
    # Ejecutar tests de validaciones
    success = True
    
    print("📋 Ejecutando tests de validaciones...")
    
    # Test 1: Validaciones de stock
    success &= run_command(
        "python -m pytest tests/test_validations.py::TestStockValidators -v",
        "Tests de validaciones de stock"
    )
    
    # Test 2: Validaciones de órdenes
    success &= run_command(
        "python -m pytest tests/test_validations.py::TestOrderValidators -v",
        "Tests de validaciones de órdenes"
    )
    
    # Test 3: Validaciones de órdenes de compra
    success &= run_command(
        "python -m pytest tests/test_validations.py::TestPurchaseOrderValidators -v",
        "Tests de validaciones de órdenes de compra"
    )
    
    # Test 4: Tests específicos del bug
    success &= run_command(
        "python -m pytest tests/test_validations.py::TestOrderCompletionBug -v",
        "Tests específicos del bug 'formulario me dice que tengo que completarlo'"
    )
    
    # Test 5: Todos los tests de validaciones
    success &= run_command(
        "python -m pytest tests/test_validations.py -v",
        "Todos los tests de validaciones"
    )
    
    # Mostrar resumen
    print("\n" + "=" * 60)
    if success:
        print("🎉 TODOS LOS TESTS DE VALIDACIONES PASARON")
        print("\n✅ Las validaciones están funcionando correctamente")
        print("✅ El bug 'formulario me dice que tengo que completarlo' está solucionado")
        print("✅ El sistema de validaciones centralizadas está operativo")
    else:
        print("❌ ALGUNOS TESTS FALLARON")
        print("\n🔧 Revisa los errores arriba y corrige los problemas")
        print("💡 Asegúrate de que todas las dependencias estén instaladas")
    
    print("\n💡 Comandos útiles:")
    print("   python demo_validations.py          # Demostración interactiva")
    print("   python -m pytest tests/ -v         # Todos los tests")
    print("   python -m pytest tests/test_validations.py -v --tb=long  # Con más detalles")

if __name__ == "__main__":
    main()
