@echo off
REM Complete setup and test script for AI-OSINT-Kit

echo ========================================
echo AI-OSINT-Kit Setup and Test
echo ========================================
echo.

REM Check if Docker is running
echo [1/6] Checking Docker...
docker --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Docker is not installed or not in PATH
    echo Please install Docker Desktop and try again
    exit /b 1
)
echo [OK] Docker is installed
echo.

REM Start services
echo [2/6] Starting Docker services...
docker compose up -d postgres redis
if errorlevel 1 (
    echo ERROR: Failed to start PostgreSQL and Redis
    exit /b 1
)
echo [OK] PostgreSQL and Redis started
echo Waiting for services to be ready...
timeout /t 10 /nobreak >nul
echo.

REM Start backend
echo [3/6] Starting backend service...
docker compose up -d backend
if errorlevel 1 (
    echo ERROR: Failed to start backend
    exit /b 1
)
echo [OK] Backend started
echo Waiting for backend to be ready...
timeout /t 5 /nobreak >nul
echo.

REM Run migration
echo [4/6] Running database migration...
docker compose exec -T backend alembic upgrade head
if errorlevel 1 (
    echo ERROR: Migration failed
    echo Trying alternative method...
    docker compose exec backend alembic upgrade head
    if errorlevel 1 (
        echo ERROR: Migration still failed
        echo Please check the logs: docker compose logs backend
        exit /b 1
    )
)
echo [OK] Migration completed
echo.

REM Verify migration
echo [5/6] Verifying database tables...
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"
if errorlevel 1 (
    echo WARNING: Could not verify tables, but migration may have succeeded
)
echo.

REM Start Celery worker
echo [6/6] Starting Celery worker...
docker compose up -d celery-worker
if errorlevel 1 (
    echo WARNING: Failed to start Celery worker
    echo You can start it manually later: docker compose up -d celery-worker
) else (
    echo [OK] Celery worker started
)
echo.

echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo Next steps:
echo 1. Test health endpoint: curl http://localhost:8000/health
echo 2. Create a scan: curl -X POST http://localhost:8000/api/v1/scan -H "Content-Type: application/json" -d "{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}"
echo 3. Check scan status: curl http://localhost:8000/api/v1/scan/1
echo 4. View logs: docker compose logs -f backend
echo 5. View Celery logs: docker compose logs -f celery-worker
echo.
echo Services status: docker compose ps
echo.

pause










