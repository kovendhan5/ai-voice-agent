@echo off
echo ========================================
echo 🧪 TESTING ORPHEUS TTS API
echo ========================================
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"
python test_orpheus_api.py

echo.
echo ========================================
echo 🎭 OPENING ORPHEUS INTERFACE
echo ========================================
echo.

start http://localhost:8080
echo 🌐 Interface opened in browser!

pause
