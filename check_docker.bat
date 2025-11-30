@echo off
REM Check if Docker is ready before starting services

echo ========================================
echo Docker Health Check
echo ========================================
echo.

echo [1/4] Checking Docker installation...
docker --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker is not installed or not in PATH
    echo Please install Docker Desktop and try again
    exit /b 1
)
echo [OK] Docker is installed
docker --version
echo.

echo [2/4] Checking Docker daemon...
docker info >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker daemon is not running
    echo.
    echo Please:
    echo 1. Open Docker Desktop
    echo 2. Wait for it to fully start (whale icon stable)
    echo 3. Wait 30-60 seconds after "Docker Desktop is running" appears
    echo 4. Run this script again
    exit /b 1
)
echo [OK] Docker daemon is running
echo.

echo [3/4] Testing Docker API...
docker ps >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Docker API is not responding
    echo.
    echo Please:
    echo 1. Restart Docker Desktop
    echo 2. Wait for it to fully start
    echo 3. Run this script again
    exit /b 1
)
echo [OK] Docker API is responding
echo.

echo [4/4] Testing image pull...
echo Attempting to pull test image...
docker pull hello-world >nul 2>&1
if errorlevel 1 (
    echo [WARNING] Cannot pull images - Docker may still be starting
    echo.
    echo Please:
    echo 1. Wait 1-2 minutes
    echo 2. Restart Docker Desktop if problem persists
    echo 3. Check your internet connection
    echo.
    echo You can still try to start services, but they may fail.
    pause
    exit /b 1
)
echo [OK] Can pull images
docker rmi hello-world >nul 2>&1
echo.

echo ========================================
echo Docker is ready!
echo ========================================
echo.
echo You can now run: setup_and_test.bat
echo.
pause










