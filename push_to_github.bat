@echo off
echo 🚀 GITHUB PUSH SCRIPT - Manual Deployment
echo ============================================
cd "k:\full stack\AI\voice model"

echo ✅ Current directory: %CD%
echo ✅ Adding all changes...
git add .

echo ✅ Committing remaining changes...
git commit -m "🔄 Complete system deployment - All Orpheus-TTS integration and fixes ready"

echo ✅ Checking status before push...
git status

echo ✅ Pushing to GitHub (this may take a moment)...
git push origin main

echo ✅ Checking final status...
git status

echo 🎉 GitHub push process completed!
echo 📊 Check your repository at: https://github.com/kovendhan5/ai-voice-agent
pause
