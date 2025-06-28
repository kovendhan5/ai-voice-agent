@echo off
echo ==========================================
echo  🎤 ORPHEUS TTS - HUMAN-LIKE SPEECH 🗣️
echo ==========================================
echo.
echo ✨ Like the demo: "Classic Zac, always so groggy! 
echo    Well, it's time to introduce Orpheus to the world..."
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"

if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo 🚀 Starting ORPHEUS with human-like speech:
echo   🎭 Natural conversation personality
echo   🗣️ Orpheus-style speech synthesis  
echo   💬 Real-time voice conversations
echo   🧠 Intelligent responses with memory
echo.
echo 🌐 Server: http://localhost:8080
echo 📱 Interface: enhanced_interface.html
echo.
echo 💫 Expected: Natural human-like speech like the demo!
echo 🎯 Try: "Hello Orpheus, how are you?"
echo.
echo Press Ctrl+C to stop the server
echo.

python app_orpheus.py
