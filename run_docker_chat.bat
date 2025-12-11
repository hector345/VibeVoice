@echo off
REM Script para ejecutar VibeVoice Chat Demo con Docker en Windows
REM Requiere Docker Desktop instalado y ejecutándose

echo ============================================
echo  VibeVoice + LM Studio Chat Demo (Docker)
echo ============================================
echo.

REM Verificar que Docker esté instalado y ejecutándose
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no está instalado o no está ejecutándose
    echo.
    echo Por favor:
    echo 1. Instala Docker Desktop desde https://docker.com/products/docker-desktop
    echo 2. Inicia Docker Desktop
    echo 3. Espera a que aparezca "Docker Desktop is running" en la bandeja del sistema
    echo.
    pause
    exit /b 1
)

REM Verificar que Docker esté ejecutándose
docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no está ejecutándose
    echo.
    echo Por favor inicia Docker Desktop y espera a que esté listo
    echo.
    pause
    exit /b 1
)

echo [INFO] Docker detectado correctamente
echo.

REM Verificar que LM Studio esté ejecutándose (verificación rápida)
echo [INFO] Verificando LM Studio en localhost:1234...
echo [INFO] (Verificación rápida - el demo hará una verificación completa al iniciar)
powershell -Command "& {$ProgressPreference='SilentlyContinue'; $ErrorActionPreference='SilentlyContinue'; try { $null = Invoke-WebRequest -Uri 'http://localhost:1234/v1/models' -TimeoutSec 2 -UseBasicParsing; Write-Host '✅ LM Studio responde correctamente'; exit 0 } catch { Write-Host '⚠️  LM Studio no responde (el demo intentará conectar de todas formas)'; exit 0 } }"

echo.
echo [INFO] Construyendo imagen simple de Docker...
docker build -f Dockerfile.simple -t vibevoice-chat-simple .

if %errorlevel% neq 0 (
    echo [ERROR] Error construyendo la imagen de Docker
    pause
    exit /b 1
)

echo.
echo [INFO] Iniciando chat demo (solo texto)...
echo [INFO] Usa Ctrl+C para salir del chat
echo.

REM Ejecutar el contenedor simple
docker run -it --rm --add-host host.docker.internal:host-gateway -v "%cd%\chat_outputs:/app/chat_outputs" vibevoice-chat-simple

echo.
echo [INFO] Demo terminado
echo [INFO] Los archivos de audio se guardaron en: chat_outputs/
pause