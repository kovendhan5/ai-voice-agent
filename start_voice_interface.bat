@echo off
echo 🎤 Orpheus TTS Voice Interface Launcher
echo =========================================
echo.
echo This will start:
echo 1. The Orpheus TTS API server (Flask)
echo 2. Open the web voice interface in your browser
echo.
echo Make sure you have a microphone connected!
echo.
pause

echo Starting API server...
start "Orpheus TTS API" python app.py

echo Waiting for server to start...
timeout /t 5 /nobreak > nul

echo Opening voice interface...
start "" voice_interface.html

echo.
echo ✅ Voice interface is ready!
echo.
echo Instructions:
echo 1. Allow microphone access when prompted
echo 2. Click the microphone button to start listening
echo 3. Speak clearly into your microphone
echo 4. Your speech will be converted to text and spoken back
echo.
echo Troubleshooting:
echo - If API connection fails, check that the server is running
echo - Make sure your microphone is working
echo - Use Chrome or Edge browser for best speech recognition
echo.
echo Press any key to exit...
pause > nul
