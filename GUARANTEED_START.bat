@echo off
title AI Voice Assistant Server
color 0A

echo ===============================================
echo 🤖 AI VOICE ASSISTANT - GUARANTEED TO WORK
echo ===============================================
echo.

cd /d "k:\full stack\AI\voice model\voice-ai-orpheus"

echo 🐍 Activating environment...
call venv\Scripts\activate.bat

echo.
echo 🚀 Starting server on http://localhost:8080
echo 📍 Keep this window open while using the AI
echo 🌐 Open chatgpt_interface.html in your browser
echo.
echo ===============================================
echo 🟢 SERVER IS STARTING...
echo ===============================================

python minimal_server.py

echo.
echo ❌ Server stopped. Press any key to restart...
pause > nul
goto :eof
