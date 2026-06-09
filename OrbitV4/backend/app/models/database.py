import sqlite3
import os
from datetime import datetime
from pathlib import Path

# Database file in backend directory
DB_DIR = Path(__file__).parent.parent.parent
DATABASE_PATH = DB_DIR / "onboarding.db"

def get_db():
    """Get database connection"""
    db = sqlite3.connect(str(DATABASE_PATH))
    db.row_factory = sqlite3.Row
    return db

def init_db():
    """Initialize database with tables"""
    db = sqlite3.connect(str(DATABASE_PATH))
    cursor = db.cursor()
    
    # Employees table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS employees (
            employee_id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            department TEXT NOT NULL,
            designation TEXT NOT NULL,
            joining_date TEXT NOT NULL,
            onboarding_status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            task_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            task_name TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            started_at TIMESTAMP,
            completed_at TIMESTAMP,
            error_message TEXT,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        )
    ''')
    
    # Logs table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            log_id INTEGER PRIMARY KEY AUTOINCREMENT,
            employee_id TEXT NOT NULL,
            action TEXT NOT NULL,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (employee_id) REFERENCES employees (employee_id)
        )
    ''')
    
    # Users table for authentication
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            role TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    db.commit()
    db.close()

def seed_initial_data():
    """Seed initial test users"""
    import hashlib
    import base64
    
    def hash_password(password: str) -> str:
        """Simple password hashing using PBKDF2"""
        salt = "onboarding-concierge"
        hash_obj = hashlib.pbkdf2_hmac('sha256', password.encode(), salt.encode(), 100000)
        return base64.b64encode(hash_obj).decode()
    
    db = sqlite3.connect(str(DATABASE_PATH))
    cursor = db.cursor()
    
    # Check if users already exist
    cursor.execute("SELECT COUNT(*) FROM users")
    if cursor.fetchone()[0] == 0:
        # Hash passwords
        hr_password = hash_password("Hr@123")
        manager_password = hash_password("Manager@123")
        
        cursor.execute('''
            INSERT INTO users (email, password, role)
            VALUES (?, ?, ?)
        ''', ("hr@company.com", hr_password, "hr"))
        
        cursor.execute('''
            INSERT INTO users (email, password, role)
            VALUES (?, ?, ?)
        ''', ("manager@company.com", manager_password, "manager"))
        
        db.commit()
    
    db.close()

if __name__ == "__main__":
    import sys
    init_db()
    seed_initial_data()
    print(f"Database initialized at: {DATABASE_PATH}")
    print("Database initialized with seed data")
