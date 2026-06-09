#!/bin/bash

# Navigate to the backend directory
cd backend

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt -q

# Initialize database
echo "Initializing database..."
python -c "from app.models.database import init_db, seed_initial_data; init_db(); seed_initial_data()"

# Start the server
echo ""
echo "Starting Onboarding Concierge Server..."
echo ""
echo "Server running at: http://127.0.0.1:8000"
echo ""
echo "Demo Credentials:"
echo "  HR: hr@company.com / Hr@123"
echo "  Manager: manager@company.com / Manager@123"
echo ""

python main.py
