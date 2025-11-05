@echo off
REM Windows batch script to run Robotics Industry Projection Analysis

echo ============================================================
echo Robotics Industry Projection Analysis 2026
echo ============================================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python 3.8 or higher
    pause
    exit /b 1
)

echo Python found. Checking dependencies...
echo.

REM Check if virtual environment exists
if exist "venv\Scripts\activate.bat" (
    echo Activating virtual environment...
    call venv\Scripts\activate.bat
) else (
    echo Virtual environment not found. Creating one...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -r requirements.txt
)

echo.
echo Running analysis...
echo ============================================================
echo.

python src\run_analysis.py

echo.
echo ============================================================
echo Analysis complete!
echo ============================================================
echo.
echo Output files are in:
echo   - data\processed\projections_2026.csv
echo   - outputs\reports\projection_report_2026.txt
echo   - outputs\figures\
echo.

pause

