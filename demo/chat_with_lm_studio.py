#!/usr/bin/env python3
"""
VibeVoice + LM Studio Chat Demo

Este demo permite conversar con un modelo de lenguaje alojado en LM Studio
y recibir respuestas en audio usando VibeVoice para síntesis de voz.

Uso:
    python demo/chat_with_lm_studio.py --model_path microsoft/VibeVoice --speaker_name Emma

Requisitos:
    - LM Studio ejecutándose en http://127.0.0.1:1234
    - Modelo VibeVoice descargado
    - Dependencias: requests, torch, transformers
"""

import argparse
import os
import sys
import time
import json
import copy
from typing import List, Dict, Any, Optional
import requests
import torch

# Agregar el directorio padre al path para importar vibevoice
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from vibevoice.modular.modeling_vibevoice_streaming_inference import VibeVoiceStreamingForConditionalGenerationInference
from vibevoice.processor.vibevoice_streaming_processor import VibeVoiceStreamingProcessor
from transformers.utils import logging

logging.set_verbosity_info()
logger = logging.get_logger(__name__)


class LMStudioClient:
    """Cliente para comunicarse con LM Studio API"""
    
    def __init__(self, base_url: str = "http://127.0.0.1:1234"):
        self.base_url = base_url.rstrip('/')
        self.chat_endpoint = f"{self.base_url}/v1/chat/completions"
        self.models_endpoint = f"{self.base_url}/v1/models"
        self.conversation_history: List[Dict[str, str]] = []
        
    def get_available_models(self) -> List[str]:
        """Obtiene la lista de modelos disponibles"""
        try:
            response = requests.get(self.models_endpoint, timeout=5)
            if response.status_code == 200:
                models_data = response.json()
                return [model['id'] for model in models_data.get('data', [])]
            else:
                print(f"Error al obtener modelos: HTTP {response.status_code}")
                return []
        except requests.RequestException as e:
            print(f"Error de conexión con LM Studio: {e}")
            return []
    
    def send_message(self, message: str, model_id: Optional[str] = None, max_tokens: int = 150) -> Optional[str]:
        """Envía un mensaje al modelo y obtiene la respuesta"""
        # Agregar mensaje del usuario al historial
        self.conversation_history.append({"role": "user", "content": message})
        
        # Preparar el payload
        payload = {
            "messages": self.conversation_history,
            "max_tokens": max_tokens,
            "temperature": 0.7,
            "stream": False
        }
        
        # Agregar model_id si se proporciona
        if model_id:
            payload["model"] = model_id
        
        try:
            response = requests.post(
                self.chat_endpoint,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                assistant_message = result['choices'][0]['message']['content']
                
                # Agregar respuesta del asistente al historial
                self.conversation_history.append({"role": "assistant", "content": assistant_message})
                
                return assistant_message
            else:
                print(f"Error en la respuesta: HTTP {response.status_code}")
                print(f"Respuesta: {response.text}")
                return None
                
        except requests.RequestException as e:
            print(f"Error de conexión: {e}")
            return None
    
    def clear_history(self):
        """Limpia el historial de conversación"""
        self.conversation_history = []
    
    def set_system_prompt(self, system_prompt: str):
        """Establece un prompt del sistema"""
        self.conversation_history = [{"role": "system", "content": system_prompt}]


class VoiceMapper:
    """Mapea nombres de speakers a archivos de voz"""
    
    def __init__(self):
        self.setup_voice_presets()
        
        # Cambiar nombres según nuestros archivos de voz preestablecidos
        new_dict = {}
        for name, path in self.voice_presets.items():
            if '_' in name:
                name = name.split('_')[0]
            if '-' in name:
                name = name.split('-')[-1]
            new_dict[name] = path
        self.voice_presets.update(new_dict)

    def setup_voice_presets(self):
        """Configurar voces preestablecidas escaneando el directorio de voces."""
        voices_dir = os.path.join(os.path.dirname(__file__), "voices/streaming_model")
        
        if not os.path.exists(voices_dir):
            print(f"Advertencia: Directorio de voces no encontrado en {voices_dir}")
            self.voice_presets = {}
            self.available_voices = {}
            return
        
        self.voice_presets = {}
        self.available_voices = {}
        
        for filename in os.listdir(voices_dir):
            if filename.endswith('.pt'):
                name = filename.replace('.pt', '')
                full_path = os.path.join(voices_dir, filename)
                self.voice_presets[name] = full_path
                
                # Crear categorías por idioma y género
                if name.startswith('en-'):
                    lang = 'english'
                elif name.startswith('es-') or name.startswith('sp-'):
                    lang = 'spanish'
                elif name.startswith('fr-'):
                    lang = 'french'
                elif name.startswith('de-'):
                    lang = 'german'
                elif name.startswith('it-'):
                    lang = 'italian'
                elif name.startswith('pt-'):
                    lang = 'portuguese'
                elif name.startswith('jp-'):
                    lang = 'japanese'
                elif name.startswith('kr-'):
                    lang = 'korean'
                elif name.startswith('nl-'):
                    lang = 'dutch'
                elif name.startswith('pl-'):
                    lang = 'polish'
                elif name.startswith('in-'):
                    lang = 'hindi'
                else:
                    lang = 'other'
                
                gender = 'female' if 'woman' in name.lower() else 'male'
                
                if lang not in self.available_voices:
                    self.available_voices[lang] = {'male': [], 'female': []}
                
                self.available_voices[lang][gender].append(name)

    def get_voice_path(self, speaker_name: str) -> Optional[str]:
        """Obtiene la ruta del archivo de voz para un speaker dado"""
        if speaker_name in self.voice_presets:
            return self.voice_presets[speaker_name]
        
        # Búsqueda fuzzy
        speaker_lower = speaker_name.lower()
        for name, path in self.voice_presets.items():
            if speaker_lower in name.lower() or name.lower() in speaker_lower:
                return path
        
        return None

    def list_available_voices(self) -> Dict[str, List[str]]:
        """Lista todas las voces disponibles organizadas por idioma"""
        return self.available_voices

    def get_random_voice(self, language: str = 'english', gender: str = 'any') -> Optional[str]:
        """Obtiene una voz aleatoria según criterios"""
        import random
        
        if language not in self.available_voices:
            # Fallback a inglés si el idioma no está disponible
            language = 'english'
        
        voices = []
        if gender == 'any':
            voices.extend(self.available_voices[language]['male'])
            voices.extend(self.available_voices[language]['female'])
        else:
            voices = self.available_voices[language].get(gender, [])
        
        return random.choice(voices) if voices else None


class ChatBot:
    """Chatbot principal que integra LM Studio y VibeVoice"""
    
    def __init__(self, model_path: str, lm_studio_url: str = "http://127.0.0.1:1234", 
                 device: str = "auto", speaker_name: str = "Emma"):
        self.lm_client = LMStudioClient(lm_studio_url)
        self.voice_mapper = VoiceMapper()
        self.model_path = model_path
        self.device = self._setup_device(device)
        self.speaker_name = speaker_name
        self.output_dir = "./chat_outputs"
        
        # Crear directorio de salida
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Inicializar VibeVoice
        self._initialize_vibevoice()
        
        # Configurar prompt del sistema por defecto
        default_system_prompt = (
            "Eres un asistente útil y amigable. Responde de manera concisa y natural. "
            "Tus respuestas serán convertidas a audio, así que escribe como si estuvieras hablando. "
            "Evita usar formato markdown o caracteres especiales innecesarios."
        )
        self.lm_client.set_system_prompt(default_system_prompt)
    
    def _setup_device(self, device: str) -> str:
        """Configura el dispositivo para la inferencia"""
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            else:
                return "cpu"
        
        # Normalizar 'mpx' a 'mps'
        if device.lower() == "mpx":
            device = "mps"
        
        # Validar disponibilidad de MPS
        if device == "mps" and not torch.backends.mps.is_available():
            print("Advertencia: MPS no disponible. Usando CPU.")
            return "cpu"
        
        return device
    
    def _initialize_vibevoice(self):
        """Inicializa el modelo VibeVoice"""
        print(f"Inicializando VibeVoice en {self.device}...")
        
        try:
            # Cargar procesador
            self.processor = VibeVoiceStreamingProcessor.from_pretrained(
                self.model_path,
                trust_remote_code=True
            )
            
            # Cargar modelo
            self.model = VibeVoiceStreamingForConditionalGenerationInference.from_pretrained(
                self.model_path,
                trust_remote_code=True,
                torch_dtype=torch.float16 if self.device == "cuda" else torch.float32,
            )
            self.model.to(self.device)
            
            print("✅ VibeVoice inicializado correctamente")
            
        except Exception as e:
            print(f"❌ Error al inicializar VibeVoice: {e}")
            sys.exit(1)
    
    def _check_lm_studio_connection(self) -> bool:
        """Verifica la conexión con LM Studio"""
        models = self.lm_client.get_available_models()
        if models:
            print(f"✅ Conectado a LM Studio. Modelos disponibles: {', '.join(models)}")
            return True
        else:
            print("❌ No se pudo conectar con LM Studio")
            return False
    
    def _text_to_speech(self, text: str, output_filename: str = None) -> str:
        """Convierte texto a audio usando VibeVoice"""
        if not output_filename:
            timestamp = int(time.time())
            output_filename = f"chat_response_{timestamp}.wav"
        
        output_path = os.path.join(self.output_dir, output_filename)
        
        try:
            # Obtener ruta de la voz
            voice_path = self.voice_mapper.get_voice_path(self.speaker_name)
            if not voice_path:
                print(f"Advertencia: Voz '{self.speaker_name}' no encontrada, usando voz por defecto")
                voice_path = list(self.voice_mapper.voice_presets.values())[0] if self.voice_mapper.voice_presets else None
            
            if not voice_path:
                print("❌ No hay voces disponibles")
                return None
            
            # Preparar entrada
            inputs = self.processor(
                tts_text=text,
                voice_preset=voice_path,
                return_tensors="pt"
            )
            
            # Mover al dispositivo correcto
            for key, value in inputs.items():
                if isinstance(value, torch.Tensor):
                    inputs[key] = value.to(self.device)
            
            # Generar audio
            with torch.no_grad():
                outputs = self.model.generate(
                    **inputs,
                    max_new_tokens=None,
                    cfg_scale=1.5,
                    tokenizer=self.processor.tokenizer,
                    generation_config={'do_sample': False},
                    verbose=False
                )
            
            # Guardar audio
            if outputs.speech_outputs and outputs.speech_outputs[0] is not None:
                self.processor.save_audio(
                    outputs.speech_outputs[0],
                    output_path=output_path
                )
                print(f"🔊 Audio guardado en: {output_path}")
                return output_path
            else:
                print("❌ No se pudo generar el audio")
                return None
                
        except Exception as e:
            print(f"❌ Error en síntesis de voz: {e}")
            return None
    
    def list_voices(self):
        """Lista las voces disponibles"""
        print("\n🎭 Voces disponibles:")
        print("=" * 50)
        
        voices = self.voice_mapper.list_available_voices()
        
        for language, genders in voices.items():
            print(f"\n{language.upper()}:")
            for gender, voice_list in genders.items():
                if voice_list:
                    print(f"  {gender.title()}: {', '.join(voice_list)}")
        
        print("\n" + "=" * 50)
    
    def run_interactive_chat(self):
        """Ejecuta el chat interactivo"""
        print("🤖 VibeVoice + LM Studio Chat Demo")
        print("=" * 50)
        
        # Verificar conexión
        if not self._check_lm_studio_connection():
            return
        
        print(f"🎭 Voz actual: {self.speaker_name}")
        print("💡 Comandos especiales:")
        print("  /help    - Mostrar ayuda")
        print("  /voices  - Listar voces disponibles") 
        print("  /voice <nombre> - Cambiar voz")
        print("  /clear   - Limpiar historial")
        print("  /quit    - Salir")
        print("=" * 50)
        
        while True:
            try:
                user_input = input("\n👤 Tú: ").strip()
                
                if not user_input:
                    continue
                
                # Comandos especiales
                if user_input.startswith('/'):
                    self._handle_command(user_input)
                    continue
                
                print("🤔 Pensando...")
                
                # Obtener respuesta del modelo
                response = self.lm_client.send_message(user_input)
                
                if response:
                    print(f"🤖 Asistente: {response}")
                    
                    # Convertir a audio
                    print("🎵 Generando audio...")
                    audio_path = self._text_to_speech(response)
                    
                    if audio_path:
                        print(f"✅ Listo! Audio disponible en: {audio_path}")
                    
                else:
                    print("❌ No se recibió respuesta del modelo")
                    
            except KeyboardInterrupt:
                print("\n\n👋 ¡Hasta luego!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
    
    def _handle_command(self, command: str):
        """Maneja comandos especiales"""
        parts = command.split()
        cmd = parts[0].lower()
        
        if cmd == '/help':
            print("\n💡 Comandos disponibles:")
            print("  /help           - Mostrar esta ayuda")
            print("  /voices         - Listar voces disponibles")
            print("  /voice <nombre> - Cambiar voz (ej: /voice Emma)")
            print("  /clear          - Limpiar historial de conversación")
            print("  /quit           - Salir del chat")
            
        elif cmd == '/voices':
            self.list_voices()
            
        elif cmd == '/voice':
            if len(parts) > 1:
                new_voice = parts[1]
                if self.voice_mapper.get_voice_path(new_voice):
                    self.speaker_name = new_voice
                    print(f"✅ Voz cambiada a: {new_voice}")
                else:
                    print(f"❌ Voz '{new_voice}' no encontrada")
                    print("Usa /voices para ver las voces disponibles")
            else:
                print("Uso: /voice <nombre_de_voz>")
                
        elif cmd == '/clear':
            self.lm_client.clear_history()
            print("✅ Historial de conversación limpiado")
            
        elif cmd == '/quit':
            print("👋 ¡Hasta luego!")
            sys.exit(0)
            
        else:
            print(f"❌ Comando desconocido: {cmd}")
            print("Usa /help para ver los comandos disponibles")


def parse_args():
    """Analiza los argumentos de línea de comandos"""
    parser = argparse.ArgumentParser(
        description="Chat demo with LM Studio and VibeVoice",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Ejemplos:
  python demo/chat_with_lm_studio.py --model_path microsoft/VibeVoice
  python demo/chat_with_lm_studio.py --speaker_name Emma --lm_studio_url http://localhost:1234
        """
    )
    
    parser.add_argument(
        "--model_path",
        type=str,
        default="microsoft/VibeVoice",
        help="Ruta al modelo VibeVoice (default: microsoft/VibeVoice)"
    )
    
    parser.add_argument(
        "--lm_studio_url",
        type=str,
        default="http://127.0.0.1:1234",
        help="URL del servidor LM Studio (default: http://127.0.0.1:1234)"
    )
    
    parser.add_argument(
        "--speaker_name",
        type=str,
        default="Emma",
        help="Nombre del speaker/voz (default: Emma)"
    )
    
    parser.add_argument(
        "--device",
        type=str,
        default="auto",
        choices=["auto", "cuda", "mps", "cpu"],
        help="Dispositivo para inferencia (default: auto)"
    )
    
    parser.add_argument(
        "--list_voices",
        action="store_true",
        help="Listar voces disponibles y salir"
    )
    
    return parser.parse_args()


def main():
    """Función principal"""
    args = parse_args()
    
    # Crear chatbot
    chatbot = ChatBot(
        model_path=args.model_path,
        lm_studio_url=args.lm_studio_url,
        device=args.device,
        speaker_name=args.speaker_name
    )
    
    # Solo listar voces si se solicita
    if args.list_voices:
        chatbot.list_voices()
        return
    
    # Ejecutar chat interactivo
    chatbot.run_interactive_chat()


if __name__ == "__main__":
    main()