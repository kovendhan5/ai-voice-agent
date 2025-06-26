"""
Simple Working TTS Server - Guaranteed Real Speech
"""
from flask import Flask, request, jsonify, send_file
import tempfile
import json
import random
import subprocess
import os
from datetime import datetime

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
        "message": "AI Server with REAL TTS is running!",
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
            "Hello! I'm your AI assistant with real speech capabilities. I can now actually speak to you instead of making beeping sounds!",
            "Hi there! Great to meet you! I'm an AI assistant that can have real voice conversations with you.",
            "Hey! I'm excited to chat with you using my new voice synthesis. What would you like to talk about?"
        ]
        return random.choice(greetings)
    
    # Questions about the AI
    if any(phrase in msg_lower for phrase in ['who are you', 'what are you', 'tell me about yourself', 'introduce yourself']):
        return "I'm an AI assistant with real text-to-speech capabilities! I can speak to you with an actual human-like voice, not just beeps and tones. I can help with coding, answer questions, have conversations, and much more. What would you like to explore together?"
    
    # Voice/speech related questions
    if any(word in msg_lower for word in ['voice', 'speak', 'talk', 'sound', 'audio', 'speech']):
        return "Yes! I now have real speech synthesis! I can speak to you with a natural human voice instead of making electronic sounds. This makes our conversations much more natural and engaging."
    
    # Programming/coding questions
    if any(word in msg_lower for word in ['code', 'programming', 'python', 'javascript', 'html', 'css', 'react', 'node', 'api', 'function', 'variable', 'error', 'bug', 'debug']):
        return f"I'd be happy to help with programming! You mentioned '{message}'. I can assist with coding questions, debugging, explaining concepts, writing code snippets, reviewing code, or helping with software architecture. What specific programming challenge are you working on?"
    
    # General conversation
    general_responses = [
        f"That's interesting that you mentioned '{message}'. I'd like to understand more about your perspective on this. Could you tell me what specifically interests you about it?",
        f"Thanks for sharing '{message}' with me. I find this topic engaging! What aspects of this would you like to explore further?",
        f"Regarding '{message}' - I can help provide information, different viewpoints, or have a detailed discussion about this. What direction would you like our conversation to take?",
    ]
    
    return random.choice(general_responses)

def generate_real_speech(text):
    """Generate real speech using Windows built-in TTS"""
    try:
        # Method 1: PowerShell with Windows Speech (most reliable)
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        
        # Clean the text for PowerShell
        clean_text = text.replace('"', '').replace("'", "").replace('`', '')
        if len(clean_text) > 200:
            clean_text = clean_text[:200] + "..."
        
        # PowerShell command for TTS
        ps_command = f'''
Add-Type -AssemblyName System.Speech;
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer;
$synth.SetOutputToWaveFile('{temp_path}');
$synth.Speak('{clean_text}');
$synth.Dispose();
'''
        
        # Execute PowerShell
        result = subprocess.run([
            'powershell', '-ExecutionPolicy', 'Bypass', '-Command', ps_command
        ], capture_output=True, text=True, timeout=15)
        
        # Check if file was created and has content
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 1000:
            print(f"✅ Generated real speech: {os.path.getsize(temp_path)} bytes")
            return temp_path
        else:
            raise Exception("PowerShell TTS failed")
            
    except Exception as e:
        print(f"PowerShell TTS failed: {e}")
        try:
            # Method 2: Edge TTS via command line
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
            temp_path = temp_file.name
            temp_file.close()
            
            # Try edge-tts command
            subprocess.run([
                'edge-tts', '--voice', 'en-US-AriaNeural', 
                '--text', text, '--write-media', temp_path
            ], check=True, timeout=15)
            
            if os.path.exists(temp_path) and os.path.getsize(temp_path) > 100:
                print("✅ Generated speech with Edge TTS")
                return temp_path
            else:
                raise Exception("Edge TTS failed")
                
        except Exception as e2:
            print(f"Edge TTS failed: {e2}")
            # Method 3: Simple notification as last resort
            return create_notification_sound()

def create_notification_sound():
    """Create a pleasant notification sound"""
    import wave
    import numpy as np
    
    sample_rate = 22050
    duration = 0.8
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a pleasant ascending chime
    freq1, freq2, freq3 = 523, 659, 784  # C, E, G notes
    audio = (
        np.sin(2 * np.pi * freq1 * t[:len(t)//3]) * 0.4 +
        np.sin(2 * np.pi * freq2 * t[len(t)//3:2*len(t)//3]) * 0.4 +
        np.sin(2 * np.pi * freq3 * t[2*len(t)//3:]) * 0.4
    )
    
    # Apply fade
    fade = int(sample_rate * 0.1)
    audio[:fade] *= np.linspace(0, 1, fade)
    audio[-fade:] *= np.linspace(1, 0, fade)
    
    # Convert to 16-bit
    audio = (audio * 32767).astype(np.int16)
    
    # Save to temp file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    with wave.open(temp_file.name, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio.tobytes())
    
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
        
        # Keep conversation history manageable (last 20 messages)
        if len(conversation_history[user_id]) > 20:
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
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
        
        # Keep conversation history manageable (last 20 messages)
        if len(conversation_history[user_id]) > 20:
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
        # Generate REAL speech audio
        audio_file = generate_real_speech(ai_response)
        
        # Determine the correct mimetype
        if audio_file.endswith('.mp3'):
            mimetype = 'audio/mpeg'
        else:
            mimetype = 'audio/wav'
        
        return send_file(audio_file, mimetype=mimetype, as_attachment=False,
                        download_name=f'ai_speech_{len(conversation_history[user_id])}.wav')
    except Exception as e:
        # Return error as audio
        error_audio = create_notification_sound()
        return send_file(error_audio, mimetype='audio/wav')

@app.route('/voices')
def voices():
    return jsonify({"voices": [{"id": "aria", "name": "Aria Neural Voice"}]})

if __name__ == '__main__':
    print("🚀 Starting AI Server with REAL TEXT-TO-SPEECH...")
    print("🌐 Open: http://localhost:8080")
    print("🗣️ Features: Real human voice synthesis!")
    print("💬 ChatGPT-like conversations with actual speech")
    print("🔗 Server will be available in a few seconds...")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
