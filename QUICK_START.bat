@echo off
cls
echo.
echo ████████████████████████████████████████
echo █          🤖 AI ASSISTANT 🤖          █
echo █                                      █
echo █  Starting your voice AI server...    █
echo █  Keep this window open!             █
echo ████████████████████████████████████████
echo.

cd /d "k:\full stack\AI\voice model\voice-ai-orpheus"

echo ⏳ Initializing AI system...
echo.

python simple_ai_server.py

echo.
echo ❌ Server stopped unexpectedly
pause
