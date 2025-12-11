@echo off
REM Script de inicio rápido para el demo de chat VibeVoice + LM Studio
REM Uso: Hacer doble clic o ejecutar desde cmd

echo ============================================
echo  VibeVoice + LM Studio Chat Demo
echo ============================================
echo.

REM Cambiar al directorio del proyecto
cd /d "%~dp0\.."

REM Verificar que Python esté instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python no está instalado o no está en el PATH
    echo Por favor instala Python desde https://python.org
    pause
    exit /b 1
)

REM Verificar conexión con LM Studio
echo [INFO] Verificando conexión con LM Studio...
python demo\test_lm_studio_connection.py
if %errorlevel% neq 0 (
    echo.
    echo [ERROR] No se pudo conectar con LM Studio
    echo.
    echo Pasos para solucionar:
    echo 1. Abrir LM Studio
    echo 2. Cargar un modelo
    echo 3. Ir a "Local Server" y hacer clic en "Start Server"
    echo 4. Verificar que el puerto sea 1234
    echo.
    pause
    exit /b 1
)

echo.
echo [INFO] Iniciando chat demo...
echo.

REM Ejecutar el demo
python demo\chat_with_lm_studio.py --model_path microsoft/VibeVoice --speaker_name Emma

echo.
echo [INFO] Demo terminado
pause