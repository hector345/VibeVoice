#!/usr/bin/env python3
"""
VibeVoice Web Chat con Reconocimiento y Síntesis de Voz

Una aplicación web que permite conversaciones fluidas por voz con LM Studio:
- Habla al micrófono → Reconocimiento de voz → LM Studio → Respuesta por voz
- Interfaz web moderna y responsiva
- Sin necesidad de escribir texto

Uso:
    python demo/web/voice_chat_app.py
    Luego visita: http://localhost:5000
"""

from flask import Flask, render_template, request, jsonify, send_from_directory
import requests
import os
import json
import time
from typing import Dict, List, Optional
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Configuración
LM_STUDIO_URL = os.environ.get('LM_STUDIO_URL', 'http://127.0.0.1:1234')
CHAT_HISTORY_LIMIT = 20  # Límite de mensajes en historial

# Almacén de conversaciones en memoria (en producción usar base de datos)
conversations: Dict[str, List[Dict]] = {}

class VoiceChatService:
    """Servicio principal para el chat de voz"""
    
    def __init__(self):
        self.lm_studio_url = LM_STUDIO_URL
        
    def check_lm_studio_connection(self) -> Dict:
        """Verifica la conexión con LM Studio"""
        try:
            response = requests.get(f"{self.lm_studio_url}/v1/models", timeout=5)
            if response.status_code == 200:
                models = response.json().get('data', [])
                return {
                    'connected': True,
                    'models': [model['id'] for model in models],
                    'model_count': len(models)
                }
            else:
                return {'connected': False, 'error': f'HTTP {response.status_code}'}
        except Exception as e:
            return {'connected': False, 'error': str(e)}
    
    def get_chat_response(self, message: str, session_id: str = 'default') -> Dict:
        """Obtiene respuesta del modelo de LM Studio"""
        try:
            # Obtener o crear historial de conversación
            if session_id not in conversations:
                conversations[session_id] = [
                    {
                        "role": "system", 
                        "content": "Eres un asistente de voz útil y amigable. Responde de manera concisa y natural, como si fueras una persona hablando. Evita usar formato markdown o caracteres especiales. Mantén las respuestas relativamente cortas para conversación por voz."
                    }
                ]
            
            # Agregar mensaje del usuario
            conversations[session_id].append({"role": "user", "content": message})
            
            # Limitar historial
            if len(conversations[session_id]) > CHAT_HISTORY_LIMIT:
                # Mantener el sistema prompt y los últimos mensajes
                system_msg = conversations[session_id][0]
                recent_msgs = conversations[session_id][-(CHAT_HISTORY_LIMIT-1):]
                conversations[session_id] = [system_msg] + recent_msgs
            
            # Preparar payload para LM Studio
            payload = {
                "messages": conversations[session_id],
                "max_tokens": 200,  # Respuestas más cortas para voz
                "temperature": 0.7,
                "stream": False
            }
            
            # Enviar a LM Studio
            response = requests.post(
                f"{self.lm_studio_url}/v1/chat/completions",
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                
                # Agregar respuesta al historial
                conversations[session_id].append({"role": "assistant", "content": assistant_message})
                
                return {
                    'success': True,
                    'response': assistant_message,
                    'session_id': session_id
                }
            else:
                return {
                    'success': False,
                    'error': f'LM Studio error: HTTP {response.status_code}'
                }
                
        except Exception as e:
            logger.error(f"Error getting chat response: {e}")
            return {
                'success': False,
                'error': str(e)
            }

# Instancia del servicio
voice_chat_service = VoiceChatService()

@app.route('/')
def index():
    """Página principal"""
    return render_template('voice_chat.html')

@app.route('/api/health')
def health_check():
    """Endpoint de salud"""
    lm_status = voice_chat_service.check_lm_studio_connection()
    return jsonify({
        'status': 'healthy',
        'lm_studio': lm_status,
        'timestamp': time.time()
    })

@app.route('/api/chat', methods=['POST'])
def chat():
    """Endpoint principal para el chat"""
    try:
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({'error': 'Mensaje requerido'}), 400
        
        message = data['message'].strip()
        session_id = data.get('session_id', 'default')
        
        if not message:
            return jsonify({'error': 'Mensaje vacío'}), 400
        
        # Obtener respuesta del modelo
        result = voice_chat_service.get_chat_response(message, session_id)
        
        if result['success']:
            return jsonify({
                'success': True,
                'response': result['response'],
                'session_id': result['session_id'],
                'timestamp': time.time()
            })
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return jsonify({'error': 'Error interno del servidor'}), 500

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Limpiar historial de conversación"""
    try:
        data = request.get_json() or {}
        session_id = data.get('session_id', 'default')
        
        if session_id in conversations:
            # Mantener solo el sistema prompt
            system_msg = conversations[session_id][0] if conversations[session_id] else None
            conversations[session_id] = [system_msg] if system_msg else []
        
        return jsonify({'success': True, 'message': 'Historial limpiado'})
        
    except Exception as e:
        logger.error(f"Error clearing history: {e}")
        return jsonify({'error': 'Error limpiando historial'}), 500

@app.route('/static/<path:filename>')
def serve_static(filename):
    """Servir archivos estáticos"""
    return send_from_directory('static', filename)

def main():
    """Función principal"""
    import argparse
    
    # Declarar global al inicio
    global LM_STUDIO_URL
    
    parser = argparse.ArgumentParser(description='VibeVoice Web Chat')
    parser.add_argument('--host', default='0.0.0.0', help='Host para el servidor')
    parser.add_argument('--port', type=int, default=5000, help='Puerto para el servidor')
    parser.add_argument('--debug', action='store_true', help='Modo debug')
    parser.add_argument('--lm-studio-url', default=LM_STUDIO_URL, help='URL de LM Studio')
    
    args = parser.parse_args()
    
    # Actualizar configuración
    LM_STUDIO_URL = args.lm_studio_url
    voice_chat_service.lm_studio_url = LM_STUDIO_URL
    
    print(f"🚀 Iniciando VibeVoice Web Chat")
    print(f"🌐 Servidor: http://{args.host}:{args.port}")
    print(f"🤖 LM Studio: {LM_STUDIO_URL}")
    print(f"💡 Usa Ctrl+C para detener")
    
    # Verificar conexión con LM Studio
    status = voice_chat_service.check_lm_studio_connection()
    if status['connected']:
        print(f"✅ LM Studio conectado - {status['model_count']} modelo(s)")
    else:
        print(f"⚠️  LM Studio no disponible: {status['error']}")
    
    # Iniciar servidor
    app.run(
        host=args.host,
        port=args.port,
        debug=args.debug,
        threaded=True
    )

if __name__ == '__main__':
    main()