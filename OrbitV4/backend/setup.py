#!/usr/bin/env python3
"""
Quick setup script for the Onboarding Concierge application.
This script sets up the database and validates the environment.
"""

import sys
import os
from pathlib import Path

def main():
    # Add app directory to path
    backend_dir = Path(__file__).parent
    app_dir = backend_dir / "app"
    sys.path.insert(0, str(app_dir))
    sys.path.insert(0, str(backend_dir))
    
    try:
        # Import and initialize database
        from models.database import init_db, seed_initial_data
        
        print("=" * 60)
        print("Onboarding Concierge - Setup Script")
        print("=" * 60)
        print()
        
        print("Initializing database...")
        init_db()
        print("✓ Database tables created")
        
        print("Seeding initial data...")
        seed_initial_data()
        print("✓ Demo accounts created")
        
        print()
        print("=" * 60)
        print("Setup Complete!")
        print("=" * 60)
        print()
        print("Demo Credentials:")
        print("  HR Admin:    hr@company.com / Hr@123")
        print("  Manager:     manager@company.com / Manager@123")
        print()
        print("To start the server, run:")
        print("  python main.py")
        print()
        print("The application will be available at:")
        print("  http://127.0.0.1:8000")
        print()
        
    except Exception as e:
        print(f"✗ Error during setup: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
