@echo off
echo Starting Orpheus TTS API Server...
echo ===================================
echo.
echo The server will start on http://localhost:8080
echo.
echo Available endpoints:
echo   GET  /          - Health check
echo   GET  /voices    - List available voices  
echo   POST /speak     - Generate speech from text
echo.
echo Press Ctrl+C to stop the server
echo.
python app.py
