@echo off
echo.
echo 🎭 Starting Orpheus TTS Server with Detailed Output
echo =========================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo ✅ Virtual environment activated
echo 🔄 Starting Python server...
echo.

python app_orpheus_authentic.py

echo.
echo ❌ Server stopped. Press any key to see output...
pause
