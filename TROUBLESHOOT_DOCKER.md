# Troubleshooting Docker Error

## Error You're Seeing

```
unable to get image 'redis:7-alpine': request returned 500 Internal Server Error
```

This usually means Docker Desktop isn't fully ready or needs to be restarted.

## Quick Fixes (Try in Order)

### Fix 1: Restart Docker Desktop

1. **Close Docker Desktop completely:**
   - Right-click the Docker icon in system tray (bottom right)
   - Click "Quit Docker Desktop"
   - Wait for it to fully close

2. **Restart Docker Desktop:**
   - Open Docker Desktop from Start menu
   - Wait for it to fully start (whale icon should be stable, not animating)
   - Wait 30-60 seconds after it shows "Docker Desktop is running"

3. **Verify Docker is ready:**
   ```powershell
   docker info
   ```
   Should return Docker system information (not an error)

### Fix 2: Check Docker Desktop Status

Make sure Docker Desktop shows:
- ✅ "Docker Desktop is running"
- ✅ No error messages
- ✅ All services are green/healthy

### Fix 3: Try Pulling Images Manually

```powershell
# Pull PostgreSQL image
docker pull postgres:15-alpine

# Pull Redis image
docker pull redis:7-alpine
```

If these fail, Docker Desktop needs to be restarted.

### Fix 4: Use Alternative Images

If the alpine images don't work, we can use regular images instead.

## Step-by-Step Solution

### Step 1: Restart Docker Desktop

1. Quit Docker Desktop (right-click tray icon → Quit)
2. Wait 10 seconds
3. Start Docker Desktop again
4. Wait until it's fully started (30-60 seconds)

### Step 2: Verify Docker is Working

```powershell
docker --version
docker info
docker ps
```

All commands should work without errors.

### Step 3: Try Starting Services Again

```powershell
docker compose up -d postgres redis
```

### Step 4: If Still Failing - Use Alternative Images

We can modify docker-compose.yml to use different image versions that might work better.

## Alternative: Use Different Image Versions

If alpine images don't work, we can try:
- `postgres:15` instead of `postgres:15-alpine`
- `redis:7` instead of `redis:7-alpine`

Let me know if you want me to update the docker-compose.yml file.










