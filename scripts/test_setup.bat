@echo off
REM Test script for AI-OSINT-Kit setup and migration (Windows)

echo Testing AI-OSINT-Kit Setup...
echo.

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker and try again.
    exit /b 1
)

echo Checking Docker services...
docker compose ps | findstr "osintkit-postgres.*Up" >nul
if errorlevel 1 (
    echo PostgreSQL is not running. Starting services...
    docker compose up -d postgres redis
    echo Waiting for services to be ready...
    timeout /t 5 /nobreak >nul
) else (
    echo PostgreSQL is running
)

echo.
echo Running database migration...
docker compose exec -T backend alembic upgrade head
if errorlevel 1 (
    echo Migration failed. Please ensure backend container is running: docker compose up -d backend
    exit /b 1
)

echo Migration completed successfully!
echo.

echo Testing database connection...
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema = 'public';"
if errorlevel 1 (
    echo Could not connect to database
    exit /b 1
)

echo Database connection successful!
echo.

echo Database tables:
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"

echo.
echo Setup test completed successfully!
echo.
echo Next steps:
echo 1. Start all services: docker compose up
echo 2. Test the API: curl http://localhost:8000/health
echo 3. Create a scan: curl -X POST http://localhost:8000/api/v1/scan -H "Content-Type: application/json" -d "{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}"











