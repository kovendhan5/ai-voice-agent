@echo off
REM Windows batch script for deploying Orpheus Voice Chat to Google Cloud
REM Project ID: ai-project-464106

echo 🚀 DEPLOYING ORPHEUS VOICE CHAT TO GOOGLE CLOUD
echo ================================================

REM Check if gcloud is installed
where gcloud >nul 2>nul
if %errorlevel% neq 0 (
    echo ❌ Google Cloud SDK is not installed
    echo Install from: https://cloud.google.com/sdk/docs/install
    pause
    exit /b 1
)

REM Set project
echo 📋 Setting up project: ai-project-464106
gcloud config set project ai-project-464106

REM Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

REM Navigate to project root
cd /d "%~dp0.."

REM Create .gcloudignore file
echo Creating .gcloudignore...
(
echo .git
echo .gitignore
echo README.md
echo docs/
echo tests/
echo scripts/
echo .vscode/
echo __pycache__/
echo *.pyc
echo *.pyo
echo *.pyd
echo .Python
echo env/
echo venv/
echo .venv/
) > .gcloudignore

REM Deploy to Cloud Run using Cloud Build
echo 🏗️ Building and deploying with Cloud Build...
gcloud builds submit --config=deploy/cloudbuild.yaml

echo ✅ Deployment completed!
echo 🌐 Your Orpheus Voice Chat should be available at:
gcloud run services describe orpheus-voice-chat --region=us-central1 --format="value(status.url)"

pause
