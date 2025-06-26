@echo off
echo Testing Orpheus TTS API...
echo.

echo Testing health check endpoint...
curl -X GET http://localhost:8080/
echo.
echo.

echo Testing voices endpoint...
curl -X GET http://localhost:8080/voices
echo.
echo.

echo Testing speech generation (saving to test_output.wav)...
curl -X POST http://localhost:8080/speak ^
     -H "Content-Type: application/json" ^
     -d "{\"text\": \"Hello from Orpheus TTS! This is a test of the speech synthesis.\", \"voice\": \"tara\"}" ^
     --output test_output.wav

if exist test_output.wav (
    echo.
    echo ✅ Audio file generated successfully: test_output.wav
    echo File size: 
    dir test_output.wav | find "test_output.wav"
    echo.
    echo You can play this file to hear the generated speech.
) else (
    echo ❌ Failed to generate audio file
)

echo.
echo Test complete!
