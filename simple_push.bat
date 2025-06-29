@echo off
chcp 65001 >nul
echo 🚀 SIMPLIFIED GITHUB PUSH
echo =========================
echo.

echo 📋 Current Status:
git status --porcelain

echo.
echo 📤 Attempting Direct Push...
echo This will push all 17 commits to GitHub
echo.

timeout /t 3 /nobreak >nul

git push origin main 2>&1

echo.
echo 📊 Post-Push Status:
git status

echo.
echo ✅ Push attempt completed!
echo Check: https://github.com/kovendhan5/ai-voice-agent
echo.
pause
