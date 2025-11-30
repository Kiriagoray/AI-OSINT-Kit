# Fix Docker Error - Step by Step

## The Error

```
unable to get image 'redis:7-alpine': request returned 500 Internal Server Error
```

## Quick Fix (Try This First)

### Step 1: Restart Docker Desktop

1. **Right-click the Docker icon** in your system tray (bottom right corner)
2. **Click "Quit Docker Desktop"**
3. **Wait 10 seconds**
4. **Open Docker Desktop** from Start menu
5. **Wait 30-60 seconds** until you see "Docker Desktop is running"
6. **Wait another 30 seconds** to make sure it's fully ready

### Step 2: Check Docker is Ready

Run this command:
```powershell
docker info
```

If it returns Docker system information (not an error), Docker is ready!

### Step 3: Try Again

```powershell
.\setup_and_test.bat
```

---

## What I Fixed

I've updated the `docker-compose.yml` file to use more reliable images:
- Changed `postgres:15-alpine` → `postgres:15`
- Changed `redis:7-alpine` → `redis:7`

These non-alpine images are more reliable and less likely to have issues.

## Alternative: Check Docker First

I've created a script to check if Docker is ready before starting services:

```powershell
.\check_docker.bat
```

This will verify:
1. Docker is installed
2. Docker daemon is running
3. Docker API is responding
4. Can pull images

Run this first, then run `setup_and_test.bat` if it passes.

## Manual Steps (If Scripts Don't Work)

### Option 1: Start Services One by One

```powershell
# 1. Pull images manually first
docker pull postgres:15
docker pull redis:7

# 2. Start PostgreSQL
docker compose up -d postgres

# 3. Wait and check it's running
Start-Sleep -Seconds 10
docker compose ps

# 4. Start Redis
docker compose up -d redis

# 5. Continue with backend
docker compose up -d backend
```

### Option 2: Use Docker Desktop UI

1. Open Docker Desktop
2. Go to "Images" tab
3. Click "Pull" and search for:
   - `postgres:15`
   - `redis:7`
4. Wait for images to download
5. Then run `setup_and_test.bat` again

## Common Causes

1. **Docker Desktop still starting** - Wait longer
2. **Docker Desktop needs restart** - Quit and restart
3. **Network issues** - Check internet connection
4. **WSL 2 not ready** - Restart Docker Desktop
5. **Docker API not ready** - Wait 1-2 minutes after Docker starts

## Verify Docker is Working

Run these commands to verify:

```powershell
# Check Docker version
docker --version

# Check Docker daemon
docker info

# List containers (should work even if empty)
docker ps

# Test pulling an image
docker pull hello-world
```

If all these work, Docker is ready!

## Next Steps

1. ✅ **Restart Docker Desktop** (most common fix)
2. ✅ **Wait 1-2 minutes** after Docker starts
3. ✅ **Run `check_docker.bat`** to verify Docker is ready
4. ✅ **Run `setup_and_test.bat`** again

## Still Having Issues?

If the error persists after restarting Docker Desktop:

1. **Check Docker Desktop logs:**
   - Open Docker Desktop
   - Click the bug icon (top right)
   - Check for errors

2. **Try updating Docker Desktop:**
   - Open Docker Desktop
   - Settings → Software Updates
   - Update if available

3. **Check WSL 2:**
   ```powershell
   wsl --status
   ```
   Should show WSL 2 is running

4. **Restart your computer:**
   - Sometimes a full restart fixes Docker issues

## Summary

**Most likely fix:** Restart Docker Desktop and wait 1-2 minutes

**What I changed:** Updated docker-compose.yml to use non-alpine images (more reliable)

**Next step:** Run `check_docker.bat` to verify Docker is ready, then run `setup_and_test.bat`

Good luck! 🚀










