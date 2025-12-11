# Demo de Chat con LM Studio + VibeVoice

Este demo permite conversar con un modelo de lenguaje alojado en LM Studio y recibir las respuestas en audio usando VibeVoice para síntesis de voz.

## 🚀 Características

- **Chat interactivo**: Conversa por texto con cualquier modelo de LM Studio
- **Respuestas en audio**: Las respuestas se convierten automáticamente a voz
- **Múltiples voces**: Elige entre diferentes voces y idiomas disponibles
- **Historial de conversación**: Mantiene contexto durante la conversación
- **Comandos especiales**: Control total sobre la experiencia de chat

## 📋 Requisitos Previos

### 1. LM Studio
- Descargar e instalar [LM Studio](https://lmstudio.ai/)
- Cargar un modelo de lenguaje en LM Studio
- Iniciar el servidor local en `http://127.0.0.1:1234`

### 2. VibeVoice
- Modelo VibeVoice descargado (ej: `microsoft/VibeVoice`)
- Voces instaladas en `demo/voices/streaming_model/`

### 3. Dependencias Python
```bash
pip install requests torch transformers
# o instalar desde el archivo de requisitos:
pip install -r demo/requirements_chat.txt
```

## 🎯 Uso Rápido

### Uso básico:
```bash
python demo/chat_with_lm_studio.py --model_path microsoft/VibeVoice
```

### Con configuración personalizada:
```bash
python demo/chat_with_lm_studio.py \
    --model_path microsoft/VibeVoice \
    --speaker_name Emma \
    --device cuda \
    --lm_studio_url http://127.0.0.1:1234
```

### Listar voces disponibles:
```bash
python demo/chat_with_lm_studio.py --list_voices
```

## 🎭 Voces Disponibles

El demo incluye soporte para múltiples idiomas y géneros:

- **Inglés**: Emma (mujer), Carter, Davis, Frank, Mike (hombres), Grace (mujer)
- **Español**: Spk0 (mujer), Spk1 (hombre) 
- **Francés**: Spk0 (hombre), Spk1 (mujer)
- **Alemán**: Spk0 (hombre), Spk1 (mujer)
- **Italiano**: Spk0 (mujer), Spk1 (hombre)
- **Portugués**: Spk0 (mujer), Spk1 (hombre)
- **Japonés**: Spk0 (hombre), Spk1 (mujer)
- **Coreano**: Spk0 (mujer), Spk1 (hombre)
- **Holandés**: Spk0 (hombre), Spk1 (mujer)
- **Polaco**: Spk0 (hombre), Spk1 (mujer)
- **Hindi**: Samuel (hombre)

## 💬 Comandos de Chat

Durante el chat, puedes usar estos comandos especiales:

- `/help` - Mostrar ayuda
- `/voices` - Listar todas las voces disponibles
- `/voice <nombre>` - Cambiar la voz (ej: `/voice Emma`)
- `/clear` - Limpiar el historial de conversación
- `/quit` - Salir del chat

## 📁 Archivos Generados

Los archivos de audio se guardan automáticamente en:
```
./chat_outputs/chat_response_<timestamp>.wav
```

## ⚙️ Configuración de LM Studio

### 1. Instalar y configurar LM Studio:
```
1. Descargar LM Studio desde https://lmstudio.ai/
2. Instalar y abrir la aplicación
3. Descargar un modelo de lenguaje (ej: Llama, Mistral, etc.)
4. Ir a la pestaña "Local Server"
5. Seleccionar el modelo cargado
6. Iniciar el servidor en puerto 1234
```

### 2. Verificar que el servidor esté funcionando:
Los logs de LM Studio deberían mostrar algo como:
```
[INFO] [LM STUDIO SERVER] Supported endpoints:
[INFO] [LM STUDIO SERVER] ->	GET  http://localhost:1234/v1/models
[INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/chat/completions
[INFO] [LM STUDIO SERVER] ->	POST http://localhost:1234/v1/completions
```

### 3. Probar la conexión:
```bash
curl http://127.0.0.1:1234/v1/models
```

## 🔧 Solución de Problemas

### Error: "No se pudo conectar con LM Studio"
- Verificar que LM Studio esté ejecutándose
- Confirmar que el servidor esté en `http://127.0.0.1:1234`
- Verificar que hay un modelo cargado en LM Studio

### Error: "Voz no encontrada"
- Usar `/voices` para ver las voces disponibles
- Verificar que los archivos `.pt` estén en `demo/voices/streaming_model/`
- Probar con una voz diferente como `Emma` o `Carter`

### Error: "Error al inicializar VibeVoice"
- Verificar que el modelo VibeVoice esté descargado correctamente
- Comprobar la ruta del modelo con `--model_path`
- Verificar disponibilidad de GPU/CPU según `--device`

### Problemas de memoria/rendimiento
- Usar `--device cpu` si hay problemas con GPU
- Cerrar otras aplicaciones que usen mucha memoria
- Para modelos grandes, considerar usar cuantización en LM Studio

## 📝 Ejemplo de Uso

```bash
$ python demo/chat_with_lm_studio.py --model_path microsoft/VibeVoice --speaker_name Emma

🤖 VibeVoice + LM Studio Chat Demo
==================================================
✅ Conectado a LM Studio. Modelos disponibles: llama-3.2-3b-instruct
✅ VibeVoice inicializado correctamente
🎭 Voz actual: Emma
💡 Comandos especiales:
  /help    - Mostrar ayuda
  /voices  - Listar voces disponibles
  /voice <nombre> - Cambiar voz
  /clear   - Limpiar historial
  /quit    - Salir
==================================================

👤 Tú: Hola, ¿cómo estás?

🤔 Pensando...
🤖 Asistente: ¡Hola! Estoy muy bien, gracias por preguntar. Soy un asistente de inteligencia artificial y estoy aquí para ayudarte con lo que necesites. ¿En qué puedo asistirte hoy?

🎵 Generando audio...
🔊 Audio guardado en: ./chat_outputs/chat_response_1703123456.wav
✅ Listo! Audio disponible en: ./chat_outputs/chat_response_1703123456.wav

👤 Tú: /voice Carter

✅ Voz cambiada a: Carter

👤 Tú: Cuéntame un chiste
```

## 🔄 Integración con Otros Servicios

Este demo puede adaptarse fácilmente para trabajar con otros servicios de IA:

- **OpenAI API**: Cambiar el endpoint a `https://api.openai.com/v1/chat/completions`
- **Anthropic Claude**: Adaptar para usar la API de Anthropic
- **Ollama**: Usar `http://localhost:11434/v1/chat/completions`
- **Otros modelos locales**: Cualquier servicio compatible con OpenAI API

## 📄 Licencia

Este demo está incluido bajo la misma licencia que VibeVoice.