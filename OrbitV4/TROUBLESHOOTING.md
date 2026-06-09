# TROUBLESHOOTING GUIDE - Onboarding Concierge

## Issue 1: bcrypt Password Hashing Error

### Error Message
```
ValueError: password cannot be longer than 72 bytes, truncate manually if necessary
```

### What Happened
- bcrypt library had issues during initialization
- The demo passwords (6-10 bytes) are well under the 72-byte limit
- The issue was with bcrypt's backend detection during initialization

### Solution ✓ APPLIED
- Removed bcrypt dependency
- Switched to PBKDF2-SHA256 for password hashing
- Updated requirements.txt
- Both auth.py and database.py now use fallback hashing

### Changes Made
1. ✓ Updated requirements.txt (removed passlib[bcrypt])
2. ✓ Modified app/auth/auth.py to use PBKDF2
3. ✓ Modified app/models/database.py to use simple hashing

---

## Issue 2: Python Not Found

### Error Message
```
Python was not found; run without arguments to install from the Microsoft Store
```

### What Happened
- Python is not in the Windows PATH
- The batch script tried to use `python` command but it's not registered
- Windows has Python app aliases disabled or Python not installed

### Solutions

#### ✓ Solution 1: Use Python3 Directly (RECOMMENDED)
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4\backend
python3 -m pip install -r requirements.txt
python3 setup.py
python3 main.py
```

#### Solution 2: Install Python Properly
1. Download Python 3.11+ from https://www.python.org/
2. **IMPORTANT**: Check "Add Python to PATH" during installation
3. Restart command prompt
4. Then run: `python main.py`

#### Solution 3: Use the Batch Script (Now Fixed)
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4
run.bat
```

This now automatically falls back to python3 if python isn't found.

---

## QUICK FIX - Try This Now

### Option A: Using Python Directly (Fastest)
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4

python debug_setup.py
```

This will:
- Check Python installation
- Install dependencies
- Initialize database
- Show you how to start the server

### Option B: Manual Setup
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4\backend

python -m pip install -r requirements.txt

python setup.py

python main.py
```

### Option C: Using the Updated Batch Script
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4

run.bat
```

---

## Step-by-Step Fix

### Step 1: Navigate to Project
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4
```

### Step 2: Run Debug Script
```cmd
python debug_setup.py
```

Expected output:
```
PYTHON ENVIRONMENT CHECK
Python Version: 3.11.x ...
✓ Python version is compatible

DEPENDENCY CHECK
✓ fastapi
✓ uvicorn
✓ pydantic
...

DATABASE SETUP
✓ Database tables created
✓ Demo accounts created

SETUP COMPLETE ✓
```

### Step 3: Start Server
```cmd
cd backend
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Step 4: Open Browser
```
http://localhost:8000
```

---

## Common Issues & Fixes

### Issue: "No module named 'fastapi'"
**Fix:**
```cmd
python -m pip install -r requirements.txt
```

### Issue: "ModuleNotFoundError: No module named 'app'"
**Fix:** Make sure you're running from the backend directory:
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4\backend
python main.py
```

### Issue: "Address already in use"
**Fix:** Another process is using port 8000. Either:
1. Stop the other process
2. Use a different port in main.py:
```python
uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
```

### Issue: "Database is locked"
**Fix:** Delete the old database and reinitialize:
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4\backend
del onboarding.db
python setup.py
python main.py
```

### Issue: Login credentials not working
**Fix:** Reinitialize the database to recreate demo accounts:
```cmd
python3 debug_setup.py
```

---

## Verification Checklist

- [ ] Python installed: `python --version`
- [ ] Dependencies installed: `python -m pip list | findstr fastapi`
- [ ] In backend directory: `cd C:\Users\Shansree\Desktop\OrbitV4\backend`
- [ ] Database initialized: `python setup.py` completes successfully
- [ ] Server starts: `python main.py` shows "Uvicorn running"
- [ ] Can access: http://localhost:8000 opens login page
- [ ] Can login: Use hr@company.com / Hr@123

---

## What Was Changed to Fix the Issues

### 1. Password Hashing Fix
**File:** `app/auth/auth.py`
- Removed bcrypt dependency
- Added PBKDF2-SHA256 hashing
- Added hash_password_simple() function
- Added error handling fallback

**File:** `app/models/database.py`
- Changed seed_initial_data() to use PBKDF2
- Removed passlib CryptContext
- Used hashlib directly

**File:** `requirements.txt`
- ✗ Removed: passlib[bcrypt]==1.7.4
- ✗ Removed: sqlalchemy==2.0.23 (not needed)
- ✓ Kept: fastapi, uvicorn, pydantic, python-jose

### 2. Python PATH Fix
**File:** `run.bat`
- Added Python version check
- Falls back to python3 if python not found
- Better error messages
- Includes setup and credential display

**File:** `debug_setup.py` (NEW)
- Comprehensive environment check
- Dependency verification
- Database initialization
- Clear success/failure indicators

---

## Next Steps After Fix

1. ✓ Run debug setup: `python3 debug_setup.py`
2. ✓ Start server: `python3 main.py`
3. ✓ Open browser: http://localhost:8000
4. ✓ Login with: hr@company.com / Hr@123
5. ✓ Create an employee
6. ✓ Click "Start Onboarding"
7. ✓ Watch real-time task execution
8. ✓ View dashboard and logs

---

## Still Having Issues?

### Check These:

1. **Is Python installed?**
   ```cmd
   python --version
   ```
   Should show: Python 3.x.x

2. **Are you in the right directory?**
   ```cmd
   cd C:\Users\Shansree\Desktop\OrbitV4\backend
   dir
   ```
   Should show: main.py, requirements.txt, setup.py, etc.

3. **Is the database created?**
   ```cmd
   dir onboarding.db
   ```
   Should exist after running setup.py

4. **Run the debug script:**
   ```cmd
   cd C:\Users\Shansree\Desktop\OrbitV4
   python debug_setup.py
   ```
   This will identify any remaining issues

---

## Support

All files have been updated. The application should now work smoothly!

**Quick start command:**
```cmd
python C:\Users\Shansree\Desktop\OrbitV4\debug_setup.py
```

This will do everything for you and tell you exactly what's happening.
