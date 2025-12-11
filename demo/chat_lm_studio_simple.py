#!/usr/bin/env python3
"""
Chat Demo Simplificado con LM Studio

Esta versión funciona solo con LM Studio para el texto y opcionalmente con VibeVoice
si está disponible. Si no hay voces disponibles, solo muestra el texto.

Uso:
    python demo/chat_lm_studio_simple.py
"""

import argparse
import os
import sys
import time
import json
from typing import List, Dict, Any, Optional
import requests

def main():
    """Función principal simplificada"""
    print("🤖 Chat Simple con LM Studio")
    print("=" * 50)
    
    # Verificar conexión con LM Studio
    lm_studio_url = os.environ.get('LM_STUDIO_URL', 'http://127.0.0.1:1234')
    print(f"🔗 Conectando a: {lm_studio_url}")
    
    try:
        response = requests.get(f"{lm_studio_url}/v1/models", timeout=5)
        if response.status_code == 200:
            models = response.json().get('data', [])
            if models:
                print(f"✅ LM Studio conectado - {len(models)} modelo(s) disponible(s)")
                for model in models:
                    print(f"  - {model['id']}")
            else:
                print("❌ LM Studio no tiene modelos cargados")
                return
        else:
            print(f"❌ LM Studio error: {response.status_code}")
            return
    except Exception as e:
        print(f"❌ No se puede conectar con LM Studio: {e}")
        print("💡 Asegúrate de que LM Studio esté ejecutándose en puerto 1234")
        return
    
    print("\n💡 Comandos: /quit para salir")
    print("=" * 50)
    
    # Historial de conversación
    conversation_history = [
        {"role": "system", "content": "Eres un asistente útil y amigable. Responde de manera concisa."}
    ]
    
    while True:
        try:
            user_input = input("\n👤 Tú: ").strip()
            
            if not user_input:
                continue
            
            if user_input.lower() in ['/quit', 'quit', 'exit']:
                print("👋 ¡Hasta luego!")
                break
            
            # Agregar mensaje del usuario
            conversation_history.append({"role": "user", "content": user_input})
            
            print("🤔 Pensando...")
            
            # Enviar a LM Studio
            payload = {
                "messages": conversation_history,
                "max_tokens": 150,
                "temperature": 0.7,
                "stream": False
            }
            
            response = requests.post(
                f"{lm_studio_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                
                # Agregar respuesta del asistente
                conversation_history.append({"role": "assistant", "content": assistant_message})
                
                print(f"🤖 Asistente: {assistant_message}")
                
                # Guardar como texto (simple)
                timestamp = int(time.time())
                os.makedirs("chat_outputs", exist_ok=True)
                with open(f"chat_outputs/chat_{timestamp}.txt", "w", encoding="utf-8") as f:
                    f.write(f"Usuario: {user_input}\n")
                    f.write(f"Asistente: {assistant_message}\n")
                
                print(f"📝 Conversación guardada en: chat_outputs/chat_{timestamp}.txt")
            else:
                print(f"❌ Error en LM Studio: {response.status_code}")
                print(f"Respuesta: {response.text}")
                
        except KeyboardInterrupt:
            print("\n\n👋 ¡Hasta luego!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")


if __name__ == "__main__":
    main()