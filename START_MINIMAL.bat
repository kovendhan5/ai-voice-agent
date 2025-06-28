@echo off
echo 🔧 Starting Minimal AI Server...
cd /d "k:\full stack\AI\voice model\voice-ai-orpheus"

echo 🐍 Activating Python environment...
call venv\Scripts\activate.bat

echo 🚀 Starting server on http://localhost:8080...
python minimal_server.py

pause
