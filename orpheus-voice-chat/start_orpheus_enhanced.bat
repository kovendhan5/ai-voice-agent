@echo off
echo 🎭 ORPHEUS VOICE CHAT - STARTUP
echo ================================
echo.

echo 🚀 Starting Orpheus Voice Chat System...
echo.

REM Check Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found! Please install Python 3.11+
    pause
    exit /b 1
)

echo ✅ Python detected
echo.

REM Run system verification
echo 🔍 Running system verification...
python safe_verification.py

echo.
echo 🎭 System ready! Choose an option:
echo.
echo 1. Run Quick Working Demo (quick_working_demo.py)
echo 2. Test Integration (test_integration.py)
echo 3. Run Live Voice Chat (app_live_orpheus.py)
echo 4. Quick Status Check (quick_status.py)
echo 5. Exit
echo.

set /p choice="Enter your choice (1-5): "

if "%choice%"=="1" (
    echo � Starting Quick Working Demo...
    python quick_working_demo.py
) else if "%choice%"=="2" (
    echo 🧪 Running Integration Tests...
    python test_integration.py
) else if "%choice%"=="3" (
    echo �️ Starting Live Voice Chat...
    python src\app_live_orpheus.py
) else if "%choice%"=="4" (
    echo 📊 Running Quick Status Check...
    python quick_status.py
) else if "%choice%"=="5" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice!
)

echo.
echo Press any key to continue...
pause >nul
