#!/bin/bash

# Orpheus TTS API Deployment Script for GCP Cloud Run
# Usage: ./deploy.sh [PROJECT_ID]

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
SERVICE_NAME="orpheus-tts"
REGION="us-central1"
MEMORY="2Gi"
CPU="1"
MAX_INSTANCES="10"
TIMEOUT="300"

echo -e "${GREEN}🚀 Orpheus TTS API Deployment Script${NC}"
echo "==========================================="

# Get project ID
if [ -z "$1" ]; then
    PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
    if [ -z "$PROJECT_ID" ]; then
        echo -e "${RED}❌ No project ID provided and no default project set${NC}"
        echo "Usage: $0 [PROJECT_ID]"
        echo "Or set default project: gcloud config set project YOUR_PROJECT_ID"
        exit 1
    fi
    echo -e "${YELLOW}📋 Using default project: $PROJECT_ID${NC}"
else
    PROJECT_ID="$1"
    echo -e "${YELLOW}📋 Using project: $PROJECT_ID${NC}"
    gcloud config set project "$PROJECT_ID"
fi

# Enable required APIs
echo -e "${YELLOW}🔧 Enabling required APIs...${NC}"
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com

# Build and push container
echo -e "${YELLOW}🏗️  Building container image...${NC}"
IMAGE_URL="gcr.io/$PROJECT_ID/$SERVICE_NAME"
gcloud builds submit --tag "$IMAGE_URL" .

# Deploy to Cloud Run
echo -e "${YELLOW}☁️  Deploying to Cloud Run...${NC}"
gcloud run deploy "$SERVICE_NAME" \
    --image "$IMAGE_URL" \
    --platform managed \
    --region "$REGION" \
    --allow-unauthenticated \
    --memory "$MEMORY" \
    --cpu "$CPU" \
    --timeout "$TIMEOUT" \
    --max-instances "$MAX_INSTANCES" \
    --set-env-vars "PORT=8080"

# Get service URL
SERVICE_URL=$(gcloud run services describe "$SERVICE_NAME" --region "$REGION" --format 'value(status.url)')

echo -e "${GREEN}✅ Deployment completed successfully!${NC}"
echo "==========================================="
echo -e "${GREEN}🌐 Service URL: $SERVICE_URL${NC}"
echo ""
echo "Test your API:"
echo "curl -X POST $SERVICE_URL/speak \\"
echo '  -H "Content-Type: application/json" \'
echo '  -d '"'"'{"text": "tara: Hello from the cloud!"}'"'"' \'
echo "  --output speech.wav"
echo ""
echo "Health check:"
echo "curl $SERVICE_URL/"
echo ""
echo "Available voices:"
echo "curl $SERVICE_URL/voices"
