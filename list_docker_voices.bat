@echo off
REM Script para listar voces disponibles usando Docker

echo ============================================
echo  Listar Voces Disponibles (Docker)
echo ============================================
echo.

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

echo [INFO] Listando voces disponibles...
echo.

docker-compose run --rm vibevoice-chat python demo/chat_with_lm_studio.py --list_voices

echo.
pause