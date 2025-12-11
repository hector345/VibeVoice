#!/usr/bin/env python3
"""
Test de conexión rápida con LM Studio

Este script verifica que LM Studio esté funcionando correctamente
y muestra los modelos disponibles.

Uso:
    python demo/test_lm_studio_connection.py
    python demo/test_lm_studio_connection.py --url http://localhost:1234
"""

import argparse
import requests
import json
import sys


def test_connection(base_url: str = "http://127.0.0.1:1234"):
    """Prueba la conexión con LM Studio"""
    
    print(f"🔗 Probando conexión con LM Studio en: {base_url}")
    print("=" * 60)
    
    # Test 1: Verificar modelos disponibles
    try:
        models_url = f"{base_url.rstrip('/')}/v1/models"
        print(f"📡 GET {models_url}")
        
        response = requests.get(models_url, timeout=5)
        
        if response.status_code == 200:
            print("✅ Conexión exitosa!")
            
            models_data = response.json()
            models = [model['id'] for model in models_data.get('data', [])]
            
            if models:
                print(f"🤖 Modelos disponibles ({len(models)}):")
                for i, model in enumerate(models, 1):
                    print(f"  {i}. {model}")
            else:
                print("⚠️  No hay modelos cargados en LM Studio")
                return False
                
        else:
            print(f"❌ Error HTTP {response.status_code}: {response.text}")
            return False
            
    except requests.ConnectionError:
        print("❌ Error: No se pudo conectar con LM Studio")
        print("💡 Asegúrate de que:")
        print("   - LM Studio esté ejecutándose")
        print("   - El servidor local esté iniciado en el puerto 1234")
        print("   - No haya firewall bloqueando la conexión")
        return False
        
    except requests.Timeout:
        print("❌ Error: Timeout - LM Studio no responde")
        return False
        
    except Exception as e:
        print(f"❌ Error inesperado: {e}")
        return False
    
    # Test 2: Probar endpoint de chat (solo si hay modelos)
    if models:
        try:
            chat_url = f"{base_url.rstrip('/')}/v1/chat/completions"
            print(f"\n📡 Probando endpoint de chat...")
            print(f"POST {chat_url}")
            
            test_payload = {
                "messages": [{"role": "user", "content": "Hello"}],
                "max_tokens": 10,
                "model": models[0]  # Usar el primer modelo disponible
            }
            
            response = requests.post(
                chat_url,
                json=test_payload,
                headers={"Content-Type": "application/json"},
                timeout=15
            )
            
            if response.status_code == 200:
                result = response.json()
                message = result.get('choices', [{}])[0].get('message', {}).get('content', 'No content')
                print(f"✅ Chat endpoint funcionando!")
                print(f"🤖 Respuesta de prueba: {message}")
            else:
                print(f"⚠️  Chat endpoint retornó HTTP {response.status_code}")
                print(f"   Respuesta: {response.text}")
                
        except Exception as e:
            print(f"⚠️  Error probando chat endpoint: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Prueba de conexión completada!")
    return True


def main():
    """Función principal"""
    parser = argparse.ArgumentParser(description="Test LM Studio connection")
    parser.add_argument(
        "--url", 
        type=str, 
        default="http://127.0.0.1:1234",
        help="URL base de LM Studio (default: http://127.0.0.1:1234)"
    )
    
    args = parser.parse_args()
    
    success = test_connection(args.url)
    
    if success:
        print("\n🎉 ¡LM Studio está listo para usar con el chat demo!")
        print("💡 Ejecuta el demo principal con:")
        print("   python demo/chat_with_lm_studio.py")
    else:
        print("\n❌ Hay problemas con la conexión a LM Studio")
        print("🔧 Pasos para solucionar:")
        print("   1. Abrir LM Studio")
        print("   2. Cargar un modelo en la pestaña 'Chat'")
        print("   3. Ir a 'Local Server' y hacer clic en 'Start Server'")
        print("   4. Verificar que el puerto sea 1234")
        sys.exit(1)


if __name__ == "__main__":
    main()