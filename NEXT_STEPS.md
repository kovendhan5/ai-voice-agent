# 🚀 Orpheus TTS API - Next Steps Guide

## ✅ Current Status
Your Orpheus TTS API is ready for testing and deployment! All files have been created and dependencies are installed.

## 📋 Project Structure
```
voice-ai-orpheus/
├── 🐍 app.py              # Main Flask API
├── 🧪 orpheus_tts.py      # Mock TTS implementation  
├── 📦 requirements.txt    # Dependencies
├── 🐳 Dockerfile         # Container config
├── 🚀 start_server.bat   # Start server (Windows)
├── 🧪 test_client.py     # API test client
├── 🧪 test_setup.py      # Setup verification
├── ☁️ deploy.bat         # GCP deployment (Windows)
├── ☁️ deploy.sh          # GCP deployment (Unix/Linux)
└── 📚 README.md          # Full documentation
```

## 🧪 Step 1: Local Testing

### Start the Server
```cmd
cd "k:\full stack\AI\voice model\voice-ai-orpheus"
start_server.bat
```
**OR**
```cmd
python app.py
```

The server will start on `http://localhost:8080`

### Test the API (New Terminal Window)
```cmd
cd "k:\full stack\AI\voice model\voice-ai-orpheus"
python test_client.py
```

### Manual Testing with curl
```cmd
# Health check
curl http://localhost:8080/

# List voices
curl http://localhost:8080/voices

# Generate speech
curl -X POST http://localhost:8080/speak ^
  -H "Content-Type: application/json" ^
  -d "{\"text\": \"tara: Hello from Orpheus!\"}" ^
  --output speech.wav
```

## ☁️ Step 2: Deploy to GCP Cloud Run

### Prerequisites
1. Install Google Cloud SDK: https://cloud.google.com/sdk/docs/install
2. Create a GCP project with billing enabled
3. Authenticate: `gcloud auth login`

### Quick Deployment
```cmd
# Set your project ID
set PROJECT_ID=your-project-id

# Deploy (this will enable APIs, build, and deploy)
deploy.bat %PROJECT_ID%
```

### Manual Deployment Steps
```cmd
# Set project
gcloud config set project YOUR_PROJECT_ID

# Enable APIs
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com

# Build container
gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/orpheus-tts

# Deploy to Cloud Run
gcloud run deploy orpheus-tts ^
  --image gcr.io/YOUR_PROJECT_ID/orpheus-tts ^
  --platform managed ^
  --region us-central1 ^
  --allow-unauthenticated ^
  --memory 2Gi ^
  --cpu 1
```

## 🔄 Step 3: Replace Mock with Real Orpheus

Once the real `orpheus-speech` package is available:

1. Update `requirements.txt`:
```
flask==3.0.0
orpheus-speech  # Real package
gunicorn==21.2.0
# ... other dependencies
```

2. Remove `orpheus_tts.py` (our mock)
3. Update imports in `app.py` to use real package
4. Redeploy

## 💡 Tips & Troubleshooting

### Local Development
- Virtual environment is already set up in `venv/`
- Use `venv\Scripts\activate` to activate it
- All dependencies are installed

### API Usage
- Default voice is "tara"
- Text format: "speaker: message"
- Returns WAV audio files
- Supports multiple voices (see `/voices` endpoint)

### Cloud Run Benefits
- ✅ Scales to zero (no cost when idle)
- ✅ 2M free requests/month
- ✅ Pay only for compute time used
- ✅ Automatic HTTPS
- ✅ Global load balancing

### Cost Optimization
- Single worker configuration
- Efficient Docker layers
- Automatic scaling
- Request-based billing

## 🎯 Next Actions

1. **Test Locally**: Run `start_server.bat` then `python test_client.py`
2. **Deploy to Cloud**: Run `deploy.bat YOUR_PROJECT_ID`
3. **Test Cloud API**: Use the provided curl commands with your Cloud Run URL
4. **Replace Mock**: When real Orpheus package is available

## 📞 Support
- Check logs: `gcloud run logs read orpheus-tts --region us-central1`
- Monitor usage: GCP Console > Cloud Run > orpheus-tts
- Debug locally: Check `app.py` logs
