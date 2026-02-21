@echo off
REM Batch file to run the Flask application on Windows
setlocal enabledelayedexpansion

:: Set colors
set "RED=<NUL set /p=^[[91m"
set "GREEN=<NUL set /p=^[[92m"
set "YELLOW=<NUL set /p=^[[93m"
set "NC=<NUL set /p=^[[0m"

echo %GREEN%=== Weather Dashboard ===%NC%
echo %YELLOW%Initializing application...%NC%

:: Check if .env file exists
if not exist .env (
    echo %YELLOW%Creating .env file from .env.example...%NC%
    copy /Y .env.example .env > nul
    if %ERRORLEVEL% NEQ 0 (
        echo %RED%Failed to create .env file%NC%
        pause
        exit /b 1
    )
    echo %GREEN%.env file created successfully%NC%
)

:: Set environment variables
for /f "usebackq tokens=*" %%a in (".env") do (
    for /f "tokens=1* delims==" %%b in ("%%a") do (
        if not "%%b"=="" if not "%%b"=="#*" (
            set "%%b=%%c"
        )
    )
)

:: Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Python is not installed or not in PATH%NC%
    echo Please install Python from https://www.python.org/downloads/
    pause
    exit /b 1
)

:: Check if virtual environment exists, create if not
if not exist "venv\" (
    echo %YELLOW%Creating Python virtual environment...%NC%
    python -m venv venv
    if %ERRORLEVEL% NEQ 0 (
        echo %RED%Failed to create virtual environment%NC%
        pause
        exit /b 1
    )
    echo %GREEN%Virtual environment created%NC%
)

:: Activate virtual environment
call venv\Scripts\activate.bat
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to activate virtual environment%NC%
    pause
    exit /b 1
)

echo %GREEN%Installing/upgrading dependencies...%NC%
python -m pip install --upgrade pip
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to upgrade pip%NC%
    pause
    exit /b 1
)

pip install -r requirements.txt
if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to install dependencies%NC%
    pause
    exit /b 1
)

echo %GREEN%=== Starting Weather Dashboard ===%NC%
echo %YELLOW%Server will be available at: http://127.0.0.1:5000/%NC%
echo %YELLOW%Press Ctrl+C to stop the server%NC%

echo.
set FLASK_APP=run.py
set FLASK_ENV=development
set FLASK_DEBUG=1

flask run --host=0.0.0.0 --port=5000

if %ERRORLEVEL% NEQ 0 (
    echo %RED%Failed to start Flask application%NC%
    pause
    exit /b 1
)

endlocal

pause
