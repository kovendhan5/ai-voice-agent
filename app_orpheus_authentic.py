"""
Real Orpheus TTS Implementation - Authentic Voice AI with Human-like Speech
Built using the actual orpheus-speech package from canopylabs/orpheus-tts
"""

from flask import Flask, request, Response, jsonify, send_file
from flask_cors import CORS
import json
import os
import tempfile
import wave
import time
import io
import threading
import queue
from datetime import datetime
import traceback

# Orpheus TTS imports with fallback handling
try:
    from orpheus_tts import OrpheusModel
    import torch
    ORPHEUS_AVAILABLE = True
    print("✅ Orpheus TTS package found!")
except ImportError as e:
    ORPHEUS_AVAILABLE = False
    print(f"⚠️ Orpheus TTS not available: {e}")
    print("📝 Using mock implementation for testing")

# Alternative text generation imports (optional)
TRANSFORMERS_AVAILABLE = False
try:
    # Only try to import if not causing DLL issues
    import os
    if os.environ.get('DISABLE_TRANSFORMERS', '').lower() != 'true':
        from transformers import pipeline
        TRANSFORMERS_AVAILABLE = True
        print("✅ Transformers package found!")
    else:
        print("⚠️ Transformers disabled via environment variable")
except Exception as e:
    TRANSFORMERS_AVAILABLE = False
    print(f"⚠️ Transformers not available ({str(e)[:50]}...), using simple responses")

app = Flask(__name__)
CORS(app)

# Mock Orpheus implementation for fallback
class MockOrpheusModel:
    def __init__(self):
        self.model_name = "mock-orpheus"
        print("🎭 Mock Orpheus Model created (for testing)")
    
    def generate_speech(self, prompt, voice="tara", **kwargs):
        """Generate mock speech for testing - completely silent audio"""
        import time
        import numpy as np
        
        print(f"🎭 Mock generating SILENT audio for: '{prompt[:50]}...' with voice '{voice}'")
        print("⚠️ MOCK MODEL ACTIVE - Generating silence (no weird noise)")
        print("🔧 To get real voice: Check if Orpheus TTS model loads properly")
        
        # Generate completely silent audio
        sample_rate = 24000
        duration = max(1.0, len(prompt) * 0.05)  # Roughly 0.05 seconds per character
        
        # Create pure silence - no noise at all
        audio_data = np.zeros(int(sample_rate * duration), dtype=np.float32)
        
        # Convert to 16-bit integers
        audio_int16 = (audio_data * 32767).astype(np.int16)
        audio_bytes = audio_int16.tobytes()
        
        print(f"📊 Generated {duration:.1f}s of SILENT audio ({len(audio_bytes)} bytes)")
        return audio_bytes

# Initialize Orpheus Model lazily
print("🎭 Orpheus TTS Server Starting...")
print("📦 Will load model on first request for faster startup...")

# Global model variable - will be loaded on first use
orpheus_model = None

def get_orpheus_model():
    """Load Orpheus model lazily on first use"""
    global orpheus_model
    if orpheus_model is None:
        print("🔄 Loading Orpheus model for first time...")
        print("📦 Attempting to load REAL Orpheus TTS model...")
        
        if not ORPHEUS_AVAILABLE:
            print("⚠️ Orpheus TTS package not available, using mock model")
            print("🔧 To get real voice: pip install orpheus-speech")
            orpheus_model = MockOrpheusModel()
            return orpheus_model
            
        try:
            print("🎯 Loading canopylabs/orpheus-tts-0.1-finetune-prod...")
            print("📥 This may take a moment to download model weights...")
            
            # Use the production finetuned model for best quality
            orpheus_model = OrpheusModel(
                model_name="canopylabs/orpheus-tts-0.1-finetune-prod"
            )
            print("✅ SUCCESS! Real Orpheus Model loaded - you'll get human-like voice!")
            print(f"🎯 Model type: {type(orpheus_model)}")
            
            # Test the model to make sure it works
            try:
                print("🧪 Testing model with sample text...")
                test_result = orpheus_model.generate_speech(
                    text="Test",
                    voice="tara"
                )
                print(f"✅ Model test successful! Output type: {type(test_result)}")
            except Exception as test_error:
                print(f"⚠️ Model test failed: {test_error}")
                
        except Exception as e:
            print(f"❌ Error loading primary model: {e}")
            print(f"� Full error details: {str(e)}")
            print("�🔄 Trying alternative model names...")
            
            # Try different model names that might work
            alternative_models = [
                "canopylabs/orpheus-3b-0.1-ft",
                "orpheus-tts",
                "canopylabs/orpheus-base"
            ]
            
            model_loaded = False
            for alt_model in alternative_models:
                try:
                    print(f"🔄 Trying {alt_model}...")
                    orpheus_model = OrpheusModel(model_name=alt_model)
                    print(f"✅ SUCCESS! Loaded {alt_model}")
                    model_loaded = True
                    break
                except Exception as e2:
                    print(f"❌ {alt_model} failed: {e2}")
            
            if not model_loaded:
                print("❌ All Orpheus models failed to load")
                print("🔧 Using mock model (SILENT audio)")
                print("💡 Solutions:")
                print("   1. Try: pip install --upgrade orpheus-speech")
                print("   2. Check internet connection for model download")
                print("   3. Check available disk space")
                orpheus_model = MockOrpheusModel()
                
    return orpheus_model

# Available voices with personality descriptions
ORPHEUS_VOICES = {
    "tara": "🎭 Natural, conversational, warm - perfect for daily conversations",
    "zac": "🎯 Clear, confident, engaging - great for explanations",
    "jess": "✨ Friendly, expressive, bubbly - excellent for upbeat content",
    "leo": "🎪 Deep, authoritative, calm - ideal for serious topics",
    "mia": "🌟 Soft, gentle, caring - perfect for supportive responses",
    "leah": "🎨 Dynamic, versatile, expressive - great for storytelling",
    "zoe": "🎵 Young, energetic, playful - fun for casual chats",
    "dan": "🎬 Mature, professional, reliable - business conversations"
}

# Emotion tags for natural speech
EMOTION_TAGS = [
    "<laugh>", "<chuckle>", "<sigh>", "<cough>", 
    "<sniffle>", "<groan>", "<yawn>", "<gasp>"
]

def add_natural_expressions(text, emotion_level=0.3):
    """Add natural expressions and emotions to text for more human-like speech"""
    import random
    
    if not text or emotion_level <= 0:
        return text
    
    # Natural conversation fillers and expressions
    fillers = ["um,", "uh,", "well,", "you know,", "like,", "so,"]
    reactions = ["<chuckle>", "<laugh>", "<sigh>"]
    
    words = text.split()
    if len(words) < 5:
        return text
    
    # Add some natural pauses and expressions
    enhanced_text = []
    for i, word in enumerate(words):
        enhanced_text.append(word)
        
        # Randomly add expressions based on emotion level
        if random.random() < emotion_level:
            if i > 0 and i < len(words) - 1:
                if random.random() < 0.3:  # Add filler
                    enhanced_text.append(random.choice(fillers))
                elif random.random() < 0.2:  # Add reaction
                    enhanced_text.append(random.choice(reactions))
    
    return " ".join(enhanced_text)

def generate_orpheus_speech(text, voice="tara", add_emotions=True):
    """Generate speech using authentic Orpheus TTS"""
    try:
        # Get the model (loads lazily on first use)
        model = get_orpheus_model()
        
        # Add natural expressions for more human-like speech
        if add_emotions:
            text = add_natural_expressions(text, emotion_level=0.4)
        
        print(f"🎭 Generating speech with voice '{voice}': {text[:100]}...")
        
        # Check if we're using the mock model
        if hasattr(model, 'model_name') and model.model_name == "mock-orpheus":
            print("⚠️ Using mock model - generating silent audio")
            print("🔧 To get real voice, ensure Orpheus TTS loads successfully")
            audio_data = model.generate_speech(text, voice, add_emotions=add_emotions)
            
            # Create a proper WAV file from the mock audio
            audio_buffer = io.BytesIO()
            with wave.open(audio_buffer, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(24000)  # 24kHz sample rate
                wf.writeframes(audio_data)
            
            audio_buffer.seek(0)
            return audio_buffer.getvalue()
        
        print("🎯 Using REAL Orpheus TTS model for human-like voice!")
        
        # Generate speech tokens using the real Orpheus model
        start_time = time.time()
        
        # Call the Orpheus model with the correct parameters
        print(f"🎯 Calling Orpheus model.generate_speech(text='{text[:30]}...', voice='{voice}')")
        try:
            # Try with minimal parameters first (based on Orpheus examples)
            speech_tokens = model.generate_speech(
                text=text,
                voice=voice
            )
        except Exception as param_error:
            print(f"⚠️ Parameter error: {param_error}")
            # Try with alternative parameter names
            try:
                speech_tokens = model.generate_speech(
                    prompt=text,
                    voice=voice
                )
            except Exception as alt_error:
                print(f"⚠️ Alternative parameters failed: {alt_error}")
                # Try with just text parameter
                speech_tokens = model.generate_speech(text)
        
        # Collect audio chunks and write to WAV
        audio_buffer = io.BytesIO()
        
        print(f"📊 Processing Orpheus model output...")
        
        # Check if speech_tokens is iterable (generator) or direct audio data
        try:
            # Try to iterate (if it's a generator)
            with wave.open(audio_buffer, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(24000)  # 24kHz sample rate
                
                total_frames = 0
                chunk_count = 0
                
                for audio_chunk in speech_tokens:
                    if audio_chunk:
                        chunk_count += 1
                        if isinstance(audio_chunk, bytes):
                            wf.writeframes(audio_chunk)
                            total_frames += len(audio_chunk) // 2  # 16-bit = 2 bytes per sample
                        else:
                            # Convert numpy array to bytes if needed
                            import numpy as np
                            if isinstance(audio_chunk, np.ndarray):
                                audio_bytes = (audio_chunk * 32767).astype(np.int16).tobytes()
                                wf.writeframes(audio_bytes)
                                total_frames += len(audio_chunk)
                        
                        # Progress feedback
                        if chunk_count % 10 == 0:
                            print(f"📊 Processed {chunk_count} audio chunks...")
                            
        except TypeError:
            # speech_tokens is not iterable, might be direct audio data
            print("📝 Direct audio data returned")
            with wave.open(audio_buffer, 'wb') as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(24000)  # 24kHz sample rate
                
                if isinstance(speech_tokens, bytes):
                    wf.writeframes(speech_tokens)
                    total_frames = len(speech_tokens) // 2
                else:
                    # Convert to bytes if it's a numpy array
                    import numpy as np
                    if isinstance(speech_tokens, np.ndarray):
                        audio_bytes = (speech_tokens * 32767).astype(np.int16).tobytes()
                        wf.writeframes(audio_bytes)
                        total_frames = len(speech_tokens)
                    else:
                        raise ValueError(f"Unexpected audio format: {type(speech_tokens)}")
        
        generation_time = time.time() - start_time
        duration = total_frames / 24000 if total_frames > 0 else 0
        
        print(f"✅ Generated {duration:.2f}s of audio in {generation_time:.2f}s")
        print(f"📈 Real-time factor: {generation_time/duration:.2f}x" if duration > 0 else "")
        
        audio_buffer.seek(0)
        return audio_buffer.getvalue()
        
    except Exception as e:
        print(f"❌ Error generating speech: {e}")
        traceback.print_exc()
        raise

# Enhanced text generation system
class TextGenerator:
    def __init__(self):
        self.generator = None
        
        # Enhanced fallback responses with better variety
        self.response_templates = {
            'questions': [
                "That's a really interesting question! {topic} is something I think about often.",
                "You know, {topic} is fascinating. What got you interested in that?",
                "Great question about {topic}! I'd love to hear your thoughts on it.",
                "That's a thoughtful question! {topic} is quite complex, isn't it?"
            ],
            'statements': [
                "That's really insightful! You've given me something to think about regarding {topic}.",
                "I find {topic} quite interesting too. What's your experience with it?",
                "You make a good point about {topic}. I hadn't considered that perspective.",
                "That's fascinating! {topic} is something that really interests me as well."
            ],
            'greetings': [
                "Hello there! <chuckle> It's great to chat with you today!",
                "Hey! <smile> How are you doing? I'm excited to talk!",
                "Hi! <warm> What's on your mind today?",
                "Hello! <friendly> Thanks for chatting with me!"
            ],
            'general': [
                "That's really interesting! Tell me more about what you're thinking.",
                "I appreciate you sharing that with me. <thoughtful> What else is on your mind?",
                "You know, that's exactly the kind of thing I enjoy discussing! <chuckle>",
                "That's a great point! <smile> I'd love to hear more of your thoughts."
            ]
        }
        
        # Try to initialize transformers text generation if available
        if TRANSFORMERS_AVAILABLE:
            try:
                print("🤖 Loading text generation model...")
                self.generator = pipeline(
                    "text-generation",
                    model="microsoft/DialoGPT-medium",
                    pad_token_id=50256
                )
                print("✅ Text generation model loaded!")
            except Exception as e:
                print(f"⚠️ Failed to load text generation model: {e}")
                print("📝 Using enhanced fallback responses")
    
    def extract_topic(self, text):
        """Extract key topic from user input"""
        # Simple keyword extraction
        words = text.lower().replace('?', '').replace('.', '').replace('!', '').split()
        
        # Filter out common words
        stop_words = {'the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'in', 'with', 'to', 'for', 'of', 'as', 'by', 'that', 'this', 'it', 'from', 'they', 'we', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'shall', 'i', 'you', 'he', 'she', 'him', 'her', 'his', 'hers', 'my', 'your', 'our', 'their'}
        
        meaningful_words = [w for w in words if w not in stop_words and len(w) > 2]
        
        if meaningful_words:
            return ' '.join(meaningful_words[:3])  # Take first 3 meaningful words
        return 'that'
    
    def classify_input(self, text):
        """Classify the type of user input"""
        text_lower = text.lower().strip()
        
        if any(greeting in text_lower for greeting in ['hello', 'hi', 'hey', 'good morning', 'good afternoon']):
            return 'greetings'
        elif '?' in text:
            return 'questions'
        elif any(word in text_lower for word in ['i think', 'i believe', 'in my opinion', 'i feel']):
            return 'statements'
        else:
            return 'general'
    
    def generate_response(self, text, personality="friendly"):
        """Generate a conversational response"""
        if self.generator and TRANSFORMERS_AVAILABLE:
            try:
                # Use the transformers pipeline for generation
                prompt = f"Human: {text}\nAssistant:"
                response = self.generator(
                    prompt,
                    max_length=len(prompt.split()) + 50,
                    num_return_sequences=1,
                    temperature=0.7,
                    do_sample=True,
                    pad_token_id=50256
                )
                
                generated_text = response[0]['generated_text']
                # Extract just the assistant's response
                if "Assistant:" in generated_text:
                    response_text = generated_text.split("Assistant:")[-1].strip()
                    if response_text:
                        return self.add_personality(response_text, personality)
            except Exception as e:
                print(f"⚠️ Text generation error: {e}")
        
        # Enhanced fallback to intelligent responses
        import random
        
        # Classify the input and extract topic
        input_type = self.classify_input(text)
        topic = self.extract_topic(text)
        
        # Select appropriate template
        templates = self.response_templates.get(input_type, self.response_templates['general'])
        template = random.choice(templates)
        
        # Fill in the topic
        if '{topic}' in template:
            base_response = template.format(topic=topic)
        else:
            base_response = template
        
        return self.add_personality(base_response, personality)
    
    def add_personality(self, text, personality):
        """Add personality-specific touches to responses"""
        fillers = {
            "friendly": ["Well, ", "You know, ", "Actually, ", "I think "],
            "excited": ["Oh wow! ", "That's amazing! ", "Incredible! ", "Fantastic! "],
            "thoughtful": ["Hmm, ", "Let me see... ", "That's interesting... ", "I wonder... "],
            "casual": ["Yeah, ", "So, ", "Like, ", "Totally! "]
        }
        
        emotions = {
            "friendly": ["<smile>", "<chuckle>", "<warm>"],
            "excited": ["<laugh>", "<gasp>", "<excitement>"],
            "thoughtful": ["<pause>", "<hmm>", "<thoughtful>"],
            "casual": ["<casual>", "<relaxed>", "<easy>"]
        }
        
        import random
        
        # Add filler words (30% chance)
        if personality in fillers and random.random() < 0.3:
            filler = random.choice(fillers[personality])
            if not text.startswith(filler.strip()):
                text = filler + text
        
        # Add emotional tags (40% chance)
        if personality in emotions and random.random() < 0.4:
            emotion = random.choice(emotions[personality])
            # Insert emotion tag randomly in the text
            words = text.split()
            if len(words) > 3:
                insert_pos = random.randint(1, len(words) - 2)
                words.insert(insert_pos, emotion)
                text = " ".join(words)
        
        return text

# Initialize text generator
text_generator = TextGenerator()

@app.route('/')
def index():
    """Serve the interactive voice chat interface"""
    try:
        with open('voice_chat_interface.html', 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return """
        <html>
        <head><title>🎭 Orpheus Voice Chat</title></head>
        <body style="font-family: Arial; padding: 40px; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white;">
            <h1>🎭 Orpheus Voice Chat</h1>
            <p>❌ Interface file not found. Please ensure voice_chat_interface.html exists.</p>
            <h3>Available API Endpoints:</h3>
            <ul>
                <li><strong>POST /chat</strong> - AI conversation with voice response</li>
                <li><strong>POST /synthesize</strong> - Generate speech</li>
                <li><strong>GET /voices</strong> - List available voices</li>
                <li><strong>GET /status</strong> - Server status</li>
            </ul>
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
        add_emotions = data.get('add_emotions', True)
        
        # Validate voice
        if voice not in ORPHEUS_VOICES:
            return jsonify({
                'error': f'Invalid voice. Available voices: {list(ORPHEUS_VOICES.keys())}'
            }), 400
        
        # Generate speech
        audio_data = generate_orpheus_speech(text, voice, add_emotions)
        
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
    return jsonify({
        'voices': ORPHEUS_VOICES,
        'total_voices': len(ORPHEUS_VOICES),
        'emotion_tags': EMOTION_TAGS,
        'model': 'canopylabs/orpheus-tts-0.1-finetune-prod'
    })

@app.route('/chat', methods=['POST'])
def chat():
    """AI conversation with voice response"""
    try:
        data = request.get_json()
        if not data or 'message' not in data:
            return jsonify({'error': 'Message is required'}), 400
        
        user_message = data['message']
        voice = data.get('voice', 'tara')
        
        # Determine personality based on voice
        voice_personalities = {
            'tara': 'friendly',
            'zac': 'casual',
            'jess': 'excited',
            'leo': 'thoughtful',
            'mia': 'friendly',
            'leah': 'excited',
            'zoe': 'casual',
            'dan': 'thoughtful'
        }
        
        personality = voice_personalities.get(voice, 'friendly')
        
        # Generate AI response using our enhanced text generator
        ai_response = text_generator.generate_response(user_message, personality)
        
        # Generate speech
        audio_data = generate_orpheus_speech(ai_response, voice, add_emotions=True)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(audio_data)
            temp_path = f.name
        
        def cleanup():
            try:
                os.unlink(temp_path)
            except:
                pass
        
        # Schedule cleanup
        threading.Timer(30.0, cleanup).start()
        
        return jsonify({
            'response': ai_response,
            'voice': voice,
            'personality': personality,
            'audio_url': f'/audio/{os.path.basename(temp_path)}',
            'timestamp': datetime.now().isoformat(),
            'generation_method': 'transformers' if text_generator.generator else 'fallback'
        })
        
    except Exception as e:
        print(f"❌ Chat error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/test', methods=['GET'])
def test_voices():
    """Test endpoint to hear all voices"""
    try:
        test_text = "Hello! <chuckle> This is a test of the authentic Orpheus TTS system. <laugh> Pretty amazing, right?"
        voice = request.args.get('voice', 'tara')
        
        if voice not in ORPHEUS_VOICES:
            voice = 'tara'
        
        audio_data = generate_orpheus_speech(test_text, voice, add_emotions=True)
        
        # Save to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            f.write(audio_data)
            temp_path = f.name
        
        def cleanup():
            try:
                os.unlink(temp_path)
            except:
                pass
        
        response = send_file(
            temp_path,
            mimetype='audio/wav',
            as_attachment=False
        )
        
        threading.Timer(30.0, cleanup).start()
        return response
        
    except Exception as e:
        print(f"❌ Test error: {e}")
        return jsonify({'error': str(e)}), 500

@app.route('/status', methods=['GET'])
def status():
    # Check if model is loaded yet
    model_loaded = orpheus_model is not None
    is_mock = False
    model_name = "canopylabs/orpheus-tts-0.1-finetune-prod (lazy loaded)"
    
    if model_loaded:
        is_mock = hasattr(orpheus_model, 'model_name') and orpheus_model.model_name == "mock-orpheus"
        model_name = orpheus_model.model_name if hasattr(orpheus_model, 'model_name') else "canopylabs/orpheus-tts-0.1-finetune-prod"
    
    model_info = {
        'status': 'running',
        'model': 'Mock Orpheus TTS' if is_mock else 'Authentic Orpheus TTS',
        'repo': model_name,
        'voices': len(ORPHEUS_VOICES),
        'emotions': len(EMOTION_TAGS),
        'features': [
            'Real human-like speech',
            'Natural emotions & laughter',
            'Multiple voice personalities',
            'Conversational expressions',
            'Enhanced text generation',
            'Lazy model loading for fast startup'
        ],
        'model_loaded': model_loaded,
        'is_mock': is_mock,
        'text_generation': 'transformers' if TRANSFORMERS_AVAILABLE else 'fallback',
        'timestamp': datetime.now().isoformat()
    }
    
    return jsonify(model_info)

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🎭 AUTHENTIC ORPHEUS TTS SERVER")
    print("="*60)
    print("🔥 Features:")
    print("   • Real human-like speech with emotions")
    print("   • Natural laughter and expressions")
    print("   • 8 unique voice personalities")
    print("   • Conversational AI responses")
    print("   • Production-quality TTS model")
    print("\n🎯 Model: canopylabs/orpheus-tts-0.1-finetune-prod")
    print("🌐 Server: http://localhost:8080")
    print("="*60)
    
    app.run(host='0.0.0.0', port=8080, debug=True, threaded=True)
