#!/usr/bin/env python3
"""
Script para debuggear el problema del token JWT
"""

import requests
import json
import sys
from pathlib import Path

def test_login_and_token():
    """Prueba el login y analiza el token generado"""
    print("🔍 DEBUGGEANDO TOKEN JWT")
    print("=" * 50)
    
    try:
        # URL base de la aplicación
        base_url = "http://localhost:5000"
        
        print("1. Probando login con credenciales de admin...")
        
        # Credenciales de admin
        login_data = {
            "username": "admin",
            "password": "Admin123!"
        }
        
        response = requests.post(
            f"{base_url}/api/auth/login",
            json=login_data,
            timeout=10
        )
        
        if response.status_code == 200:
            print("   ✅ Login exitoso")
            
            data = response.json()
            print(f"   📊 Respuesta del servidor:")
            print(f"      - access_token presente: {'access_token' in data}")
            print(f"      - refresh_token presente: {'refresh_token' in data}")
            print(f"      - user presente: {'user' in data}")
            
            if 'access_token' in data:
                token = data['access_token']
                print(f"   🔑 Token generado:")
                print(f"      - Longitud: {len(token)} caracteres")
                print(f"      - Formato: {token[:20]}...{token[-20:]}")
                
                # Analizar el token JWT
                analyze_jwt_token(token)
            else:
                print("   ❌ No se generó access_token")
                return False
                
        else:
            print(f"   ❌ Error en login: {response.status_code}")
            print(f"   Respuesta: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("❌ Error: No se puede conectar a la aplicación")
        print("   Asegúrate de que la aplicación esté ejecutándose en http://localhost:5000")
        return False
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False

def analyze_jwt_token(token):
    """Analiza un token JWT"""
    print("\n2. Analizando token JWT...")
    
    try:
        # Dividir el token en partes
        parts = token.split('.')
        print(f"   📋 Partes del token: {len(parts)}")
        
        if len(parts) != 3:
            print("   ❌ Token no tiene formato JWT válido (debe tener 3 partes)")
            return False
        
        # Decodificar header
        import base64
        import json
        
        # Agregar padding si es necesario
        header_padded = parts[0] + '=' * (4 - len(parts[0]) % 4)
        header_decoded = base64.b64decode(header_padded)
        header = json.loads(header_decoded)
        
        print(f"   📋 Header del token:")
        print(f"      - alg: {header.get('alg', 'N/A')}")
        print(f"      - typ: {header.get('typ', 'N/A')}")
        
        # Decodificar payload
        payload_padded = parts[1] + '=' * (4 - len(parts[1]) % 4)
        payload_decoded = base64.b64decode(payload_padded)
        payload = json.loads(payload_decoded)
        
        print(f"   📋 Payload del token:")
        print(f"      - sub: {payload.get('sub', 'N/A')} (tipo: {type(payload.get('sub', 'N/A'))})")
        print(f"      - exp: {payload.get('exp', 'N/A')}")
        print(f"      - iat: {payload.get('iat', 'N/A')}")
        print(f"      - role: {payload.get('role', 'N/A')}")
        print(f"      - username: {payload.get('username', 'N/A')}")
        
        # Verificar claims requeridos
        required_claims = ['sub', 'exp', 'iat']
        missing_claims = []
        
        for claim in required_claims:
            if claim not in payload:
                missing_claims.append(claim)
        
        if missing_claims:
            print(f"   ❌ Claims faltantes: {missing_claims}")
            return False
        else:
            print(f"   ✅ Todos los claims requeridos están presentes")
        
        # Verificar tipo de subject
        if not isinstance(payload.get('sub'), str):
            print(f"   ❌ Subject no es string: {type(payload.get('sub'))}")
            return False
        else:
            print(f"   ✅ Subject es string")
        
        # Verificar expiración
        import time
        now = int(time.time())
        exp = payload.get('exp', 0)
        
        if exp < now:
            print(f"   ❌ Token expirado (exp: {exp}, now: {now})")
            return False
        else:
            print(f"   ✅ Token no ha expirado (expira en {exp - now} segundos)")
        
        print("   ✅ Token JWT es válido según análisis")
        return True
        
    except Exception as e:
        print(f"   ❌ Error analizando token: {e}")
        return False

def test_jwt_validator():
    """Prueba el validador JWT del frontend"""
    print("\n3. Probando validador JWT del frontend...")
    
    try:
        # Leer el archivo jwt-validator.js
        validator_path = Path("static/js/jwt-validator.js")
        if not validator_path.exists():
            print("   ❌ Archivo jwt-validator.js no encontrado")
            return False
        
        with open(validator_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Verificar que el validador esté presente
        if "validateToken" in content:
            print("   ✅ Validador JWT encontrado en el frontend")
        else:
            print("   ❌ Validador JWT no encontrado en el frontend")
            return False
        
        # Verificar algoritmos válidos
        if "validAlgorithms" in content:
            print("   ✅ Configuración de algoritmos encontrada")
        else:
            print("   ❌ Configuración de algoritmos no encontrada")
            return False
        
        return True
        
    except Exception as e:
        print(f"   ❌ Error verificando validador: {e}")
        return False

def main():
    """Función principal"""
    print("🔧 DEBUG DE TOKEN JWT")
    print("=" * 50)
    print("Este script analiza el token JWT generado por el servidor")
    print("y verifica por qué el validador del frontend lo rechaza.")
    print()
    
    # Test 1: Login y análisis de token
    login_ok = test_login_and_token()
    
    # Test 2: Verificar validador
    validator_ok = test_jwt_validator()
    
    if login_ok and validator_ok:
        print("\n" + "=" * 50)
        print("🎉 ANÁLISIS COMPLETADO")
        print("✅ El token JWT parece ser válido")
        print("❓ El problema puede estar en la validación del frontend")
        print("\n💡 Posibles soluciones:")
        print("   1. Verificar que el validador JWT esté cargado correctamente")
        print("   2. Revisar la configuración de algoritmos válidos")
        print("   3. Verificar que no haya conflictos en la validación")
    else:
        print("\n" + "=" * 50)
        print("❌ PROBLEMAS ENCONTRADOS")
        print("Revisa los errores mostrados arriba.")
    
    return login_ok and validator_ok

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
