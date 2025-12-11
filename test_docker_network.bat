@echo off
REM Test de conectividad Docker con LM Studio

echo ============================================
echo  Test de Conectividad Docker + LM Studio
echo ============================================
echo.

echo [INFO] Construyendo imagen de test...
docker build -f Dockerfile.simple -t vibevoice-test .

if %errorlevel% neq 0 (
    echo [ERROR] Error construyendo imagen
    pause
    exit /b 1
)

echo.
echo [INFO] Probando conectividad desde Docker...
echo.

docker run --rm --add-host host.docker.internal:host-gateway vibevoice-test python demo/test_docker_network.py

echo.
echo [INFO] Test completado
pause