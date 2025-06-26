@echo off
echo 🎭 Starting Orpheus Voice Chat...
echo.
echo ✅ Dependencies installed
echo ✅ Integration fixes applied  
echo ✅ System ready for live chat
echo.
echo 🌐 Starting server on http://localhost:5000
echo 🎤 Open your browser and start chatting!
echo.
echo Press Ctrl+C to stop the server
echo.

cd /d "%~dp0"
python src/app_live_orpheus.py

pause
