@echo off
chcp 65001 >nul 2>&1
title GitHub Push - Final Solution

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                    🚀 GITHUB PUSH - FINAL SOLUTION            ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

cd /d "k:\full stack\AI\voice model"

echo 📋 Step 1: Add any remaining files...
git add final_github_push.bat
git add smart_github_push.py
git add DEPLOYMENT_COMPLETE.md

echo 📝 Step 2: Commit remaining files...
git commit -m "🚀 Final deployment scripts and documentation" 2>nul

echo 📊 Step 3: Current status...
git status

echo.
echo 📤 Step 4: Direct push attempt...
echo ⏳ This may take several minutes for large uploads...
echo.

REM Clear any cached credentials and try fresh
git config --unset credential.helper 2>nul
git config credential.helper manager-core

echo Starting push...
git push origin main --progress --verbose

echo.
echo 📊 Step 5: Verification...
git status

if %ERRORLEVEL% EQU 0 (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║                        ✅ SUCCESS!                             ║
    echo ║              Repository updated on GitHub!                     ║
    echo ║                                                                ║
    echo ║   🔗 https://github.com/kovendhan5/ai-voice-agent              ║
    echo ║                                                                ║
    echo ║   Your Orpheus-TTS voice chat system is now live!             ║
    echo ╚════════════════════════════════════════════════════════════════╝
) else (
    echo.
    echo ╔════════════════════════════════════════════════════════════════╗
    echo ║                       ⚠️ PUSH ISSUES                          ║
    echo ║                                                                ║
    echo ║  Alternative solutions:                                        ║
    echo ║  1. Use GitHub Desktop application                             ║
    echo ║  2. Check your GitHub token/password                           ║
    echo ║  3. Try smaller batches: git push origin main --force          ║
    echo ║  4. Check network connection                                    ║
    echo ╚════════════════════════════════════════════════════════════════╝
)

echo.
echo Press any key to continue...
pause >nul
