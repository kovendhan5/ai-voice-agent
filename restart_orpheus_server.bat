@echo off
echo 🔄 Restarting Authentic Orpheus TTS Server...
echo.

REM Kill any existing python processes on port 8080
for /f "tokens=5" %%a in ('netstat -aon ^| find ":8080" ^| find "LISTENING"') do (
    echo 🛑 Stopping existing server on port 8080...
    taskkill /f /pid %%a 2>nul
)

echo.
echo 🎭 Starting Enhanced Orpheus TTS server...
echo 🌐 Server will be available at: http://localhost:8080
echo 🎤 Interface will be available at: http://localhost:8080
echo.
echo ⚡ Enhanced Features:
echo   • Better text generation with Transformers
echo   • Improved error handling
echo   • Voice personality matching
echo   • Fallback responses for reliability
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat
python app_orpheus_authentic.py

pause
