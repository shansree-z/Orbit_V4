# New-Hire Onboarding Concierge

A professional AI-powered employee onboarding management system with orchestrator agent coordination and real-time progress tracking.

## Features

- **Orchestrator Agent**: Pure rule-based workflow coordinator with 8 sequential onboarding tasks
- **Real-time Progress Tracking**: Live dashboard updates with task execution status
- **Dual Role System**: Separate interfaces for HR and Manager roles
- **Task Retry Management**: Managers can retry failed tasks
- **Comprehensive Logging**: All actions tracked with execution history
- **Enterprise UI Theme**: Professional corporate design with blue primary color
- **JWT Authentication**: Secure token-based authentication
- **SQLite Database**: Lightweight persistent data storage

## Architecture

### Backend
- **FastAPI**: Modern Python web framework
- **SQLite**: Lightweight relational database
- **Orchestrator Agent**: Rule-based workflow coordinator
- **Mock Tasks**: 8 simulated onboarding task functions

### Frontend
- **Responsive HTML/CSS/JavaScript**: No framework dependencies
- **Enterprise Dashboard**: Real-time status monitoring
- **Real-time Updates**: 2-5 second auto-refresh intervals

### Database Schema
- **Employees**: Employee records and onboarding status
- **Tasks**: Individual task execution and status tracking
- **Logs**: Comprehensive action logging
- **Users**: Authentication credentials and roles

## Onboarding Tasks

The orchestrator executes 8 sequential tasks:

1. Create Employee Account
2. Create Company Email
3. Request Laptop
4. Assign Software Licenses
5. Generate Employee ID Card
6. Add Employee to Team Workspace
7. Grant System Access Permissions
8. Register Employee in HR Database

Each task includes:
- Random execution time (1-2 seconds)
- 10% failure rate for realistic scenarios
- Detailed error messages on failure
- Retry capability for failed tasks

## Getting Started

### Prerequisites
- Python 3.8+
- pip package manager

### Installation

1. Navigate to the backend directory:
```bash
cd backend
```

2. Create a virtual environment (optional but recommended):
```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Initialize the database:
```bash
python -c "from app.models.database import init_db, seed_initial_data; init_db(); seed_initial_data()"
```

### Running the Application

1. Start the FastAPI server:
```bash
python main.py
```

The server will start at `http://127.0.0.1:8000`

2. Open your browser and navigate to:
```
http://localhost:8000
```

## Demo Accounts

### HR Admin
- **Email**: hr@company.com
- **Password**: Hr@123

### Manager
- **Email**: manager@company.com
- **Password**: Manager@123

## User Workflows

### HR Admin Workflow

1. Log in with HR credentials
2. Navigate to "New Employee" page
3. Fill in employee details:
   - Name
   - Employee ID
   - Email
   - Department
   - Designation
   - Joining Date
4. Click "Create Employee"
5. Click "Start Onboarding" to trigger the orchestrator
6. View real-time progress on the employee status page
7. Use the dashboard to monitor all onboarding processes

### Manager Workflow

1. Log in with manager credentials
2. View the "Manager Dashboard" with all employees
3. Monitor onboarding progress and failed tasks
4. Click "View Details" on any employee to see task timeline
5. Retry failed tasks individually
6. Track execution logs and history

## API Endpoints

### Authentication
- `POST /api/auth/login` - User login and token generation

### Employee Management
- `POST /api/employees/create` - Create new employee
- `GET /api/employees/list` - List all employees
- `GET /api/employees/status/{employee_id}` - Get employee status
- `POST /api/employees/start-onboarding/{employee_id}` - Start onboarding workflow
- `POST /api/employees/retry-task/{employee_id}/{task_name}` - Retry a failed task

### Dashboard
- `GET /api/dashboard/stats` - Get dashboard statistics
- `GET /api/dashboard/onboarding-list` - Get onboarding list with progress

## Orchestrator Agent Details

The OnboardingOrchestrator class:

- **Coordinates**: Sequential execution of 8 onboarding tasks
- **Tracks**: Task status, timestamps, and completion percentage
- **Logs**: All actions and status changes to database
- **Handles**: Task failures with meaningful error messages
- **Retries**: Supports individual task retries for failed tasks
- **Updates**: Real-time progress updates to frontend

### Orchestration Flow

```
1. Receive employee onboarding request
2. Mark employee status as "onboarding"
3. Execute each task sequentially:
   - Update task status to "running"
   - Execute task function (1-2 second simulation)
   - Record result (success/failure)
   - Update task status and log action
4. Calculate progress percentage
5. Determine final status:
   - "completed" if all tasks succeeded
   - "partial" if some tasks failed
   - "failed" if most tasks failed
6. Return execution summary
```

## UI Features

### Color Scheme
- **Primary Blue**: #0066cc (main actions and primary color)
- **Success Green**: #22c55e (completed tasks)
- **Warning Orange**: #f97316 (in-progress tasks)
- **Danger Red**: #ef4444 (failed tasks)
- **Corporate Gray**: Professional neutral tones

### Key UI Components
- **Status Badges**: Visual task status indicators
- **Progress Bars**: Percentage completion visualization
- **Timeline Views**: Detailed task execution history
- **Real-time Updates**: Auto-refreshing dashboards
- **Search & Filter**: Employee list filtering
- **Modal Dialogs**: Confirmation and feedback modals

## Database Structure

### employees table
```sql
CREATE TABLE employees (
    employee_id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    department TEXT NOT NULL,
    designation TEXT NOT NULL,
    joining_date TEXT NOT NULL,
    onboarding_status TEXT DEFAULT 'pending',
    created_at TIMESTAMP,
    updated_at TIMESTAMP
);
```

### tasks table
```sql
CREATE TABLE tasks (
    task_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    task_name TEXT NOT NULL,
    status TEXT DEFAULT 'pending',
    started_at TIMESTAMP,
    completed_at TIMESTAMP,
    error_message TEXT,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);
```

### logs table
```sql
CREATE TABLE logs (
    log_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_id TEXT NOT NULL,
    action TEXT NOT NULL,
    timestamp TIMESTAMP,
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
);
```

### users table
```sql
CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT NOT NULL,
    created_at TIMESTAMP
);
```

## Technical Stack

- **Backend**: FastAPI, SQLite, Python
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Authentication**: JWT (JSON Web Tokens)
- **Password Hashing**: bcrypt
- **Database**: SQLite with relational schema

## Features Demonstrated

✅ Orchestrator Agent Coordination
✅ Real-time Task Execution
✅ Progress Tracking
✅ Error Handling and Retry Logic
✅ Comprehensive Logging
✅ Role-Based Access Control
✅ Responsive Enterprise UI
✅ REST API Design
✅ Database Schema Management
✅ JWT Authentication
✅ Task Status Management
✅ Execution History

## Development Notes

- All task functions are simulated with random delays
- 10% failure rate ensures realistic scenarios
- No external LLM dependency - pure rule-based orchestration
- SQLite database initializes automatically on first run
- Demo accounts seed automatically in database

## License

This project is provided as-is for demonstration purposes.
