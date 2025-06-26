@echo off
echo 🚀 Orpheus Voice Chat - Cloud Deployment Script
echo ===============================================
echo.

REM Check if gcloud is installed
gcloud --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Google Cloud SDK not found!
    echo.
    echo 📥 Please install Google Cloud SDK first:
    echo    https://cloud.google.com/sdk/docs/install
    echo.
    echo 🔧 After installation, run:
    echo    gcloud auth login
    echo    gcloud config set project YOUR-PROJECT-ID
    echo.
    pause
    exit /b 1
)

echo ✅ Google Cloud SDK found!
echo.

REM Set default values
set PROJECT_ID=orpheus-voice-chat
set SERVICE_NAME=orpheus-tts
set REGION=us-central1

echo 🔧 Configuration:
echo    Project ID: %PROJECT_ID%
echo    Service Name: %SERVICE_NAME%
echo    Region: %REGION%
echo.

echo 📋 Setting up project...
gcloud config set project %PROJECT_ID%

echo 🔌 Enabling required APIs...
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

echo 🏗️ Building container image...
gcloud builds submit --tag gcr.io/%PROJECT_ID%/%SERVICE_NAME% .

if errorlevel 1 (
    echo ❌ Build failed! Check the error messages above.
    pause
    exit /b 1
)

echo ✅ Build successful!
echo.

echo 🚀 Deploying to Cloud Run...
gcloud run deploy %SERVICE_NAME% ^
  --image gcr.io/%PROJECT_ID%/%SERVICE_NAME% ^
  --platform managed ^
  --region %REGION% ^
  --allow-unauthenticated ^
  --memory 2Gi ^
  --cpu 1 ^
  --timeout 300 ^
  --max-instances 10

if errorlevel 1 (
    echo ❌ Deployment failed! Check the error messages above.
    pause
    exit /b 1
)

echo ✅ Deployment successful!
echo.

echo 🌐 Getting service URL...
for /f "delims=" %%i in ('gcloud run services describe %SERVICE_NAME% --region %REGION% --format "value(status.url)"') do set SERVICE_URL=%%i

echo.
echo 🎉 SUCCESS! Your Orpheus Voice Chat is live!
echo 📱 URL: %SERVICE_URL%
echo.
echo 🧪 Test your deployment:
echo    curl -X POST %SERVICE_URL%/speak -H "Content-Type: application/json" -d "{\"text\":\"tara: Hello from the cloud!\"}" --output test.wav
echo.
echo 📤 Share this URL with your friends!
echo.
pause
