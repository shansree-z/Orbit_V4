from fastapi import APIRouter, HTTPException, Query
from pydantic import BaseModel
from typing import List, Optional
import sqlite3
from datetime import datetime
import threading

# Ensure models can be imported
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import get_db
from orchestrator.agent import OnboardingOrchestrator

router = APIRouter(prefix="/api/employees", tags=["employees"])

class EmployeeCreate(BaseModel):
    name: str
    employee_id: str
    email: str
    department: str
    designation: str
    joining_date: str

class EmployeeResponse(BaseModel):
    employee_id: str
    name: str
    email: str
    department: str
    designation: str
    joining_date: str
    onboarding_status: str

class TaskResponse(BaseModel):
    task_id: int
    task_name: str
    status: str
    started_at: Optional[str]
    completed_at: Optional[str]
    error_message: Optional[str]

class EmployeeStatusResponse(BaseModel):
    employee_id: str
    name: str
    email: str
    department: str
    designation: str
    joining_date: str
    onboarding_status: str
    progress: int
    tasks_completed: int
    total_tasks: int
    tasks: List[TaskResponse]

@router.post("/create", response_model=dict)
async def create_employee(employee: EmployeeCreate):
    """Create new employee record"""
    db = get_db()
    cursor = db.cursor()
    
    try:
        cursor.execute('''
            INSERT INTO employees (employee_id, name, email, department, designation, joining_date, onboarding_status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (employee.employee_id, employee.name, employee.email, employee.department, 
              employee.designation, employee.joining_date, 'pending'))
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Employee {employee.name} created successfully",
            "employee_id": employee.employee_id
        }
    except sqlite3.IntegrityError:
        db.close()
        raise HTTPException(status_code=400, detail="Employee ID or email already exists")
    finally:
        db.close()

@router.post("/start-onboarding/{employee_id}", response_model=dict)
async def start_onboarding(employee_id: str):
    """Start onboarding workflow for employee"""
    db = get_db()
    cursor = db.cursor()
    
    # Get employee data
    cursor.execute('''
        SELECT name, email, department, designation, joining_date, onboarding_status 
        FROM employees WHERE employee_id = ?
    ''', (employee_id,))
    
    employee = cursor.fetchone()
    db.close()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    if employee[5] not in ['pending', 'failed', 'partial']:
        raise HTTPException(status_code=400, detail="Onboarding already in progress or completed")
    
    employee_data = {
        "name": employee[0],
        "email": employee[1],
        "department": employee[2],
        "designation": employee[3],
        "joining_date": employee[4]
    }
    
    # Start orchestration in background thread
    orchestrator = OnboardingOrchestrator(employee_id, employee_data)
    
    def run_orchestration():
        orchestrator.execute_orchestration()
    
    thread = threading.Thread(target=run_orchestration, daemon=True)
    thread.start()
    
    return {
        "success": True,
        "message": f"Onboarding started for employee {employee_id}",
        "employee_id": employee_id
    }

@router.get("/list", response_model=List[EmployeeResponse])
async def list_employees():
    """List all employees"""
    db = get_db()
    cursor = db.cursor()
    cursor.execute('''
        SELECT employee_id, name, email, department, designation, joining_date, onboarding_status 
        FROM employees ORDER BY created_at DESC
    ''')
    employees = cursor.fetchall()
    db.close()
    
    return [
        {
            "employee_id": emp[0],
            "name": emp[1],
            "email": emp[2],
            "department": emp[3],
            "designation": emp[4],
            "joining_date": emp[5],
            "onboarding_status": emp[6]
        }
        for emp in employees
    ]

@router.get("/status/{employee_id}", response_model=EmployeeStatusResponse)
async def get_employee_status(employee_id: str):
    """Get employee onboarding status with task details"""
    db = get_db()
    cursor = db.cursor()
    
    # Get employee info
    cursor.execute('''
        SELECT employee_id, name, email, department, designation, joining_date, onboarding_status 
        FROM employees WHERE employee_id = ?
    ''', (employee_id,))
    
    employee = cursor.fetchone()
    
    if not employee:
        db.close()
        raise HTTPException(status_code=404, detail="Employee not found")
    
    # Get tasks
    cursor.execute('''
        SELECT task_id, task_name, status, started_at, completed_at, error_message 
        FROM tasks WHERE employee_id = ? ORDER BY task_id
    ''', (employee_id,))
    
    tasks = cursor.fetchall()
    db.close()
    
    # Calculate progress
    total_tasks = 8
    completed_tasks = sum(1 for task in tasks if task[2] == 'completed')
    progress = int((completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
    
    return {
        "employee_id": employee[0],
        "name": employee[1],
        "email": employee[2],
        "department": employee[3],
        "designation": employee[4],
        "joining_date": employee[5],
        "onboarding_status": employee[6],
        "progress": progress,
        "tasks_completed": completed_tasks,
        "total_tasks": total_tasks,
        "tasks": [
            {
                "task_id": task[0],
                "task_name": task[1],
                "status": task[2],
                "started_at": task[3],
                "completed_at": task[4],
                "error_message": task[5]
            }
            for task in tasks
        ]
    }

@router.post("/retry-task/{employee_id}/{task_name}", response_model=dict)
async def retry_task(employee_id: str, task_name: str):
    """Retry a failed task"""
    db = get_db()
    cursor = db.cursor()
    
    # Get employee data
    cursor.execute('''
        SELECT name, email, department, designation, joining_date 
        FROM employees WHERE employee_id = ?
    ''', (employee_id,))
    
    employee = cursor.fetchone()
    db.close()
    
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    
    employee_data = {
        "name": employee[0],
        "email": employee[1],
        "department": employee[2],
        "designation": employee[3],
        "joining_date": employee[4]
    }
    
    orchestrator = OnboardingOrchestrator(employee_id, employee_data)
    result = orchestrator.retry_failed_task(task_name)
    
    return result
