@echo off
echo 🎭 STARTING ORPHEUS-QUALITY AI VOICE CHAT
echo ==========================================
echo 🧠 AI: Google Gemini Pro with your API key
echo 🎤 Voice: Microsoft Neural TTS (Edge-quality)
echo 🎭 Features: SSML emotions, human-like speech
echo 😄 Voices: 8 professional neural personalities
echo.

cd "k:\full stack\AI\voice model\orpheus-voice-chat"

echo 🔄 Activating virtual environment...
call venv\Scripts\activate

echo 🎯 Starting Enhanced Orpheus Voice Chat...
python src\app_orpheus_enhanced.py

pause
