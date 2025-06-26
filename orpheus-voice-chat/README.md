# Orpheus Voice Chat 🎭

A lightweight voice-interactive AI API using the Orpheus-TTS model that allows real-time AI conversations with human-like speech including laughter, emotions, and tone variations.

## ✅ Current Status
- 🎯 **Core System Working**: Clean test tones, no weird noise
- 🌐 **Cloud Ready**: Fully configured for Google Cloud deployment
- 🎭 **TTS Upgrade**: In progress - installing real Orpheus TTS
- 👥 **Multi-User**: Ready for sharing with friends

## Features

- 🎭 **Human-like Speech**: Powered by Orpheus-TTS with authentic emotions
- 🗣️ **8 Voice Personalities**: tara, zac, jess, leo, mia, leah, zoe, dan
- 😄 **Emotion Tags**: `<laugh>`, `<chuckle>`, `<sigh>`, `<gasp>`, etc.
- 💬 **Interactive Chat**: Real-time voice conversations
- 📱 **Modern UI**: Responsive glassmorphism design
- ☁️ **Cloud Ready**: Deployable on GCP Cloud Run (Free Tier)

## 🚀 Quick Start Options

### Option A: Test Tones (Working Now)
```bash
scripts\start_minimal.bat
```
- ✅ Clean test tones (no noise)
- ✅ Full API functionality
- ✅ Ready for friends to test

### Option B: Real Voice (Upgrading)
```bash
scripts\start.bat
```
- 🔄 Installing real Orpheus TTS
- 🎯 Human-like voice with emotions
- ⏳ May take time to download models

### Option C: Cloud Deployment
```bash
scripts\deploy_to_cloud.bat
```
- ☁️ Deploy to Google Cloud (free tier)
- 🌍 Share with friends worldwide
- 📱 Access from any device

## Project Structure

```
orpheus-voice-chat/
├── src/
│   ├── app.py                    # Main Flask server
│   └── voice_chat_interface.html # Web interface
├── scripts/
│   ├── start.bat                 # Server startup
│   └── restart.bat               # Server restart
├── tests/
│   └── test_api.py               # API tests
├── deploy/
│   ├── Dockerfile                # Container config
│   └── .dockerignore            # Docker ignore
├── docs/
│   └── SUCCESS_REPORT.md         # Implementation details
├── requirements.txt              # Python dependencies
├── .env.example                  # Environment template
└── README.md                     # This file
```

## API Endpoints

### POST /speak
Generate speech from text input.

**Request:**
```json
{
  "text": "tara: Hello, world!",
  "voice": "tara"  // optional, defaults to "tara"
}
```

**Response:** WAV audio file

### GET /
Health check endpoint.

### GET /voices
List available voices.

## Local Development

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Run the application:
```bash
python app.py
```

3. Test the API:
```bash
curl -X POST http://localhost:8080/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "tara: Hello from Orpheus!"}' \
  --output speech.wav
```

## ☁️ Cloud Deployment (Share with Friends!)

### Prerequisites
1. **Google Account** (free tier available)
2. **Google Cloud SDK**: https://cloud.google.com/sdk/docs/install

### Quick Deploy
```bash
# 1. Login and setup
gcloud auth login
gcloud config set project YOUR-PROJECT-ID

# 2. Run our deploy script
scripts\deploy_to_cloud.bat
```

### Manual Deploy
```bash
# Enable APIs
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

# Build and deploy
gcloud builds submit --tag gcr.io/YOUR-PROJECT-ID/orpheus-tts
gcloud run deploy orpheus-tts \
  --image gcr.io/YOUR-PROJECT-ID/orpheus-tts \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi
```

### 💰 Cost: FREE TIER
- **2M requests/month free**
- **Perfect for friend sharing**
- **Scales to zero when not used**

📚 **Detailed Guide**: `docs/CLOUD_DEPLOYMENT_GUIDE.md`

## Cost Optimization

- Cloud Run automatically scales to zero when not in use
- The free tier includes 2 million requests per month
- CPU is only allocated during request processing
- Memory allocation can be adjusted based on model requirements

## Environment Variables

You can configure the following environment variables:

- `PORT`: Server port (default: 8080)
- `MODEL_NAME`: Orpheus model to use (default: "canopylabs/orpheus-tts-0.1-finetune-prod")

## Security Notes

- The API is deployed with `--allow-unauthenticated` for demo purposes
- For production, consider adding authentication
- Input validation is implemented for text content
- Temporary files are automatically cleaned up

## Troubleshooting

- If the model fails to load, check the logs: `gcloud run logs read orpheus-tts --region us-central1`
- For memory issues, increase the memory allocation in the deployment command
- Cold starts may take longer due to model initialization
