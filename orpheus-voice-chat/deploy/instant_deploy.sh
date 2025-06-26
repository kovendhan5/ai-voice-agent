#!/bin/bash
echo "🚀 INSTANT ORPHEUS VOICE CHAT DEPLOYMENT"
echo "========================================"

# Enable required APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Set project (use current project)
PROJECT_ID=$(gcloud config get-value project)
echo "📋 Using project: $PROJECT_ID"

# Quick build and deploy
echo "🏗️ Building container..."
gcloud builds submit --tag gcr.io/$PROJECT_ID/orpheus-voice-fast .

echo "🚀 Deploying to Cloud Run..."
gcloud run deploy orpheus-voice-fast \
  --image gcr.io/$PROJECT_ID/orpheus-voice-fast \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 1Gi \
  --timeout 60

# Get URL
URL=$(gcloud run services describe orpheus-voice-fast --region us-central1 --format 'value(status.url)')

echo ""
echo "🎉 SUCCESS! Your voice chat is LIVE!"
echo "📱 URL: $URL"
echo ""
echo "🧪 Test it:"
echo "curl -X POST $URL/synthesize -H 'Content-Type: application/json' -d '{\"text\":\"Hello from the cloud!\"}'"
echo ""
echo "👥 Share this URL with friends: $URL"
