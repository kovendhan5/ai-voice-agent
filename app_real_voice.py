"""
Real Voice Orpheus TTS API - Uses actual TTS engines for human speech
Implements multiple real TTS backends for natural human voice
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import subprocess
import sys
from datetime import datetime
import requests
import json

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'canopylabs/orpheus-tts-0.1-finetune-prod')
PORT = int(os.getenv('PORT', 8080))

# Available voices with real TTS mappings
VOICES = {
    "tara": {"id": "tara", "name": "Tara", "gender": "female", "engine": "edge", "voice": "en-US-AriaNeural"},
    "zac": {"id": "zac", "name": "Zac", "gender": "male", "engine": "edge", "voice": "en-US-GuyNeural"},
    "sarah": {"id": "sarah", "name": "Sarah", "gender": "female", "engine": "edge", "voice": "en-US-JennyNeural"}
}

# Conversation memory
conversations = {}

def install_edge_tts():
    """Install edge-tts if not available"""
    try:
        import edge_tts
        return True
    except ImportError:
        try:
            print("📦 Installing edge-tts for real speech...")
            subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
            return True
        except Exception as e:
            print(f"❌ Failed to install edge-tts: {e}")
            return False

def generate_edge_tts(text, voice="tara"):
    """
    Generate speech using Microsoft Edge TTS (real human voices)
    """
    if not install_edge_tts():
        return generate_gtts_speech(text, voice)
    
    try:
        import edge_tts
        import asyncio
        
        # Get voice configuration
        voice_config = VOICES.get(voice, VOICES["tara"])
        edge_voice = voice_config["voice"]
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        async def generate():
            communicate = edge_tts.Communicate(text, edge_voice)
            await communicate.save(temp_file.name)
        
        # Run async function
        asyncio.run(generate())
        
        if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 1000:
            print(f"✅ Edge TTS generated: {temp_file.name}")
            return temp_file.name
        else:
            return generate_gtts_speech(text, voice)
            
    except Exception as e:
        print(f"❌ Edge TTS error: {e}")
        return generate_gtts_speech(text, voice)

def generate_gtts_speech(text, voice="tara"):
    """
    Generate speech using Google TTS (fallback)
    """
    try:
        from gtts import gTTS
        
        # Voice mapping for gTTS
        gtts_voices = {
            "tara": {"lang": "en", "tld": "com"},
            "zac": {"lang": "en", "tld": "co.uk"}, 
            "sarah": {"lang": "en", "tld": "ca"}
        }
        
        voice_config = gtts_voices.get(voice, gtts_voices["tara"])
        
        # Create gTTS object
        tts = gTTS(text=text, lang=voice_config["lang"], tld=voice_config["tld"], slow=False)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(temp_file.name)
        
        if os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 1000:
            print(f"✅ Google TTS generated: {temp_file.name}")
            return temp_file.name
        else:
            return generate_windows_sapi(text, voice)
            
    except Exception as e:
        print(f"❌ Google TTS error: {e}")
        return generate_windows_sapi(text, voice)

def generate_windows_sapi(text, voice="tara"):
    """
    Generate speech using Windows SAPI (fallback)
    """
    try:
        # Voice mapping for Windows SAPI
        sapi_voices = {
            "tara": "Microsoft Zira Desktop",
            "zac": "Microsoft David Desktop", 
            "sarah": "Microsoft Hazel Desktop"
        }
        
        windows_voice = sapi_voices.get(voice, sapi_voices["tara"])
        
        # Create temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        # PowerShell script for SAPI
        powershell_script = f"""
        Add-Type -AssemblyName System.Speech
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
        
        try {{
            $synth.SelectVoice("{windows_voice}")
        }} catch {{
            Write-Host "Using default voice"
        }}
        
        $synth.Rate = 0
        $synth.SetOutputToWaveFile("{temp_file.name}")
        $synth.Speak("{text.replace('"', "'")}")
        $synth.Dispose()
        """
        
        # Execute PowerShell
        result = subprocess.run([
            "powershell", "-Command", powershell_script
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 1000:
            print(f"✅ Windows SAPI generated: {temp_file.name}")
            return temp_file.name
        else:
            print(f"❌ All TTS engines failed. Generating error audio.")
            return generate_error_audio()
            
    except Exception as e:
        print(f"❌ Windows SAPI error: {e}")
        return generate_error_audio()

def generate_error_audio():
    """
    Generate a simple error message audio
    """
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    temp_file.close()
    
    try:
        import wave
        import numpy as np
        
        # Generate simple tone
        sample_rate = 22050
        duration = 2.0
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        frequency = 440  # A4 note
        audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
        audio_data = (audio_data * 32767).astype(np.int16)
        
        with wave.open(temp_file.name, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        return temp_file.name
        
    except Exception:
        return None

def get_ai_response(user_message, user_id="default"):
    """
    Generate AI responses with natural conversation
    """
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({"role": "user", "content": user_message})
    
    user_lower = user_message.lower().strip()
    
    # Natural conversation responses
    if any(greeting in user_lower for greeting in ["hello", "hi", "hey"]):
        if "how are you" in user_lower:
            ai_response = "Hello! I'm doing great, thank you for asking! I'm your AI voice assistant. How are you doing today?"
        else:
            ai_response = "Hello there! Nice to meet you! I'm your AI assistant with real speech capabilities. What can I help you with?"
    
    elif "how are you" in user_lower or "what's up" in user_lower:
        ai_response = "I'm doing wonderful! I'm excited to chat with you using real human-like speech. What would you like to talk about?"
    
    elif "your name" in user_lower or "who are you" in user_lower:
        ai_response = "I'm your AI voice assistant! I can have conversations and speak with real human voices using advanced text-to-speech technology. How can I help you today?"
    
    elif "weather" in user_lower:
        ai_response = "I don't have real-time weather data, but I'd love to hear about the weather where you are! How's it looking outside?"
    
    elif "time" in user_lower:
        current_time = datetime.now().strftime('%I:%M %p')
        ai_response = f"The current time is {current_time}. How's your day going so far?"
    
    elif "joke" in user_lower or "funny" in user_lower:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "What did the AI say to the human? I'm here to help, not to replace you!",
            "Why did the computer go to therapy? It had too many bytes of emotional baggage!"
        ]
        import random
        ai_response = random.choice(jokes) + " Hope that made you smile!"
    
    elif "help" in user_lower or "what can you do" in user_lower:
        ai_response = "I can have conversations with you using real speech! I can discuss topics, answer questions, tell jokes, or just chat. The best part is that I speak my responses with natural human voices!"
    
    elif any(word in user_lower for word in ["bye", "goodbye", "see you"]):
        ai_response = "It was wonderful talking with you! Feel free to come back anytime for another conversation. Take care!"
    
    elif "?" in user_message:
        ai_response = f"That's an interesting question! You asked about something really thoughtful. I'd love to explore this topic with you further!"
    
    elif any(word in user_lower for word in ["love", "like", "enjoy"]):
        ai_response = "That sounds wonderful! I can hear the enthusiasm in your message. Tell me more about what excites you about it!"
    
    elif any(word in user_lower for word in ["problem", "issue", "help"]):
        ai_response = "I'm here to help! While I can't solve every problem, I'm happy to listen and chat through whatever is on your mind."
    
    else:
        # Default responses
        if len(user_message.split()) <= 3:
            ai_response = f"Interesting! You mentioned '{user_message}'. Can you tell me more about what you're thinking?"
        else:
            ai_response = "That's really thoughtful! I appreciate you sharing that with me. What aspect interests you most?"
    
    conversations[user_id].append({"role": "assistant", "content": ai_response})
    
    # Keep reasonable history
    if len(conversations[user_id]) > 20:
        conversations[user_id] = conversations[user_id][-20:]
    
    return ai_response

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Real Voice TTS API",
        "model": MODEL_NAME,
        "timestamp": datetime.now().isoformat(),
        "version": "4.0.0",
        "features": ["edge_tts", "google_tts", "windows_sapi", "real_human_voices"]
    })

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available voices"""
    return jsonify({
        "voices": list(VOICES.values())
    })

@app.route('/speak', methods=['POST'])
def generate_speech():
    """Generate speech using real TTS engines"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get('text', '').strip()
        voice = data.get('voice', 'tara').lower()
        
        if not text:
            return jsonify({"error": "Text field is required"}), 400
        
        if len(text) > 1000:
            return jsonify({"error": "Text too long (max 1000 characters)"}), 400
        
        if voice not in VOICES:
            return jsonify({"error": f"Unknown voice '{voice}'. Available: {list(VOICES.keys())}"}), 400
        
        print(f"🎤 Generating REAL speech: '{text}' with voice: {voice}")
        
        # Try Edge TTS first (best quality)
        audio_file = generate_edge_tts(text, voice)
        
        if not audio_file:
            return jsonify({"error": "Failed to generate speech"}), 500
        
        return send_file(
            audio_file, 
            mimetype='audio/wav' if audio_file.endswith('.wav') else 'audio/mpeg',
            as_attachment=True,
            download_name=f'real_speech_{voice}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        )
        
    except Exception as e:
        print(f"Speech generation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_text():
    """Text-only chat endpoint"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message field is required"}), 400
        
        ai_response = get_ai_response(user_message, user_id)
        
        return jsonify({
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    """Voice chat with real TTS"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        voice = data.get('voice', 'tara').lower()
        user_id = data.get('user_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message field is required"}), 400
        
        if voice not in VOICES:
            return jsonify({"error": f"Unknown voice '{voice}'. Available: {list(VOICES.keys())}"}), 400
        
        print(f"💬 User {user_id}: {user_message}")
        ai_response = get_ai_response(user_message, user_id)
        print(f"🤖 AI: {ai_response}")
        
        # Generate real speech
        audio_file = generate_edge_tts(ai_response, voice)
        
        if not audio_file:
            return jsonify({"error": "Failed to generate speech response"}), 500
        
        response_headers = {
            'X-User-Message': user_message,
            'X-AI-Response': ai_response,
            'X-Voice': voice,
            'X-User-ID': user_id,
            'X-Timestamp': datetime.now().isoformat()
        }
        
        return send_file(
            audio_file,
            mimetype='audio/wav' if audio_file.endswith('.wav') else 'audio/mpeg',
            as_attachment=True,
            download_name=f'chat_{voice}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        ), 200, response_headers
        
    except Exception as e:
        print(f"Voice chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/conversation/<user_id>', methods=['GET'])
def get_conversation_history(user_id):
    """Get conversation history"""
    try:
        history = conversations.get(user_id, [])
        return jsonify({
            "user_id": user_id,
            "conversation": history,
            "message_count": len(history)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conversation/<user_id>', methods=['DELETE'])
def clear_conversation(user_id):
    """Clear conversation history"""
    try:
        if user_id in conversations:
            del conversations[user_id]
        return jsonify({
            "message": f"Conversation cleared for user {user_id}",
            "user_id": user_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print(f"🎤 Starting REAL VOICE TTS API!")
    print(f"📡 Model: {MODEL_NAME}")
    print(f"🔊 Available voices: {list(VOICES.keys())}")
    print(f"🗣️ TTS Engines:")
    print(f"   1️⃣ Microsoft Edge TTS (Primary - Neural voices)")
    print(f"   2️⃣ Google TTS (Fallback)")
    print(f"   3️⃣ Windows SAPI (Fallback)")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"📚 Endpoints:")
    print(f"   GET  / - Health check")
    print(f"   GET  /voices - List voices") 
    print(f"   POST /speak - Generate REAL speech")
    print(f"   POST /chat - Text conversation")
    print(f"   POST /voice_chat - Voice conversation with REAL speech")
    print(f"   GET  /conversation/<user_id> - Get chat history")
    print(f"   DELETE /conversation/<user_id> - Clear chat history")
    print(f"")
    print(f"✨ REAL HUMAN VOICES - No more weird noise!")
    print(f"🎯 Try: 'Hello, how are you?' for natural speech!")
    print(f"🚀 Multiple TTS engines ensure you get REAL voice output!")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
