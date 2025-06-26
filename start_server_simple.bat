@echo off
echo.
echo 🎭 Starting Orpheus TTS Server (No Transformers)
echo =========================================================
echo.

cd /d "%~dp0"
call venv\Scripts\activate.bat

echo ✅ Virtual environment activated
echo 🔧 Disabling problematic transformers package...
set DISABLE_TRANSFORMERS=true

echo 🔄 Starting Python server with fallback responses...
echo.

python app_orpheus_authentic.py

echo.
echo ❌ Server stopped. Press any key to continue...
pause
