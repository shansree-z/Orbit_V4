# Quick Start Guide - New-Hire Onboarding Concierge

## Installation & Setup (Windows)

### Step 1: Install Python
If you haven't already, download and install Python 3.8+ from https://www.python.org/
Make sure to check "Add Python to PATH" during installation.

### Step 2: Install Dependencies
Open Command Prompt and navigate to the project directory:
```cmd
cd C:\Users\Shansree\Desktop\OrbitV4\backend
pip install -r requirements.txt
```

### Step 3: Initialize Database
Run the setup script:
```cmd
python setup.py
```

This will:
- Create the SQLite database (onboarding.db)
- Create all necessary tables
- Seed demo user accounts

### Step 4: Start the Server
```cmd
python main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

### Step 5: Access the Application
Open your web browser and go to:
```
http://localhost:8000
```

## Quick Start on macOS/Linux

### Step 1-2: Install Python & Dependencies
```bash
cd ~/Desktop/OrbitV4/backend
pip3 install -r requirements.txt
```

### Step 3-4: Initialize & Run
```bash
python3 setup.py
python3 main.py
```

Then open http://localhost:8000 in your browser.

## Demo Workflow

### As HR Admin:

1. **Login**
   - Email: hr@company.com
   - Password: Hr@123
   - Role: HR

2. **Create Employee**
   - Click "New Employee"
   - Fill in employee details
   - Click "Create Employee"
   - Click "Start Onboarding"

3. **Monitor Progress**
   - View real-time task execution
   - See progress percentage
   - Check execution logs
   - Notice task timeline updates

### As Manager:

1. **Login**
   - Email: manager@company.com
   - Password: Manager@123
   - Role: Manager

2. **Monitor Dashboard**
   - View all employees
   - See onboarding progress
   - Identify failed tasks

3. **Manage Failed Tasks**
   - Click on an employee to see details
   - Click "Retry Task" on failed tasks
   - Monitor retry attempts

## Key Features to Try

### Real-time Updates
- Task progress updates every 2 seconds
- Dashboard auto-refreshes every 5 seconds
- Watch tasks execute in real-time

### Task Failures
- 10% of tasks randomly fail to simulate real scenarios
- See detailed error messages
- Retry individual failed tasks

### Progress Tracking
- Visual progress bars show completion
- Task timeline shows all executed steps
- Execution logs record all actions

### Role-Based Access
- HR: Create employees, start onboarding, view all data
- Manager: Monitor progress, manage failures, view logs

## Troubleshooting

### Port 8000 Already in Use
Change the port in main.py:
```python
uvicorn.run(app, host="127.0.0.1", port=8001, reload=True)
```

### Database Issues
Delete the onboarding.db file and run setup.py again:
```cmd
del onboarding.db
python setup.py
```

### Module Import Errors
Make sure you're running the server from the backend directory:
```cmd
cd backend
python main.py
```

### Can't Find localhost:8000
Make sure the server is running and check http://127.0.0.1:8000

## Project Structure

```
OrbitV4/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── auth/              # JWT authentication
│   │   ├── models/            # Database models
│   │   ├── orchestrator/       # Workflow agent
│   │   └── routes/            # API endpoints
│   ├── main.py                # Entry point
│   ├── requirements.txt        # Python dependencies
│   ├── setup.py              # Database setup
│   └── .env                  # Configuration
├── frontend/                  # Web interface
│   ├── css/                  # Styling
│   ├── js/                   # Client-side logic
│   ├── index.html            # Login page
│   ├── dashboard.html        # HR dashboard
│   ├── new-employee.html     # Employee creation
│   ├── employee-status.html  # Task tracking
│   └── manager-monitoring.html # Manager view
├── README.md                 # Full documentation
└── run.bat / run.sh         # Quick start scripts
```

## API Documentation

Once the server is running, view the API docs at:
```
http://localhost:8000/docs
```

## Next Steps

1. Explore the UI and try creating employees
2. Monitor real-time task execution
3. Test retry functionality on failed tasks
4. Review execution logs
5. Check the database (onboarding.db) using SQLite viewer

## Support

For more detailed information, see README.md
