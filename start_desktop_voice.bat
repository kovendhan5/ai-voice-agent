@echo off
echo 🎤 Orpheus TTS Desktop Voice Interface
echo ======================================
echo.
echo This will start:
echo 1. The Orpheus TTS API server (if not running)
echo 2. The desktop voice interface application
echo.

REM Check if server is already running
echo Checking if API server is running...
curl -s http://localhost:8080/ > nul 2>&1
if %errorlevel% neq 0 (
    echo Starting API server...
    start "Orpheus TTS API" python app.py
    echo Waiting for server to start...
    timeout /t 5 /nobreak > nul
) else (
    echo ✅ API server is already running
)

echo Starting desktop voice interface...
python voice_desktop_app.py

echo.
echo Voice interface closed.
pause
