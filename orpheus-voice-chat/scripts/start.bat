@echo off
echo ========================================
echo 🎭 ORPHEUS VOICE CHAT SERVER 
echo ========================================
echo.

cd /d "%~dp0\.."
echo 📁 Working directory: %cd%

echo 🐍 Checking Python environment...
if not exist "venv\Scripts\activate.bat" (
    echo ❌ Virtual environment not found!
    echo 🔧 Please run setup first: scripts\setup.bat
    pause
    exit /b 1
)

echo ✅ Activating virtual environment...
call venv\Scripts\activate.bat

echo 🔍 Checking core dependencies...
python -c "import flask" 2>nul
if errorlevel 1 (
    echo ❌ Flask not found! Please run: scripts\setup.bat
    pause
    exit /b 1
)

python -c "import flask_cors" 2>nul
if errorlevel 1 (
    echo ❌ Flask-CORS not found! Please run: scripts\setup.bat
    pause
    exit /b 1
)

echo ✅ Core dependencies found

echo.
echo 🔧 Setting environment variables...
set DISABLE_TRANSFORMERS=true
set PYTHONPATH=%cd%\src;%PYTHONPATH%

echo.
echo 🚀 Starting Orpheus Voice Chat server...
echo 🌐 Server will be available at: http://localhost:8080
echo 📱 Interface will be available at: http://localhost:8080
echo.
echo ⚠️  Note: First run may take longer if downloading models
echo 💾 If Orpheus TTS is not installed, server runs in mock mode
echo.

python src\app.py

echo.
echo 🛑 Server stopped.
pause

echo.
echo 🛑 Server stopped.
pause
