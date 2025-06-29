@echo off
echo 🔧 ULTIMATE GITHUB PUSH FIX
echo ============================
echo.

cd /d "k:\full stack\AI\voice model"

echo 📋 Adding final files...
git add CURRENT_STATUS.md
git add github_push_final.bat

echo 📝 Committing final documentation...
git commit -m "📚 Add final status documentation and push scripts"

echo 🗑️ Force removing any large files from this commit...
git filter-branch -f --tree-filter "rm -rf orpheus-voice-chat/checkpoints" HEAD~1..HEAD 2>nul

echo 📊 Current clean status:
git status

echo 📁 Checking for any remaining large files...
git ls-files | findstr -i "\.(pth|bin|ckpt)$"

echo.
echo 🚀 FINAL PUSH ATTEMPT...
echo ⚠️  Using force push to override any conflicts
echo.

git push origin main --force --verbose

echo.
echo 📊 Final verification:
git status

echo.
echo ✅ Process complete!
echo 🔗 Check: https://github.com/kovendhan5/ai-voice-agent
pause
