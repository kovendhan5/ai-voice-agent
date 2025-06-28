# Orpheus TTS API

A lightweight text-to-speech API using Orpheus-TTS, designed for deployment on GCP Cloud Run.

## Project Structure

```
voice-ai-orpheus/
│
├── app.py              # Flask API application
├── requirements.txt    # Python dependencies
├── Dockerfile         # Container configuration
├── .dockerignore      # Docker ignore patterns
└── README.md          # This file
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

## GCP Cloud Run Deployment

### Prerequisites

1. Install Google Cloud SDK
2. Set up a GCP project with billing enabled
3. Enable required APIs:
```bash
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable artifactregistry.googleapis.com
```

### Deployment Steps

1. **Set your project ID:**
```bash
export PROJECT_ID=your-project-id
gcloud config set project $PROJECT_ID
```

2. **Build and push the container:**
```bash
gcloud builds submit --tag gcr.io/$PROJECT_ID/orpheus-tts
```

3. **Deploy to Cloud Run:**
```bash
gcloud run deploy orpheus-tts \
  --image gcr.io/$PROJECT_ID/orpheus-tts \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 2Gi \
  --cpu 1 \
  --timeout 300 \
  --max-instances 10
```

4. **Get the service URL:**
```bash
gcloud run services describe orpheus-tts --region us-central1 --format 'value(status.url)'
```

### Testing the Deployed API

```bash
curl -X POST https://your-service-url.a.run.app/speak \
  -H "Content-Type: application/json" \
  -d '{"text": "tara: Hello from the cloud!"}' \
  --output cloud_speech.wav
```

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
