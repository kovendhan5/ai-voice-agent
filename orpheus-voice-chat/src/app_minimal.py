"""
Orpheus Voice Chat - Minimal Version
Works without Orpheus TTS installation for testing purposes
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import json
import os
import tempfile
import wave
import time
import io
import threading
from datetime import datetime
import numpy as np

app = Flask(__name__)
CORS(app)

# Simple mock TTS that always works
class SimpleMockTTS:
    def __init__(self):
        self.model_name = "simple-mock"
        print("🎭 Simple Mock TTS initialized (always works)")
    
    def generate_speech(self, text, voice="tara", **kwargs):
        """Generate SILENT mock audio - NO WEIRD NOISE"""
        print(f"🎭 Generating SILENT audio for: '{text[:50]}...' with voice '{voice}'")
        print("⚠️ MOCK MODE: Generating pure silence (no weird noise)")
        
        # Generate completely SILENT audio - NO NOISE
        sample_rate = 24000
        duration = max(1.0, len(text) * 0.05)  # 0.05 seconds per character
        
        # Create pure SILENCE - no sine wave, no noise
        audio_data = np.zeros(int(sample_rate * duration), dtype=np.float32)
        
        # Convert to 16-bit integers
        audio_int16 = (audio_data * 32767).astype(np.int16)
        audio_bytes = audio_int16.tobytes()
        
        print(f"📊 Generated {duration:.1f}s of test audio ({len(audio_bytes)} bytes)")
        return audio_bytes

# Initialize mock TTS
mock_tts = SimpleMockTTS()

# Available voices
VOICES = {
    "tara": "🎭 Natural and warm",
    "zac": "🎯 Clear and confident", 
    "jess": "✨ Friendly and bubbly",
    "leo": "🎪 Deep and authoritative",
    "mia": "🌟 Soft and gentle",
    "leah": "🎨 Dynamic and expressive",
    "zoe": "🎵 Young and energetic",
    "dan": "🎬 Mature and professional"
}

def generate_speech(text, voice="tara"):
    """Generate speech using mock TTS"""
    try:
        # Generate audio data
        audio_data = mock_tts.generate_speech(text, voice)
        
        # Create WAV file
        audio_buffer = io.BytesIO()
        with wave.open(audio_buffer, 'wb') as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(24000)  # 24kHz
            wf.writeframes(audio_data)
        
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
        
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        raise

# Simple response generator
def generate_response(text):
    """Generate simple AI responses"""
    responses = [
        f"That's interesting! You mentioned: {text[:30]}...",
        "I hear you! Thanks for sharing that with me.",
        "That's a great point! Tell me more about it.",
        "Fascinating! I'd love to learn more about your thoughts.",
        "You've given me something to think about!",
        "That's really insightful. What else is on your mind?"
    ]
    
    import random
    return random.choice(responses)

@app.route('/')
def index():
    """Serve a simple interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎭 Orpheus Voice Chat - Test Mode</title>
        <style>
            body { 
                font-family: Arial; 
                padding: 40px; 
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                text-align: center;
            }
            .container { max-width: 600px; margin: 0 auto; }
            button { 
                padding: 15px 30px; 
                font-size: 16px; 
                margin: 10px; 
                border: none; 
                border-radius: 8px; 
                background: #4CAF50; 
                color: white; 
                cursor: pointer;
            }
            button:hover { background: #45a049; }
            input { 
                padding: 10px; 
                width: 300px; 
                margin: 10px; 
                border: none; 
                border-radius: 5px;
            }
            select {
                padding: 10px; 
                margin: 10px; 
                border: none; 
                border-radius: 5px;
            }
            .status { 
                background: rgba(255,255,255,0.1); 
                padding: 20px; 
                border-radius: 10px; 
                margin: 20px 0;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Orpheus Voice Chat</h1>
            <h2>Test Mode - Mock Audio</h2>
            
            <div class="status">
                <h3>✅ Server Status: Running</h3>
                <p>🎭 TTS Engine: Mock (Test Tones)</p>
                <p>🌐 API: Fully Functional</p>
                <p>🎵 Audio: Simple test tones instead of speech</p>
            </div>
            
            <h3>🎤 Test Speech Synthesis</h3>
            <input type="text" id="textInput" placeholder="Enter text to synthesize..." value="Hello! This is a test.">
            <br>
            <select id="voiceSelect">
                <option value="tara">Tara - Natural</option>
                <option value="zac">Zac - Confident</option>
                <option value="jess">Jess - Friendly</option>
                <option value="leo">Leo - Authoritative</option>
            </select>
            <br>
            <button onclick="testSynthesis()">🎵 Generate Test Audio</button>
            
            <h3>💬 Test Chat</h3>
            <input type="text" id="chatInput" placeholder="Say something..." value="Hello, how are you?">
            <br>
            <button onclick="testChat()">💬 Send Message</button>
            
            <div id="response" style="margin-top: 20px;"></div>
            
            <h3>📋 Available Endpoints</h3>
            <ul style="text-align: left;">
                <li><strong>POST /synthesize</strong> - Generate speech</li>
                <li><strong>POST /chat</strong> - AI conversation</li>
                <li><strong>GET /voices</strong> - List voices</li>
                <li><strong>GET /status</strong> - Server status</li>
            </ul>
        </div>
        
        <script>
            function testSynthesis() {
                const text = document.getElementById('textInput').value;
                const voice = document.getElementById('voiceSelect').value;
                
                fetch('/synthesize', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({text: text, voice: voice})
                })
                .then(response => response.blob())
                .then(blob => {
                    const audio = new Audio(URL.createObjectURL(blob));
                    audio.play();
                    document.getElementById('response').innerHTML = 
                        `<p>✅ Generated test audio for: "${text}"</p>`;
                })
                .catch(error => {
                    document.getElementById('response').innerHTML = 
                        `<p>❌ Error: ${error}</p>`;
                });
            }
            
            function testChat() {
                const message = document.getElementById('chatInput').value;
                
                fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message: message, voice: 'tara'})
                })
                .then(response => response.json())
                .then(data => {
                    document.getElementById('response').innerHTML = 
                        `<p><strong>AI Response:</strong> ${data.response}</p>`;
                })
                .catch(error => {
                    document.getElementById('response').innerHTML = 
                        `<p>❌ Error: ${error}</p>`;
                });
            }
        </script>
    </body>
    </html>
    """

@app.route('/synthesize', methods=['POST'])
def synthesize():
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        voice = data.get('voice', 'tara')
        
        # Generate speech
        audio_data = generate_speech(text, voice)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(audio_data)
            temp_path = f.name
        
        def cleanup():
            try:
                os.unlink(temp_path)
            except:
                pass
        
        # Return audio file
        response = send_file(
            temp_path,
            mimetype='audio/wav',
            as_attachment=False
        )
        
        # Schedule cleanup
        threading.Timer(30.0, cleanup).start()
        
        return response
        
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        voice = data.get('voice', 'tara')
        
        # Generate AI response
        ai_response = generate_response(user_message)
        
        return jsonify({
            'response': ai_response,
            'voice': voice,
            'timestamp': datetime.now().isoformat(),
            'mode': 'mock'
        })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/voices', methods=['GET'])
def get_voices():
    return jsonify({
        'voices': VOICES,
        'total_voices': len(VOICES),
        'model': 'mock-tts'
    })

@app.route('/status', methods=['GET'])
def status():
    return jsonify({
        'status': 'running',
        'model': 'Mock TTS (Test Mode)',
        'voices': len(VOICES),
        'mode': 'testing',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎭 ORPHEUS VOICE CHAT - TEST MODE")
    print("="*60)
    print("🔥 Features:")
    print("   • Mock TTS with test tones")
    print("   • Full API functionality")
    print("   • No complex dependencies")
    print("   • Works on any system")
    print("\n🎯 Mode: Testing (Mock Audio)")
    print("🌐 Server: http://localhost:8080")
    print("="*60)
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
