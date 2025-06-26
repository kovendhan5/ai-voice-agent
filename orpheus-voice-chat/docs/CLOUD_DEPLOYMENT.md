# 🚀 Orpheus Voice Chat - Cloud Deployment Guide

## Quick Deploy to Google Cloud Run

### Project: ai-project-464106

### Prerequisites
1. **Google Cloud SDK installed**
   ```bash
   # Install from: https://cloud.google.com/sdk/docs/install
   ```

2. **Authentication**
   ```bash
   gcloud auth login
   gcloud auth application-default login
   ```

### 🎯 One-Click Deployment

**Windows:**
```batch
cd deploy
deploy.bat
```

**Linux/Mac:**
```bash
cd deploy
chmod +x deploy.sh
./deploy.sh
```

### 📋 Manual Deployment Steps

1. **Set Project:**
   ```bash
   gcloud config set project ai-project-464106
   ```

2. **Enable APIs:**
   ```bash
   gcloud services enable cloudbuild.googleapis.com
   gcloud services enable run.googleapis.com
   gcloud services enable containerregistry.googleapis.com
   ```

3. **Deploy:**
   ```bash
   gcloud builds submit --config=deploy/cloudbuild.yaml
   ```

### 🌐 Access Your App

After deployment, get your URL:
```bash
gcloud run services describe orpheus-voice-chat --region=us-central1 --format="value(status.url)"
```

### 💰 Cost Optimization (Zero-Cost Tier)

- **Memory:** 2GB (optimized for AI processing)
- **CPU:** 2 vCPU (for real-time audio)
- **Min Instances:** 0 (scales to zero)
- **Max Instances:** 10 (prevents runaway costs)
- **Request Timeout:** 300s (for long audio generation)

### 🎤 Features Deployed

✅ **Live Voice Chat** - Real-time conversation  
✅ **8 AI Personalities** - Tara, Jessica, Leo, Daniel, Mia, Leah, Zachary, Zoe  
✅ **Edge TTS** - High-quality neural voices  
✅ **Speech Recognition** - Browser-based voice input  
✅ **Auto-Chat Mode** - Continuous conversation  
✅ **Multi-User Support** - Share with friends  

### 🔧 Environment Variables

The app automatically uses:
- `PORT` - Set by Cloud Run
- `PYTHONUNBUFFERED=1` - For logging
- Built-in Gemini API key

### 📱 Share With Friends

Once deployed, anyone can access your Orpheus Voice Chat at the Cloud Run URL!

### 🐛 Troubleshooting

1. **Build Fails:** Check `gcloud builds log [BUILD_ID]`
2. **503 Errors:** App may be cold starting (first request takes ~30s)
3. **Audio Issues:** Browser needs HTTPS for microphone access (Cloud Run provides this)

### 📊 Monitoring

```bash
# View logs
gcloud logs read --limit=50 --format="table(timestamp,severity,textPayload)"

# Check status
gcloud run services describe orpheus-voice-chat --region=us-central1
```
