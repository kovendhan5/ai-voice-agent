@echo off
echo ================================================
echo ⚡ Quick Fix - Installing Essential Dependencies
echo ================================================

cd /d "%~dp0\.."
echo 📁 Working directory: %cd%

echo.
echo 🐍 Activating virtual environment...
if exist "venv\Scripts\activate.bat" (
    call venv\Scripts\activate.bat
) else (
    echo ❌ Virtual environment not found!
    echo 🔧 Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
)

echo.
echo ⚡ Installing ONLY essential dependencies (no problematic packages)...

echo Installing Flask...
pip install flask
if errorlevel 1 (
    echo ❌ Failed to install Flask
    pause
    exit /b 1
)

echo Installing Flask-CORS...
pip install flask-cors
if errorlevel 1 (
    echo ❌ Failed to install Flask-CORS
    pause
    exit /b 1
)

echo Installing requests...
pip install requests
if errorlevel 1 (
    echo ❌ Failed to install requests
    pause
    exit /b 1
)

echo Installing numpy...
pip install numpy
if errorlevel 1 (
    echo ❌ Failed to install numpy
    pause
    exit /b 1
)

echo.
echo ✅ Essential dependencies installed!
echo 📝 Note: Orpheus TTS is NOT installed (server will run in mock mode)
echo 🎭 This means you'll get silent audio instead of real voice
echo.
echo 🚀 To start the server: scripts\start.bat
echo 🌐 Server will be available at: http://localhost:8080
echo.
echo 💡 To install Orpheus TTS later (optional):
echo    pip install orpheus-speech
echo.

pause
