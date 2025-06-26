"""
Real AI Voice Chat with Gemini AI + Human-like TTS
Creates authentic voice conversations using your Gemini API key
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

# AI and TTS imports
import google.generativeai as genai
import pyttsx3

app = Flask(__name__)
CORS(app)

# Configure Gemini AI with your API key
GEMINI_API_KEY = "AIzaSyBu5izidIfzknhhMCzZB6yn1GKnzwZoUIQ"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# Real TTS Engine for Human-like Speech
class RealTTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self.setup_voices()
        print("🎤 Real TTS Engine initialized!")
    
    def setup_voices(self):
        """Configure voice personalities"""
        voices = self.engine.getProperty('voices')
        
        # Voice mapping for different personalities
        self.voice_config = {
            "tara": {"rate": 180, "volume": 0.9, "voice_id": 0},  # Natural female
            "jess": {"rate": 200, "volume": 0.95, "voice_id": 0}, # Bubbly female
            "mia": {"rate": 160, "volume": 0.8, "voice_id": 0},   # Soft female
            "leah": {"rate": 190, "volume": 0.9, "voice_id": 0},  # Dynamic female
            "zoe": {"rate": 210, "volume": 1.0, "voice_id": 0},   # Young female
            "zac": {"rate": 170, "volume": 0.9, "voice_id": 1 if len(voices) > 1 else 0},  # Male
            "leo": {"rate": 150, "volume": 0.85, "voice_id": 1 if len(voices) > 1 else 0}, # Deep male
            "dan": {"rate": 160, "volume": 0.9, "voice_id": 1 if len(voices) > 1 else 0},  # Professional male
        }
        
        print(f"📢 Found {len(voices)} system voices")
        for i, voice in enumerate(voices):
            print(f"   Voice {i}: {voice.name}")
    
    def generate_speech(self, text, voice="tara"):
        """Generate real human-like speech"""
        try:
            # Clean text for better speech
            clean_text = self.process_emotions(text)
            
            # Configure voice settings
            config = self.voice_config.get(voice, self.voice_config["tara"])
            
            # Set voice properties
            voices = self.engine.getProperty('voices')
            if voices and len(voices) > config["voice_id"]:
                self.engine.setProperty('voice', voices[config["voice_id"]].id)
            
            self.engine.setProperty('rate', config["rate"])
            self.engine.setProperty('volume', config["volume"])
            
            # Generate speech to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_path = temp_file.name
            
            self.engine.save_to_file(clean_text, temp_path)
            self.engine.runAndWait()
            
            # Read the generated audio file
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # Cleanup
            try:
                os.unlink(temp_path)
            except:
                pass
                
            print(f"🎤 Generated real speech: {len(audio_data)} bytes for voice '{voice}'")
            return audio_data
            
        except Exception as e:
            print(f"❌ TTS Error: {e}")
            # Fallback to simple beep if TTS fails
            return self.generate_fallback_beep(voice)
    
    def process_emotions(self, text):
        """Process emotion tags in text"""
        # Remove emotion tags and replace with pauses/emphasis
        emotion_map = {
            "<laugh>": "haha! ",
            "<chuckle>": "hehe, ",
            "<sigh>": "*sigh* ",
            "<gasp>": "oh! ",
            "<whisper>": "",
            "<excited>": "",
            "<calm>": "",
            "<happy>": "",
            "<sad>": ""
        }
        
        for emotion, replacement in emotion_map.items():
            text = text.replace(emotion, replacement)
        
        return text
    
    def generate_fallback_beep(self, voice):
        """Fallback beep if TTS fails"""
        sample_rate = 22050
        duration = 0.8
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        freq = 440  # A4
        audio_data = 0.3 * np.sin(2 * np.pi * freq * t)
        audio_int16 = (audio_data * 32767).astype(np.int16)
        
        # Create WAV file
        audio_buffer = io.BytesIO()
        with wave.open(audio_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())
        
        return audio_buffer.getvalue()

# Initialize TTS
tts_engine = RealTTS()

# AI Conversation Manager
class AIConversation:
    def __init__(self):
        self.conversation_history = []
        self.personality_prompts = {
            "tara": "You are Tara, a warm and natural AI assistant. Speak conversationally and add natural expressions like 'hmm', 'oh', and gentle laughter where appropriate.",
            "jess": "You are Jess, a friendly and bubbly AI assistant. Be enthusiastic and use expressions like <excited> and <chuckle> in your responses.",
            "mia": "You are Mia, a soft and gentle AI assistant. Speak calmly and thoughtfully, using <whisper> for emphasis and <sigh> occasionally.",
            "leah": "You are Leah, a dynamic and expressive AI assistant. Vary your tone and use emotions like <gasp> and <laugh> naturally.",
            "zoe": "You are Zoe, a young and energetic AI assistant. Be vibrant and use <excited> frequently with lots of enthusiasm!",
            "zac": "You are Zac, a clear and confident AI assistant. Speak with authority but remain friendly and approachable.",
            "leo": "You are Leo, a deep and authoritative AI assistant. Speak with wisdom and gravitas, occasionally using <calm> for emphasis.",
            "dan": "You are Dan, a mature and professional AI assistant. Be polished and articulate while remaining personable."
        }
    
    def generate_response(self, user_message, voice="tara"):
        """Generate AI response using Gemini"""
        try:
            # Get personality prompt
            personality = self.personality_prompts.get(voice, self.personality_prompts["tara"])
            
            # Create conversation context
            context = f"{personality}\n\nUser: {user_message}\n\nRespond naturally and conversationally:"
            
            # Generate response with Gemini
            response = model.generate_content(context)
            ai_text = response.text
            
            # Add to conversation history
            self.conversation_history.append({
                "user": user_message,
                "ai": ai_text,
                "voice": voice,
                "timestamp": datetime.now().isoformat()
            })
            
            # Keep only last 10 exchanges
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            print(f"🤖 AI Response ({voice}): {ai_text[:100]}...")
            return ai_text
            
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return f"I'm having trouble connecting right now, but I'm here to chat! Could you try asking me something else?"

# Initialize AI
ai_chat = AIConversation()

# Available voices with descriptions
VOICES = {
    "tara": "🎭 Natural and warm - Perfect for everyday conversations",
    "zac": "🎯 Clear and confident - Great for information and advice", 
    "jess": "✨ Friendly and bubbly - Enthusiastic and upbeat",
    "leo": "🎪 Deep and authoritative - Wise and thoughtful responses",
    "mia": "🌟 Soft and gentle - Calm and soothing conversations",
    "leah": "🎨 Dynamic and expressive - Varied emotional responses",
    "zoe": "🎵 Young and energetic - Vibrant and exciting chats",
    "dan": "🎬 Mature and professional - Polished and articulate"
}

def generate_speech(text, voice="tara"):
    """Generate real speech with AI-powered TTS"""
    return tts_engine.generate_speech(text, voice)

@app.route('/')
def index():
    """Serve the AI voice chat interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🤖 AI Voice Chat - Powered by Gemini</title>
        <style>
            body { 
                font-family: 'Segoe UI', Arial, sans-serif; 
                margin: 0;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); 
                color: white; 
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }
            .container { 
                max-width: 800px; 
                margin: 0 auto; 
                padding: 40px;
                background: rgba(255,255,255,0.1);
                border-radius: 20px;
                backdrop-filter: blur(10px);
                box-shadow: 0 8px 32px rgba(0,0,0,0.3);
            }
            .header {
                text-align: center;
                margin-bottom: 30px;
            }
            .status { 
                background: rgba(76, 175, 80, 0.2); 
                padding: 20px; 
                border-radius: 15px; 
                margin: 20px 0;
                border: 1px solid rgba(76, 175, 80, 0.5);
            }
            .chat-container {
                background: rgba(255,255,255,0.05);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                min-height: 200px;
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid rgba(255,255,255,0.1);
            }
            .message {
                margin: 10px 0;
                padding: 10px 15px;
                border-radius: 10px;
            }
            .user-message {
                background: rgba(103, 126, 234, 0.3);
                margin-left: 20px;
            }
            .ai-message {
                background: rgba(118, 75, 162, 0.3);
                margin-right: 20px;
            }
            .input-group {
                display: flex;
                gap: 10px;
                margin: 20px 0;
                align-items: center;
            }
            input[type="text"] { 
                flex: 1;
                padding: 15px; 
                border: none; 
                border-radius: 10px;
                background: rgba(255,255,255,0.1);
                color: white;
                font-size: 16px;
                backdrop-filter: blur(5px);
            }
            input[type="text"]::placeholder {
                color: rgba(255,255,255,0.7);
            }
            select {
                padding: 15px; 
                border: none; 
                border-radius: 10px;
                background: rgba(255,255,255,0.1);
                color: white;
                font-size: 16px;
                min-width: 200px;
            }
            option {
                background: #4a4a4a;
                color: white;
            }
            button { 
                padding: 15px 25px; 
                font-size: 16px; 
                border: none; 
                border-radius: 10px; 
                background: linear-gradient(45deg, #4CAF50, #45a049);
                color: white; 
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: bold;
            }
            button:hover { 
                transform: translateY(-2px);
                box-shadow: 0 5px 15px rgba(0,0,0,0.3);
            }
            .voice-info {
                font-size: 14px;
                color: rgba(255,255,255,0.8);
                margin-top: 5px;
            }
            .loading {
                display: none;
                text-align: center;
                color: #4CAF50;
                font-style: italic;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🤖 AI Voice Chat</h1>
                <h2>Powered by Gemini AI + Human-like Speech</h2>
            </div>
            
            <div class="status">
                <h3>✅ AI Voice System: LIVE</h3>
                <p>🧠 AI Brain: Google Gemini Pro</p>
                <p>🎤 Voice Engine: Real Human-like TTS</p>
                <p>💬 Features: Emotional expressions, personality voices</p>
                <p>🌟 Ready for natural conversations!</p>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="ai-message">
                    <strong>AI:</strong> Hello! I'm your AI voice assistant. Choose a voice personality and start chatting with me! I can speak with emotions and have real conversations. 😊
                </div>
            </div>
            
            <div class="input-group">
                <select id="voiceSelect" onchange="updateVoiceInfo()">
                    <option value="tara">🎭 Tara - Natural & Warm</option>
                    <option value="jess">✨ Jess - Friendly & Bubbly</option>
                    <option value="mia">🌟 Mia - Soft & Gentle</option>
                    <option value="leah">🎨 Leah - Dynamic & Expressive</option>
                    <option value="zoe">🎵 Zoe - Young & Energetic</option>
                    <option value="zac">🎯 Zac - Clear & Confident</option>
                    <option value="leo">🎪 Leo - Deep & Authoritative</option>
                    <option value="dan">🎬 Dan - Mature & Professional</option>
                </select>
                <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">💬 Send & Speak</button>
            </div>
            
            <div class="voice-info" id="voiceInfo">
                Perfect for everyday conversations with natural warmth
            </div>
            
            <div class="loading" id="loading">
                🤖 AI is thinking and preparing speech...
            </div>
            
            <div style="text-align: center; margin-top: 30px;">
                <p><strong>🎯 Try asking:</strong></p>
                <p>"Tell me a joke with some laughter" • "What's your favorite hobby?" • "Sing me a short song"</p>
            </div>
        </div>
        
        <script>
            const voices = {
                "tara": "Perfect for everyday conversations with natural warmth",
                "jess": "Enthusiastic and upbeat - great for fun chats",
                "mia": "Calm and soothing - ideal for relaxing conversations",
                "leah": "Varied emotional responses - dynamic personality",
                "zoe": "Vibrant and exciting - full of energy and life",
                "zac": "Great for information and advice with confidence",
                "leo": "Wise and thoughtful responses with authority",
                "dan": "Polished and articulate - professional conversations"
            };
            
            function updateVoiceInfo() {
                const voice = document.getElementById('voiceSelect').value;
                document.getElementById('voiceInfo').textContent = voices[voice];
            }
            
            function handleKeyPress(event) {
                if (event.key === 'Enter') {
                    sendMessage();
                }
            }
            
            async function sendMessage() {
                const messageInput = document.getElementById('messageInput');
                const message = messageInput.value.trim();
                const voice = document.getElementById('voiceSelect').value;
                
                if (!message) return;
                
                // Add user message to chat
                addMessage('user', message);
                messageInput.value = '';
                
                // Show loading
                document.getElementById('loading').style.display = 'block';
                
                try {
                    // Send to AI
                    const response = await fetch('/chat', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({message: message, voice: voice})
                    });
                    
                    const data = await response.json();
                    
                    // Add AI response to chat
                    addMessage('ai', data.response, voice);
                    
                    // Generate and play speech
                    const speechResponse = await fetch('/synthesize', {
                        method: 'POST',
                        headers: {'Content-Type': 'application/json'},
                        body: JSON.stringify({text: data.response, voice: voice})
                    });
                    
                    const audioBlob = await speechResponse.blob();
                    const audio = new Audio(URL.createObjectURL(audioBlob));
                    audio.play();
                    
                } catch (error) {
                    addMessage('ai', '❌ Sorry, I had trouble processing that. Please try again!');
                } finally {
                    document.getElementById('loading').style.display = 'none';
                }
            }
            
            function addMessage(sender, text, voice = '') {
                const container = document.getElementById('chatContainer');
                const messageDiv = document.createElement('div');
                messageDiv.className = `message ${sender}-message`;
                
                if (sender === 'user') {
                    messageDiv.innerHTML = `<strong>You:</strong> ${text}`;
                } else {
                    const voiceLabel = voice ? ` (${voice})` : '';
                    messageDiv.innerHTML = `<strong>AI${voiceLabel}:</strong> ${text}`;
                }
                
                container.appendChild(messageDiv);
                container.scrollTop = container.scrollHeight;
            }
            
            // Initialize
            updateVoiceInfo();
        </script>
    </body>
    </html>
    """

@app.route('/chat', methods=['POST'])
def chat():
    """Handle AI conversation with Gemini"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        voice = data.get('voice', 'tara')
        
        print(f"💬 User ({voice}): {user_message}")
        
        # Generate AI response
        ai_response = ai_chat.generate_response(user_message, voice)
        
        return jsonify({
            'response': ai_response,
            'voice': voice,
            'timestamp': datetime.now().isoformat(),
            'mode': 'gemini-ai'
        })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """Generate real speech from AI responses"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        voice = data.get('voice', 'tara')
        
        print(f"🎤 Generating speech for: '{text[:50]}...' with voice '{voice}'")
        
        # Generate real speech
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

@app.route('/voices', methods=['GET'])
def get_voices():
    """Get available voice personalities"""
    return jsonify({
        'voices': VOICES,
        'total_voices': len(VOICES),
        'model': 'real-tts-gemini'
    })

@app.route('/status', methods=['GET'])
def status():
    """Check system status"""
    return jsonify({
        'status': 'running',
        'ai_model': 'Google Gemini Pro',
        'tts_engine': 'Real Human-like TTS',
        'voices': len(VOICES),
        'mode': 'production',
        'features': ['emotional_expressions', 'personality_voices', 'real_conversations'],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🤖 AI VOICE CHAT - POWERED BY GEMINI AI")
    print("="*70)
    print("🧠 AI Brain: Google Gemini Pro")
    print("🎤 Voice Engine: Real Human-like TTS")
    print("🎭 Voice Personalities: 8 unique characters")
    print("😄 Features: Emotions, laughter, natural speech")
    print("💬 Mode: Real AI Conversations")
    print("🌐 Server: http://localhost:8080")
    print("="*70)
    print("🚀 Ready for natural AI voice conversations!")
    print("   Ask me anything - I'll respond with real human-like speech!")
    print("="*70)
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
