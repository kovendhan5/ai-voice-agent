@echo off
echo Starting Orpheus TTS API Demo...
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"

if exist venv (
    echo Activating virtual environment...
    call venv\Scripts\activate
) else (
    echo No virtual environment found. Using system Python.
)

echo.
echo Starting server on port 8080...
echo Press Ctrl+C to stop the server
echo.

python app_demo.py
