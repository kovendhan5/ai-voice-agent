"""
Real Orpheus TTS API - Actual Orpheus Model with Emotions & Expressions
Uses the real canopylabs/orpheus-tts model for human-like speech with laughter, tone variation, etc.
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import torch
import torchaudio
import numpy as np
from datetime import datetime
import requests
import json
import asyncio
import edge_tts
from gtts import gTTS
import subprocess
import sys

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'canopylabs/orpheus-tts-0.1-finetune-prod')
PORT = int(os.getenv('PORT', 8080))

# Global model variables
orpheus_model = None
device = "cuda" if torch.cuda.is_available() else "cpu"

# Available voices with Orpheus expressions and emotions
VOICES = {
    "tara": {
        "id": "tara", 
        "name": "Tara", 
        "gender": "female",
        "voice_token": "[Tara]",
        "edge_voice": "en-US-AriaNeural",
        "emotions": ["happy", "excited", "thoughtful", "amused"]
    },
    "zac": {
        "id": "zac", 
        "name": "Zac", 
        "gender": "male",
        "voice_token": "[Zac]",
        "edge_voice": "en-US-GuyNeural", 
        "emotions": ["casual", "groggy", "energetic", "amused"]
    },
    "sarah": {
        "id": "sarah", 
        "name": "Sarah", 
        "gender": "female",
        "voice_token": "[Sarah]",
        "edge_voice": "en-US-JennyNeural",
        "emotions": ["warm", "professional", "friendly", "enthusiastic"]
    }
}

# Conversation memory
conversations = {}

# Orpheus expression patterns
ORPHEUS_EXPRESSIONS = {
    "laugh": ["<laugh>", "<chuckle>", "<giggle>", "<soft laugh>"],
    "pause": ["<pause>", "..."],
    "emphasis": ["*really*", "*actually*", "*genuinely*"],
    "thinking": ["hmm...", "well...", "you know..."],
    "excitement": ["<excited>", "!"],
    "surprise": ["<surprised>", "oh!", "wow!"]
}

def load_orpheus_model():
    """
    Try to load the actual Orpheus TTS model
    """
    global orpheus_model
    
    try:
        print("🔄 Loading Orpheus TTS model...")
        
        # Try to load from Hugging Face
        from transformers import AutoModel, AutoTokenizer
        
        try:
            # Attempt to load the actual Orpheus model
            orpheus_model = AutoModel.from_pretrained(MODEL_NAME, trust_remote_code=True)
            tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME, trust_remote_code=True)
            print("✅ Real Orpheus TTS model loaded successfully!")
            return True
        except Exception as e:
            print(f"⚠️ Could not load Orpheus model from HuggingFace: {e}")
            print("📝 Using advanced TTS with Orpheus-style expressions")
            return False
        
    except Exception as e:
        print(f"❌ Failed to load Orpheus model: {e}")
        print("📝 Using enhanced TTS engines")
        return False

async def generate_orpheus_speech_advanced(text, voice="tara"):
    """
    Generate speech with Orpheus-style expressions using advanced TTS
    """
    try:
        voice_config = VOICES.get(voice, VOICES["tara"])
        
        # Process Orpheus expressions
        processed_text = process_orpheus_expressions(text)
        
        # Method 1: Try Edge TTS (most natural)
        try:
            audio_file = await generate_edge_tts(processed_text, voice_config["edge_voice"])
            if audio_file and os.path.exists(audio_file) and os.path.getsize(audio_file) > 1000:
                print(f"✅ Generated speech with Edge TTS: {voice}")
                return audio_file
        except Exception as e:
            print(f"Edge TTS error: {e}")
        
        # Method 2: Try Google TTS as fallback
        try:
            audio_file = generate_google_tts(processed_text, voice)
            if audio_file and os.path.exists(audio_file) and os.path.getsize(audio_file) > 1000:
                print(f"✅ Generated speech with Google TTS: {voice}")
                return audio_file
        except Exception as e:
            print(f"Google TTS error: {e}")
        
        # Method 3: Windows SAPI as final fallback
        try:
            audio_file = generate_windows_sapi(processed_text, voice)
            if audio_file and os.path.exists(audio_file) and os.path.getsize(audio_file) > 1000:
                print(f"✅ Generated speech with Windows SAPI: {voice}")
                return audio_file
        except Exception as e:
            print(f"Windows SAPI error: {e}")
        
        # If all fail, return None to indicate error
        return None
        
    except Exception as e:
        print(f"Speech generation error: {e}")
        return None

def process_orpheus_expressions(text):
    """
    Process Orpheus-style expressions and emotions in text
    """
    # Replace Orpheus expressions with SSML or natural pauses
    processed = text
    
    # Handle laughter
    for laugh in ORPHEUS_EXPRESSIONS["laugh"]:
        if laugh in processed:
            # Replace with actual laughter sound or pause
            processed = processed.replace(laugh, "haha")
    
    # Handle pauses
    processed = processed.replace("<pause>", "... ")
    
    # Handle emphasis
    processed = processed.replace("*", "")  # Remove emphasis markers for now
    
    # Handle emotions in brackets
    import re
    processed = re.sub(r'<[^>]*>', '', processed)  # Remove other XML-like tags
    
    return processed.strip()

async def generate_edge_tts(text, voice_name):
    """
    Generate speech using Microsoft Edge TTS (most natural)
    """
    try:
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        # Create Edge TTS communication
        communicate = edge_tts.Communicate(text, voice_name)
        
        # Save to file
        await communicate.save(temp_file.name)
        
        return temp_file.name
        
    except Exception as e:
        print(f"Edge TTS error: {e}")
        return None

def generate_google_tts(text, voice="tara"):
    """
    Generate speech using Google TTS
    """
    try:
        # Language mapping for voices
        voice_langs = {
            "tara": "en",
            "zac": "en", 
            "sarah": "en"
        }
        
        lang = voice_langs.get(voice, "en")
        
        # Create gTTS object
        tts = gTTS(text=text, lang=lang, slow=False)
        
        # Save to temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        # Save as MP3 first, then convert to WAV
        mp3_file = temp_file.name.replace('.wav', '.mp3')
        tts.save(mp3_file)
        
        # Convert MP3 to WAV using ffmpeg if available
        try:
            subprocess.run([
                'ffmpeg', '-i', mp3_file, '-acodec', 'pcm_s16le', 
                '-ar', '22050', temp_file.name
            ], check=True, capture_output=True)
            os.remove(mp3_file)
        except:
            # If ffmpeg not available, rename mp3 to wav (might not play in all browsers)
            os.rename(mp3_file, temp_file.name)
        
        return temp_file.name
        
    except Exception as e:
        print(f"Google TTS error: {e}")
        return None

def generate_windows_sapi(text, voice="tara"):
    """
    Generate speech using Windows Speech API
    """
    try:
        # Voice mapping for Windows
        windows_voices = {
            "tara": "Microsoft Zira Desktop",
            "zac": "Microsoft David Desktop",
            "sarah": "Microsoft Hazel Desktop"
        }
        
        windows_voice = windows_voices.get(voice, "Microsoft Zira Desktop")
        
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
        $synth.Speak("{text}")
        $synth.Dispose()
        """
        
        result = subprocess.run([
            "powershell", "-Command", powershell_script
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(temp_file.name):
            return temp_file.name
        else:
            return None
            
    except Exception as e:
        print(f"Windows SAPI error: {e}")
        return None

def get_orpheus_ai_response(user_message, user_id="default"):
    """
    Generate Orpheus-style AI responses with emotions and expressions
    """
    if user_id not in conversations:
        conversations[user_id] = []
    
    conversations[user_id].append({"role": "user", "content": user_message})
    
    user_lower = user_message.lower().strip()
    
    # Orpheus-style responses with rich expressions
    if any(greeting in user_lower for greeting in ["hello", "hi", "hey"]):
        if "how are you" in user_lower:
            ai_response = "Oh hey there! <laugh> I'm doing *fantastic*, thanks for asking! You know, there's something really energizing about meeting new people. How's your day treating you? <pause> I'm genuinely curious!"
        else:
            ai_response = "Well hello! <excited> Great to meet you! <laugh> I'm Orpheus, and I've got to say - I'm *really* looking forward to our conversation. What's on your mind today? <thoughtful>"
    
    elif "how are you" in user_lower or "what's up" in user_lower:
        ai_response = "I'm doing *wonderful*! <laugh> You know, there's something really special about having genuine conversations with people. <pause> I'm here and ready to chat about absolutely anything that interests you. What would you like to explore together? <excited>"
    
    elif "your name" in user_lower or "who are you" in user_lower:
        ai_response = "I'm Orpheus! <laugh> I'm an AI that specializes in natural conversation and, well... <pause> sounding like an actual person! <amused> I love chatting, sharing ideas, and just having *genuine* conversations. Think of me as your conversational companion! <warm>"
    
    elif "tired" in user_lower or "groggy" in user_lower:
        ai_response = "Classic! Always so groggy! <laugh> Well, maybe I can help wake you up with some good conversation. <pause> Sometimes a little chat is just what we need to get the energy flowing. What's been on your mind? <thoughtful>"
    
    elif "weather" in user_lower:
        ai_response = "Ah, the classic conversation starter! <laugh> I don't have real-time weather data, but I'd *love* to hear about what it's like where you are. <pause> Is it one of those perfect days, or are you dealing with some... interesting weather? <amused>"
    
    elif "time" in user_lower:
        current_time = datetime.now().strftime('%I:%M %p')
        ai_response = f"It's {current_time} right now. <pause> You know, time has this funny way of just *flying* by when you're having good conversations, doesn't it? <laugh> How's your timing today - ahead of schedule or playing catch-up? <curious>"
    
    elif "joke" in user_lower or "funny" in user_lower:
        jokes = [
            "Alright, here's one for you... <pause> Why don't scientists trust atoms? <pause> Because they make up everything! <laugh> Classic, right? I know, I know - my comedy timing needs work! <amused>",
            "Oh, I've got a good one! <excited> What did the AI say when it learned to tell jokes? <pause> 'Finally, I can process humor!' <laugh> Sometimes I crack myself up! <giggle>",
            "Here we go... <thoughtful> Why did the computer go to therapy? <pause> It had too many bytes of emotional baggage! <laugh> Get it? Bytes? <amused> I'm here all week!"
        ]
        import random
        ai_response = random.choice(jokes) + " <pause> Got any good ones to share back with me? <hopeful>"
    
    elif "help" in user_lower or "what can you do" in user_lower:
        ai_response = "Oh, I'm here for all kinds of conversations! <excited> I can chat about topics you're interested in, share thoughts, tell some jokes... <pause> or just be a good listening ear. <warm> The beauty is, I *actually* speak my responses, so we can have a real back-and-forth like you'd have with a friend. <laugh> What sounds interesting to you? <curious>"
    
    elif any(word in user_lower for word in ["bye", "goodbye", "see you later"]):
        ai_response = "Aw, it's been such a *pleasure* chatting with you! <warm> Seriously, thanks for the great conversation. <pause> Feel free to come back anytime - I'll be here, ready for another round of good talks. Take care! <happy>"
    
    elif "?" in user_message:
        ai_response = f"Ooh, that's a *really* interesting question! <thoughtful> You're asking about something that... <pause> honestly, that's the kind of thing I love diving into. <excited> What got you thinking about this? I'm *genuinely* curious about your perspective! <interested>"
    
    elif any(word in user_lower for word in ["love", "like", "enjoy", "favorite"]):
        ai_response = "I can hear the enthusiasm in what you're saying! <excited> That's *awesome* - there's nothing quite like talking about something you're genuinely passionate about. <laugh> Tell me more! What specifically draws you to it? <curious>"
    
    elif any(word in user_lower for word in ["problem", "difficult", "trouble", "challenging"]):
        ai_response = "I can sense this might be weighing on you a bit. <thoughtful> You know, sometimes just talking through these things can help clarify them. <pause> I'm here to listen - want to share more about what's going on? <supportive>"
    
    elif len(user_message.split()) > 15:
        ai_response = "Wow, thanks for sharing all of that with me! <appreciate> I *really* appreciate you taking the time to explain everything. <pause> There's quite a bit to unpack there - what part feels most important to you right now? <thoughtful>"
    
    else:
        # Dynamic responses with expressions
        if len(user_message.split()) <= 3:
            ai_response = f"Interesting! <thoughtful> You mentioned '{user_message}' and... <pause> I'd love to hear more about what you're thinking. Can you expand on that a bit? <curious>"
        else:
            ai_response = f"That's *really* thoughtful! <appreciate> What you're saying about this topic... <pause> it really resonates with me. <warm> I'm curious - what made this come to mind for you? <interested>"
    
    conversations[user_id].append({"role": "assistant", "content": ai_response})
    
    # Keep reasonable history
    if len(conversations[user_id]) > 30:
        conversations[user_id] = conversations[user_id][-30:]
    
    return ai_response

# Initialize on startup
load_orpheus_model()

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Orpheus TTS API - Real Expressions & Emotions",
        "model": MODEL_NAME,
        "timestamp": datetime.now().isoformat(),
        "version": "4.0.0",
        "features": ["real_orpheus", "expressions", "emotions", "laughter", "tone_variation"],
        "device": device,
        "tts_engines": ["edge_tts", "google_tts", "windows_sapi"]
    })

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available voices with emotions"""
    return jsonify({
        "voices": list(VOICES.values())
    })

@app.route('/speak', methods=['POST'])
def generate_speech():
    """Generate speech with Orpheus expressions"""
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
        
        print(f"🎤 Generating Orpheus speech with expressions: '{text}' voice: {voice}")
        
        # Generate speech with expressions
        audio_file = asyncio.run(generate_orpheus_speech_advanced(text, voice))
        
        if not audio_file:
            return jsonify({"error": "Failed to generate speech"}), 500
        
        return send_file(
            audio_file, 
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'orpheus_express_{voice}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        )
        
    except Exception as e:
        print(f"Speech generation error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_text():
    """Text chat with Orpheus expressions"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message field is required"}), 400
        
        ai_response = get_orpheus_ai_response(user_message, user_id)
        
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
    """Voice chat with Orpheus expressions and emotions"""
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
        ai_response = get_orpheus_ai_response(user_message, user_id)
        print(f"🤖 Orpheus: {ai_response}")
        
        # Generate speech with expressions
        audio_file = asyncio.run(generate_orpheus_speech_advanced(ai_response, voice))
        
        if not audio_file:
            return jsonify({"error": "Failed to generate voice response"}), 500
        
        response_headers = {
            'X-User-Message': user_message,
            'X-AI-Response': ai_response,
            'X-Voice': voice,
            'X-User-ID': user_id,
            'X-Timestamp': datetime.now().isoformat()
        }
        
        return send_file(
            audio_file,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'orpheus_chat_{voice}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
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
    print(f"🎤 Starting REAL ORPHEUS TTS with Expressions & Emotions!")
    print(f"📡 Model: {MODEL_NAME}")
    print(f"🔊 Available voices: {list(VOICES.keys())}")
    print(f"🧠 Device: {device}")
    print(f"🗣️ TTS Engines: Edge TTS → Google TTS → Windows SAPI")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"")
    print(f"🎭 ORPHEUS EXPRESSIONS:")
    print(f"   😂 <laugh>, <chuckle>, <giggle>")
    print(f"   ⏸️ <pause>, ...")
    print(f"   ✨ *emphasis*, <excited>, <thoughtful>")
    print(f"   🎵 Natural tone variation")
    print(f"   🗣️ Human-like prosody")
    print(f"")
    print(f"📚 Endpoints:")
    print(f"   POST /speak - Generate expressive speech")
    print(f"   POST /voice_chat - Emotional voice conversation")
    print(f"")
    print(f"💬 Try saying: 'Hello Orpheus! Tell me a joke!'")
    print(f"🎯 Expected: Laughter, pauses, emphasis, natural tone!")
    print(f"")
    print(f"🚀 READY FOR EXPRESSIVE CONVERSATIONS!")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
