#!/usr/bin/env python
"""
Debug and Setup Script for Onboarding Concierge
This script helps diagnose and fix common setup issues.
"""

import sys
import os
from pathlib import Path
import subprocess

def check_python():
    """Check Python version"""
    print("\n" + "="*60)
    print("PYTHON ENVIRONMENT CHECK")
    print("="*60)
    print(f"Python Version: {sys.version}")
    print(f"Python Executable: {sys.executable}")
    print(f"Python Path: {sys.prefix}")
    
    if sys.version_info < (3, 8):
        print("⚠️  WARNING: Python 3.8+ required!")
        return False
    print("✓ Python version is compatible")
    return True

def check_dependencies():
    """Check if required packages are installed"""
    print("\n" + "="*60)
    print("DEPENDENCY CHECK")
    print("="*60)
    
    required = [
        'fastapi',
        'uvicorn',
        'pydantic',
        'jose',
    ]
    
    missing = []
    for package in required:
        try:
            __import__(package)
            print(f"✓ {package}")
        except ImportError:
            print(f"✗ {package} - MISSING")
            missing.append(package)
    
    if missing:
        print(f"\n⚠️  Missing packages: {', '.join(missing)}")
        return False
    
    print("\n✓ All dependencies installed")
    return True

def setup_database():
    """Initialize database"""
    print("\n" + "="*60)
    print("DATABASE SETUP")
    print("="*60)
    
    try:
        backend_dir = Path(__file__).parent / "backend"
        app_dir = backend_dir / "app"
        
        sys.path.insert(0, str(app_dir))
        sys.path.insert(0, str(backend_dir))
        
        from models.database import init_db, seed_initial_data
        
        print("Initializing database...")
        init_db()
        print("✓ Database tables created")
        
        print("Seeding demo accounts...")
        seed_initial_data()
        print("✓ Demo accounts created")
        
        db_path = backend_dir / "onboarding.db"
        print(f"\n✓ Database ready: {db_path}")
        return True
        
    except Exception as e:
        print(f"✗ Database setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def install_dependencies():
    """Install required dependencies"""
    print("\n" + "="*60)
    print("INSTALLING DEPENDENCIES")
    print("="*60)
    
    requirements_file = Path(__file__).parent / "backend" / "requirements.txt"
    
    if not requirements_file.exists():
        print(f"✗ requirements.txt not found: {requirements_file}")
        return False
    
    try:
        print("Installing packages...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", str(requirements_file)])
        print("✓ Dependencies installed")
        return True
    except subprocess.CalledProcessError as e:
        print(f"✗ Installation failed: {e}")
        return False

def main():
    """Run all checks and setup"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "ONBOARDING CONCIERGE - DEBUG & SETUP" + " "*7 + "║")
    print("╚" + "="*58 + "╝")
    
    # Check Python
    if not check_python():
        print("\n✗ Python check failed. Please install Python 3.8+")
        sys.exit(1)
    
    # Check/install dependencies
    if not check_dependencies():
        print("\n→ Installing missing dependencies...")
        if not install_dependencies():
            print("✗ Failed to install dependencies")
            sys.exit(1)
        
        # Re-check
        if not check_dependencies():
            print("✗ Dependencies still missing after installation")
            sys.exit(1)
    
    # Setup database
    if not setup_database():
        print("✗ Database setup failed")
        sys.exit(1)
    
    # Final status
    print("\n" + "="*60)
    print("SETUP COMPLETE ✓")
    print("="*60)
    print("\nYou can now start the server with:")
    print("  python main.py")
    print("\nOr from the backend directory:")
    print("  cd backend")
    print("  python main.py")
    print("\nThen open: http://localhost:8000")
    print("\nDemo Credentials:")
    print("  HR: hr@company.com / Hr@123")
    print("  Manager: manager@company.com / Manager@123")
    print("\n" + "="*60)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n✗ Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
