@echo off
REM Script para ejecutar VibeVoice Web Chat con Docker

echo ============================================
echo  VibeVoice Web Chat (Docker)
echo ============================================
echo.

REM Verificar Docker
docker --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no está instalado
    pause
    exit /b 1
)

docker info >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Docker no está ejecutándose
    pause
    exit /b 1
)

echo [INFO] Docker detectado correctamente
echo.

REM Verificar LM Studio rápidamente
echo [INFO] Verificando LM Studio...
powershell -Command "& {$ProgressPreference='SilentlyContinue'; $ErrorActionPreference='SilentlyContinue'; try { $null = Invoke-WebRequest -Uri 'http://localhost:1234/v1/models' -TimeoutSec 2 -UseBasicParsing; Write-Host '✅ LM Studio responde correctamente' } catch { Write-Host '⚠️  LM Studio no responde (la app web intentará conectar de todas formas)' } }"

echo.
echo [INFO] Construyendo imagen web...
docker build -f Dockerfile.web -t vibevoice-web .

if %errorlevel% neq 0 (
    echo [ERROR] Error construyendo imagen web
    pause
    exit /b 1
)

echo.
echo [INFO] Iniciando servidor web...
echo [INFO] La aplicación estará disponible en: http://localhost:5000
echo [INFO] Usa Ctrl+C para detener
echo.

REM Ejecutar contenedor web
docker run -it --rm --add-host host.docker.internal:host-gateway -p 5000:5000 vibevoice-web

echo.
echo [INFO] Servidor web detenido
pause