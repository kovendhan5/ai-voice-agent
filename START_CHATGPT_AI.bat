@echo off
echo 🚀 Starting ChatGPT-like AI Voice Assistant
echo.

cd /d "k:\full stack\AI\voice model\voice-ai-orpheus"

echo 🐍 Activating Python environment...
call venv\Scripts\activate.bat

echo 🌐 Starting AI server on http://localhost:8080...
echo.
echo 📝 Features available:
echo   • Type messages like ChatGPT
echo   • Voice input with speech recognition
echo   • AI voice responses  
echo   • Conversation history
echo   • Intelligent contextual responses
echo.

start "" "chatgpt_interface.html"

echo 🚀 Server starting... Interface will open automatically.
echo 🔗 If interface doesn't open, manually open: chatgpt_interface.html
echo.

python minimal_server.py

pause
