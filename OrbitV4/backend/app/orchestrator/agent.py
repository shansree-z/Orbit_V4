import time
import random
import sqlite3
from datetime import datetime
from typing import List, Dict

# Ensure database can be imported
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from models.database import get_db

# List of 8 onboarding tasks
ONBOARDING_TASKS = [
    "Create Employee Account",
    "Create Company Email",
    "Request Laptop",
    "Assign Software Licenses",
    "Generate Employee ID Card",
    "Add Employee to Team Workspace",
    "Grant System Access Permissions",
    "Register Employee in HR Database"
]

# Mock task functions that simulate real operations
def create_employee_account(employee_id: str, name: str) -> Dict:
    """Task 1: Create employee account"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:  # 10% failure rate
        return {
            "success": False,
            "error": f"Account creation failed: Username conflict for {name}"
        }
    return {
        "success": True,
        "data": f"Account created with username: {employee_id.lower()}"
    }

def create_company_email(employee_id: str, name: str, email: str) -> Dict:
    """Task 2: Create company email"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:
        return {
            "success": False,
            "error": f"Email provisioning failed: Service temporarily unavailable"
        }
    company_email = f"{employee_id.lower()}@company.com"
    return {
        "success": True,
        "data": f"Company email created: {company_email}"
    }

def request_laptop(employee_id: str, designation: str) -> Dict:
    """Task 3: Request laptop"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:
        return {
            "success": False,
            "error": "Laptop request failed: Budget limit exceeded"
        }
    return {
        "success": True,
        "data": f"Laptop request submitted: Model appropriate for {designation}"
    }

def assign_software_licenses(employee_id: str, department: str) -> Dict:
    """Task 4: Assign software licenses"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:
        return {
            "success": False,
            "error": "License assignment failed: License pool exhausted"
        }
    return {
        "success": True,
        "data": f"Software licenses assigned for {department} department"
    }

def generate_employee_id_card(employee_id: str, name: str) -> Dict:
    """Task 5: Generate employee ID card"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:
        return {
            "success": False,
            "error": "Card generation failed: Printer offline"
        }
    card_number = f"ID-{int(time.time())}-{random.randint(100, 999)}"
    return {
        "success": True,
        "data": f"ID Card generated: {card_number}"
    }

def add_to_team_workspace(employee_id: str, department: str) -> Dict:
    """Task 6: Add employee to team workspace"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:
        return {
            "success": False,
            "error": "Workspace access failed: Invalid department mapping"
        }
    return {
        "success": True,
        "data": f"Added to {department} team workspace"
    }

def grant_system_access(employee_id: str, designation: str) -> Dict:
    """Task 7: Grant system access permissions"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:
        return {
            "success": False,
            "error": "Access grant failed: Permission database locked"
        }
    return {
        "success": True,
        "data": f"System access permissions granted for {designation} role"
    }

def register_in_hr_database(employee_id: str, email: str) -> Dict:
    """Task 8: Register employee in HR database"""
    time.sleep(random.uniform(1, 2))
    if random.random() < 0.10:
        return {
            "success": False,
            "error": "HR registration failed: Database connection timeout"
        }
    return {
        "success": True,
        "data": f"Employee registered in HR system: {email}"
    }

class OnboardingOrchestrator:
    """
    Orchestrator agent that coordinates and executes onboarding tasks sequentially.
    Acts as a workflow coordinator managing task execution, status updates, and logging.
    """
    
    def __init__(self, employee_id: str, employee_data: dict):
        self.employee_id = employee_id
        self.employee_data = employee_data
        self.tasks_completed = 0
        self.total_tasks = len(ONBOARDING_TASKS)
        self.execution_history = []
        
    def log_action(self, action: str):
        """Log action to database"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            INSERT INTO logs (employee_id, action, timestamp)
            VALUES (?, ?, ?)
        ''', (self.employee_id, action, datetime.utcnow().isoformat()))
        db.commit()
        db.close()
    
    def update_task_status(self, task_name: str, status: str, error_message: str = None):
        """Update task status in database"""
        db = get_db()
        cursor = db.cursor()
        
        timestamp = datetime.utcnow().isoformat()
        
        if status == "running":
            cursor.execute('''
                INSERT INTO tasks (employee_id, task_name, status, started_at)
                VALUES (?, ?, ?, ?)
            ''', (self.employee_id, task_name, status, timestamp))
        elif status in ["completed", "failed"]:
            cursor.execute('''
                SELECT task_id FROM tasks 
                WHERE employee_id = ? AND task_name = ? AND status = 'running'
                ORDER BY task_id DESC LIMIT 1
            ''', (self.employee_id, task_name))
            result = cursor.fetchone()
            if result:
                task_id = result[0]
                cursor.execute('''
                    UPDATE tasks 
                    SET status = ?, completed_at = ?, error_message = ?
                    WHERE task_id = ?
                ''', (status, timestamp, error_message, task_id))
        
        db.commit()
        db.close()
    
    def update_employee_status(self, status: str):
        """Update employee onboarding status"""
        db = get_db()
        cursor = db.cursor()
        cursor.execute('''
            UPDATE employees 
            SET onboarding_status = ?, updated_at = ?
            WHERE employee_id = ?
        ''', (status, datetime.utcnow().isoformat(), self.employee_id))
        db.commit()
        db.close()
    
    def get_progress_percentage(self) -> int:
        """Calculate and return progress percentage"""
        if self.total_tasks == 0:
            return 0
        return int((self.tasks_completed / self.total_tasks) * 100)
    
    def execute_orchestration(self) -> Dict:
        """
        Main orchestration method that executes all onboarding tasks sequentially.
        Returns execution summary with status and progress.
        """
        self.log_action("Onboarding workflow started")
        self.update_employee_status("onboarding")
        
        task_functions = [
            (ONBOARDING_TASKS[0], create_employee_account),
            (ONBOARDING_TASKS[1], create_company_email),
            (ONBOARDING_TASKS[2], request_laptop),
            (ONBOARDING_TASKS[3], assign_software_licenses),
            (ONBOARDING_TASKS[4], generate_employee_id_card),
            (ONBOARDING_TASKS[5], add_to_team_workspace),
            (ONBOARDING_TASKS[6], grant_system_access),
            (ONBOARDING_TASKS[7], register_in_hr_database),
        ]
        
        failed_tasks = []
        
        for task_name, task_func in task_functions:
            try:
                # Mark task as running
                self.update_task_status(task_name, "running")
                self.log_action(f"Task started: {task_name}")
                
                # Execute task based on type
                if task_name == ONBOARDING_TASKS[0]:  # Create Employee Account
                    result = task_func(self.employee_id, self.employee_data.get("name"))
                elif task_name == ONBOARDING_TASKS[1]:  # Create Company Email
                    result = task_func(self.employee_id, self.employee_data.get("name"), self.employee_data.get("email"))
                elif task_name == ONBOARDING_TASKS[2]:  # Request Laptop
                    result = task_func(self.employee_id, self.employee_data.get("designation"))
                elif task_name == ONBOARDING_TASKS[3]:  # Assign Software Licenses
                    result = task_func(self.employee_id, self.employee_data.get("department"))
                elif task_name == ONBOARDING_TASKS[4]:  # Generate Employee ID Card
                    result = task_func(self.employee_id, self.employee_data.get("name"))
                elif task_name == ONBOARDING_TASKS[5]:  # Add to Team Workspace
                    result = task_func(self.employee_id, self.employee_data.get("department"))
                elif task_name == ONBOARDING_TASKS[6]:  # Grant System Access
                    result = task_func(self.employee_id, self.employee_data.get("designation"))
                elif task_name == ONBOARDING_TASKS[7]:  # Register in HR Database
                    result = task_func(self.employee_id, self.employee_data.get("email"))
                
                # Process result
                if result["success"]:
                    self.update_task_status(task_name, "completed")
                    self.log_action(f"Task completed: {task_name} - {result.get('data', '')}")
                    self.tasks_completed += 1
                    self.execution_history.append({
                        "task": task_name,
                        "status": "completed",
                        "result": result.get("data")
                    })
                else:
                    self.update_task_status(task_name, "failed", result.get("error"))
                    self.log_action(f"Task failed: {task_name} - {result.get('error')}")
                    failed_tasks.append(task_name)
                    self.execution_history.append({
                        "task": task_name,
                        "status": "failed",
                        "error": result.get("error")
                    })
            
            except Exception as e:
                error_msg = f"Unexpected error: {str(e)}"
                self.update_task_status(task_name, "failed", error_msg)
                self.log_action(f"Task error: {task_name} - {error_msg}")
                failed_tasks.append(task_name)
                self.execution_history.append({
                    "task": task_name,
                    "status": "failed",
                    "error": error_msg
                })
        
        # Determine final status
        if len(failed_tasks) == 0:
            final_status = "completed"
        else:
            final_status = "failed" if self.tasks_completed == 0 else "partial"
        
        self.update_employee_status(final_status)
        self.log_action(f"Onboarding workflow {final_status}: {self.tasks_completed}/{self.total_tasks} tasks completed")
        
        return {
            "employee_id": self.employee_id,
            "status": final_status,
            "progress": self.get_progress_percentage(),
            "tasks_completed": self.tasks_completed,
            "total_tasks": self.total_tasks,
            "failed_tasks": failed_tasks,
            "execution_history": self.execution_history
        }
    
    def retry_failed_task(self, task_name: str) -> Dict:
        """
        Retry a specific failed task.
        Called by managers to retry failed onboarding tasks.
        """
        if task_name not in ONBOARDING_TASKS:
            return {"success": False, "error": "Invalid task name"}
        
        task_functions = {
            ONBOARDING_TASKS[0]: create_employee_account,
            ONBOARDING_TASKS[1]: create_company_email,
            ONBOARDING_TASKS[2]: request_laptop,
            ONBOARDING_TASKS[3]: assign_software_licenses,
            ONBOARDING_TASKS[4]: generate_employee_id_card,
            ONBOARDING_TASKS[5]: add_to_team_workspace,
            ONBOARDING_TASKS[6]: grant_system_access,
            ONBOARDING_TASKS[7]: register_in_hr_database,
        }
        
        try:
            self.update_task_status(task_name, "running")
            self.log_action(f"Task retry started: {task_name}")
            
            task_func = task_functions[task_name]
            
            # Execute task with appropriate parameters
            if task_name == ONBOARDING_TASKS[0]:
                result = task_func(self.employee_id, self.employee_data.get("name"))
            elif task_name == ONBOARDING_TASKS[1]:
                result = task_func(self.employee_id, self.employee_data.get("name"), self.employee_data.get("email"))
            elif task_name == ONBOARDING_TASKS[2]:
                result = task_func(self.employee_id, self.employee_data.get("designation"))
            elif task_name == ONBOARDING_TASKS[3]:
                result = task_func(self.employee_id, self.employee_data.get("department"))
            elif task_name == ONBOARDING_TASKS[4]:
                result = task_func(self.employee_id, self.employee_data.get("name"))
            elif task_name == ONBOARDING_TASKS[5]:
                result = task_func(self.employee_id, self.employee_data.get("department"))
            elif task_name == ONBOARDING_TASKS[6]:
                result = task_func(self.employee_id, self.employee_data.get("designation"))
            elif task_name == ONBOARDING_TASKS[7]:
                result = task_func(self.employee_id, self.employee_data.get("email"))
            
            if result["success"]:
                self.update_task_status(task_name, "completed")
                self.log_action(f"Task retry successful: {task_name}")
                return {
                    "success": True,
                    "task": task_name,
                    "result": result.get("data")
                }
            else:
                self.update_task_status(task_name, "failed", result.get("error"))
                self.log_action(f"Task retry failed: {task_name} - {result.get('error')}")
                return {
                    "success": False,
                    "task": task_name,
                    "error": result.get("error")
                }
        
        except Exception as e:
            error_msg = f"Unexpected error during retry: {str(e)}"
            self.update_task_status(task_name, "failed", error_msg)
            self.log_action(f"Task retry error: {task_name} - {error_msg}")
            return {
                "success": False,
                "task": task_name,
                "error": error_msg
            }
