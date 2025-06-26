"""
Live Interactive Orpheus Voice Chat
Real-time voice conversation with speech-to-text and text-to-speech
Now powered by REAL OpenVoice/Orpheus TTS with authentic emotional synthesis
"""

from flask import Flask, request, jsonify, send_file, render_template_string
from flask_cors import CORS
import google.generativeai as genai
import pyttsx3
import speech_recognition as sr
import threading
import queue
import time
import os
import logging
import json
from datetime import datetime
import tempfile
import asyncio
from threading import Thread
import edge_tts
import io

# Import OpenVoice integration
try:
    from openvoice_integration import create_orpheus_tts
    OPENVOICE_AVAILABLE = True
except ImportError as e:
    logging.warning(f"OpenVoice integration not available: {e}")
    OPENVOICE_AVAILABLE = False

# Configure logging for Cloud Run
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
GEMINI_API_KEY = "AIzaSyBu5izidIfzknhhMCzZB6yn1GKnzwZoUIQ"
genai.configure(api_key=GEMINI_API_KEY)

class LiveOrpheusChat:
    def __init__(self):
        self.conversations = {}
        self.audio_queue = queue.Queue()
        self.is_listening = False
        self.current_voice = "tara"
        
        # Initialize AI
        self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize OpenVoice/Orpheus TTS System
        logger.info("🎭 Initializing OpenVoice/Orpheus TTS System...")
        try:
            self.orpheus_tts = create_orpheus_tts(prefer_openvoice=True)
            if hasattr(self.orpheus_tts, 'models_loaded') and self.orpheus_tts.models_loaded:
                logger.info("✅ Real OpenVoice/Orpheus TTS initialized successfully!")
                self.tts_system = "openvoice"
            else:
                logger.info("⚠️ Using Edge TTS fallback (OpenVoice models not available)")
                self.tts_system = "edge_tts"
        except Exception as e:
            logger.error(f"❌ OpenVoice initialization failed: {e}")
            self.orpheus_tts = None
            self.tts_system = "edge_tts"
        
        # Initialize fallback TTS
        try:
            self.tts_engine = pyttsx3.init()
            voices = self.tts_engine.getProperty('voices')
            self.system_voices = voices
            self.tts_engine.setProperty('rate', 200)
            self.tts_engine.setProperty('volume', 0.9)
            logger.info("✅ Fallback TTS Engine initialized")
        except Exception as e:
            logger.error(f"❌ Fallback TTS Error: {e}")
            self.tts_engine = None
        
        # Initialize Speech Recognition
        try:
            self.recognizer = sr.Recognizer()
            self.microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            logger.info("✅ Speech Recognition initialized")
        except Exception as e:
            logger.error(f"❌ Speech Recognition Error: {e}")
            self.recognizer = None
            self.microphone = None
        
        # Voice personalities with high-quality Edge TTS voices
        self.voice_personalities = {
            "tara": {
                "name": "Tara",
                "personality": "Warm, empathetic, and naturally conversational. Loves to engage in meaningful dialogue and responds with genuine interest.",
                "conversation_style": "Ask follow-up questions, show curiosity about the user, use natural conversational flow",
                "voice_type": "female",
                "energy": "medium",
                "traits": ["empathetic", "curious", "warm"],
                "edge_voice": "en-US-JennyNeural",
                "style": "cheerful"
            },
            "jess": {
                "name": "Jessica", 
                "personality": "Bubbly, energetic, and enthusiastic. Gets excited about conversations and loves to share experiences.",
                "conversation_style": "Use exclamations, ask about user's experiences, be enthusiastic and reactive",
                "voice_type": "female",
                "energy": "high",
                "traits": ["enthusiastic", "reactive", "social"],
                "edge_voice": "en-US-AriaNeural",
                "style": "excited"
            },
            "leo": {
                "name": "Leo",
                "personality": "Thoughtful, intelligent, and engaging. Enjoys deep conversations and philosophical discussions.",
                "conversation_style": "Ask thought-provoking questions, share insights, be reflective and wise",
                "voice_type": "male",
                "energy": "medium",
                "traits": ["thoughtful", "wise", "analytical"],
                "edge_voice": "en-US-DavisNeural",
                "style": "calm"
            },
            "dan": {
                "name": "Daniel",
                "personality": "Casual, friendly, and relatable. Like talking to your best friend - easy-going and fun.",
                "conversation_style": "Use casual language, make jokes, be relatable and down-to-earth",
                "voice_type": "male",
                "energy": "medium",
                "traits": ["casual", "funny", "relatable"],
                "edge_voice": "en-US-GuyNeural",
                "style": "friendly"
            },
            "mia": {
                "name": "Mia",
                "personality": "Creative, artistic, and expressive. Loves to explore ideas and be imaginative in conversations.",
                "conversation_style": "Be creative with responses, use metaphors, explore artistic and creative topics",
                "voice_type": "female",
                "energy": "medium-high",
                "traits": ["creative", "imaginative", "expressive"],
                "edge_voice": "en-US-SaraNeural",
                "style": "cheerful"
            },
            "leah": {
                "name": "Leah",
                "personality": "Gentle, caring, and supportive. Like a kind therapist who really listens and cares.",
                "conversation_style": "Be supportive, ask about feelings, show genuine care and understanding",
                "voice_type": "female", 
                "energy": "low-medium",
                "traits": ["caring", "supportive", "gentle"],
                "edge_voice": "en-US-AmberNeural",
                "style": "gentle"
            },
            "zac": {
                "name": "Zachary",
                "personality": "Tech-savvy, modern, and quick-witted. Loves technology and contemporary topics.",
                "conversation_style": "Reference modern topics, be quick with responses, show tech knowledge",
                "voice_type": "male",
                "energy": "high",
                "traits": ["tech-savvy", "quick", "modern"],
                "edge_voice": "en-US-JasonNeural",
                "style": "excited"
            },
            "zoe": {
                "name": "Zoe",
                "personality": "Sophisticated, witty, and intellectually curious. Enjoys clever wordplay and interesting discussions.",
                "conversation_style": "Use clever language, make witty observations, engage in intellectual topics",
                "voice_type": "female",
                "energy": "medium",
                "traits": ["witty", "sophisticated", "clever"],
                "edge_voice": "en-US-MonicaNeural",
                "style": "cheerful"
            }
        }
    
    def listen_for_speech(self):
        """Listen for speech input in real-time"""
        if not self.recognizer or not self.microphone:
            return None
        
        try:
            logger.info("🎤 Listening for speech...")
            with self.microphone as source:
                # Listen for speech with timeout
                audio = self.recognizer.listen(source, timeout=1, phrase_time_limit=10)
            
            # Recognize speech
            text = self.recognizer.recognize_google(audio)
            logger.info(f"🗣️ Heard: {text}")
            return text.strip()
            
        except sr.WaitTimeoutError:
            return None  # No speech detected
        except sr.UnknownValueError:
            logger.warning("Could not understand audio")
            return None
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            return None
    
    def generate_live_response(self, user_input, voice="tara", conversation_id="default"):
        """Generate live, interactive AI response"""
        try:
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            
            history = self.conversations[conversation_id]
            personality = self.voice_personalities.get(voice, self.voice_personalities["tara"])
            
            # Create a more engaging, live conversation prompt
            live_prompt = f"""You are {personality['name']}, having a LIVE voice conversation with a real person.

Your personality: {personality['personality']}
Conversation style: {personality['conversation_style']}
Your traits: {', '.join(personality['traits'])}

CRITICAL RULES FOR VOICE CONVERSATION:
1. You are speaking OUT LOUD to a human - be completely natural and conversational
2. NEVER mention HTML, code, websites, or technical elements 
3. Keep responses to 1-2 short sentences (people are listening, not reading)
4. Use emotion tags naturally: <laugh>, <chuckle>, <sigh>, <gasp>, <excited>
5. Be a real person having a genuine conversation
6. Ask engaging follow-up questions to keep talking
7. React naturally to what the user says
8. NO technical jargon, NO code references, NO HTML mentions
9. Speak like you're talking to a friend face-to-face

Recent conversation:
{json.dumps(history[-3:], indent=2) if history else "This is the start of your conversation"}

Human said: "{user_input}"

Respond as {personality['name']} speaking naturally out loud. Be conversational, use 1-2 emotion tags, and keep the conversation flowing like real speech."""

            # Generate response
            response = self.ai_model.generate_content(live_prompt)
            ai_text = response.text.strip()
            
            # Store conversation
            history.append({
                "user": user_input, 
                "ai": ai_text, 
                "timestamp": datetime.now().isoformat(),
                "voice": voice
            })
            self.conversations[conversation_id] = history[-15:]  # Keep last 15 exchanges
            
            return ai_text
            
        except Exception as e:
            logger.error(f"Error generating live response: {e}")
            # Personality-based fallback responses for live chat
            fallbacks = {
                "tara": "<chuckle> I'm having a little connection hiccup! What were you saying?",
                "jess": "<laugh> Oops! My brain just glitched for a second! Can you repeat that?",
                "leo": "Hmm, I seem to have lost my train of thought there. Could you say that again?",
                "dan": "<sigh> Man, I totally spaced out there! What did you just say?",
                "mia": "<gasp> Oh no! I just had a creative block! What were we talking about?",
                "leah": "I'm so sorry, I didn't catch that. Could you please repeat what you said?",
                "zac": "Whoa, system lag! <chuckle> Can you run that by me again?",
                "zoe": "How embarrassing - I just had a momentary lapse! What did you say?"
            }
            return fallbacks.get(voice, "I'm sorry, could you repeat that?")
    
    async def generate_speech_openvoice(self, text, voice="tara"):
        """Generate authentic emotional speech using real OpenVoice/Orpheus TTS"""
        try:
            if not self.orpheus_tts:
                raise Exception("OpenVoice TTS not available")
            
            logger.info(f"🎭 Generating OpenVoice speech: {voice} - {text[:50]}...")
            
            # Use OpenVoice with personality-based emotional synthesis
            audio_path = self.orpheus_tts.synthesize_with_personality(
                text=text,
                personality=voice,
                speed=1.0
            )
            
            if audio_path and os.path.exists(audio_path):
                # Read the generated audio file
                with open(audio_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                
                # Clean up temp file
                try:
                    os.unlink(audio_path)
                except:
                    pass
                
                logger.info(f"✅ Generated {len(audio_bytes)} bytes of OpenVoice audio")
                return audio_bytes, None
            else:
                raise Exception("Failed to generate OpenVoice audio")
                
        except Exception as e:
            logger.error(f"❌ OpenVoice error: {e}")
            return None, str(e)

    async def generate_speech_edge_tts(self, text, voice="tara"):
        """Generate high-quality speech using Edge TTS with emotions"""
        try:
            personality = self.voice_personalities[voice]
            edge_voice = personality["edge_voice"]
            style = personality.get("style", "cheerful")
            
            # Process emotion tags to SSML for natural expression
            ssml_text = self.process_emotions_to_ssml(text, style)
            
            logger.info(f"🎤 Generating Edge TTS: {edge_voice} - {ssml_text[:50]}...")
            
            # Generate speech using Edge TTS
            communicate = edge_tts.Communicate(ssml_text, edge_voice)
            
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Save audio to file
            await communicate.save(temp_path)
            
            # Read the audio file
            with open(temp_path, 'rb') as audio_file:
                audio_bytes = audio_file.read()
            
            # Clean up temp file
            try:
                os.unlink(temp_path)
            except:
                pass
            
            logger.info(f"✅ Generated {len(audio_bytes)} bytes of Edge TTS audio")
            return audio_bytes, None
            
        except Exception as e:
            logger.error(f"❌ Edge TTS error: {e}")
            return None, str(e)
    
    def process_emotions_to_ssml(self, text, base_style="cheerful"):
        """Convert Orpheus emotion tags to SSML for natural expression"""
        
        # Clean text first - remove any potential HTML/XML elements
        clean_text = text.strip()
        
        # Remove any HTML tags that might have leaked through
        import re
        clean_text = re.sub(r'<(?!/?(?:laugh|chuckle|sigh|gasp|excited|yawn|cough|sniffle|groan))[^>]*>', '', clean_text)
        
        # Simple emotion mapping to natural speech
        emotion_map = {
            "<laugh>": "haha! ",
            "<chuckle>": "hehe ",
            "<sigh>": "*sigh* ",
            "<gasp>": "oh! ",
            "<excited>": "",  # Just use the excited style
            "</excited>": "",
            "<yawn>": "*yawn* ",
            "<cough>": "*cough* ",
            "<sniffle>": "*sniff* ",
            "<groan>": "ugh "
        }
        
        # Process text with emotion replacements
        processed_text = clean_text
        for emotion, replacement in emotion_map.items():
            processed_text = processed_text.replace(emotion, replacement)
        
        # Keep it simple - just return clean text for Edge TTS
        # Edge TTS will handle natural intonation automatically
        return processed_text
    
    def speak_text(self, text, voice="tara"):
        """Generate speech using OpenVoice or Edge TTS fallback"""
        self.current_voice = voice
        
        try:
            # Run async function in event loop
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            
            # Choose TTS system based on availability
            if self.tts_system == "openvoice" and self.orpheus_tts:
                audio_bytes, error = loop.run_until_complete(
                    self.generate_speech_openvoice(text, voice)
                )
                if audio_bytes:
                    logger.info(f"🎭 Using OpenVoice for {voice}")
                    loop.close()
                    return audio_bytes
                else:
                    logger.warning(f"OpenVoice failed, falling back to Edge TTS: {error}")
            
            # Fallback to Edge TTS
            audio_bytes, error = loop.run_until_complete(
                self.generate_speech_edge_tts(text, voice)
            )
            loop.close()
            
            if audio_bytes:
                logger.info(f"🎤 Using Edge TTS for {voice}")
                return audio_bytes
            else:
                logger.error(f"Speech generation failed: {error}")
                return None
                
        except Exception as e:
            logger.error(f"Speech generation error: {e}")
            return None

# Global instance
live_chat = LiveOrpheusChat()

@app.route('/')
def home():
    """Live Interactive Orpheus Voice Chat Interface"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎙️ LIVE Orpheus Voice Chat</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            color: white;
            overflow-x: hidden;
            overflow-y: auto;
        }
        .live-header {
            text-align: center;
            padding: 15px;
            background: rgba(0,0,0,0.4);
            backdrop-filter: blur(20px);
            border-bottom: 2px solid #ff4444;
            position: relative;
        }
        .live-indicator {
            position: absolute;
            top: 10px;
            right: 20px;
            background: #ff4444;
            color: white;
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 50% { opacity: 1; }
            25%, 75% { opacity: 0.5; }
        }
        .container {
            flex: 1;
            max-width: 1000px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 15px;
            min-height: calc(100vh - 200px);
        }
        .voice-selector {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(120px, 1fr));
            gap: 8px;
            margin-bottom: 15px;
        }
        .voice-btn {
            background: rgba(255,255,255,0.15);
            border: 2px solid transparent;
            border-radius: 12px;
            padding: 10px 8px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .voice-btn:hover { background: rgba(255,255,255,0.25); }
        .voice-btn.active {
            background: rgba(255,255,255,0.3);
            border-color: #00ffff;
            box-shadow: 0 0 20px rgba(0,255,255,0.4);
        }
        .chat-container {
            flex: 1;
            background: rgba(255,255,255,0.1);
            border-radius: 20px;
            padding: 20px;
            backdrop-filter: blur(15px);
            overflow-y: auto;
            border: 1px solid rgba(255,255,255,0.2);
        }
        .message {
            margin: 10px 0;
            padding: 12px 18px;
            border-radius: 18px;
            max-width: 80%;
            animation: slideIn 0.4s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(15px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            background: linear-gradient(45deg, #4facfe, #00f2fe);
            margin-left: auto;
            text-align: right;
            box-shadow: 0 4px 15px rgba(79, 172, 254, 0.3);
        }
        .ai-message {
            background: rgba(255,255,255,0.18);
            border-left: 4px solid #00ffff;
        }
        .live-controls {
            display: flex;
            gap: 10px;
            align-items: center;
            padding: 15px;
            background: rgba(0,0,0,0.3);
            border-radius: 25px;
            backdrop-filter: blur(15px);
            position: sticky;
            bottom: 20px;
            margin-top: auto;
            z-index: 100;
        }
        .text-input {
            flex: 1;
            padding: 12px 20px;
            border-radius: 20px;
            border: 2px solid rgba(255,255,255,0.3);
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 15px;
        }
        .text-input:focus {
            outline: none;
            border-color: #00ffff;
            box-shadow: 0 0 15px rgba(0,255,255,0.3);
        }
        .text-input::placeholder { color: rgba(255,255,255,0.6); }
        .control-btn {
            background: linear-gradient(45deg, #ff6b6b, #ee5a24);
            border: none;
            border-radius: 50%;
            width: 50px;
            height: 50px;
            color: white;
            font-size: 18px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .control-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 0 20px rgba(255,107,107,0.5);
        }
        .control-btn.listening {
            background: linear-gradient(45deg, #00ff00, #32cd32);
            animation: pulse 1s infinite;
        }
        #continuousBtn {
            background: linear-gradient(45deg, #28a745, #20c997);
            border-radius: 25px;
            width: auto;
            padding: 8px 12px;
            font-size: 14px;
            min-width: 60px;
        }
        #continuousBtn.active {
            background: linear-gradient(45deg, #ff4444, #dc3545);
        }
        .audio-player {
            margin: 8px 0;
            width: 100%;
            border-radius: 8px;
        }
        .typing-indicator {
            font-style: italic;
            opacity: 0.8;
            color: #00ffff;
        }
        .live-status {
            position: fixed;
            bottom: 20px;
            right: 20px;
            background: rgba(0,0,0,0.8);
            padding: 10px 15px;
            border-radius: 20px;
            font-size: 12px;
        }
        .floating-mic {
            position: fixed;
            bottom: 100px;
            right: 30px;
            background: linear-gradient(45deg, #ff4444, #cc0000);
            border: none;
            border-radius: 50%;
            width: 70px;
            height: 70px;
            color: white;
            font-size: 24px;
            cursor: pointer;
            transition: all 0.3s ease;
            z-index: 1000;
            box-shadow: 0 4px 20px rgba(255,68,68,0.4);
        }
        .floating-mic:hover {
            transform: scale(1.1);
            box-shadow: 0 6px 30px rgba(255,68,68,0.6);
        }
        .floating-mic.listening {
            background: linear-gradient(45deg, #00ff00, #32cd32);
            animation: pulse 1s infinite;
        }
    </style>
</head>
<body>
    <div class="live-header">
        <div class="live-indicator">🔴 LIVE</div>
        <h1>🎙️ LIVE Orpheus Voice Chat</h1>
        <p>Real-time voice conversation with AI personalities</p>
    </div>
    
    <div class="container">
        <div class="voice-selector">
            <div class="voice-btn active" data-voice="tara">
                <div>👩‍💼 Tara</div>
                <small>Warm & Engaging</small>
            </div>
            <div class="voice-btn" data-voice="jess">
                <div>😊 Jessica</div>
                <small>Bubbly & Fun</small>
            </div>
            <div class="voice-btn" data-voice="leo">
                <div>🧔 Leo</div>
                <small>Thoughtful & Wise</small>
            </div>
            <div class="voice-btn" data-voice="dan">
                <div>👨 Daniel</div>
                <small>Casual & Funny</small>
            </div>
            <div class="voice-btn" data-voice="mia">
                <div>🎨 Mia</div>
                <small>Creative & Artistic</small>
            </div>
            <div class="voice-btn" data-voice="leah">
                <div>👩‍🎓 Leah</div>
                <small>Gentle & Caring</small>
            </div>
            <div class="voice-btn" data-voice="zac">
                <div>🧑‍💻 Zachary</div>
                <small>Tech & Modern</small>
            </div>
            <div class="voice-btn" data-voice="zoe">
                <div>👩‍🎨 Zoe</div>
                <small>Witty & Clever</small>
            </div>
        </div>
        
        <div class="chat-container" id="chatArea">
            <div class="message ai-message">
                <strong>🎭 Live Orpheus System:</strong> Welcome to live voice chat! Choose a personality above and start talking. 
                You can type or use voice input for a natural conversation experience! 🎤✨
            </div>
        </div>
        
        <div class="live-controls">
            <input type="text" class="text-input" id="textInput" 
                   placeholder="Type your message or use voice input..."
                   onkeypress="handleKeyPress(event)">
            <button class="control-btn" id="voiceBtn" onclick="toggleVoiceInput()" title="Voice Input">🎤</button>
            <button class="control-btn" onclick="sendMessage()" title="Send Message">📤</button>
            <button class="control-btn" id="continuousBtn" onclick="toggleContinuous()" title="Auto-Chat Mode">🔁</button>
        </div>
    </div>
    
    <div class="live-status" id="liveStatus">
        Ready for conversation
    </div>
    
    <button class="floating-mic" id="floatingMic" onclick="toggleVoiceInput()" title="Voice Input (Always Available)">
        🎤
    </button>

    <script>
        let selectedVoice = 'tara';
        let isProcessing = false;
        let isListening = false;
        let continuousMode = false;
        
        // Toggle continuous conversation mode
        function toggleContinuous() {
            continuousMode = !continuousMode;
            const btn = document.getElementById('continuousBtn');
            if (continuousMode) {
                btn.textContent = '🔁 Stop Auto-Chat';
                btn.style.background = '#ff4444';
                updateStatus('Continuous mode ON - say something to start!');
            } else {
                btn.textContent = '🔁 Auto-Chat';
                btn.style.background = '#007bff';
                updateStatus('Continuous mode OFF');
            }
        }
        
        // Voice selection
        document.querySelectorAll('.voice-btn').forEach(btn => {
            btn.addEventListener('click', () => {
                document.querySelectorAll('.voice-btn').forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                selectedVoice = btn.dataset.voice;
                updateStatus(`Switched to ${selectedVoice.charAt(0).toUpperCase() + selectedVoice.slice(1)}`);
            });
        });
        
        function updateStatus(message) {
            document.getElementById('liveStatus').textContent = message;
        }
        
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
            
            addMessage(message, 'user');
            addTypingIndicator();
            updateStatus('AI is responding...');
            
            try {
                const response = await fetch('/live-chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        voice: selectedVoice
                    })
                });
                
                const data = await response.json();
                removeTypingIndicator();
                
                if (data.success) {
                    addMessage(data.response, 'ai');
                    
                    if (data.audio_url) {
                        addAudioPlayer(data.audio_url);
                        updateStatus('Playing response...');
                        
                        // Auto-listen for next response after audio finishes
                        setTimeout(() => {
                            updateStatus('Ready - say something to continue...');
                            // Auto-start listening for continuous conversation
                            if (continuousMode) {
                                setTimeout(() => {
                                    if (!isProcessing && !isListening) {
                                        startVoiceInput();
                                    }
                                }, 2000); // Wait 2 seconds after audio
                            }
                        }, 3000); // Estimate audio duration
                    }
                } else {
                    addMessage(`Error: ${data.error}`, 'ai');
                }
                
            } catch (error) {
                removeTypingIndicator();
                addMessage('Connection error. Please try again.', 'ai');
                updateStatus('Connection error');
            }
            
            isProcessing = false;
            updateStatus('Ready for conversation');
        }
        
        function toggleVoiceInput() {
            const voiceBtn = document.getElementById('voiceBtn');
            const floatingMic = document.getElementById('floatingMic');
            
            if (!isListening) {
                startVoiceInput();
            } else {
                stopVoiceInput();
            }
        }
        
        function startVoiceInput() {
            if (!('webkitSpeechRecognition' in window) && !('SpeechRecognition' in window)) {
                alert('Speech recognition not supported in this browser');
                return;
            }
            
            const recognition = new (window.SpeechRecognition || window.webkitSpeechRecognition)();
            recognition.continuous = false;
            recognition.interimResults = false;
            recognition.lang = 'en-US';
            
            const voiceBtn = document.getElementById('voiceBtn');
            const floatingMic = document.getElementById('floatingMic');
            
            // Update both buttons
            if (voiceBtn) {
                voiceBtn.classList.add('listening');
                voiceBtn.innerHTML = '🔴';
            }
            floatingMic.classList.add('listening');
            floatingMic.innerHTML = '🔴';
            
            isListening = true;
            updateStatus('Listening...');
            
            recognition.onresult = function(event) {
                const text = event.results[0][0].transcript;
                document.getElementById('textInput').value = text;
                updateStatus('Voice input received - sending to AI...');
                
                // Auto-send message after speech recognition
                setTimeout(() => {
                    sendMessage();
                }, 500); // Small delay for better UX
            };
            
            recognition.onerror = function(event) {
                updateStatus('Voice input error');
                stopVoiceInput();
            };
            
            recognition.onend = function() {
                stopVoiceInput();
            };
            
            recognition.start();
            
            // Auto-stop after 10 seconds
            setTimeout(() => {
                if (isListening) {
                    recognition.stop();
                }
            }, 10000);
        }
        
        function stopVoiceInput() {
            const voiceBtn = document.getElementById('voiceBtn');
            const floatingMic = document.getElementById('floatingMic');
            
            // Update both buttons
            if (voiceBtn) {
                voiceBtn.classList.remove('listening');
                voiceBtn.innerHTML = '🎤';
            }
            floatingMic.classList.remove('listening');
            floatingMic.innerHTML = '🎤';
            
            isListening = false;
            updateStatus('Ready for conversation');
        }
        
        function addMessage(text, sender) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            const senderName = sender === 'user' ? 'You' : 
                              `${selectedVoice.charAt(0).toUpperCase()}${selectedVoice.slice(1)}`;
            
            messageDiv.innerHTML = `<strong>${senderName}:</strong> ${text}`;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function addTypingIndicator() {
            const chatArea = document.getElementById('chatArea');
            const typingDiv = document.createElement('div');
            typingDiv.className = 'message ai-message typing-indicator';
            typingDiv.id = 'typing';
            typingDiv.innerHTML = `<strong>${selectedVoice.charAt(0).toUpperCase()}${selectedVoice.slice(1)}:</strong> <em>is thinking...</em>`;
            chatArea.appendChild(typingDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function removeTypingIndicator() {
            const typing = document.getElementById('typing');
            if (typing) typing.remove();
        }
        
        function addAudioPlayer(audioUrl) {
            const chatArea = document.getElementById('chatArea');
            const audioDiv = document.createElement('div');
            audioDiv.innerHTML = `
                <audio controls class="audio-player" autoplay>
                    <source src="${audioUrl}" type="audio/wav">
                    Audio not supported
                </audio>
            `;
            chatArea.appendChild(audioDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        // Auto-scroll chat
        setInterval(() => {
            const chatArea = document.getElementById('chatArea');
            chatArea.scrollTop = chatArea.scrollHeight;
        }, 1000);
    </script>
</body>
</html>
    """)

@app.route('/live-chat', methods=['POST'])
def live_chat_endpoint():
    """Live chat endpoint with enhanced interactivity"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        voice = data.get('voice', 'tara')
        conversation_id = data.get('conversation_id', 'live')
        
        if not user_message:
            return jsonify({"success": False, "error": "No message provided"})
        
        logger.info(f"🎙️ LIVE Chat: {user_message[:50]}... (voice: {voice})")
        
        # Generate live response
        ai_response = live_chat.generate_live_response(user_message, voice, conversation_id)
        
        # Generate speech
        audio_bytes, error = live_chat.speak_text(ai_response, voice)
        
        response_data = {
            "success": True,
            "response": ai_response,
            "voice": voice,
            "mode": "live"
        }
        
        if audio_bytes:
            audio_filename = f"live_audio_{int(time.time())}_{voice}.wav"
            audio_path = os.path.join(os.getcwd(), audio_filename)
            
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
            
            response_data["audio_url"] = f"/audio/{audio_filename}"
        elif error:
            response_data["error"] = error
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ Live chat error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/voice-input', methods=['POST'])
def voice_input():
    """Process voice input"""
    try:
        # This would handle voice input from browser
        # For now, return success
        return jsonify({"success": True, "message": "Voice input received"})
    except Exception as e:
        return jsonify({"success": False, "error": str(e)})

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve audio files"""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='audio/wav')
        else:
            return "Audio file not found", 404
    except Exception as e:
        return "Error serving audio", 500

@app.route('/system-status')
def system_status():
    """Get current TTS system status"""
    try:
        status = {
            "tts_system": live_chat.tts_system,
            "openvoice_available": hasattr(live_chat, 'orpheus_tts') and live_chat.orpheus_tts is not None,
            "models_loaded": False,
            "system_info": {
                "real_orpheus": False,
                "edge_tts_fallback": True,
                "emotion_synthesis": "basic"
            }
        }
        
        if live_chat.orpheus_tts:
            status["models_loaded"] = getattr(live_chat.orpheus_tts, 'models_loaded', False)
            if status["models_loaded"]:
                status["system_info"] = {
                    "real_orpheus": True,
                    "edge_tts_fallback": False,
                    "emotion_synthesis": "authentic",
                    "available_emotions": ["default", "whispering", "cheerful", "terrified", "angry", "sad", "friendly"]
                }
        
        return jsonify(status)
    except Exception as e:
        return jsonify({"error": str(e)})

if __name__ == '__main__':
    print("\n🎙️ LIVE ORPHEUS VOICE CHAT STARTING...")
    print("=" * 60)
    print("🎯 LIVE INTERACTIVE FEATURES:")
    print("  ✅ Real-time voice conversation")
    print("  ✅ Speech-to-text input")
    print("  ✅ Enhanced personality responses") 
    print("  ✅ Live conversation flow")
    print("  ✅ Interactive voice controls")
    print("  ✅ Natural dialogue patterns")
    print("=" * 60)
    
    # Show TTS system status
    if live_chat.tts_system == "openvoice":
        print("🎭 TTS SYSTEM: Real OpenVoice/Orpheus TTS")
        print("  ✅ Authentic emotional synthesis")
        print("  ✅ Human-like laughter and expressions")
        print("  ✅ Advanced voice cloning")
    else:
        print("🎤 TTS SYSTEM: Edge TTS (Fallback)")
        print("  ⚠️  Basic emotion simulation")
        print("  💡 Install OpenVoice for authentic emotions")
    print("=" * 60)
    
    # Get port from environment (Cloud Run compatibility) or default to 5000 for local
    port = int(os.environ.get('PORT', 5000))
    host = '0.0.0.0'
    
    if port == 5000:
        print(f"\n🌐 Starting LOCAL server on http://127.0.0.1:{port}")
    else:
        print(f"\n🌐 Starting CLOUD server on port {port}")
    
    print("🎤 Experience truly interactive Orpheus conversations!")
    
    app.run(debug=False, host=host, port=port, threaded=True)
