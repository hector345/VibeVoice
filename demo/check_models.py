#!/usr/bin/env python3
"""
Script de verificación para VibeVoice en Docker

Verifica qué modelos están disponibles y sugiere alternativas.
"""

import os
import sys
from transformers import AutoProcessor, AutoConfig

def check_model_availability():
    """Verifica disponibilidad de modelos VibeVoice"""
    
    print("🔍 Verificando disponibilidad de modelos VibeVoice...")
    print("=" * 60)
    
    # Posibles ubicaciones del modelo
    model_paths = [
        "microsoft/VibeVoice",
        "./VibeVoice",
        "../VibeVoice",
        "/app/VibeVoice",
        "microsoft/speecht5_tts",  # Alternativa
    ]
    
    available_models = []
    
    for model_path in model_paths:
        try:
            print(f"🔎 Probando: {model_path}...")
            
            if model_path.startswith("microsoft/speecht5_tts"):
                # Modelo alternativo más simple
                from transformers import SpeechT5Processor
                processor = SpeechT5Processor.from_pretrained(model_path)
                print(f"✅ Modelo alternativo disponible: {model_path}")
                available_models.append(("alternative", model_path))
                
            else:
                # Modelo VibeVoice original
                config = AutoConfig.from_pretrained(model_path, trust_remote_code=True)
                print(f"✅ Modelo VibeVoice disponible: {model_path}")
                available_models.append(("vibevoice", model_path))
                
        except Exception as e:
            print(f"❌ {model_path}: {str(e)[:100]}...")
    
    print("\n" + "=" * 60)
    
    if available_models:
        print(f"🎉 {len(available_models)} modelo(s) disponible(s):")
        for model_type, path in available_models:
            print(f"  📦 {path} ({model_type})")
        
        # Usar el primer modelo disponible
        model_type, model_path = available_models[0]
        print(f"\n💡 Usando: {model_path}")
        return model_path, model_type
        
    else:
        print("❌ No se encontraron modelos de síntesis de voz")
        print("\n💡 Opciones:")
        print("1. Descargar VibeVoice manualmente:")
        print("   git lfs install")
        print("   git clone https://huggingface.co/microsoft/VibeVoice")
        print("2. Usar modelo alternativo (menos calidad pero funcional)")
        
        return None, None

def suggest_alternatives():
    """Sugiere modelos alternativos si VibeVoice no está disponible"""
    print("\n🔄 Modelos alternativos de síntesis de voz:")
    print("=" * 60)
    
    alternatives = [
        ("microsoft/speecht5_tts", "SpeechT5 - Modelo básico de Microsoft"),
        ("facebook/mms-tts-eng", "MMS TTS - Modelo multilingüe de Meta"),
        ("espnet/kan-bayashi_ljspeech_vits", "VITS - Modelo de calidad media"),
    ]
    
    for model_id, description in alternatives:
        print(f"📦 {model_id}")
        print(f"   {description}")
        print()

if __name__ == "__main__":
    model_path, model_type = check_model_availability()
    
    if not model_path:
        suggest_alternatives()
        print("\n⚠️  Sin modelo de síntesis de voz, solo funcionará el chat de texto")
        sys.exit(1)
    
    print(f"\n✅ Listo para usar {model_path}")