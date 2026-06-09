# System Architecture & Workflow Diagram

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                          │
├──────────────────┬──────────────────┬──────────────────────────┤
│  Login Page      │  HR Dashboard    │  Manager Dashboard       │
│  (index.html)    │  (dashboard.html)│  (manager-monitoring.html)
│                  │                  │                          │
│ • Email/Pass     │ • Stats Cards    │ • Employee List          │
│ • Role Select    │ • New Employee   │ • Status Filters         │
│ • JWT Auth       │ • Active List    │ • Failed Tasks           │
└──────────────────┴──────────────────┴──────────────────────────┘
                           ↓
              ┌────────────────────────────────┐
              │   FRONTEND (HTML/CSS/JS)       │
              │  • Responsive Design            │
              │  • Real-time Updates (2-5s)     │
              │  • Status Badges & Colors       │
              │  • Progress Bars                │
              │  • Task Timeline                │
              │  • Execution Logs               │
              └────────────────────────────────┘
                           ↓
         ┌─────────────────────────────────────────┐
         │          REST API (FastAPI)             │
         ├──────────────┬──────────────────────────┤
         │ /api/auth    │ /api/employees           │
         │ • login      │ • create                 │
         │              │ • list                   │
         │              │ • status                 │
         │              │ • start-onboarding       │
         │              │ • retry-task             │
         │              │                          │
         │              │ /api/dashboard           │
         │              │ • stats                  │
         │              │ • onboarding-list        │
         └──────────────┴──────────────────────────┘
                           ↓
         ┌─────────────────────────────────────────┐
         │    APPLICATION LOGIC LAYER              │
         ├─────────────────────────────────────────┤
         │                                         │
         │  ┌──────────────────────────────────┐   │
         │  │  ORCHESTRATOR AGENT              │   │
         │  │  (OnboardingOrchestrator)        │   │
         │  │                                  │   │
         │  │  • Coordinates task execution    │   │
         │  │  • Updates task status           │   │
         │  │  • Tracks progress               │   │
         │  │  • Handles failures & retries    │   │
         │  │  • Logs all actions              │   │
         │  └──────────────────────────────────┘   │
         │                  ↓                       │
         │  ┌──────────────────────────────────┐   │
         │  │  TASK EXECUTION FUNCTIONS        │   │
         │  │  (8 Mock Tasks)                  │   │
         │  │                                  │   │
         │  │  1. create_employee_account()    │   │
         │  │  2. create_company_email()       │   │
         │  │  3. request_laptop()             │   │
         │  │  4. assign_software_licenses()   │   │
         │  │  5. generate_employee_id_card()  │   │
         │  │  6. add_to_team_workspace()      │   │
         │  │  7. grant_system_access()        │   │
         │  │  8. register_in_hr_database()    │   │
         │  └──────────────────────────────────┘   │
         │                                         │
         │  ┌──────────────────────────────────┐   │
         │  │  AUTHENTICATION (JWT)            │   │
         │  │  • Token generation              │   │
         │  │  • Password hashing              │   │
         │  │  • Role validation               │   │
         │  └──────────────────────────────────┘   │
         │                                         │
         └─────────────────────────────────────────┘
                           ↓
         ┌─────────────────────────────────────────┐
         │        DATABASE LAYER (SQLite)          │
         ├──────────┬──────────┬────────┬──────────┤
         │Employees │  Tasks   │ Logs   │  Users   │
         │          │          │        │          │
         │ • ID     │ • ID     │ • ID   │ • ID     │
         │ • Name   │ • Emp ID │ • Emp  │ • Email  │
         │ • Email  │ • Name   │   ID   │ • Pass   │
         │ • Dept   │ • Status │ • Action│ • Role  │
         │ • Desig  │ • Times  │ • Time  │          │
         │ • Date   │ • Error  │        │          │
         │ • Status │          │        │          │
         └──────────┴──────────┴────────┴──────────┘
                           ↓
                   [onboarding.db]
```

## Onboarding Task Execution Flow

```
START ONBOARDING
       ↓
   [Webhook Event Triggered]
       ↓
[ORCHESTRATOR INITIALIZES]
   • Load employee data
   • Set status = "onboarding"
   • Initialize progress = 0%
       ↓
   ┌─────────────────────────────┐
   │  TASK EXECUTION LOOP        │
   │  (8 Sequential Tasks)       │
   └─────────────────────────────┘
       ↓
   ┌─── TASK 1: Create Account ───┐
   │ Status: running              │
   │ Execute (1-2 seconds)         │
   │ Result: Success/Failure       │
   │ Progress: 12.5%               │
   │ Log action                    │
   └──────────────────────────────┘
       ↓
   ┌─── TASK 2: Create Email ─────┐
   │ Status: running              │
   │ Execute (1-2 seconds)         │
   │ Result: Success/Failure       │
   │ Progress: 25%                 │
   │ Log action                    │
   └──────────────────────────────┘
       ↓
   ┌─── TASK 3: Request Laptop ───┐
   │ Status: running              │
   │ Execute (1-2 seconds)         │
   │ Result: Success/Failure       │
   │ Progress: 37.5%               │
   │ Log action                    │
   └──────────────────────────────┘
       ↓
   [... TASKS 4-8 CONTINUE ...]
       ↓
   ┌──────────────────────────────┐
   │  DETERMINE FINAL STATUS      │
   │                              │
   │  All Success → "completed"   │
   │  Some Fail → "partial"       │
   │  All Fail → "failed"         │
   └──────────────────────────────┘
       ↓
   [ORCHESTRATOR FINISHES]
   • Update employee status
   • Calculate final progress
   • Log completion
   • Return execution summary
       ↓
END ONBOARDING (100% or Failed)
```

## User Workflow: HR Admin

```
LOGIN
  ↓
[Enter credentials]
  ↓
[Verify JWT Token]
  ↓
DASHBOARD
  ├─ View Stats
  │  ├─ Total Employees
  │  ├─ Active Onboarding
  │  ├─ Completed
  │  └─ Failed Tasks
  │
  ├─ Recent Activity
  │
  └─ Employee Table
     ├─ Search/Filter
     └─ Click Employee
        ↓
        [VIEW DETAILS PAGE]
        ├─ Employee Info
        ├─ Progress Bar
        ├─ Task Timeline
        ├─ Logs
        └─ Retry Failed
              ↓
            [RETRY TASK]
            [Update Timeline]
            [Monitor Progress]
  
  ├─ NEW EMPLOYEE
  │  ↓
  │  [Employee Form]
  │  ├─ Name
  │  ├─ Employee ID
  │  ├─ Email
  │  ├─ Department
  │  ├─ Designation
  │  └─ Joining Date
  │      ↓
  │    [CREATE EMPLOYEE]
  │      ↓
  │    [SUCCESS MODAL]
  │      ↓
  │    [START ONBOARDING]
  │      ↓
  │    [ORCHESTRATOR RUNS]
  │      ↓
  │    [TASK EXECUTION BEGINS]
  │
  └─ LOGOUT

REAL-TIME UPDATES
  • Dashboard refreshes every 5 seconds
  • Employee status updates every 2 seconds
  • Progress bars animate
  • Timeline updates with completed tasks
```

## Manager Monitoring Workflow

```
LOGIN
  ↓
[Enter credentials]
  ↓
[Verify JWT Token]
  ↓
MANAGER DASHBOARD
  │
  ├─ FILTER & SEARCH
  │  ├─ Search by Name
  │  ├─ Search by Email
  │  └─ Filter by Status
  │
  ├─ EMPLOYEE TABLE
  │  ├─ Employee ID
  │  ├─ Name
  │  ├─ Department
  │  ├─ Status Badge
  │  ├─ Progress Bar
  │  ├─ Task Count
  │  ├─ Failed Count
  │  └─ View Details Button
  │      ↓
  │      [EMPLOYEE DETAIL PAGE]
  │      ├─ Full Information
  │      ├─ Task Timeline
  │      ├─ Error Messages
  │      └─ RETRY BUTTON
  │          ↓
  │        [SELECT TASK]
  │          ↓
  │        [CONFIRM RETRY]
  │          ↓
  │        [TASK EXECUTES]
  │          ↓
  │        [MONITOR RESULT]
  │
  ├─ FAILED TASKS SECTION
  │  ├─ Employee with Failures
  │  ├─ Task Count
  │  ├─ Current Progress
  │  └─ Quick Retry Button
  │
  └─ AUTO-REFRESH (5 seconds)
     └─ Monitor all employees
```

## Data Flow: Task Execution

```
REQUEST
  │
  ├─→ /start-onboarding/{employee_id}
  │
  ↓
API ROUTE (employee_routes.py)
  │
  ├─ Validate employee exists
  ├─ Get employee data
  ├─ Create Orchestrator instance
  └─ Start background thread
      │
      ↓
  ORCHESTRATOR.execute_orchestration()
      │
      ├─ Log: "Workflow started"
      ├─ Update: Status = "onboarding"
      │
      └─ For each task in [1-8]:
         │
         ├─ update_task_status("running")
         ├─ log_action("Task started")
         │
         ├─ EXECUTE TASK FUNCTION
         │  ├─ Wait 1-2 seconds
         │  ├─ Random success/failure
         │  └─ Return result
         │
         ├─ IF SUCCESS:
         │  ├─ update_task_status("completed")
         │  ├─ tasks_completed++
         │  └─ log_action("Task succeeded")
         │
         └─ IF FAILURE:
            ├─ update_task_status("failed", error_msg)
            └─ log_action("Task failed: ...")
      │
      ├─ Calculate final_status
      ├─ Update employee_status
      ├─ Calculate progress_percentage
      └─ Log: "Workflow {status}"
      │
      ↓
  DATABASE UPDATES
  ├─ employees table: status updated
  ├─ tasks table: all task records created
  └─ logs table: all actions logged
      │
      ↓
  FRONTEND AUTO-REFRESH
  ├─ Fetch /employees/status/{id}
  ├─ Update progress bar
  ├─ Update task timeline
  ├─ Display completion percentage
  └─ Show status badges
      │
      ↓
  USER SEES REAL-TIME UPDATES
```

## Database Schema Relationships

```
┌─────────────────┐
│     USERS       │
├─────────────────┤
│ user_id (PK)    │
│ email (UNIQUE)  │
│ password        │
│ role            │
│ created_at      │
└─────────────────┘

┌──────────────────────┐         ┌────────────────────────┐
│   EMPLOYEES          │◄────────│      TASKS             │
├──────────────────────┤ 1    n  ├────────────────────────┤
│ employee_id (PK)     │         │ task_id (PK)           │
│ name                 │         │ employee_id (FK) ──────┤
│ email (UNIQUE)       │         │ task_name              │
│ department           │         │ status                 │
│ designation          │         │ started_at             │
│ joining_date         │         │ completed_at           │
│ onboarding_status    │         │ error_message          │
│ created_at           │         └────────────────────────┘
│ updated_at           │
└──────────────────────┘

┌──────────────────────┐
│       LOGS           │
├──────────────────────┤
│ log_id (PK)          │
│ employee_id (FK) ────┼─→ EMPLOYEES
│ action               │
│ timestamp            │
└──────────────────────┘
```

## Status Badge Colors

```
┌─────────────┬──────────────────┬─────────────────┐
│   Status    │   Background     │   Text Color    │
├─────────────┼──────────────────┼─────────────────┤
│ Pending     │ #fee2e2 (light)  │ #991b1b (dark)  │
│ Running     │ #fef3c7 (yellow) │ #92400e (brown) │
│ Completed   │ #dcfce7 (green)  │ #166534 (dark)  │
│ Failed      │ #fee2e2 (red)    │ #7f1d1d (dark)  │
│ Onboarding  │ #fef3c7 (yellow) │ #92400e (brown) │
│ Partial     │ #fed7aa (orange) │ #92400e (brown) │
└─────────────┴──────────────────┴─────────────────┘
```

## API Response Examples

### Login Response
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIs...",
  "token_type": "bearer",
  "role": "hr",
  "email": "hr@company.com"
}
```

### Employee Status Response
```json
{
  "employee_id": "EMP001",
  "name": "John Doe",
  "email": "john@company.com",
  "department": "Engineering",
  "designation": "Senior Engineer",
  "joining_date": "2024-01-15",
  "onboarding_status": "onboarding",
  "progress": 62,
  "tasks_completed": 5,
  "total_tasks": 8,
  "tasks": [
    {
      "task_id": 1,
      "task_name": "Create Employee Account",
      "status": "completed",
      "started_at": "2024-01-15T10:00:00",
      "completed_at": "2024-01-15T10:00:02",
      "error_message": null
    },
    ...
  ]
}
```

## Execution Timeline Example

```
10:00:00 ┬─ HR clicks "Start Onboarding"
         ├─ Orchestrator initializes
         │
10:00:01 ├─ Task 1: Create Account ████ (SUCCESS)
         │
10:00:03 ├─ Task 2: Create Email ████ (SUCCESS)
         │
10:00:05 ├─ Task 3: Request Laptop ████ (FAILED - Budget limit)
         │
10:00:07 ├─ Task 4: Assign Licenses ████ (SUCCESS)
         │
10:00:09 ├─ Task 5: Generate ID Card ████ (SUCCESS)
         │
10:00:11 ├─ Task 6: Team Workspace ████ (SUCCESS)
         │
10:00:13 ├─ Task 7: System Access ████ (SUCCESS)
         │
10:00:15 ├─ Task 8: HR Database ████ (SUCCESS)
         │
         └─ Final Status: PARTIAL (7/8 completed)
            Progress: 87.5%
            Manager can retry Task 3
```

## Security Flow

```
USER LOGIN
    ↓
[Submit credentials]
    ↓
API: /auth/login
    ├─ Query users table
    ├─ Find user by email
    ├─ Verify password with bcrypt
    │  ├─ Hash submitted password
    │  └─ Compare with stored hash
    ├─ Generate JWT token
    │  ├─ Add user data to payload
    │  ├─ Set expiration (30 min)
    │  └─ Sign with SECRET_KEY
    └─ Return token to client
        ↓
    [Client stores token]
        ↓
    [Token sent with each request]
        ├─ Authorization header
        └─ Bearer token format
            ↓
        [Server verifies token]
        ├─ Decode JWT
        ├─ Check signature
        ├─ Check expiration
        └─ Allow or deny access
```

This architecture ensures:
✅ Scalable design
✅ Real-time updates
✅ Reliable task execution
✅ Comprehensive logging
✅ Secure authentication
✅ Clean separation of concerns
