# Step-by-Step Setup Guide

## What I've Already Done For You ✅

1. ✅ **Database Migration Created** - `backend/alembic/versions/001_initial_migration.py`
2. ✅ **SSL Certificate Module Implemented** - `backend/app/services/osint/ssl.py`
3. ✅ **Scan Endpoint Connected to Database** - `backend/app/api/v1/endpoints/scan.py`
4. ✅ **Celery Tasks Implemented** - `backend/app/tasks/scan.py`
5. ✅ **Docker Compose Configuration** - `docker-compose.yml` (fixed version warning)
6. ✅ **Setup Scripts Created** - `setup_and_test.bat`

## What You Need to Do - Step by Step

### STEP 1: Open PowerShell or Command Prompt

1. Press `Win + X` and select "Windows PowerShell" or "Terminal"
2. Navigate to the project directory:
   ```powershell
   cd C:\Users\ADMIN\Videos\AI-OSINT-Kit
   ```

### STEP 2: Verify Docker is Running

Run this command to check:
```powershell
docker --version
```

**Expected output:** `Docker version 28.5.1, build e180ab8` (or similar)

If Docker is not running:
- Open Docker Desktop from the Start menu
- Wait for it to start (whale icon in system tray should be stable)

### STEP 3: Start PostgreSQL and Redis

Run this command:
```powershell
docker compose up -d postgres redis
```

**What to expect:**
- You should see messages like "Creating osintkit-postgres..." and "Creating osintkit-redis..."
- Containers should start successfully

**Wait 10-15 seconds** for services to be ready.

### STEP 4: Verify Services Started

Check if services are running:
```powershell
docker compose ps
```

**Expected output:**
```
NAME                  STATUS
osintkit-postgres     Running
osintkit-redis        Running
```

If you see "Up" or "Running" status, you're good to continue.

### STEP 5: Start Backend Service

Run this command:
```powershell
docker compose up -d backend
```

**What to expect:**
- First time: It will build the Docker image (this may take 2-5 minutes)
- You'll see messages about building and starting the backend container
- Wait for it to complete

**Wait 10-15 seconds** for backend to be ready.

### STEP 6: Run Database Migration

This creates all the database tables. Run:
```powershell
docker compose exec backend alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Context impl PostgresqlImpl.
INFO  [alembic.runtime.migration] Will assume transactional DDL.
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial, Initial migration
```

**If you see errors:**
- Wait a bit longer and try again (backend might still be starting)
- Check logs: `docker compose logs backend`

### STEP 7: Verify Database Tables Were Created

Check if tables exist:
```powershell
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"
```

**Expected output:**
```
              List of relations
 Schema |   Name    | Type  |  Owner
--------+-----------+-------+----------
 public | entities  | table | postgres
 public | findings  | table | postgres
 public | reports   | table | postgres
 public | scans     | table | postgres
 public | users     | table | postgres
```

You should see 5 tables: users, scans, entities, findings, reports

### STEP 8: Start Celery Worker

This handles background OSINT tasks:
```powershell
docker compose up -d celery-worker
```

**Expected output:**
- Container should start successfully
- You can verify with: `docker compose ps`

### STEP 9: Test the API - Health Check

Test if the backend is working:
```powershell
curl http://localhost:8000/health
```

**Expected output:**
```json
{"status":"healthy","service":"ai-osint-kit-api","version":"0.1.0"}
```

**If this doesn't work:**
- Check if backend is running: `docker compose ps backend`
- Check backend logs: `docker compose logs backend`
- Wait a bit longer and try again

### STEP 10: Create Your First OSINT Scan

Test the scan endpoint:
```powershell
curl -X POST http://localhost:8000/api/v1/scan -H "Content-Type: application/json" -d "{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}"
```

**Expected output:**
```json
{
  "scan_id": 1,
  "status": "queued",
  "target": "example.com",
  "type": "domain",
  "created_at": "2024-..."
}
```

**Note the `scan_id`** from the response (it will be `1` for the first scan).

### STEP 11: Check Scan Status

Replace `1` with your scan_id from step 10:
```powershell
curl http://localhost:8000/api/v1/scan/1
```

**Expected output:**
```json
{
  "scan_id": 1,
  "target": "example.com",
  "type": "domain",
  "status": "completed",
  "settings": {"modules": ["whois", "ssl"]},
  "created_at": "...",
  "started_at": "...",
  "finished_at": "..."
}
```

**Status progression:**
- `queued` → `running` → `completed` (or `failed` if there's an error)

### STEP 12: View Celery Worker Logs

See the OSINT tasks being executed:
```powershell
docker compose logs -f celery-worker
```

**What you should see:**
- Messages like "Starting scan 1 for target example.com"
- "Running WHOIS for example.com"
- "WHOIS completed for example.com"
- "Running SSL certificate lookup for example.com"
- "Scan 1 completed successfully"

Press `Ctrl+C` to exit the logs view.

### STEP 13: Check Database for Results

See what was stored in the database:
```powershell
# Check scans
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, target, type, status FROM scans;"

# Check entities (domains, subdomains found)
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, scan_id, type, canonical_value FROM entities LIMIT 10;"

# Check findings (OSINT results)
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, entity_id, source, type FROM findings LIMIT 10;"
```

## Troubleshooting Common Issues

### Issue: "docker compose" command not found

**Solution:**
- Try: `docker-compose` (with hyphen) instead of `docker compose`
- Or update Docker Desktop to the latest version

### Issue: Port already in use

**Solution:**
```powershell
# Check what's using the port
netstat -ano | findstr :8000
netstat -ano | findstr :5432
netstat -ano | findstr :6379

# Stop conflicting services or change ports in docker-compose.yml
```

### Issue: Migration fails

**Solution:**
```powershell
# Check backend logs
docker compose logs backend

# Check if backend is ready
docker compose ps backend

# Wait longer and try again
docker compose exec backend alembic upgrade head
```

### Issue: Backend won't start

**Solution:**
```powershell
# Check logs
docker compose logs backend

# Rebuild the container
docker compose up -d --build backend

# Check if PostgreSQL is running
docker compose ps postgres
```

### Issue: Celery tasks not running

**Solution:**
```powershell
# Check Celery worker logs
docker compose logs celery-worker

# Check if Redis is running
docker compose ps redis

# Restart Celery worker
docker compose restart celery-worker
```

### Issue: API returns errors

**Solution:**
```powershell
# Check all service status
docker compose ps

# Check backend logs
docker compose logs backend

# Restart all services
docker compose restart
```

## Quick Reference Commands

```powershell
# View all running services
docker compose ps

# View logs (replace [service] with: backend, celery-worker, postgres, redis)
docker compose logs -f [service]

# Restart a service
docker compose restart [service]

# Stop all services
docker compose down

# Start all services
docker compose up -d

# Rebuild and start
docker compose up -d --build

# Access database directly
docker compose exec postgres psql -U postgres -d osintkit
```

## Success Checklist

After completing all steps, you should have:

- [ ] ✅ Docker is running
- [ ] ✅ PostgreSQL container is running
- [ ] ✅ Redis container is running
- [ ] ✅ Backend container is running
- [ ] ✅ Celery worker container is running
- [ ] ✅ Database migration completed
- [ ] ✅ 5 tables created in database (users, scans, entities, findings, reports)
- [ ] ✅ Health endpoint returns healthy status
- [ ] ✅ Can create a scan via API
- [ ] ✅ Scan status changes to "completed"
- [ ] ✅ Entities and findings stored in database
- [ ] ✅ Celery worker logs show task execution

## Next Steps After Setup

1. **Explore the API:**
   - Visit http://localhost:8000/docs for interactive API documentation
   - Try creating different types of scans (domain, email, ip)

2. **Check Results:**
   - View entities found in database
   - Check findings for each entity
   - See what OSINT data was collected

3. **View Logs:**
   - Monitor backend logs: `docker compose logs -f backend`
   - Monitor Celery logs: `docker compose logs -f celery-worker`

4. **Test More Features:**
   - Create scans with different modules
   - Test different target types
   - Check database for stored results

## Need Help?

If you encounter issues:

1. **Check the logs:**
   ```powershell
   docker compose logs -f
   ```

2. **Verify services are running:**
   ```powershell
   docker compose ps
   ```

3. **Check specific service logs:**
   ```powershell
   docker compose logs [service-name]
   ```

4. **Review documentation:**
   - `TESTING_GUIDE.md` - Detailed testing instructions
   - `IMPLEMENTATION_SUMMARY.md` - Implementation details
   - `RUN_SETUP.md` - Alternative setup instructions

## Summary

**What's Ready:**
- ✅ All code is implemented
- ✅ Database migration is ready
- ✅ OSINT modules are implemented
- ✅ API endpoints are connected
- ✅ Celery tasks are ready

**What You Need to Do:**
1. Start Docker services (Steps 3-8)
2. Run migration (Step 6)
3. Test the API (Steps 9-11)
4. Verify results (Steps 12-13)

**Estimated Time:** 10-15 minutes (depending on Docker image build time)

Good luck! 🚀










