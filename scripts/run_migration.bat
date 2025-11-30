@echo off
REM Run database migration (Windows)

echo Running database migration...

REM Check if Docker is running
docker info >nul 2>&1
if errorlevel 1 (
    echo Docker is not running. Please start Docker and try again.
    exit /b 1
)

REM Check if backend container is running
docker compose ps | findstr "osintkit-backend.*Up" >nul
if errorlevel 1 (
    echo Backend container is not running. Starting it...
    docker compose up -d backend
    echo Waiting for backend to be ready...
    timeout /t 3 /nobreak >nul
)

REM Run migration
echo Running Alembic migration...
docker compose exec backend alembic upgrade head
if errorlevel 1 (
    echo Migration failed!
    exit /b 1
)

echo Migration completed successfully!
echo.

echo Verifying database tables...
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"

echo.
echo Migration verification complete!











