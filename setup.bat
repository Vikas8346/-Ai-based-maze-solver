@echo off
REM Setup script for AI-Based Maze Solver (Windows)

echo ==========================================
echo   AI-Based Maze Solver - Setup Script
echo ==========================================
echo.

REM Check Python
echo Checking Python version...
python --version
if %errorlevel% neq 0 (
    echo X Python not found. Please install Python 3.8+
    exit /b 1
)
echo + Python found
echo.

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo X Failed to create virtual environment
    exit /b 1
)
echo + Virtual environment created
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip -q
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt
if %errorlevel% neq 0 (
    echo X Failed to install dependencies
    exit /b 1
)
echo + Dependencies installed successfully
echo.

REM Create results directory
echo Creating results directory...
if not exist results mkdir results
echo + Results directory created
echo.

REM Run quick test
echo Running quick test...
python -c "from src.maze import Maze; from src.algorithms import PathfindingAlgorithms; print('+ Import test passed')"
if %errorlevel% neq 0 (
    echo X Import test failed
    exit /b 1
)
echo.

echo ==========================================
echo   Setup Complete!
echo ==========================================
echo.
echo To get started:
echo   1. Activate the virtual environment:
echo      venv\Scripts\activate
echo.
echo   2. Run the application:
echo      python main.py              # GUI mode
echo      python main.py --console    # Console mode
echo      python demo.py              # Quick demo
echo.
echo For more information, see README.md
echo.
pause
