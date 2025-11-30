# Run Setup - Step by Step Instructions

## Docker is Installed! Let's Set Up the Application

### Quick Option: Run the Setup Script

**Double-click or run:**
```
setup_and_test.bat
```

This will automatically:
1. Check Docker
2. Start all services
3. Run the migration
4. Verify everything is working

---

### Manual Option: Step by Step

Open PowerShell or Command Prompt in the project directory and run these commands:

#### Step 1: Start PostgreSQL and Redis

```powershell
docker compose up -d postgres redis
```

Wait about 10 seconds for services to start.

#### Step 2: Check Services are Running

```powershell
docker compose ps
```

You should see `osintkit-postgres` and `osintkit-redis` with status "Running".

#### Step 3: Start Backend Service

```powershell
docker compose up -d backend
```

Wait about 5-10 seconds for the backend to start.

#### Step 4: Run Database Migration

```powershell
docker compose exec backend alembic upgrade head
```

This will create all the database tables. You should see output like:
```
INFO  [alembic.runtime.migration] Running upgrade  -> 001_initial, Initial migration
```

#### Step 5: Verify Database Tables

```powershell
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"
```

You should see tables: users, scans, entities, findings, reports

#### Step 6: Start Celery Worker

```powershell
docker compose up -d celery-worker
```

#### Step 7: Test the API

```powershell
# Health check
curl http://localhost:8000/health
```

Expected response:
```json
{"status":"healthy","service":"ai-osint-kit-api","version":"0.1.0"}
```

#### Step 8: Create a Test Scan

```powershell
curl -X POST http://localhost:8000/api/v1/scan -H "Content-Type: application/json" -d "{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}"
```

Expected response:
```json
{
  "scan_id": 1,
  "status": "queued",
  "target": "example.com",
  "type": "domain",
  "created_at": "2024-..."
}
```

#### Step 9: Check Scan Status

```powershell
# Replace 1 with the scan_id from the previous response
curl http://localhost:8000/api/v1/scan/1
```

#### Step 10: View Logs

```powershell
# Backend logs
docker compose logs -f backend

# Celery worker logs (to see OSINT task execution)
docker compose logs -f celery-worker
```

---

## Troubleshooting

### If services won't start:

1. **Check Docker is running:**
   ```powershell
   docker info
   ```

2. **Check for port conflicts:**
   ```powershell
   netstat -ano | findstr :5432  # PostgreSQL
   netstat -ano | findstr :6379  # Redis
   netstat -ano | findstr :8000  # Backend
   ```

3. **Rebuild containers:**
   ```powershell
   docker compose down
   docker compose up -d --build
   ```

### If migration fails:

1. **Check backend logs:**
   ```powershell
   docker compose logs backend
   ```

2. **Check database connection:**
   ```powershell
   docker compose exec postgres psql -U postgres -d osintkit -c "SELECT 1;"
   ```

3. **Try migration again:**
   ```powershell
   docker compose exec backend alembic upgrade head
   ```

### If API doesn't respond:

1. **Check backend is running:**
   ```powershell
   docker compose ps backend
   ```

2. **Check backend logs:**
   ```powershell
   docker compose logs backend
   ```

3. **Restart backend:**
   ```powershell
   docker compose restart backend
   ```

---

## Success Checklist

- [ ] Docker is running (`docker info` works)
- [ ] PostgreSQL is running (`docker compose ps` shows postgres as "Running")
- [ ] Redis is running (`docker compose ps` shows redis as "Running")
- [ ] Backend is running (`docker compose ps` shows backend as "Running")
- [ ] Migration completed (`alembic upgrade head` succeeded)
- [ ] Tables created (5 tables: users, scans, entities, findings, reports)
- [ ] Health endpoint works (`curl http://localhost:8000/health` returns JSON)
- [ ] Scan creation works (POST `/api/v1/scan` returns scan_id)
- [ ] Celery worker is running (`docker compose ps` shows celery-worker as "Running")

---

## Next Steps After Setup

1. ✅ Create your first OSINT scan
2. ✅ Check scan results in the database
3. ✅ View entities and findings
4. ✅ Explore the API documentation at http://localhost:8000/docs

---

## Useful Commands Reference

```powershell
# View all running services
docker compose ps

# View logs
docker compose logs -f [service-name]

# Restart a service
docker compose restart [service-name]

# Stop all services
docker compose down

# Start all services
docker compose up -d

# Access database
docker compose exec postgres psql -U postgres -d osintkit

# Check database tables
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"

# View scan data
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT * FROM scans;"
```

---

## Need Help?

- Check the logs: `docker compose logs -f`
- Review TESTING_GUIDE.md for detailed testing instructions
- Check IMPLEMENTATION_SUMMARY.md for implementation details










