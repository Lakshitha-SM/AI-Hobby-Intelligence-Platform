@echo off
REM AI Hobby Intelligence Platform - Windows Launcher
setlocal enabledelayedexpansion

cls
echo ============================================================================
echo  AI HOBBY INTELLIGENCE PLATFORM - Windows Setup & Launch
echo ============================================================================

REM Check Python installation
echo.
echo [CHECK] Verifying Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo.
    echo ERROR: Python not found in PATH!
    echo Please install Python 3.8+ from https://www.python.org/
    echo Make sure to check "Add Python to PATH" during installation.
    echo.
    pause
    exit /b 1
)
for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYVER=%%i
echo [OK] Python %PYVER% found

REM Fix requirements.txt
echo.
echo [STEP 1] Fixing requirements.txt...
(
    echo pandas^>=2.0.0
    echo sentence-transformers^>=2.2.0
    echo chromadb^>=0.4.0
    echo google-generativeai^>=0.3.0
    echo rich^>=13.0.0
    echo python-dotenv^>=1.0.0
) > requirements.txt
echo [OK] requirements.txt created

REM Install dependencies
echo.
echo [STEP 2] Installing dependencies...
echo This may take 2-5 minutes on first run...
echo.
python -m pip install -q --upgrade pip
python -m pip install -q pandas
python -m pip install -q sentence-transformers
python -m pip install -q chromadb
python -m pip install -q google-generativeai
python -m pip install -q rich
python -m pip install -q python-dotenv

if errorlevel 1 (
    echo.
    echo [WARNING] Some packages may not have installed correctly.
    echo The platform may still work if core packages are installed.
)
echo [OK] Dependencies installed

REM Run diagnostics
echo.
echo [STEP 3] Running diagnostics...
python test_all.py
if errorlevel 1 (
    echo.
    echo [WARNING] Some diagnostics failed, but attempting to launch...
)

REM Launch the platform
echo.
echo ============================================================================
echo  LAUNCHING AI HOBBY INTELLIGENCE PLATFORM
echo ============================================================================
echo.
echo Starting interactive CLI...
echo Press Ctrl+C to exit at any time
echo.
python main.py

exit /b 0
