"""
Real Orpheus-TTS Voice Chat API
Windows-compatible implementation using the actual Orpheus model
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import google.generativeai as genai
import asyncio
import time
import os
import logging
import json
from datetime import datetime
import threading
import queue

# Import our Windows-compatible Orpheus implementation
from orpheus_windows_compatible import OrpheusWindowsModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
GEMINI_API_KEY = "AIzaSyBu5izidIfzknhhMCzZB6yn1GKnzwZoUIQ"
genai.configure(api_key=GEMINI_API_KEY)

class RealOrpheusVoiceChat:
    def __init__(self):
        self.conversations = {}
        self.orpheus_model = None
        self.model_loading = False
        self.model_ready = False
        
        # Initialize Gemini AI
        self.ai_model = genai.GenerativeModel('gemini-pro')
        
        # Voice personalities with Orpheus-compatible names
        self.voice_personalities = {
            "tara": {
                "name": "Tara",
                "personality": "Warm, friendly, and naturally expressive. Speaks with gentle enthusiasm and authentic emotions.",
                "style": "conversational, empathetic, uses natural speech patterns with laughter and sighs"
            },
            "jess": {
                "name": "Jessica", 
                "personality": "Bubbly, energetic, and optimistic. Loves to laugh and express joy in conversation.",
                "style": "animated, expressive, frequent laughter and excited tones"
            },
            "leo": {
                "name": "Leo",
                "personality": "Thoughtful, articulate, and calm. Speaks with measured confidence and occasional humor.",
                "style": "clear, professional yet warm, thoughtful pauses"
            },
            "dan": {
                "name": "Daniel",
                "personality": "Casual, friendly guy-next-door type. Easy-going with natural masculine warmth.",
                "style": "relaxed, conversational, natural speech rhythm"
            },
            "mia": {
                "name": "Mia",
                "personality": "Creative, artistic, and expressive. Speaks with passion about interesting topics.",
                "style": "expressive, varied intonation, creative speech patterns"
            },
            "leah": {
                "name": "Leah",
                "personality": "Gentle, caring, and nurturing. Speaks with maternal warmth and understanding.",
                "style": "soft, comforting, empathetic tones"
            },
            "zac": {
                "name": "Zachary",
                "personality": "Young, energetic, and tech-savvy. Speaks with modern enthusiasm.",
                "style": "upbeat, contemporary, energetic delivery"
            },
            "zoe": {
                "name": "Zoe",
                "personality": "Sophisticated, intelligent, and witty. Enjoys clever conversation and humor.",
                "style": "articulate, witty, intelligent humor"
            }
        }
        
        # Start loading Orpheus model in background
        self._start_model_loading()
    
    def _start_model_loading(self):
        """Load Orpheus model in background thread"""
        def load_model():
            try:
                logger.info("🔄 Loading Orpheus TTS model...")
                self.model_loading = True
                self.orpheus_model = OrpheusWindowsModel()
                self.model_ready = True
                self.model_loading = False
                logger.info("✅ Orpheus TTS model loaded successfully!")
            except Exception as e:
                logger.error(f"❌ Failed to load Orpheus model: {e}")
                self.model_loading = False
                self.model_ready = False
        
        thread = threading.Thread(target=load_model, daemon=True)
        thread.start()
    
    def get_ai_response(self, user_input, voice="tara", conversation_id="default"):
        """Generate AI response with personality"""
        try:
            # Get or create conversation history
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            
            history = self.conversations[conversation_id]
            personality = self.voice_personalities.get(voice, self.voice_personalities["tara"])
            
            # Create context-aware prompt
            personality_prompt = f"""You are {personality['name']}, a voice AI with this personality: {personality['personality']}
            
Speaking style: {personality['style']}

Important: You can use these emotion tags in your speech:
<laugh> - for laughter
<chuckle> - for light laughter  
<sigh> - for sighs
<gasp> - for surprise
<yawn> - for tiredness
<cough> - for coughs
<sniffle> - for sniffles
<groan> - for frustration

Use these emotion tags naturally in your responses to make speech more human-like.

Conversation history:
{json.dumps(history[-6:], indent=2) if history else "No previous conversation"}

User says: {user_input}

Respond as {personality['name']} with your unique personality and speaking style. Keep responses conversational and natural, around 1-3 sentences. Use emotion tags when appropriate."""

            # Generate response
            response = self.ai_model.generate_content(personality_prompt)
            ai_text = response.text.strip()
            
            # Store conversation
            history.append({"user": user_input, "ai": ai_text, "timestamp": datetime.now().isoformat()})
            self.conversations[conversation_id] = history[-20:]  # Keep last 20 exchanges
            
            return ai_text
            
        except Exception as e:
            logger.error(f"Error generating AI response: {e}")
            return f"<sigh> Sorry, I'm having trouble thinking right now. {str(e)}"
    
    def generate_speech_orpheus(self, text, voice="tara"):
        """Generate speech using real Orpheus TTS"""
        if not self.model_ready:
            if self.model_loading:
                return None, "Model is still loading, please wait..."
            else:
                return None, "Orpheus model failed to load"
        
        try:
            logger.info(f"🎙️ Generating Orpheus speech: {text[:50]}...")
            
            # Generate audio using Orpheus
            audio_data = self.orpheus_model.generate_speech(
                prompt=text,
                voice=voice,
                temperature=0.8
            )
            
            # Convert to bytes for web delivery
            audio_bytes = self.orpheus_model.get_audio_bytes(audio_data)
            
            logger.info(f"✅ Generated {len(audio_bytes)} bytes of Orpheus audio")
            return audio_bytes, None
            
        except Exception as e:
            logger.error(f"❌ Orpheus speech generation error: {e}")
            return None, f"Speech generation failed: {str(e)}"

# Create global chat instance
chat_system = RealOrpheusVoiceChat()

@app.route('/')
def home():
    """Serve the voice chat interface"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎤 Real Orpheus Voice Chat</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            color: white;
        }
        .header {
            text-align: center;
            padding: 20px;
            background: rgba(0,0,0,0.2);
            backdrop-filter: blur(10px);
        }
        .container {
            flex: 1;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .status {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .voice-selector {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 10px;
            margin: 20px 0;
        }
        .voice-btn {
            background: rgba(255,255,255,0.2);
            border: 2px solid transparent;
            border-radius: 10px;
            padding: 15px 10px;
            color: white;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
        }
        .voice-btn:hover { background: rgba(255,255,255,0.3); }
        .voice-btn.active {
            background: rgba(255,255,255,0.4);
            border-color: #ffff00;
            box-shadow: 0 0 20px rgba(255,255,0,0.3);
        }
        .chat-area {
            background: rgba(255,255,255,0.1);
            border-radius: 15px;
            padding: 20px;
            backdrop-filter: blur(10px);
            flex: 1;
            min-height: 300px;
            overflow-y: auto;
        }
        .message {
            margin: 10px 0;
            padding: 10px 15px;
            border-radius: 20px;
            max-width: 80%;
        }
        .user-message {
            background: rgba(100,200,255,0.3);
            margin-left: auto;
            text-align: right;
        }
        .ai-message {
            background: rgba(255,255,255,0.2);
        }
        .input-area {
            display: flex;
            gap: 10px;
            align-items: center;
        }
        .text-input {
            flex: 1;
            padding: 15px;
            border-radius: 25px;
            border: none;
            background: rgba(255,255,255,0.2);
            color: white;
            font-size: 16px;
        }
        .text-input::placeholder { color: rgba(255,255,255,0.7); }
        .send-btn, .voice-btn-main {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border: none;
            border-radius: 50%;
            width: 60px;
            height: 60px;
            color: white;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .send-btn:hover, .voice-btn-main:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(255,107,107,0.5);
        }
        .audio-player {
            margin: 10px 0;
            width: 100%;
        }
        .loading {
            opacity: 0.7;
            pointer-events: none;
        }
        .model-status {
            position: fixed;
            top: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 15px;
            border-radius: 25px;
            font-size: 14px;
        }
        .status-loading { color: #ffa500; }
        .status-ready { color: #00ff00; }
        .status-error { color: #ff4444; }
    </style>
</head>
<body>
    <div class="model-status" id="modelStatus">
        <span class="status-loading">🔄 Loading Orpheus...</span>
    </div>
    
    <div class="header">
        <h1>🎤 Real Orpheus Voice Chat</h1>
        <p>Authentic Orpheus-TTS with Human-like Speech & Emotions</p>
    </div>
    
    <div class="container">
        <div class="status">
            <h3>🎭 Choose Your AI Voice Personality</h3>
            <div class="voice-selector">
                <div class="voice-btn active" data-voice="tara">
                    <div>👩‍💼 Tara</div>
                    <small>Warm & Natural</small>
                </div>
                <div class="voice-btn" data-voice="jess">
                    <div>😊 Jessica</div>
                    <small>Bubbly & Fun</small>
                </div>
                <div class="voice-btn" data-voice="leo">
                    <div>🧔 Leo</div>
                    <small>Thoughtful & Calm</small>
                </div>
                <div class="voice-btn" data-voice="dan">
                    <div>👨 Daniel</div>
                    <small>Casual & Friendly</small>
                </div>
                <div class="voice-btn" data-voice="mia">
                    <div>🎨 Mia</div>
                    <small>Creative & Expressive</small>
                </div>
                <div class="voice-btn" data-voice="leah">
                    <div>👩‍🎓 Leah</div>
                    <small>Gentle & Caring</small>
                </div>
                <div class="voice-btn" data-voice="zac">
                    <div>🧑‍💻 Zachary</div>
                    <small>Tech-savvy & Young</small>
                </div>
                <div class="voice-btn" data-voice="zoe">
                    <div>👩‍🎨 Zoe</div>
                    <small>Witty & Sophisticated</small>
                </div>
            </div>
        </div>
        
        <div class="chat-area" id="chatArea">
            <div class="message ai-message">
                <strong>System:</strong> Welcome to Real Orpheus Voice Chat! Select a voice personality above and start chatting. 
                The authentic Orpheus-TTS model will generate human-like speech with emotions and natural expression.
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" class="text-input" id="textInput" 
                   placeholder="Type your message and press Enter or click Send..."
                   onkeypress="handleKeyPress(event)">
            <button class="send-btn" onclick="sendMessage()">📤</button>
        </div>
    </div>

    <script>
        let selectedVoice = 'tara';
        let isProcessing = false;
        
        // Voice selection
        document.querySelectorAll('.voice-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.voice-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedVoice = btn.dataset.voice;
                console.log('Selected voice:', selectedVoice);
            });
        });
        
        // Check model status
        async function checkModelStatus() {
            try {
                const response = await fetch('/status');
                const status = await response.json();
                const statusEl = document.getElementById('modelStatus');
                
                if (status.model_ready) {
                    statusEl.innerHTML = '<span class="status-ready">✅ Orpheus Ready</span>';
                } else if (status.model_loading) {
                    statusEl.innerHTML = '<span class="status-loading">🔄 Loading Orpheus...</span>';
                } else {
                    statusEl.innerHTML = '<span class="status-error">❌ Model Error</span>';
                }
            } catch (error) {
                console.error('Status check failed:', error);
            }
        }
        
        // Check status every 3 seconds
        setInterval(checkModelStatus, 3000);
        checkModelStatus();
        
        function handleKeyPress(event) {
            if (event.key === 'Enter' && !isProcessing) {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            if (isProcessing) return;
            
            const input = document.getElementById('textInput');
            const message = input.value.trim();
            if (!message) return;
            
            isProcessing = true;
            input.value = '';
            
            // Add user message
            addMessage(message, 'user');
            
            try {
                // Send to API
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        voice: selectedVoice
                    })
                });
                
                const data = await response.json();
                
                if (data.success) {
                    // Add AI response
                    addMessage(data.response, 'ai');
                    
                    // Play audio if available
                    if (data.audio_url) {
                        addAudioPlayer(data.audio_url);
                    } else if (data.error) {
                        addMessage(`Audio Error: ${data.error}`, 'ai');
                    }
                } else {
                    addMessage(`Error: ${data.error}`, 'ai');
                }
                
            } catch (error) {
                console.error('Chat error:', error);
                addMessage('Connection error. Please try again.', 'ai');
            }
            
            isProcessing = false;
        }
        
        function addMessage(text, sender) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            messageDiv.innerHTML = `<strong>${sender === 'user' ? 'You' : selectedVoice.charAt(0).toUpperCase() + selectedVoice.slice(1)}:</strong> ${text}`;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function addAudioPlayer(audioUrl) {
            const chatArea = document.getElementById('chatArea');
            const audioDiv = document.createElement('div');
            audioDiv.innerHTML = `
                <audio controls class="audio-player" autoplay>
                    <source src="${audioUrl}" type="audio/wav">
                    Your browser does not support audio playback.
                </audio>
            `;
            chatArea.appendChild(audioDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
    </script>
</body>
</html>
    """)

@app.route('/status')
def status():
    """Get model loading status"""
    return jsonify({
        "model_ready": chat_system.model_ready,
        "model_loading": chat_system.model_loading,
        "voices": list(chat_system.voice_personalities.keys())
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Main chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        voice = data.get('voice', 'tara')
        conversation_id = data.get('conversation_id', 'default')
        
        if not user_message:
            return jsonify({"success": False, "error": "No message provided"})
        
        logger.info(f"💬 Chat request: {user_message[:50]}... (voice: {voice})")
        
        # Generate AI response
        ai_response = chat_system.get_ai_response(user_message, voice, conversation_id)
        
        # Generate speech
        audio_bytes, error = chat_system.generate_speech_orpheus(ai_response, voice)
        
        response_data = {
            "success": True,
            "response": ai_response,
            "voice": voice
        }
        
        if audio_bytes:
            # Save audio temporarily
            audio_filename = f"temp_audio_{int(time.time())}.wav"
            audio_path = os.path.join(os.getcwd(), audio_filename)
            
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
            
            response_data["audio_url"] = f"/audio/{audio_filename}"
        elif error:
            response_data["error"] = error
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ Chat error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve generated audio files"""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='audio/wav')
        else:
            return "Audio file not found", 404
    except Exception as e:
        logger.error(f"❌ Audio serve error: {e}")
        return "Error serving audio", 500

if __name__ == '__main__':
    print("\n🎤 Real Orpheus Voice Chat API Starting...")
    print("=" * 50)
    print("🔧 Features:")
    print("  ✅ Real Orpheus-TTS Model (Windows Compatible)")
    print("  ✅ 8 Voice Personalities (tara, jess, leo, dan, mia, leah, zac, zoe)")
    print("  ✅ Emotion Support (<laugh>, <chuckle>, <sigh>, etc.)")
    print("  ✅ Google Gemini AI Integration")
    print("  ✅ Real-time Voice Chat Interface")
    print("  ✅ Conversation Memory")
    print("=" * 50)
    print("\n🌐 Starting server on http://localhost:5000")
    print("🎯 Open your browser and start chatting with real Orpheus voices!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
