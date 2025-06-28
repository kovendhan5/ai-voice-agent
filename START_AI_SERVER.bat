@echo off
title AI Voice Assistant Server
color 0a

echo.
echo  ████████████████████████████████████████████
echo  █                                          █
echo  █     🤖 AI VOICE ASSISTANT SERVER 🤖     █  
echo  █                                          █
echo  ████████████████████████████████████████████
echo.
echo  Starting your AI Voice Assistant...
echo  Keep this window open while using the AI!
echo.

cd /d "k:\full stack\AI\voice model\voice-ai-orpheus"

echo ⏳ Loading AI models...
python ai_voice_assistant.py

echo.
echo ❌ Server stopped. Press any key to restart...
pause > nul
goto start
