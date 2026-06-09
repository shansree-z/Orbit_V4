@echo off
REM Navigate to the backend directory
cd backend

REM Create virtual environment if it doesn't exist
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
)

REM Activate virtual environment
call venv\Scripts\activate.bat

REM Install dependencies
echo Installing dependencies...
python -m pip install --upgrade pip -q
python -m pip install -r requirements.txt -q

REM Initialize database
echo Initializing database...
python setup.py

REM Start the server
echo.
echo Starting Onboarding Concierge Server...
echo.
echo Server running at: http://127.0.0.1:8000
echo.
echo Demo Credentials:
echo   HR: hr@company.com / Hr@123
echo   Manager: manager@company.com / Manager@123
echo.
echo Press Ctrl+C to stop the server
echo.

python main.py
pause
