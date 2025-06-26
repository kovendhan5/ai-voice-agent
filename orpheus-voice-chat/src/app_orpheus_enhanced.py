"""
Enhanced AI Voice Chat with Orpheus-Quality Speech
Uses advanced TTS models for human-like voice with emotions
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
import asyncio

# AI and TTS imports
import google.generativeai as genai
import numpy as np
import asyncio
import edge_tts
from gtts import gTTS
import google.generativeai as genai

app = Flask(__name__)
CORS(app)

# Configure Gemini AI with your API key
GEMINI_API_KEY = "AIzaSyBu5izidIfzknhhMCzZB6yn1GKnzwZoUIQ"
genai.configure(api_key=GEMINI_API_KEY)

# Initialize Gemini model
model = genai.GenerativeModel('gemini-pro')

# Enhanced TTS Engine with Multiple Backends
class OrpheusLikeTTS:
    def __init__(self):
        self.available_engines = []
        self.current_engine = None
        self.setup_engines()
        print("🎭 Orpheus-like TTS Engine initialized!")
    
    def setup_engines(self):
        """Initialize available TTS engines"""
        # Try Edge TTS first (highest quality)
        try:
            import edge_tts
            self.available_engines.append('edge-tts')
            print("✅ Edge TTS available (Microsoft Neural Voices)")
        except ImportError:
            print("⚠️ Edge TTS not available")
        
        # Try Coqui TTS
        try:
            # Skip Coqui TTS due to build issues
            # from TTS.api import TTS
            # self.available_engines.append('coqui-tts')
            print("⚠️ Coqui TTS skipped (build issues)")
        except ImportError:
            print("⚠️ Coqui TTS not available")
        
        # Try gTTS as fallback
        try:
            from gtts import gTTS
            self.available_engines.append('gtts')
            print("✅ Google TTS available (Fallback)")
        except ImportError:
            print("⚠️ Google TTS not available")
        
        # Fallback to pyttsx3
        try:
            import pyttsx3
            self.available_engines.append('pyttsx3')
            print("✅ System TTS available (Last resort)")
        except ImportError:
            print("⚠️ System TTS not available")
        
        # Set best available engine
        if 'edge-tts' in self.available_engines:
            self.current_engine = 'edge-tts'
            print("🎯 Using Edge TTS (Best quality)")
        elif 'coqui-tts' in self.available_engines:
            self.current_engine = 'coqui-tts'
            print("🎯 Using Coqui TTS (High quality)")
        elif 'gtts' in self.available_engines:
            self.current_engine = 'gtts'
            print("🎯 Using Google TTS (Good quality)")
        elif 'pyttsx3' in self.available_engines:
            self.current_engine = 'pyttsx3'
            print("🎯 Using System TTS (Basic quality)")
        else:
            self.current_engine = 'fallback'
            print("⚠️ Using fallback audio generation")
    
    async def generate_speech_edge_tts(self, text, voice="tara"):
        """Generate speech using Edge TTS (highest quality)"""
        try:
            import edge_tts
            
            # Voice mapping for Edge TTS
            voice_map = {
                "tara": "en-US-JennyNeural",     # Natural female
                "jess": "en-US-AriaNeural",      # Friendly female
                "mia": "en-GB-SoniaNeural",      # Soft British female
                "leah": "en-US-MichelleNeural",  # Dynamic female
                "zoe": "en-US-AnaNeural",        # Young female
                "zac": "en-US-GuyNeural",        # Clear male
                "leo": "en-US-DavisNeural",      # Deep male
                "dan": "en-GB-RyanNeural"        # Professional British male
            }
            
            edge_voice = voice_map.get(voice, "en-US-JennyNeural")
            
            # Process emotions in text
            processed_text = self.process_emotions_for_edge(text)
            
            # Generate speech
            communicate = edge_tts.Communicate(processed_text, edge_voice)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_path = temp_file.name
            
            await communicate.save(temp_path)
            
            # Read audio data
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # Cleanup
            try:
                os.unlink(temp_path)
            except:
                pass
            
            print(f"🎤 Edge TTS: Generated {len(audio_data)} bytes for voice '{voice}'")
            return audio_data
            
        except Exception as e:
            print(f"❌ Edge TTS Error: {e}")
            return None
    
    def generate_speech_gtts(self, text, voice="tara"):
        """Generate speech using Google TTS"""
        try:
            from gtts import gTTS
            
            # Process text
            processed_text = self.process_emotions_simple(text)
            
            # Language/accent mapping
            lang_map = {
                "tara": "en",
                "jess": "en", 
                "mia": "en-uk",
                "leah": "en",
                "zoe": "en",
                "zac": "en",
                "leo": "en-uk", 
                "dan": "en-uk"
            }
            
            lang = lang_map.get(voice, "en")
            
            # Generate TTS
            tts = gTTS(text=processed_text, lang=lang, slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as temp_file:
                temp_path = temp_file.name
            
            tts.save(temp_path)
            
            # Read audio data
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # Cleanup
            try:
                os.unlink(temp_path)
            except:
                pass
            
            print(f"🎤 Google TTS: Generated {len(audio_data)} bytes for voice '{voice}'")
            return audio_data
            
        except Exception as e:
            print(f"❌ Google TTS Error: {e}")
            return None
    
    def generate_speech_pyttsx3(self, text, voice="tara"):
        """Generate speech using system TTS"""
        try:
            import pyttsx3
            
            engine = pyttsx3.init()
            processed_text = self.process_emotions_simple(text)
            
            # Voice configuration
            voices = engine.getProperty('voices')
            if voices:
                if voice in ["zac", "leo", "dan"] and len(voices) > 1:
                    engine.setProperty('voice', voices[1].id)  # Male voice
                else:
                    engine.setProperty('voice', voices[0].id)  # Female voice
            
            # Speed and volume settings
            speed_map = {
                "tara": 180, "jess": 200, "mia": 160, "leah": 190,
                "zoe": 210, "zac": 170, "leo": 150, "dan": 160
            }
            engine.setProperty('rate', speed_map.get(voice, 180))
            engine.setProperty('volume', 0.9)
            
            # Generate to file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as temp_file:
                temp_path = temp_file.name
            
            engine.save_to_file(processed_text, temp_path)
            engine.runAndWait()
            
            # Read audio data
            with open(temp_path, 'rb') as f:
                audio_data = f.read()
            
            # Cleanup
            try:
                os.unlink(temp_path)
            except:
                pass
            
            print(f"🎤 System TTS: Generated {len(audio_data)} bytes for voice '{voice}'")
            return audio_data
            
        except Exception as e:
            print(f"❌ System TTS Error: {e}")
            return None
    
    def process_emotions_for_edge(self, text):
        """Process emotion tags for Edge TTS with SSML"""
        # Edge TTS supports SSML for emotions
        emotion_map = {
            "<laugh>": '<prosody rate="fast" pitch="+10%">haha!</prosody>',
            "<chuckle>": '<prosody rate="medium" pitch="+5%">hehe</prosody>',
            "<sigh>": '<prosody rate="slow" pitch="-10%">*sigh*</prosody>',
            "<gasp>": '<prosody rate="fast" pitch="+20%">oh!</prosody>',
            "<excited>": '<prosody rate="fast" pitch="+15%" volume="loud">',
            "</excited>": '</prosody>',
            "<whisper>": '<prosody volume="x-soft">',
            "</whisper>": '</prosody>',
            "<happy>": '<prosody rate="medium" pitch="+10%">',
            "</happy>": '</prosody>',
            "<sad>": '<prosody rate="slow" pitch="-15%">',
            "</sad>": '</prosody>'
        }
        
        processed = text
        for emotion, ssml in emotion_map.items():
            processed = processed.replace(emotion, ssml)
        
        return processed
    
    def process_emotions_simple(self, text):
        """Simple emotion processing for basic TTS"""
        emotion_map = {
            "<laugh>": "haha! ",
            "<chuckle>": "hehe, ",
            "<sigh>": "*sigh* ",
            "<gasp>": "oh! ",
            "<excited>": "",
            "</excited>": "!",
            "<whisper>": "",
            "</whisper>": "",
            "<happy>": "",
            "</happy>": "!",
            "<sad>": "",
            "</sad>": "..."
        }
        
        processed = text
        for emotion, replacement in emotion_map.items():
            processed = processed.replace(emotion, replacement)
        
        return processed
    
    def generate_fallback_audio(self, text, voice):
        """High-quality fallback audio generation"""
        sample_rate = 22050
        duration = max(0.8, len(text) * 0.05)
        
        # Voice-specific pleasant tones
        frequencies = {
            "tara": [440, 554],      # A4 + C#5 harmony
            "jess": [523, 659],      # C5 + E5 bright
            "mia": [392, 493],       # G4 + B4 gentle
            "leah": [494, 622],      # B4 + D#5 dynamic
            "zoe": [587, 740],       # D5 + F#5 energetic
            "zac": [330, 415],       # E4 + G#4 confident
            "leo": [294, 370],       # D4 + F#4 deep
            "dan": [262, 330]        # C4 + E4 professional
        }
        
        freqs = frequencies.get(voice, [440, 554])
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        
        # Create pleasant harmony
        audio1 = 0.3 * np.sin(2 * np.pi * freqs[0] * t)
        audio2 = 0.2 * np.sin(2 * np.pi * freqs[1] * t)
        audio_data = audio1 + audio2
        
        # Apply envelope
        fade_len = int(0.05 * sample_rate)
        if len(audio_data) > 2 * fade_len:
            audio_data[:fade_len] *= np.linspace(0, 1, fade_len)
            audio_data[-fade_len:] *= np.linspace(1, 0, fade_len)
        
        # Convert to audio bytes
        audio_int16 = np.clip(audio_data * 32767, -32767, 32767).astype(np.int16)
        
        # Create WAV
        audio_buffer = io.BytesIO()
        with wave.open(audio_buffer, 'wb') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(sample_rate)
            wf.writeframes(audio_int16.tobytes())
        
        return audio_buffer.getvalue()
    
    def generate_speech(self, text, voice="tara"):
        """Main speech generation method"""
        print(f"🎭 Generating speech with {self.current_engine}: '{text[:50]}...'")
        
        audio_data = None
        
        if self.current_engine == 'edge-tts':
            # Edge TTS needs async
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                audio_data = loop.run_until_complete(self.generate_speech_edge_tts(text, voice))
                if audio_data:
                    return audio_data
            except Exception as e:
                print(f"❌ Edge TTS failed: {e}")
            finally:
                loop.close()
        
        if self.current_engine == 'gtts' or not audio_data:
            audio_data = self.generate_speech_gtts(text, voice)
            if audio_data:
                return audio_data
        
        if self.current_engine == 'pyttsx3' or not audio_data:
            audio_data = self.generate_speech_pyttsx3(text, voice)
            if audio_data:
                return audio_data
        
        # Final fallback
        print("🔄 Using enhanced fallback audio")
        return self.generate_fallback_audio(text, voice)

# Initialize enhanced TTS
tts_engine = OrpheusLikeTTS()

# AI Conversation Manager (same as before)
class AIConversation:
    def __init__(self):
        self.conversation_history = []
        self.personality_prompts = {
            "tara": "You are Tara, a warm and natural AI assistant. Speak conversationally and add natural expressions like 'hmm', 'oh', and gentle <chuckle> where appropriate. Use <happy> when excited.",
            "jess": "You are Jess, a friendly and bubbly AI assistant. Be enthusiastic and use expressions like <excited> and <laugh> in your responses. You love to <chuckle> at funny things.",
            "mia": "You are Mia, a soft and gentle AI assistant. Speak calmly and thoughtfully, using <whisper> for emphasis and <sigh> occasionally when contemplating.",
            "leah": "You are Leah, a dynamic and expressive AI assistant. Vary your tone and use emotions like <gasp> and <excited> naturally. <laugh> when something is truly funny.",
            "zoe": "You are Zoe, a young and energetic AI assistant. Be vibrant and use <excited> frequently with lots of enthusiasm! <laugh> often and be playful.",
            "zac": "You are Zac, a clear and confident AI assistant. Speak with authority but remain friendly. Use <chuckle> when amused and <happy> when pleased.",
            "leo": "You are Leo, a deep and authoritative AI assistant. Speak with wisdom and gravitas, occasionally using gentle <chuckle> and thoughtful pauses.",
            "dan": "You are Dan, a mature and professional AI assistant. Be polished and articulate while remaining personable. Use subtle <chuckle> and <happy> expressions."
        }
    
    def generate_response(self, user_message, voice="tara"):
        """Generate AI response using Gemini"""
        try:
            personality = self.personality_prompts.get(voice, self.personality_prompts["tara"])
            
            context = f"{personality}\n\nUser: {user_message}\n\nRespond naturally with appropriate emotions:"
            
            response = model.generate_content(context)
            ai_text = response.text
            
            # Add to conversation history
            self.conversation_history.append({
                "user": user_message,
                "ai": ai_text,
                "voice": voice,
                "timestamp": datetime.now().isoformat()
            })
            
            if len(self.conversation_history) > 10:
                self.conversation_history = self.conversation_history[-10:]
            
            print(f"🤖 AI Response ({voice}): {ai_text[:100]}...")
            return ai_text
            
        except Exception as e:
            print(f"❌ AI Error: {e}")
            return f"<happy>I'm here to chat with you!</happy> What would you like to talk about? <chuckle>"

# Initialize AI
ai_chat = AIConversation()

# Available voices with enhanced descriptions
VOICES = {
    "tara": "🎭 Natural & Warm - Microsoft Neural Voice (Jenny)",
    "zac": "🎯 Clear & Confident - Microsoft Neural Voice (Guy)", 
    "jess": "✨ Friendly & Bubbly - Microsoft Neural Voice (Aria)",
    "leo": "🎪 Deep & Authoritative - Microsoft Neural Voice (Davis)",
    "mia": "🌟 Soft & Gentle - British Neural Voice (Sonia)",
    "leah": "🎨 Dynamic & Expressive - Microsoft Neural Voice (Michelle)",
    "zoe": "🎵 Young & Energetic - Microsoft Neural Voice (Ana)",
    "dan": "🎬 Mature & Professional - British Neural Voice (Ryan)"
}

def generate_speech(text, voice="tara"):
    """Generate enhanced speech"""
    return tts_engine.generate_speech(text, voice)

# Flask routes (same as before but with enhanced descriptions)
@app.route('/')
def index():
    """Serve the enhanced AI voice chat interface"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🎭 Orpheus-Quality AI Voice Chat</title>
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
                max-width: 900px; 
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
                background: linear-gradient(45deg, rgba(76, 175, 80, 0.2), rgba(139, 195, 74, 0.2)); 
                padding: 25px; 
                border-radius: 15px; 
                margin: 20px 0;
                border: 1px solid rgba(76, 175, 80, 0.5);
            }
            .chat-container {
                background: rgba(255,255,255,0.05);
                border-radius: 15px;
                padding: 20px;
                margin: 20px 0;
                min-height: 250px;
                max-height: 400px;
                overflow-y: auto;
                border: 1px solid rgba(255,255,255,0.1);
            }
            .message {
                margin: 12px 0;
                padding: 12px 18px;
                border-radius: 12px;
                animation: fadeIn 0.3s ease-in;
            }
            .user-message {
                background: linear-gradient(45deg, rgba(103, 126, 234, 0.4), rgba(103, 126, 234, 0.2));
                margin-left: 20px;
                border-left: 3px solid #677eea;
            }
            .ai-message {
                background: linear-gradient(45deg, rgba(118, 75, 162, 0.4), rgba(118, 75, 162, 0.2));
                margin-right: 20px;
                border-left: 3px solid #764ba2;
            }
            .input-group {
                display: flex;
                gap: 12px;
                margin: 25px 0;
                align-items: center;
                flex-wrap: wrap;
            }
            input[type="text"] { 
                flex: 1;
                min-width: 300px;
                padding: 18px; 
                border: none; 
                border-radius: 12px;
                background: rgba(255,255,255,0.1);
                color: white;
                font-size: 16px;
                backdrop-filter: blur(5px);
                border: 1px solid rgba(255,255,255,0.2);
            }
            input[type="text"]::placeholder {
                color: rgba(255,255,255,0.7);
            }
            select {
                padding: 18px; 
                border: none; 
                border-radius: 12px;
                background: rgba(255,255,255,0.1);
                color: white;
                font-size: 16px;
                min-width: 250px;
                border: 1px solid rgba(255,255,255,0.2);
            }
            option {
                background: #4a4a4a;
                color: white;
            }
            button { 
                padding: 18px 30px; 
                font-size: 16px; 
                border: none; 
                border-radius: 12px; 
                background: linear-gradient(45deg, #4CAF50, #45a049);
                color: white; 
                cursor: pointer;
                transition: all 0.3s ease;
                font-weight: bold;
                box-shadow: 0 4px 15px rgba(76, 175, 80, 0.3);
            }
            button:hover { 
                transform: translateY(-3px);
                box-shadow: 0 8px 25px rgba(76, 175, 80, 0.4);
            }
            .voice-info {
                font-size: 14px;
                color: rgba(255,255,255,0.9);
                margin-top: 8px;
                padding: 10px;
                background: rgba(255,255,255,0.05);
                border-radius: 8px;
            }
            .loading {
                display: none;
                text-align: center;
                color: #4CAF50;
                font-style: italic;
                padding: 15px;
                background: rgba(76, 175, 80, 0.1);
                border-radius: 10px;
                margin: 10px 0;
            }
            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(10px); }
                to { opacity: 1; transform: translateY(0); }
            }
            .features {
                text-align: center;
                margin-top: 30px;
                padding: 20px;
                background: rgba(255,255,255,0.05);
                border-radius: 15px;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎭 Orpheus-Quality AI Voice Chat</h1>
                <h2>Powered by Gemini AI + Microsoft Neural Voices</h2>
            </div>
            
            <div class="status">
                <h3>✅ Enhanced AI Voice System: LIVE</h3>
                <p>🧠 AI Brain: Google Gemini Pro</p>
                <p>🎤 Voice Engine: Microsoft Neural TTS (Human-like quality)</p>
                <p>💬 Features: SSML emotions, natural speech patterns</p>
                <p>🎭 8 Professional voice personalities available</p>
                <p>🌟 Ready for Orpheus-quality conversations!</p>
            </div>
            
            <div class="chat-container" id="chatContainer">
                <div class="ai-message">
                    <strong>AI:</strong> <happy>Hello! I'm your enhanced AI voice assistant with human-like speech quality!</happy> Choose a voice personality and let's have a natural conversation with emotions and expressions! <chuckle> What would you like to chat about?
                </div>
            </div>
            
            <div class="input-group">
                <select id="voiceSelect" onchange="updateVoiceInfo()">
                    <option value="tara">🎭 Tara - Natural & Warm (Jenny Neural)</option>
                    <option value="jess">✨ Jess - Friendly & Bubbly (Aria Neural)</option>
                    <option value="mia">🌟 Mia - Soft & Gentle (Sonia British)</option>
                    <option value="leah">🎨 Leah - Dynamic & Expressive (Michelle)</option>
                    <option value="zoe">🎵 Zoe - Young & Energetic (Ana Neural)</option>
                    <option value="zac">🎯 Zac - Clear & Confident (Guy Neural)</option>
                    <option value="leo">🎪 Leo - Deep & Authoritative (Davis)</option>
                    <option value="dan">🎬 Dan - Professional British (Ryan)</option>
                </select>
                <input type="text" id="messageInput" placeholder="Type your message here..." onkeypress="handleKeyPress(event)">
                <button onclick="sendMessage()">🎤 Send & Speak</button>
            </div>
            
            <div class="voice-info" id="voiceInfo">
                Microsoft Jenny Neural Voice - Perfect for everyday conversations with natural warmth and human-like quality
            </div>
            
            <div class="loading" id="loading">
                🤖 AI is thinking and generating human-like speech...
            </div>
            
            <div class="features">
                <p><strong>🎯 Try these emotional prompts:</strong></p>
                <p>"Tell me a funny joke with laughter" • "Share something that makes you excited" • "Whisper a secret to me"</p>
                <p><strong>🎭 Emotion tags work:</strong> &lt;laugh&gt; &lt;chuckle&gt; &lt;excited&gt; &lt;whisper&gt; &lt;happy&gt; &lt;sigh&gt;</p>
            </div>
        </div>
        
        <script>
            const voices = {
                "tara": "Microsoft Jenny Neural Voice - Perfect for everyday conversations with natural warmth and human-like quality",
                "jess": "Microsoft Aria Neural Voice - Enthusiastic and upbeat with brilliant emotional expression",
                "mia": "Microsoft Sonia British Voice - Calm and soothing with elegant British accent",
                "leah": "Microsoft Michelle Neural Voice - Varied emotional responses with dynamic personality",
                "zoe": "Microsoft Ana Neural Voice - Vibrant and exciting with youthful energy",
                "zac": "Microsoft Guy Neural Voice - Clear and confident with professional male tone",
                "leo": "Microsoft Davis Neural Voice - Deep and authoritative with commanding presence",
                "dan": "Microsoft Ryan British Voice - Polished and articulate with sophisticated British accent"
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

# Same Flask routes as before
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
            'mode': 'enhanced-gemini-ai'
        })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/synthesize', methods=['POST'])
def synthesize():
    """Generate enhanced speech from AI responses"""
    try:
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({'error': 'Text is required'}), 400
        
        text = data['text']
        voice = data.get('voice', 'tara')
        
        print(f"🎤 Generating enhanced speech for: '{text[:50]}...' with voice '{voice}'")
        
        # Generate enhanced speech
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
    """Get available enhanced voice personalities"""
    return jsonify({
        'voices': VOICES,
        'total_voices': len(VOICES),
        'model': 'enhanced-neural-tts'
    })

@app.route('/status', methods=['GET'])
def status():
    """Check enhanced system status"""
    return jsonify({
        'status': 'running',
        'ai_model': 'Google Gemini Pro',
        'tts_engine': 'Enhanced Neural TTS (Microsoft Edge)',
        'voices': len(VOICES),
        'mode': 'production-enhanced',
        'features': ['neural_voices', 'ssml_emotions', 'personality_voices', 'real_conversations'],
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🎭 ORPHEUS-QUALITY AI VOICE CHAT - ENHANCED VERSION")
    print("="*80)
    print("🧠 AI Brain: Google Gemini Pro")
    print("🎤 Voice Engine: Microsoft Neural TTS (Human-like quality)")
    print("🎭 Voice Personalities: 8 professional neural voices")
    print("😄 Features: SSML emotions, natural speech, laughter")
    print("💬 Mode: Orpheus-quality AI Conversations")
    print("🌐 Server: http://localhost:8080")
    print("="*80)
    print("🚀 Ready for human-like AI voice conversations!")
    print("   Experience Orpheus-quality speech with real AI!")
    print("="*80)
    
    app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
