#!/usr/bin/env python3
"""
Script de configuración para el demo de chat VibeVoice + LM Studio

Este script ayuda a configurar el entorno necesario para ejecutar
el demo de chat con verificaciones automáticas.

Uso:
    python demo/setup_chat_demo.py
"""

import os
import sys
import subprocess
import platform
from pathlib import Path


def check_python_version():
    """Verifica la versión de Python"""
    print("🐍 Verificando versión de Python...")
    
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print(f"❌ Python {version.major}.{version.minor} detectado")
        print("💡 Se requiere Python 3.8 o superior")
        return False
    
    print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    return True


def check_pip():
    """Verifica que pip esté disponible"""
    print("\n📦 Verificando pip...")
    
    try:
        import pip
        print("✅ pip disponible")
        return True
    except ImportError:
        print("❌ pip no encontrado")
        return False


def install_requirements():
    """Instala las dependencias necesarias"""
    print("\n📥 Instalando dependencias...")
    
    requirements = [
        "requests>=2.31.0",
        "torch>=1.9.0",
        "transformers>=4.21.0",
    ]
    
    for req in requirements:
        try:
            print(f"  Instalando {req}...")
            subprocess.check_call([
                sys.executable, "-m", "pip", "install", req, "--quiet"
            ])
            print(f"  ✅ {req}")
        except subprocess.CalledProcessError:
            print(f"  ❌ Error instalando {req}")
            return False
    
    return True


def check_vibevoice_model():
    """Verifica si VibeVoice está disponible"""
    print("\n🎤 Verificando modelo VibeVoice...")
    
    try:
        from transformers import AutoProcessor
        processor = AutoProcessor.from_pretrained("microsoft/VibeVoice", trust_remote_code=True)
        print("✅ Modelo VibeVoice accesible desde Hugging Face")
        return True
    except Exception as e:
        print(f"⚠️  No se pudo cargar desde Hugging Face: {e}")
        
        # Verificar modelo local
        possible_paths = [
            "./VibeVoice",
            "../VibeVoice", 
            "microsoft/VibeVoice"
        ]
        
        for path in possible_paths:
            if os.path.exists(path):
                print(f"✅ Modelo local encontrado en: {path}")
                return True
        
        print("❌ Modelo VibeVoice no encontrado")
        return False


def check_voices_directory():
    """Verifica el directorio de voces"""
    print("\n🎭 Verificando voces...")
    
    voices_dir = Path("demo/voices/streaming_model")
    
    if not voices_dir.exists():
        print(f"❌ Directorio de voces no encontrado: {voices_dir}")
        print("💡 Asegúrate de descargar las voces en el directorio correcto")
        return False
    
    voice_files = list(voices_dir.glob("*.pt"))
    
    if not voice_files:
        print(f"❌ No se encontraron archivos de voz (.pt) en {voices_dir}")
        return False
    
    print(f"✅ {len(voice_files)} voces encontradas:")
    for voice in sorted(voice_files)[:5]:  # Mostrar solo las primeras 5
        print(f"  - {voice.name}")
    
    if len(voice_files) > 5:
        print(f"  ... y {len(voice_files) - 5} más")
    
    return True


def test_lm_studio():
    """Prueba la conexión con LM Studio"""
    print("\n🔗 Probando conexión con LM Studio...")
    
    try:
        import requests
        response = requests.get("http://127.0.0.1:1234/v1/models", timeout=3)
        
        if response.status_code == 200:
            models = response.json().get('data', [])
            if models:
                print(f"✅ LM Studio conectado - {len(models)} modelo(s) disponible(s)")
                return True
            else:
                print("⚠️  LM Studio conectado pero sin modelos cargados")
                return False
        else:
            print(f"❌ LM Studio respondió con error: {response.status_code}")
            return False
            
    except Exception as e:
        print("❌ No se pudo conectar con LM Studio")
        print("💡 Asegúrate de que LM Studio esté ejecutándose en puerto 1234")
        return False


def create_output_directory():
    """Crea el directorio de salida"""
    print("\n📁 Configurando directorio de salida...")
    
    output_dir = Path("chat_outputs")
    output_dir.mkdir(exist_ok=True)
    
    print(f"✅ Directorio creado: {output_dir.absolute()}")


def show_instructions():
    """Muestra las instrucciones finales"""
    print("\n" + "=" * 60)
    print("🎉 CONFIGURACIÓN COMPLETADA")
    print("=" * 60)
    
    print("\n💡 Pasos siguientes:")
    print("1. Asegúrate de que LM Studio esté ejecutándose:")
    print("   - Abrir LM Studio")
    print("   - Cargar un modelo")
    print("   - Iniciar Local Server en puerto 1234")
    
    print("\n2. Probar la conexión:")
    print("   python demo/test_lm_studio_connection.py")
    
    print("\n3. Ejecutar el demo de chat:")
    print("   python demo/chat_with_lm_studio.py")
    
    print("\n4. Comandos útiles:")
    print("   # Listar voces disponibles")
    print("   python demo/chat_with_lm_studio.py --list_voices")
    print("   ")
    print("   # Usar voz específica")
    print("   python demo/chat_with_lm_studio.py --speaker_name Emma")
    
    print("\n📖 Ver README_chat.md para más información")


def main():
    """Función principal"""
    print("🚀 Configuración del Demo VibeVoice + LM Studio")
    print("=" * 60)
    
    checks = [
        ("Versión de Python", check_python_version),
        ("Pip", check_pip),
        ("Instalación de dependencias", install_requirements),
        ("Modelo VibeVoice", check_vibevoice_model),
        ("Directorio de voces", check_voices_directory),
        ("Conexión LM Studio", test_lm_studio),
    ]
    
    failed_checks = []
    
    for check_name, check_func in checks:
        if not check_func():
            failed_checks.append(check_name)
    
    # Crear directorio de salida siempre
    create_output_directory()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE VERIFICACIONES")
    print("=" * 60)
    
    if failed_checks:
        print(f"❌ {len(failed_checks)} verificación(es) fallaron:")
        for check in failed_checks:
            print(f"  - {check}")
        
        print("\n🔧 Soluciones sugeridas:")
        
        if "Modelo VibeVoice" in failed_checks:
            print("  📥 Descargar VibeVoice:")
            print("     git clone https://huggingface.co/microsoft/VibeVoice")
        
        if "Directorio de voces" in failed_checks:
            print("  🎭 Descargar voces:")
            print("     Colocar archivos .pt en demo/voices/streaming_model/")
        
        if "Conexión LM Studio" in failed_checks:
            print("  🔗 Configurar LM Studio:")
            print("     1. Descargar de https://lmstudio.ai/")
            print("     2. Cargar un modelo")
            print("     3. Iniciar Local Server")
        
        print(f"\n⚠️  Algunas funciones pueden no estar disponibles")
        
    else:
        print("✅ Todas las verificaciones pasaron correctamente!")
    
    show_instructions()


if __name__ == "__main__":
    main()