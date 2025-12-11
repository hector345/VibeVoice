@echo off
REM Script para ejecutar VibeVoice Web Chat con docker-compose

echo ============================================
echo  VibeVoice Web Chat (docker-compose)
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

echo [INFO] Iniciando VibeVoice Web Chat...
echo [INFO] La aplicación estará disponible en: http://localhost:5000
echo [INFO] Usa Ctrl+C para detener
echo.

REM Ejecutar con docker-compose
docker-compose up --build vibevoice-web

echo.
echo [INFO] Servidor web detenido
pause