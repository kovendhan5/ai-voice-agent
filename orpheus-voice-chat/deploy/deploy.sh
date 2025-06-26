#!/bin/bash

# Cloud deployment script for Orpheus Voice Chat
# Project ID: ai-project-464106

set -e

echo "🚀 DEPLOYING ORPHEUS VOICE CHAT TO GOOGLE CLOUD"
echo "================================================"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ Google Cloud SDK is not installed"
    echo "Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Set project
echo "📋 Setting up project: ai-project-464106"
gcloud config set project ai-project-464106

# Enable required APIs
echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

# Create .gcloudignore file
cat > .gcloudignore << EOF
.git
.gitignore
README.md
docs/
tests/
scripts/
.vscode/
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
.venv/
EOF

# Deploy to Cloud Run using Cloud Build
echo "🏗️ Building and deploying with Cloud Build..."
gcloud builds submit --config=deploy/cloudbuild.yaml

echo "✅ Deployment completed!"
echo "🌐 Your Orpheus Voice Chat should be available at:"
gcloud run services describe orpheus-voice-chat --region=us-central1 --format="value(status.url)"
