@echo off
echo ========================================
echo 🎭 ORPHEUS VOICE CHAT - MINIMAL MODE
echo ========================================
echo.
echo 🔥 Starting minimal server (no complex dependencies)
echo 📝 This version works with just Flask and numpy
echo 🎵 Generates test tones instead of real speech
echo.

cd /d "%~dp0\.."
echo 📁 Working directory: %cd%

echo 🐍 Checking Python environment...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo 🔧 Please run setup first: scripts\quick_fix.bat
    pause
    exit /b 1
)

echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

echo 🔍 Checking minimal dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Flask not found! Please run: scripts\quick_fix.bat
    pause
    exit /b 1
)

echo ✅ Dependencies OK

echo.
echo 🚀 Starting Minimal Orpheus Voice Chat server...
echo 🌐 Server will be available at: http://localhost:8080
echo 🎵 Audio: Test tones (not real speech)
echo 📝 Perfect for testing API functionality
echo.

python src\app_minimal.py

echo.
echo 🛑 Server stopped.
pause
