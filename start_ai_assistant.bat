@echo off
echo 🤖 Orpheus AI Voice Assistant Launcher
echo =========================================
echo.
echo This will start:
echo 1. The AI Voice Assistant API server
echo 2. Open the interactive voice interface
echo.
echo Features:
echo - Real AI conversations (not just echoing)
echo - Voice input and voice responses
echo - Multiple users can chat with the same AI
echo - Conversation history
echo - Multiple AI voices
echo.
echo Make sure you have a microphone connected!
echo.
pause

echo Starting AI Voice Assistant server...
start "AI Voice Assistant" python ai_voice_assistant.py

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo Opening AI voice interface...
start "" ai_voice_interface.html

echo.
echo ✅ AI Voice Assistant is ready!
echo.
echo Instructions:
echo 1. Allow microphone access when prompted
echo 2. Click the microphone button to start talking
echo 3. Have a natural conversation with the AI
echo 4. The AI will respond with voice and you can continue chatting
echo.
echo Share the interface:
echo - Once deployed to cloud, you can share the URL with friends
echo - Multiple people can talk to the same AI assistant
echo.
echo Troubleshooting:
echo - If microphone doesn't work, check browser permissions
echo - Use Chrome or Edge for best speech recognition
echo - Make sure speakers/headphones are working for AI responses
echo.
echo Press any key to continue...
pause > nul
