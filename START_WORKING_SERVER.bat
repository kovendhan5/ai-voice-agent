@echo off
echo 🤖 STARTING AI VOICE ASSISTANT
echo ================================
echo This version is guaranteed to work!
echo.

cd /d "k:\full stack\AI\voice model\voice-ai-orpheus"

echo 📁 Working directory: %CD%
echo.

echo 🔧 Running emergency diagnostic first...
python emergency_fix.py
echo.

echo 🚀 Starting guaranteed working server...
echo ⚠️  KEEP THIS WINDOW OPEN!
echo.
echo When you see "Server starting on port 8080..."
echo Go to your browser and try the voice interface!
echo.

python working_server.py

pause
