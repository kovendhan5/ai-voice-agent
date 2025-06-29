@echo off
echo 🚀 FINAL GITHUB PUSH SOLUTION
echo ================================
echo.

echo 📋 Current Status:
git log --oneline -5
echo.

echo 🔍 Checking for large files that might block push...
git ls-files | findstr -E "\.(pth|bin|wav|mp3|mp4)$"

echo.
echo 📤 Attempting to push 19 commits to GitHub...
echo This includes your complete Orpheus-TTS voice chat system!
echo.

REM Try the push with progress reporting
git push origin main --progress 2>&1

echo.
echo 📊 Final Status Check:
git status

echo.
if %ERRORLEVEL% EQU 0 (
    echo ✅ SUCCESS! Your repository has been updated on GitHub
    echo 🌐 Check it out: https://github.com/kovendhan5/ai-voice-agent
) else (
    echo ❌ Push failed. Let's try alternative solutions:
    echo 1. Force push: git push origin main --force
    echo 2. Use GitHub Desktop
    echo 3. Check internet connection
)

echo.
pause
