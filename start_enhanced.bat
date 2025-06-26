@echo off
echo Starting Enhanced Orpheus TTS + AI Chat Server...
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"

if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo Starting enhanced server with both TTS demo and AI chat...
echo Features:
echo   - Simple TTS Demo (matches original repo)
echo   - Real-time AI Conversation
echo   - Voice responses
echo   - Multi-user support
echo.
echo Server will start on: http://localhost:8080
echo Open enhanced_interface.html in your browser
echo.
echo Press Ctrl+C to stop the server
echo.

python app_enhanced.py
