@echo off
echo ==========================================
echo  🗣️ REAL HUMAN VOICE TTS - NO MORE NOISE! 
echo ==========================================
echo.
echo ❌ BEFORE: Weird synthetic noise
echo ✅ NOW: Actual human speech using:
echo    • Microsoft Edge TTS (Neural voices)
echo    • Google Text-to-Speech  
echo    • Windows Speech API
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"

if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo 🚀 Starting REAL VOICE server:
echo   🎭 Multiple TTS engines for backup
echo   🗣️ Microsoft Edge Neural voices (primary)
echo   💬 Natural conversation AI
echo   🔊 ACTUAL human speech - no synthetic noise!
echo.
echo 🌐 Server: http://localhost:8080
echo 📱 Interface: enhanced_interface.html
echo.
echo 🎯 Try: "Hello, how are you today?"
echo ✨ Expected: Clear, natural human speech!
echo.
echo Press Ctrl+C to stop the server
echo.

python app_real_voice.py
