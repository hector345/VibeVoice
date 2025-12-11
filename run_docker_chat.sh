#!/bin/bash
# Script para ejecutar VibeVoice Chat Demo con Docker en Linux/Mac
# Requiere Docker instalado y ejecutándose

set -e

echo "============================================"
echo " VibeVoice + LM Studio Chat Demo (Docker)"
echo "============================================"
echo

# Verificar que Docker esté instalado
if ! command -v docker &> /dev/null; then
    echo "[ERROR] Docker no está instalado"
    echo
    echo "Por favor instala Docker desde:"
    echo "- Linux: https://docs.docker.com/engine/install/"
    echo "- Mac: https://docker.com/products/docker-desktop"
    echo
    exit 1
fi

# Verificar que Docker esté ejecutándose
if ! docker info &> /dev/null; then
    echo "[ERROR] Docker no está ejecutándose"
    echo
    echo "Por favor inicia el servicio Docker:"
    echo "- Linux: sudo systemctl start docker"
    echo "- Mac: Inicia Docker Desktop"
    echo
    exit 1
fi

echo "[INFO] Docker detectado correctamente"
echo

# Verificar que docker-compose esté disponible
if command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
elif docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
else
    echo "[ERROR] Docker Compose no está disponible"
    echo "Por favor instala Docker Compose"
    exit 1
fi

echo "[INFO] Usando: $COMPOSE_CMD"

# Verificar que LM Studio esté ejecutándose
echo "[INFO] Verificando LM Studio en localhost:1234..."
if curl -s http://localhost:1234/v1/models > /dev/null 2>&1; then
    echo "[INFO] ✅ LM Studio conectado correctamente"
else
    echo "[WARNING] No se pudo conectar con LM Studio"
    echo
    echo "Asegúrate de que:"
    echo "1. LM Studio esté ejecutándose"
    echo "2. Tengas un modelo cargado"
    echo "3. El servidor local esté iniciado en puerto 1234"
    echo
    read -p "¿Continuar de todas formas? (y/n): " continue
    if [[ ! "$continue" =~ ^[Yy]$ ]]; then
        echo "Operación cancelada"
        exit 1
    fi
fi

echo
echo "[INFO] Construyendo imagen de Docker (puede tardar unos minutos la primera vez)..."
$COMPOSE_CMD build vibevoice-chat

echo
echo "[INFO] Iniciando chat demo..."
echo "[INFO] Usa Ctrl+C para salir del chat"
echo

# Crear directorio de outputs si no existe
mkdir -p chat_outputs

# Ejecutar el contenedor de manera interactiva
$COMPOSE_CMD run --rm vibevoice-chat

echo
echo "[INFO] Demo terminado"
echo "[INFO] Los archivos de audio se guardaron en: chat_outputs/"