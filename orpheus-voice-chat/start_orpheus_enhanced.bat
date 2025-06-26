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
python final_verification.py

echo.
echo 🎭 System ready! Choose an option:
echo.
echo 1. Run Live Voice Chat (app_live_orpheus.py)
echo 2. Test Ultra-Realistic Demo (ultra_realistic_demo.py)
echo 3. Quick Status Check (quick_status.py)
echo 4. Exit
echo.

set /p choice="Enter your choice (1-4): "

if "%choice%"=="1" (
    echo 🎙️ Starting Live Voice Chat...
    python src\app_live_orpheus.py
) else if "%choice%"=="2" (
    echo 🎭 Starting Ultra-Realistic Demo...
    python ultra_realistic_demo.py
) else if "%choice%"=="3" (
    echo 📊 Running Quick Status Check...
    python quick_status.py
) else if "%choice%"=="4" (
    echo 👋 Goodbye!
    exit /b 0
) else (
    echo ❌ Invalid choice!
)

echo.
echo Press any key to continue...
pause >nul
