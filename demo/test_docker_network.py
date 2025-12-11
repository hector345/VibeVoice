#!/usr/bin/env python3
"""
Test de conectividad con LM Studio desde Docker
"""
import os
import requests

def test_connection():
    lm_studio_url = os.environ.get('LM_STUDIO_URL', 'http://127.0.0.1:1234')
    
    print(f"🔗 Probando conexión a: {lm_studio_url}")
    
    urls_to_try = [
        lm_studio_url,
        "http://host.docker.internal:1234",
        "http://127.0.0.1:1234",
        "http://localhost:1234"
    ]
    
    for url in urls_to_try:
        try:
            print(f"Probando: {url}")
            response = requests.get(f"{url}/v1/models", timeout=5)
            if response.status_code == 200:
                models = response.json().get('data', [])
                print(f"✅ ÉXITO con {url}")
                print(f"Modelos encontrados: {len(models)}")
                for model in models:
                    print(f"  - {model['id']}")
                return url
            else:
                print(f"❌ {url} - HTTP {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    print("❌ No se pudo conectar con ninguna URL")
    return None

if __name__ == "__main__":
    test_connection()