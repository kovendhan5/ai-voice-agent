@echo off
echo ========================================
echo 🎭 AUTHENTIC ORPHEUS TTS SERVER 
echo ========================================
echo.
echo 🔥 Starting the REAL Orpheus TTS server...
echo 📦 Model: canopylabs/orpheus-tts-0.1-finetune-prod
echo 🎯 Features: Human-like speech with real emotions
echo.

cd /d "k:\full stack\AI\voice model\ai-voice-agent"

echo 🐍 Activating Python environment...
call venv\Scripts\activate

echo 📋 Installing/Updating required packages...
pip install orpheus-speech snac vllm torch torchaudio transformers

echo.
echo 🚀 Starting Authentic Orpheus TTS server...
echo 🌐 Server will be available at: http://localhost:8080
echo 📱 Interface will be available at: http://localhost:8080
echo.
echo ⚠️  Note: First run may take longer to download the model
echo 💾 Model size: ~3GB (Orpheus-3B)
echo.

python app_orpheus_authentic.py

echo.
echo 🛑 Server stopped.
pause
