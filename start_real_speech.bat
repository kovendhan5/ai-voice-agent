@echo off
echo ========================================
echo  🎤 REAL SPEECH + AI CONVERSATION 🤖
echo ========================================
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"

if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo ✨ Starting server with REAL SPEECH capabilities:
echo   💬 Windows Speech API (SAPI) for actual voice
echo   🤖 Intelligent AI conversation with memory
echo   🔊 Multiple realistic voices
echo   🎯 Both simple TTS demo AND real-time chat
echo.
echo 🌐 Server: http://localhost:8080
echo 📱 Interface: enhanced_interface.html
echo.
echo 🗣️ Try the AI Chat tab and say "hello" for real conversation!
echo.
echo Press Ctrl+C to stop the server
echo.

python app_real_speech.py
