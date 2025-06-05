@echo off
REM Batch file to run the Flask application on Windows

echo Setting up Python virtual environment...
python -m venv venv

if %ERRORLEVEL% NEQ 0 (
    echo Failed to create virtual environment
    pause
    exit /b 1
)

call venv\Scripts\activate

if %ERRORLEVEL% NEQ 0 (
    echo Failed to activate virtual environment
    pause
    exit /b 1
)

echo Installing dependencies...
pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo Failed to install dependencies
    pause
    exit /b 1
)

echo Starting the application...
set FLASK_APP=run.py
set FLASK_ENV=development
flask run

pause
