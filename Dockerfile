# Dockerfile para VibeVoice + LM Studio Chat Demo
FROM python:3.10-slim

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git \
    curl \
    wget \
    build-essential \
    ffmpeg \
    portaudio19-dev \
    && rm -rf /var/lib/apt/lists/*

# Establecer directorio de trabajo
WORKDIR /app

# Copiar archivos de requisitos primero (para mejor caching de Docker)
COPY demo/requirements_chat.txt /app/requirements_chat.txt
COPY pyproject.toml /app/pyproject.toml

# Instalar dependencias de Python
RUN pip install --no-cache-dir --upgrade pip
RUN pip install --no-cache-dir -r requirements_chat.txt
RUN pip install --no-cache-dir torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cpu
RUN pip install --no-cache-dir transformers>=4.21.0 accelerate diffusers datasets librosa soundfile numpy scipy

# Copiar el código fuente
COPY . /app/

# Crear directorio para outputs
RUN mkdir -p /app/chat_outputs

# Crear un usuario no-root para mayor seguridad
RUN useradd --create-home --shell /bin/bash appuser
RUN chown -R appuser:appuser /app
USER appuser

# Exponer puerto para futuras extensiones web (opcional)
EXPOSE 8000

# Variables de entorno
ENV PYTHONPATH=/app
ENV MODEL_PATH=microsoft/VibeVoice
ENV DEVICE=cpu
ENV LM_STUDIO_URL=http://host.docker.internal:1234

# Comando por defecto - chat simple que solo usa LM Studio
CMD ["python", "demo/chat_lm_studio_simple.py"]