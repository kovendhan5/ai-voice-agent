@echo off
REM Orpheus TTS API Deployment Script for GCP Cloud Run (Windows)
REM Usage: deploy.bat [PROJECT_ID]

setlocal enabledelayedexpansion

echo 🚀 Orpheus TTS API Deployment Script
echo ===========================================

REM Configuration
set SERVICE_NAME=orpheus-tts
set REGION=us-central1
set MEMORY=2Gi
set CPU=1
set MAX_INSTANCES=10
set TIMEOUT=300

REM Get project ID
if "%1"=="" (
    for /f "tokens=*" %%i in ('gcloud config get-value project 2^>nul') do set PROJECT_ID=%%i
    if "!PROJECT_ID!"=="" (
        echo ❌ No project ID provided and no default project set
        echo Usage: %0 [PROJECT_ID]
        echo Or set default project: gcloud config set project YOUR_PROJECT_ID
        exit /b 1
    )
    echo 📋 Using default project: !PROJECT_ID!
) else (
    set PROJECT_ID=%1
    echo 📋 Using project: !PROJECT_ID!
    gcloud config set project "!PROJECT_ID!"
)

REM Enable required APIs
echo 🔧 Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

REM Build and push container
echo 🏗️ Building container image...
set IMAGE_URL=gcr.io/!PROJECT_ID!/!SERVICE_NAME!
gcloud builds submit --tag "!IMAGE_URL!" .

REM Deploy to Cloud Run
echo ☁️ Deploying AI Voice Assistant to Cloud Run...
gcloud run deploy "!SERVICE_NAME!" ^
    --image "!IMAGE_URL!" ^
    --platform managed ^
    --region "!REGION!" ^
    --allow-unauthenticated ^
    --memory "!MEMORY!" ^
    --cpu "!CPU!" ^
    --timeout "!TIMEOUT!" ^
    --max-instances "!MAX_INSTANCES!" ^
    --set-env-vars "PORT=8080,DEBUG=false" ^
    --description "Orpheus AI Voice Assistant - Interactive conversations with AI"

REM Get service URL
for /f "tokens=*" %%i in ('gcloud run services describe "!SERVICE_NAME!" --region "!REGION!" --format "value(status.url)"') do set SERVICE_URL=%%i

echo ✅ Deployment completed successfully!
echo ===========================================
echo 🌐 Service URL: !SERVICE_URL!
echo.
echo Test your AI Voice Assistant:
echo curl -X POST !SERVICE_URL!/voice_chat \
echo   -H "Content-Type: application/json" \
echo   -d "{\"message\": \"Hello AI, how are you?\", \"user_id\": \"TestUser\"}" \
echo   --output ai_response.wav
echo.
echo Chat with AI (text only):
echo curl -X POST !SERVICE_URL!/chat \
echo   -H "Content-Type: application/json" \
echo   -d "{\"message\": \"Hello AI!\", \"user_id\": \"TestUser\"}"
echo.
echo Open the voice interface:
echo !SERVICE_URL! (share this link with friends!)
echo.
echo Health check:
echo curl !SERVICE_URL!/

pause
