from fastapi import APIRouter
from pydantic import BaseModel
from typing import List
import sqlite3
from datetime import datetime

# Ensure models can be imported
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import get_db

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])

class DashboardStats(BaseModel):
    total_employees: int
    active_onboarding: int
    completed_onboarding: int
    failed_tasks_count: int
    recent_activities: List[dict]

@router.get("/stats", response_model=DashboardStats)
async def get_dashboard_stats():
    """Get dashboard statistics"""
    db = get_db()
    cursor = db.cursor()
    
    # Total employees
    cursor.execute("SELECT COUNT(*) FROM employees")
    total_employees = cursor.fetchone()[0]
    
    # Active onboarding
    cursor.execute("SELECT COUNT(*) FROM employees WHERE onboarding_status = 'onboarding'")
    active_onboarding = cursor.fetchone()[0]
    
    # Completed onboarding
    cursor.execute("SELECT COUNT(*) FROM employees WHERE onboarding_status = 'completed'")
    completed_onboarding = cursor.fetchone()[0]
    
    # Failed tasks
    cursor.execute("SELECT COUNT(*) FROM tasks WHERE status = 'failed'")
    failed_tasks_count = cursor.fetchone()[0]
    
    # Recent activities
    cursor.execute('''
        SELECT employee_id, action, timestamp 
        FROM logs 
        ORDER BY timestamp DESC 
        LIMIT 10
    ''')
    activities = cursor.fetchall()
    
    db.close()
    
    recent_activities = [
        {
            "employee_id": act[0],
            "action": act[1],
            "timestamp": act[2]
        }
        for act in activities
    ]
    
    return {
        "total_employees": total_employees,
        "active_onboarding": active_onboarding,
        "completed_onboarding": completed_onboarding,
        "failed_tasks_count": failed_tasks_count,
        "recent_activities": recent_activities
    }

@router.get("/onboarding-list", response_model=dict)
async def get_onboarding_list():
    """Get list of all employees with onboarding status"""
    db = get_db()
    cursor = db.cursor()
    
    cursor.execute('''
        SELECT employee_id, name, email, department, onboarding_status, created_at 
        FROM employees 
        ORDER BY created_at DESC
    ''')
    
    employees = cursor.fetchall()
    
    db.close()
    
    employee_list = []
    for emp in employees:
        # Get task count for each employee
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            SELECT COUNT(*) as total, 
                   SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed,
                   SUM(CASE WHEN status = 'failed' THEN 1 ELSE 0 END) as failed
            FROM tasks WHERE employee_id = ?
        ''', (emp[0],))
        task_stats = cursor.fetchone()
        db.close()
        
        total_tasks = task_stats[0] if task_stats[0] else 0
        completed_tasks = task_stats[1] if task_stats[1] else 0
        failed_tasks = task_stats[2] if task_stats[2] else 0
        
        progress = int((completed_tasks / 8) * 100) if total_tasks > 0 else 0
        
        employee_list.append({
            "employee_id": emp[0],
            "name": emp[1],
            "email": emp[2],
            "department": emp[3],
            "onboarding_status": emp[4],
            "created_at": emp[5],
            "total_tasks": 8,
            "completed_tasks": completed_tasks,
            "failed_tasks": failed_tasks,
            "progress": progress
        })
    
    return {
        "employees": employee_list,
        "total_count": len(employee_list)
    }
