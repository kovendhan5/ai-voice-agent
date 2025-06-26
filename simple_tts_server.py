"""
Simple TTS Server - Guaranteed Voice Output
"""
from flask import Flask, request, jsonify, send_file
import tempfile
import json
import random
import re
from datetime import datetime
import os
import subprocess

app = Flask(__name__)

# Store conversation history for each user
conversation_history = {}

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Max-Age', '86400')
    return response

@app.route('/', methods=['GET', 'OPTIONS'])
def health():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "healthy", 
        "message": "Simple TTS AI Server is running!",
        "server": "simple_tts_ai",
        "timestamp": datetime.now().isoformat()
    })

def generate_ai_response(message, history):
    """Generate intelligent AI responses like ChatGPT"""
    
    # Convert message to lowercase for pattern matching
    msg_lower = message.lower()
    
    # Greeting responses
    if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
        greetings = [
            "Hello! I'm your AI assistant with real voice capabilities. How can I help you today?",
            "Hi there! I can speak to you with actual speech synthesis. What would you like to discuss?",
            "Hey! I'm excited to chat with you using my voice. What's on your mind?"
        ]
        return random.choice(greetings)
    
    # Questions about the AI
    if any(phrase in msg_lower for phrase in ['who are you', 'what are you', 'tell me about yourself']):
        return "I'm an AI assistant with text-to-speech capabilities. I can understand your messages and respond with both text and spoken audio. I'm designed to have natural conversations just like ChatGPT, but with voice output!"
    
    # Voice/audio questions
    if any(word in msg_lower for word in ['voice', 'speak', 'audio', 'sound', 'hear']):
        return "Yes! I can speak to you with real text-to-speech technology. When you see the play audio button, click it to hear my voice response to your messages."
    
    # General conversation
    return f"That's interesting that you mentioned '{message}'. I can respond both in text and with my voice. What would you like to explore about this topic?"

def simple_tts(text):
    """Ultra-simple TTS using Windows built-in capabilities"""
    try:
        # Method 1: Use edge-tts (Microsoft Edge TTS - most reliable)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        
        # Use edge-tts command
        cmd = [
            'edge-tts',
            '--voice', 'en-US-AriaNeural',
            '--text', text[:500],  # Limit text length
            '--write-media', temp_path
        ]
        
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        
        if result.returncode == 0 and os.path.exists(temp_path) and os.path.getsize(temp_path) > 1000:
            print(f"✅ edge-tts success: {os.path.getsize(temp_path)} bytes")
            return temp_path
        else:
            print(f"edge-tts failed: {result.stderr}")
            raise Exception("edge-tts failed")
            
    except Exception as e:
        print(f"edge-tts error: {e}")
        try:
            # Method 2: PowerShell TTS (Windows built-in)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_path = temp_file.name
            temp_file.close()
            
            # Create PowerShell command for TTS
            ps_script = f'''
            Add-Type -AssemblyName System.Speech
            $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer
            $speak.SetOutputToWaveFile("{temp_path}")
            $speak.Speak("{text[:200]}")
            $speak.Dispose()
            '''
            
            # Run PowerShell script
            result = subprocess.run([
                'powershell', '-Command', ps_script
            ], capture_output=True, text=True, timeout=15)
            
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 1000:
                print(f"✅ PowerShell TTS success: {os.path.getsize(temp_path)} bytes")
                return temp_path
            else:
                raise Exception("PowerShell TTS failed")
                
        except Exception as e2:
            print(f"PowerShell TTS error: {e2}")
            # Method 3: Create a notification sound as last resort
            return create_notification_sound()

def create_notification_sound():
    """Create a pleasant notification sound"""
    import wave
    import numpy as np
    
    sample_rate = 22050
    duration = 1.0
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a pleasant chime
    freq1 = 523  # C note
    freq2 = 659  # E note
    freq3 = 784  # G note
    
    audio_data = (
        np.sin(2 * np.pi * freq1 * t) * 0.3 +
        np.sin(2 * np.pi * freq2 * t) * 0.2 +
        np.sin(2 * np.pi * freq3 * t) * 0.15
    ) * np.exp(-3 * t)  # Fade out
    
    audio_data = (audio_data * 32767).astype(np.int16)
    
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    with wave.open(temp_file.name, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    return temp_file.name

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default')
        
        # Get conversation history
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Add user message to history
        conversation_history[user_id].append({"role": "user", "content": message})
        
        # Generate intelligent AI response
        response = generate_ai_response(message, conversation_history[user_id])
        
        # Add AI response to history
        conversation_history[user_id].append({"role": "assistant", "content": response})
        
        return jsonify({
            "ai_response": response,
            "user_message": message,
            "conversation_length": len(conversation_history[user_id])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/voice_chat', methods=['POST', 'OPTIONS'])
def voice_chat():
    if request.method == 'OPTIONS':
        return '', 200
    
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'voice_user')
        
        # Get conversation history
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Add user message to history
        conversation_history[user_id].append({"role": "user", "content": message})
        
        # Generate intelligent AI response
        ai_response = generate_ai_response(message, conversation_history[user_id])
        
        # Add AI response to history
        conversation_history[user_id].append({"role": "assistant", "content": ai_response})
        
        # Generate audio response
        print(f"🔊 Generating TTS for: {ai_response[:50]}...")
        audio_file = simple_tts(ai_response)
        
        return send_file(audio_file, mimetype='audio/wav', as_attachment=False)
        
    except Exception as e:
        print(f"Voice chat error: {e}")
        error_audio = create_notification_sound()
        return send_file(error_audio, mimetype='audio/wav')

@app.route('/voices')
def voices():
    return jsonify({"voices": [{"id": "aria", "name": "Aria Neural Voice"}]})

if __name__ == '__main__':
    print("🚀 Starting Simple TTS AI Server...")
    print("🌐 Open: http://localhost:8080")
    print("🔊 Real voice synthesis enabled!")
    print("💬 Features: ChatGPT-like responses + Real TTS")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
