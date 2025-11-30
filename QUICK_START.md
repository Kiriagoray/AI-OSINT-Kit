# Quick Start Guide

## Docker is Installed - Let's Get Started!

### Option 1: Automated Setup (Recommended)

Run the automated setup script:

```bash
# Windows
setup_and_test.bat

# This will:
# 1. Check Docker installation
# 2. Start PostgreSQL and Redis
# 3. Start Backend service
# 4. Run database migration
# 5. Verify tables were created
# 6. Start Celery worker
```

### Option 2: Manual Setup

#### Step 1: Start Services

```powershell
# Start PostgreSQL and Redis
docker compose up -d postgres redis

# Wait for services to be ready (10-15 seconds)
Start-Sleep -Seconds 10

# Start backend
docker compose up -d backend

# Wait for backend to be ready
Start-Sleep -Seconds 5
```

#### Step 2: Run Migration

```powershell
# Run database migration
docker compose exec backend alembic upgrade head

# Verify migration
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"
```

#### Step 3: Start Celery Worker

```powershell
# Start Celery worker for background tasks
docker compose up -d celery-worker
```

#### Step 4: Test the API

```powershell
# Health check
curl http://localhost:8000/health

# Create a test scan
curl -X POST http://localhost:8000/api/v1/scan `
  -H "Content-Type: application/json" `
  -d '{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}'

# Check scan status (replace 1 with scan_id from response)
curl http://localhost:8000/api/v1/scan/1
```

## Verify Everything is Working

### Check Service Status

```powershell
docker compose ps
```

You should see:
- `osintkit-postgres` - Running
- `osintkit-redis` - Running
- `osintkit-backend` - Running
- `osintkit-celery` - Running

### Check Logs

```powershell
# Backend logs
docker compose logs -f backend

# Celery worker logs
docker compose logs -f celery-worker

# All logs
docker compose logs -f
```

### Check Database

```powershell
# Connect to database
docker compose exec postgres psql -U postgres -d osintkit

# List tables
\dt

# Check scans
SELECT id, target, type, status, created_at FROM scans;

# Check entities
SELECT id, scan_id, type, canonical_value FROM entities LIMIT 10;

# Check findings
SELECT id, entity_id, source, type FROM findings LIMIT 10;

# Exit
\q
```

## Troubleshooting

### Services Won't Start

```powershell
# Check if ports are in use
netstat -ano | findstr :5432  # PostgreSQL
netstat -ano | findstr :6379  # Redis
netstat -ano | findstr :8000  # Backend

# Stop conflicting services or change ports in docker-compose.yml
```

### Migration Fails

```powershell
# Check backend logs
docker compose logs backend

# Check database connection
docker compose exec postgres psql -U postgres -d osintkit -c "SELECT 1;"

# Try running migration again
docker compose exec backend alembic upgrade head
```

### Celery Tasks Not Running

```powershell
# Check Celery worker is running
docker compose ps celery-worker

# Check Redis is running
docker compose ps redis

# Check Celery logs
docker compose logs celery-worker

# Restart Celery worker
docker compose restart celery-worker
```

### API Not Responding

```powershell
# Check backend is running
docker compose ps backend

# Check backend logs
docker compose logs backend

# Check if port 8000 is accessible
curl http://localhost:8000/health

# Restart backend
docker compose restart backend
```

## Next Steps

1. ✅ Run setup script: `setup_and_test.bat`
2. ✅ Verify services are running: `docker compose ps`
3. ✅ Test health endpoint: `curl http://localhost:8000/health`
4. ✅ Create your first scan
5. ✅ Check scan results in database
6. ✅ View Celery worker logs to see task execution

## Useful Commands

```powershell
# Start all services
docker compose up -d

# Stop all services
docker compose down

# View logs
docker compose logs -f [service-name]

# Restart a service
docker compose restart [service-name]

# Rebuild and restart
docker compose up -d --build [service-name]

# Access database
docker compose exec postgres psql -U postgres -d osintkit

# Access Redis
docker compose exec redis redis-cli
```

## Success Indicators

You'll know everything is working when:

1. ✅ All services show as "Running" in `docker compose ps`
2. ✅ Health endpoint returns: `{"status":"healthy","service":"ai-osint-kit-api","version":"0.1.0"}`
3. ✅ Creating a scan returns a scan_id
4. ✅ Scan status changes from "queued" → "running" → "completed"
5. ✅ Entities and findings appear in the database
6. ✅ Celery worker logs show task execution

## Need Help?

- Check logs: `docker compose logs -f`
- Verify services: `docker compose ps`
- Check database: `docker compose exec postgres psql -U postgres -d osintkit`
- Review TESTING_GUIDE.md for detailed testing instructions










