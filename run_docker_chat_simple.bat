@echo off
REM Script simplificado para ejecutar VibeVoice Chat Demo con Docker en Windows
REM Versión que no requiere curl - usa Docker directamente

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

echo [INFO] Construyendo imagen de Docker (puede tardar unos minutos la primera vez)...
docker-compose build vibevoice-chat

if %errorlevel% neq 0 (
    echo [ERROR] Error construyendo la imagen de Docker
    pause
    exit /b 1
)

echo.
echo [INFO] ✅ Imagen construida correctamente
echo.
echo [INFO] Verificando LM Studio desde Docker...
echo [INFO] (El demo verificará la conexión automáticamente al iniciar)
echo.
echo [INFO] Iniciando chat demo...
echo [INFO] Usa Ctrl+C para salir del chat
echo.

REM Ejecutar el contenedor de manera interactiva
docker-compose run --rm vibevoice-chat

echo.
echo [INFO] Demo terminado
echo [INFO] Los archivos de audio se guardaron en: chat_outputs/
pause