# Setup Checklist - Quick Reference

## ✅ What's Already Done (Automated)

- [x] Database migration file created
- [x] SSL certificate OSINT module implemented
- [x] Scan endpoint connected to database
- [x] Celery tasks implemented
- [x] Docker compose configuration ready
- [x] Setup scripts created

## 📋 What You Need to Do (Manual Steps)

### Prerequisites
- [ ] Docker Desktop is installed and running
- [ ] PowerShell or Command Prompt is open
- [ ] You're in the project directory: `C:\Users\ADMIN\Videos\AI-OSINT-Kit`

### Setup Steps

#### Step 1: Start Database Services
```powershell
docker compose up -d postgres redis
```
- [ ] Command executed successfully
- [ ] Services are running (check with `docker compose ps`)

#### Step 2: Start Backend Service
```powershell
docker compose up -d backend
```
- [ ] Command executed successfully
- [ ] Backend container is running
- [ ] Wait 10-15 seconds for backend to start

#### Step 3: Run Database Migration
```powershell
docker compose exec backend alembic upgrade head
```
- [ ] Migration completed successfully
- [ ] No errors in output
- [ ] See message: "Running upgrade -> 001_initial, Initial migration"

#### Step 4: Verify Database Tables
```powershell
docker compose exec -T postgres psql -U postgres -d osintkit -c "\dt"
```
- [ ] See 5 tables: users, scans, entities, findings, reports
- [ ] No errors

#### Step 5: Start Celery Worker
```powershell
docker compose up -d celery-worker
```
- [ ] Celery worker started successfully
- [ ] Container is running

#### Step 6: Test Health Endpoint
```powershell
curl http://localhost:8000/health
```
- [ ] Returns: `{"status":"healthy","service":"ai-osint-kit-api","version":"0.1.0"}`
- [ ] No errors

#### Step 7: Create Test Scan
```powershell
curl -X POST http://localhost:8000/api/v1/scan -H "Content-Type: application/json" -d "{\"target\":\"example.com\",\"type\":\"domain\",\"modules\":[\"whois\",\"ssl\"]}"
```
- [ ] Returns scan_id (e.g., `{"scan_id": 1, ...}`)
- [ ] Status is "queued"

#### Step 8: Check Scan Status
```powershell
curl http://localhost:8000/api/v1/scan/1
```
- [ ] Returns scan details
- [ ] Status eventually changes to "completed" (wait 30-60 seconds)

#### Step 9: View Celery Logs
```powershell
docker compose logs -f celery-worker
```
- [ ] See messages about scan execution
- [ ] See "WHOIS completed" and "SSL certificate lookup completed"
- [ ] See "Scan X completed successfully"

#### Step 10: Verify Database Results
```powershell
# Check scans
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, target, status FROM scans;"

# Check entities
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, type, canonical_value FROM entities LIMIT 10;"

# Check findings
docker compose exec -T postgres psql -U postgres -d osintkit -c "SELECT id, source, type FROM findings LIMIT 10;"
```
- [ ] See scan record in database
- [ ] See entities (domains, subdomains) in database
- [ ] See findings (OSINT results) in database

## 🎯 Success Criteria

All of these should be true:

- [ ] All Docker containers are running (`docker compose ps` shows all services)
- [ ] Health endpoint returns healthy status
- [ ] Can create a scan via API
- [ ] Scan completes successfully (status = "completed")
- [ ] Entities are stored in database
- [ ] Findings are stored in database
- [ ] Celery worker logs show task execution

## 🚨 Troubleshooting

### If a step fails:

1. **Check service status:**
   ```powershell
   docker compose ps
   ```

2. **Check logs:**
   ```powershell
   docker compose logs [service-name]
   ```

3. **Restart services:**
   ```powershell
   docker compose restart [service-name]
   ```

4. **Rebuild if needed:**
   ```powershell
   docker compose up -d --build [service-name]
   ```

## 📝 Notes

- First time building Docker images may take 2-5 minutes
- Wait 10-15 seconds between starting services
- Scan execution takes 30-60 seconds depending on OSINT modules
- Check logs if something doesn't work

## 🎉 When Complete

You should be able to:
- ✅ Create OSINT scans via API
- ✅ See scans execute in Celery worker logs
- ✅ View results in database
- ✅ Access API documentation at http://localhost:8000/docs

## Quick Command Reference

```powershell
# Start all services
docker compose up -d

# Check status
docker compose ps

# View logs
docker compose logs -f [service]

# Restart service
docker compose restart [service]

# Stop all
docker compose down

# Access database
docker compose exec postgres psql -U postgres -d osintkit
```










