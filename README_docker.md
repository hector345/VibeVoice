# 🐳 VibeVoice Chat Demo con Docker

Esta guía te permite usar el demo de chat VibeVoice + LM Studio sin necesidad de instalar Python localmente, utilizando Docker para encapsular todas las dependencias.

## 🚀 Inicio Rápido

### Windows (Modo Fácil)
```cmd
# 1. Asegúrate de que LM Studio esté ejecutándose
# 2. Ejecuta el script:
run_docker_chat.bat
```

### Linux/Mac (Modo Fácil)
```bash
# 1. Asegúrate de que LM Studio esté ejecutándose
# 2. Dale permisos de ejecución y ejecuta:
chmod +x run_docker_chat.sh
./run_docker_chat.sh
```

## 📋 Requisitos Previos

### 1. Docker
- **Windows**: [Docker Desktop](https://docker.com/products/docker-desktop)
- **Mac**: [Docker Desktop](https://docker.com/products/docker-desktop) 
- **Linux**: [Docker Engine](https://docs.docker.com/engine/install/)

### 2. LM Studio
- Descargar de [lmstudio.ai](https://lmstudio.ai/)
- Cargar un modelo
- Iniciar servidor local en puerto 1234

### 3. Verificar instalación
```bash
# Verificar Docker
docker --version
docker info

# Verificar LM Studio
curl http://localhost:1234/v1/models
```

## 🛠️ Configuración Manual

### 1. Construir la imagen
```bash
docker-compose build vibevoice-chat
```

### 2. Ejecutar el chat
```bash
docker-compose run --rm vibevoice-chat
```

### 3. Con parámetros personalizados
```bash
docker-compose run --rm vibevoice-chat python demo/chat_with_lm_studio.py --speaker_name Emma --device cpu
```

## 🎭 Comandos Útiles

### Listar voces disponibles
```bash
# Windows
list_docker_voices.bat

# Linux/Mac
docker-compose run --rm vibevoice-chat python demo/chat_with_lm_studio.py --list_voices
```

### Probar conexión con LM Studio
```bash
# Windows  
test_docker_connection.bat

# Linux/Mac
docker-compose run --rm vibevoice-chat python demo/test_lm_studio_connection.py
```

### Usar voz específica
```bash
docker-compose run --rm vibevoice-chat python demo/chat_with_lm_studio.py --speaker_name Carter
```

### Ejecutar en modo interactivo (debugging)
```bash
docker-compose run --rm vibevoice-chat /bin/bash
```

## 📁 Volúmenes y Persistencia

### Archivos de audio generados
Los archivos de audio se guardan automáticamente en:
```
./chat_outputs/  # En tu máquina local
```

### Cache de HuggingFace
Los modelos descargados se guardan en un volumen Docker para evitar re-descargas:
```
huggingface_cache  # Volumen Docker persistente
```

### Voces personalizadas
Si tienes voces locales, colócalas en:
```
./demo/voices/streaming_model/*.pt
```

## ⚙️ Configuración Avanzada

### Variables de entorno
Puedes modificar `docker-compose.yml` o usar variables de entorno:

```yaml
environment:
  - MODEL_PATH=microsoft/VibeVoice
  - DEVICE=cpu  # cpu, cuda (requiere nvidia-docker)
  - LM_STUDIO_URL=http://host.docker.internal:1234
```

### Para usar GPU (Linux con NVIDIA)
```yaml
# En docker-compose.yml, agregar:
runtime: nvidia
environment:
  - DEVICE=cuda
```

### Cambiar puerto de LM Studio
Si LM Studio usa un puerto diferente:
```bash
docker-compose run --rm -e LM_STUDIO_URL=http://host.docker.internal:8080 vibevoice-chat
```

## 🌐 Modo Web (Experimental)

Para ejecutar una versión web del demo:
```bash
docker-compose --profile web up vibevoice-web
```

Luego visita: `http://localhost:8000`

## 🔧 Solución de Problemas

### Error: "Docker no está ejecutándose"
```bash
# Windows: Iniciar Docker Desktop
# Linux: sudo systemctl start docker
# Mac: Iniciar Docker Desktop desde Applications
```

### Error: "No se pudo conectar con LM Studio"
```bash
# Verificar que LM Studio esté ejecutándose
curl http://localhost:1234/v1/models

# En Windows, asegúrate de que Windows Firewall permita conexiones
# En Linux/Mac, verificar que no haya firewalls bloqueando
```

### Error: "host.docker.internal not found"
```bash
# En Linux, puede ser necesario agregar:
docker run --add-host host.docker.internal:host-gateway ...

# O usar la IP del host directamente:
docker-compose run --rm -e LM_STUDIO_URL=http://192.168.1.100:1234 vibevoice-chat
```

### Problemas de memoria/rendimiento
```bash
# Aumentar memoria asignada a Docker (Docker Desktop > Settings > Resources)
# Por defecto usa CPU - para mejores tiempos de respuesta considera GPU local

# Verificar recursos:
docker stats
```

### Cache de modelos grande
```bash
# Limpiar cache de HuggingFace si es necesario:
docker volume rm vibevoice_huggingface_cache

# Ver uso de espacio:
docker system df
```

## 📝 Estructura de Archivos Docker

```
VibeVoice/
├── Dockerfile                    # Imagen principal
├── docker-compose.yml           # Configuración de servicios
├── run_docker_chat.bat          # Script Windows
├── run_docker_chat.sh           # Script Linux/Mac  
├── test_docker_connection.bat   # Test conexión Windows
├── list_docker_voices.bat       # Listar voces Windows
└── README_docker.md             # Esta documentación
```

## 🆚 Docker vs Instalación Local

| Aspecto | Docker | Local |
|---------|--------|-------|
| **Instalación** | Solo Docker | Python + dependencias |
| **Aislamiento** | ✅ Completo | ❌ Puede conflicto |
| **Portabilidad** | ✅ Funciona igual | ❌ Depende del sistema |
| **Performance** | ❌ Overhead ligero | ✅ Nativo |
| **Debugging** | ❌ Más complejo | ✅ Directo |
| **Actualizaciones** | ✅ Rebuild imagen | ❌ Manual |

## 💡 Consejos y Mejores Prácticas

### Para desarrollo
```bash
# Montar código local para desarrollo en tiempo real:
docker-compose run --rm -v $(pwd):/app vibevoice-chat /bin/bash
```

### Para producción
```bash
# Usar imagen optimizada:
docker build -t vibevoice-chat:prod -f Dockerfile.prod .
```

### Para múltiples usuarios
```bash
# Ejecutar múltiples instancias:
docker-compose up --scale vibevoice-chat=3
```

### Limpieza periódica
```bash
# Limpiar imágenes no usadas:
docker system prune -a

# Limpiar solo volúmenes:
docker volume prune
```

## 🔗 Enlaces Útiles

- [Docker Desktop](https://docker.com/products/docker-desktop)
- [LM Studio](https://lmstudio.ai/)
- [Docker Compose](https://docs.docker.com/compose/)
- [VibeVoice en HuggingFace](https://huggingface.co/microsoft/VibeVoice)

---

## 🎯 Ejemplo Completo de Uso

```bash
# 1. Instalar Docker Desktop y LM Studio
# 2. Iniciar LM Studio y cargar un modelo
# 3. Clonar este repositorio
git clone https://github.com/microsoft/VibeVoice.git
cd VibeVoice

# 4. Ejecutar (Windows)
run_docker_chat.bat

# 4. Ejecutar (Linux/Mac)
chmod +x run_docker_chat.sh
./run_docker_chat.sh

# 5. Usar el chat:
👤 Tú: Hola, ¿cómo estás?
🤔 Pensando...
🤖 Asistente: ¡Hola! Estoy muy bien...
🎵 Generando audio...
✅ Listo! Audio disponible en: ./chat_outputs/chat_response_xxx.wav

👤 Tú: /voice Carter
✅ Voz cambiada a: Carter

👤 Tú: /quit
👋 ¡Hasta luego!
```

¡Listo para conversar! 🎉