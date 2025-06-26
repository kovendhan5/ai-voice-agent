@echo off
echo ============================================
echo  🎭 REAL ORPHEUS - EXPRESSIONS & EMOTIONS 
echo ============================================
echo.
echo ✨ Like the demo with REAL expressions:
echo    "Classic Zac, always so groggy! <laugh>"
echo    "Well, it's time to introduce Orpheus..."
echo.
echo 🎯 Features:
echo    😂 Actual laughter and chuckles
echo    ⏸️ Natural pauses and timing
echo    🎵 Tone variation and emphasis  
echo    🗣️ Human-like prosody
echo    💬 Emotional expressions
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"

if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo 🚀 Starting REAL ORPHEUS with multiple TTS engines:
echo   🥇 Edge TTS (most natural)
echo   🥈 Google TTS (fallback)
echo   🥉 Windows SAPI (final fallback)
echo.
echo 🌐 Server: http://localhost:8080
echo 📱 Interface: enhanced_interface.html
echo.
echo 💫 Try: "Hello Orpheus! Tell me a joke!"
echo 🎭 Expected: Real laughter, pauses, emphasis!
echo.
echo Press Ctrl+C to stop the server
echo.

python app_orpheus_real.py
