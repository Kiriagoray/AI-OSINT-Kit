# Docker Setup Guide for AI-OSINT-Kit

## Docker is Not Installed

Docker is required to run the AI-OSINT-Kit application. Follow these steps to install Docker and then proceed with the setup.

## Installation Steps

### For Windows (Your System)

1. **Download Docker Desktop for Windows**
   - Visit: https://www.docker.com/products/docker-desktop/
   - Download Docker Desktop for Windows
   - Make sure you have Windows 10/11 64-bit with WSL 2 enabled

2. **Install Docker Desktop**
   - Run the installer (Docker Desktop Installer.exe)
   - Follow the installation wizard
   - Restart your computer when prompted

3. **Enable WSL 2 (if not already enabled)**
   - Open PowerShell as Administrator
   - Run: `wsl --install`
   - Restart your computer
   - For more details: https://docs.docker.com/desktop/wsl/

4. **Start Docker Desktop**
   - Launch Docker Desktop from the Start menu
   - Wait for Docker to start (you'll see a whale icon in the system tray)
   - Verify installation: Open PowerShell and run `docker --version`

### Alternative: Docker Toolbox (for older Windows versions)

If you're on Windows 10 Home or an older version without WSL 2:
- Download Docker Toolbox: https://github.com/docker/toolbox/releases
- Follow the installation instructions

## After Docker Installation

Once Docker is installed and running, follow these steps:

### 1. Verify Docker Installation

```powershell
# Check Docker version
docker --version

# Check Docker Compose version
docker compose version

# Verify Docker is running
docker info
```

### 2. Start Docker Services

```powershell
# Navigate to project directory
cd C:\Users\ADMIN\Videos\AI-OSINT-Kit

# Start PostgreSQL and Redis
docker compose up -d postgres redis

# Wait for services to be ready (about 10-15 seconds)
timeout /t 10

# Start backend and Celery worker
docker compose up -d backend celery-worker
```

### 3. Run Database Migration

```powershell
# Using the provided script
scripts\run_migration.bat

# Or manually
docker compose exec backend alembic upgrade head
```

### 4. Verify Migration

```powershell
# Check if tables were created
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"
```

You should see these tables:
- users
- scans
- entities
- findings
- reports

### 5. Test the API

```powershell
# Health check
curl http://localhost:8000/health

# Create a test scan
curl -X POST http://localhost:8000/api/v1/scan -H "Content-Type: application/json" -d "{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}"

# Check scan status (replace 1 with the scan_id from previous response)
curl http://localhost:8000/api/v1/scan/1
```

## Quick Start Script

After Docker is installed, you can use the provided setup script:

```powershell
# Run setup script (when available)
scripts\setup.bat
```

## Troubleshooting

### Docker Desktop Won't Start

1. **Check WSL 2 is enabled:**
   ```powershell
   wsl --status
   ```

2. **Update WSL 2:**
   ```powershell
   wsl --update
   ```

3. **Check Hyper-V is enabled** (Windows Pro/Enterprise):
   - Open "Turn Windows features on or off"
   - Enable "Hyper-V" and "Virtual Machine Platform"
   - Restart computer

### Port Already in Use

If you get port conflicts:
- Check if PostgreSQL (5432) or Redis (6379) are already running
- Stop conflicting services or change ports in `docker-compose.yml`

### Docker Compose Command Not Found

If `docker compose` doesn't work, try:
```powershell
docker-compose up -d
```

### Services Won't Start

1. **Check Docker is running:**
   ```powershell
   docker ps
   ```

2. **Check logs:**
   ```powershell
   docker compose logs postgres
   docker compose logs backend
   ```

3. **Rebuild containers:**
   ```powershell
   docker compose down
   docker compose up -d --build
   ```

## What's Next?

After Docker is installed and services are running:

1. ✅ Run database migration
2. ✅ Test the API endpoints
3. ✅ Create your first OSINT scan
4. ✅ Verify entities and findings are stored in the database
5. ✅ Check Celery worker logs for task execution

## Additional Resources

- Docker Documentation: https://docs.docker.com/
- Docker Desktop for Windows: https://docs.docker.com/desktop/windows/
- WSL 2 Installation: https://docs.microsoft.com/windows/wsl/install

## Need Help?

If you encounter issues:
1. Check the logs: `docker compose logs [service-name]`
2. Verify Docker is running: `docker info`
3. Check service status: `docker compose ps`
4. Review the TESTING_GUIDE.md for detailed testing instructions











