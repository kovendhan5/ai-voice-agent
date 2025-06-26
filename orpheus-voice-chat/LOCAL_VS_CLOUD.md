# 🎙️ Orpheus Voice Chat - Local vs Cloud Deployment

## 🏠 **LOCAL VERSION** (Your Development Server)
**URL:** http://127.0.0.1:5000/
- ✅ Running on your local machine
- ✅ Port 5000 (Flask development server)
- ✅ Direct file access and hot reloading
- ✅ Full debugging capabilities
- ⚠️ Only accessible from your computer

## ☁️ **CLOUD VERSION** (Production Deployment) 
**URL:** https://orpheus-voice-chat-1070324547772.us-central1.run.app/
- ✅ Same exact codebase as local
- ✅ Port 8080 (Cloud Run standard)
- ✅ Production-ready with Gunicorn
- ✅ Auto-scaling and load balancing
- ✅ Accessible from anywhere in the world
- ✅ HTTPS encryption
- ✅ Zero-cost tier compatible

## 🔄 **What's Identical Between Local & Cloud:**

### Features:
- ✅ All 8 AI personalities (Tara, Jessica, Leo, Daniel, Mia, Leah, Zachary, Zoe)
- ✅ Real-time voice conversation
- ✅ Speech-to-text input (browser-based)
- ✅ High-quality Edge TTS neural voices
- ✅ Auto-chat continuous mode
- ✅ Live conversation flow
- ✅ Interactive voice controls
- ✅ Natural dialogue patterns
- ✅ Emotion support in speech

### Technical:
- ✅ Same Python Flask app (`app_live_orpheus.py`)
- ✅ Same AI model (Google Gemini 1.5 Flash)
- ✅ Same speech synthesis (Microsoft Edge TTS)
- ✅ Same web interface and JavaScript
- ✅ Same conversation memory and personality system

## 🎯 **Key Differences:**

| Feature | Local (127.0.0.1:5000) | Cloud (Production) |
|---------|-------------------------|-------------------|
| **Access** | Your computer only | Global access |
| **Port** | 5000 | 8080 |
| **Server** | Flask dev server | Gunicorn (production) |
| **Scaling** | Single instance | Auto-scaling 0-10 |
| **SSL** | HTTP | HTTPS |
| **Reliability** | Depends on your PC | Google Cloud SLA |
| **Cost** | Free (uses your electricity) | Free (Google Cloud tier) |

## 🚀 **Usage:**

**For Development & Testing:**
```
http://127.0.0.1:5000/
```

**For Sharing & Production:**
```
https://orpheus-voice-chat-1070324547772.us-central1.run.app/
```

## 📱 **Share with Friends:**

Send your friends the **cloud URL** - they'll get the exact same experience as your local version, but accessible from anywhere!

Both versions provide the same amazing Orpheus voice chat experience! 🎭✨
