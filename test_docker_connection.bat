@echo off
REM Script para probar la conexión con LM Studio usando Docker

echo ============================================
echo  Test LM Studio Connection (Docker)
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

echo [INFO] Probando conexión directa con PowerShell...
powershell -Command "try { Write-Host 'Conectando a LM Studio...'; $response = Invoke-RestMethod -Uri 'http://localhost:1234/v1/models' -TimeoutSec 5; Write-Host '✅ Conexión exitosa!'; Write-Host 'Modelos disponibles:'; $response.data | ForEach-Object { Write-Host '  -' $_.id } } catch { Write-Host '❌ No se pudo conectar con LM Studio' }"

echo.
echo [INFO] Construyendo imagen Docker si es necesario...
docker-compose build vibevoice-chat >nul 2>&1

echo [INFO] Probando conexión desde Docker...
echo.

docker-compose run --rm vibevoice-chat python demo/test_lm_studio_connection.py

echo.
pause