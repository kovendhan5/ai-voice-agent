@echo off
echo 🔧 GITHUB PUSH FIX SCRIPT
echo ============================
echo.

echo 📋 Step 1: Checking current status...
git status

echo.
echo 📋 Step 2: Removing any remaining large files from tracking...
git rm -r --cached orpheus-voice-chat/checkpoints 2>nul
git rm --cached orpheus-voice-chat/*.wav 2>nul
git rm --cached orpheus-voice-chat/*.mp3 2>nul

echo.
echo 📋 Step 3: Ensuring .gitignore is up to date...
git add orpheus-voice-chat/.gitignore

echo.
echo 📋 Step 4: Committing cleanup changes...
git commit -m "🧹 Final cleanup - Remove all large files for GitHub push" 2>nul

echo.
echo 📋 Step 5: Checking what we're about to push...
git log --oneline origin/main..HEAD

echo.
echo 📋 Step 6: Attempting push to GitHub...
echo This may take a moment...
git push origin main

echo.
echo 📋 Step 7: Final status check...
git status

echo.
echo ✅ Script completed!
echo Check your repository at: https://github.com/kovendhan5/ai-voice-agent
echo.
pause
