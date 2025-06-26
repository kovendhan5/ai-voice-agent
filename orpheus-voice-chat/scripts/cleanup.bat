@echo off
echo ================================================
echo 🧹 Cleaning up old voice model files
echo ================================================

cd /d "%~dp0\.."

echo 📁 Current directory: %cd%

echo.
echo ⚠️ This will remove the old ai-voice-agent and voice-ai-orpheus folders
echo 💾 The new organized project is in: orpheus-voice-chat\
echo.
set /p confirm="Continue with cleanup? (y/n): "

if /i "%confirm%"=="y" (
    echo.
    echo 🗑️ Removing old ai-voice-agent folder...
    if exist "ai-voice-agent" (
        rmdir /s /q "ai-voice-agent"
        echo ✅ ai-voice-agent folder removed
    ) else (
        echo ⚠️ ai-voice-agent folder not found
    )
    
    echo 🗑️ Removing old voice-ai-orpheus folder...
    if exist "voice-ai-orpheus" (
        rmdir /s /q "voice-ai-orpheus"
        echo ✅ voice-ai-orpheus folder removed
    ) else (
        echo ⚠️ voice-ai-orpheus folder not found
    )
    
    echo.
    echo ✨ Cleanup complete!
    echo 📂 Your organized project is now in: orpheus-voice-chat\
    echo 🚀 To start the server: cd orpheus-voice-chat && scripts\start.bat
) else (
    echo ❌ Cleanup cancelled
)

echo.
pause
