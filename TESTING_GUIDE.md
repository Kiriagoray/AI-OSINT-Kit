# Testing Guide

This guide will help you test the AI-OSINT-Kit implementation after setup.

## Prerequisites

1. Docker and Docker Compose installed
2. All services running (PostgreSQL, Redis, Backend, Celery Worker)

## Quick Start

### 1. Start Services

```bash
# Start all services
docker compose up -d

# Or start specific services
docker compose up -d postgres redis backend celery-worker
```

### 2. Run Database Migration

```bash
# Using the provided script (Linux/Mac)
./scripts/run_migration.sh

# Or manually
docker compose exec backend alembic upgrade head

# On Windows
scripts\run_migration.bat
```

### 3. Verify Migration

```bash
# Check if tables were created
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"

# You should see:
# - users
# - scans
# - entities
# - findings
# - reports
```

## Testing the API

### 1. Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{
  "status": "healthy",
  "service": "ai-osint-kit-api",
  "version": "0.1.0"
}
```

### 2. Create a Scan

```bash
curl -X POST http://localhost:8000/api/v1/scan \
  -H "Content-Type: application/json" \
  -d '{
    "target": "example.com",
    "type": "domain",
    "modules": ["whois", "ssl"]
  }'
```

Expected response:
```json
{
  "scan_id": 1,
  "status": "queued",
  "target": "example.com",
  "type": "domain",
  "created_at": "2024-01-01T00:00:00"
}
```

### 3. Check Scan Status

```bash
# Replace {scan_id} with the ID from the previous response
curl http://localhost:8000/api/v1/scan/1
```

Expected response (when completed):
```json
{
  "scan_id": 1,
  "target": "example.com",
  "type": "domain",
  "status": "completed",
  "settings": {"modules": ["whois", "ssl"]},
  "created_at": "2024-01-01T00:00:00",
  "started_at": "2024-01-01T00:00:01",
  "finished_at": "2024-01-01T00:00:30"
}
```

### 4. Check Entities

```bash
# Get entities for a scan (when endpoint is implemented)
curl http://localhost:8000/api/v1/entity?scan_id=1
```

## Testing OSINT Modules

### WHOIS Module

The WHOIS module should:
- Query domain registration information
- Extract name servers
- Store domain entity and findings

### SSL Certificate Module

The SSL certificate module should:
- Query crt.sh for certificate transparency logs
- Extract subdomains
- Store subdomain entities
- Store certificate findings

## Checking Celery Tasks

### View Celery Logs

```bash
# View Celery worker logs
docker compose logs -f celery-worker

# You should see task execution logs like:
# [INFO] Starting scan 1 for target example.com
# [INFO] Running WHOIS for example.com
# [INFO] WHOIS completed for example.com
# [INFO] Running SSL certificate lookup for example.com
# [INFO] SSL certificate lookup completed for example.com, found X subdomains
# [INFO] Scan 1 completed successfully
```

### Check Redis (Celery Broker)

```bash
# Connect to Redis
docker compose exec redis redis-cli

# Check Celery tasks
KEYS celery*

# Monitor tasks
MONITOR
```

## Database Verification

### Check Scans

```bash
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, target, type, status, created_at FROM scans;"
```

### Check Entities

```bash
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, scan_id, type, canonical_value FROM entities LIMIT 10;"
```

### Check Findings

```bash
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, entity_id, source, type, confidence_score FROM findings LIMIT 10;"
```

## Troubleshooting

### Migration Fails

If migration fails, check:
1. PostgreSQL is running: `docker compose ps postgres`
2. Database connection: `docker compose exec postgres psql -U postgres -d osintkit -c "SELECT 1;"`
3. Migration file exists: `ls backend/alembic/versions/`

### Celery Tasks Not Running

If tasks aren't running:
1. Check Celery worker is running: `docker compose ps celery-worker`
2. Check Redis is running: `docker compose ps redis`
3. Check Celery logs: `docker compose logs celery-worker`
4. Verify task is queued in Redis

### API Errors

If API returns errors:
1. Check backend logs: `docker compose logs backend`
2. Verify database connection in backend logs
3. Check if scan was created in database
4. Verify Celery broker URL in environment

## Next Steps

After successful testing:
1. Implement additional OSINT modules
2. Add unit tests for modules
3. Implement frontend integration
4. Add authentication and authorization
5. Implement report generation

## Useful Commands

```bash
# View all logs
docker compose logs -f

# View specific service logs
docker compose logs -f backend
docker compose logs -f celery-worker

# Restart services
docker compose restart backend celery-worker

# Rebuild and restart
docker compose up -d --build backend celery-worker

# Access database
docker compose exec postgres psql -U postgres -d osintkit

# Access Redis
docker compose exec redis redis-cli

# Stop all services
docker compose down

# Stop and remove volumes (WARNING: deletes data)
docker compose down -v
```











