# ☁️ Cloud Deployment Guide

## Quick Deploy to Google Cloud (Free Tier)

### Prerequisites
1. **Google Account** with billing enabled (free tier available)
2. **Google Cloud SDK** installed locally

### Step 1: Install Google Cloud SDK
Download and install from: https://cloud.google.com/sdk/docs/install

### Step 2: Setup Project
```bash
# Login to your Google account
gcloud auth login

# Create a new project (or use existing)
gcloud projects create orpheus-voice-chat-123 --name="Orpheus Voice Chat"

# Set the project
gcloud config set project orpheus-voice-chat-123

# Enable billing (required for Cloud Run)
# Go to: https://console.cloud.google.com/billing
```

### Step 3: Enable Required APIs
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Step 4: Deploy (Automatic)
Run our deployment script:
```bash
scripts\deploy_to_cloud.bat
```

### Step 5: Manual Deployment (Alternative)
```bash
# Build the container
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/orpheus-tts

# Deploy to Cloud Run
gcloud run deploy orpheus-tts \
  --image gcr.io/YOUR-PROJECT-ID/orpheus-tts \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10
```

### Step 6: Get Your Live URL
```bash
gcloud run services describe orpheus-tts --region us-central1 --format 'value(status.url)'
```

## 💰 Cost Information

### Free Tier Limits (Monthly)
- **2 million requests** per month
- **180,000 vCPU-seconds** 
- **360,000 GiB-seconds** of memory
- **1 GiB** network egress from North America

### Estimated Usage
- **Voice generation**: ~1-2 seconds per request
- **Concurrent users**: Up to 10 (max-instances setting)
- **Storage**: Minimal (temporary files only)

Your app should easily stay within free tier limits for personal/friend usage!

## 🔗 Sharing with Friends

Once deployed, you'll get a URL like:
`https://orpheus-tts-abc123-uc.a.run.app`

Share this URL with friends - they can:
- Use the web interface directly
- Make API calls for voice generation
- Integrate into their own apps

## 🛡️ Security Notes

- Deployed with `--allow-unauthenticated` for easy sharing
- For production use, consider adding authentication
- Input validation is built-in
- No sensitive data stored

## 🔧 Troubleshooting

### Build Issues
```bash
# Check build logs
gcloud builds list --limit=5

# View detailed logs
gcloud builds log [BUILD-ID]
```

### Runtime Issues
```bash
# Check service logs
gcloud run logs read orpheus-tts --region=us-central1

# View service details
gcloud run services describe orpheus-tts --region=us-central1
```

### Memory Issues
If you get memory errors, increase memory allocation:
```bash
gcloud run services update orpheus-tts --memory 4Gi --region=us-central1
```

## 🎯 Next Steps

1. ✅ **Deploy to cloud** (you're here!)
2. 🧪 **Test with friends**
3. 🎨 **Customize the interface**
4. 🔊 **Upgrade to real Orpheus TTS** (if needed)
5. 🚀 **Scale up** (increase memory/instances if popular)

Your voice AI is now ready to share with the world! 🌍
