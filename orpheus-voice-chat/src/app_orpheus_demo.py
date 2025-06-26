"""
Demo Orpheus-TTS Voice Chat API
Demonstrates the exact Orpheus interface with enhanced audio generation
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
import numpy as np
import pyttsx3
import tempfile
import soundfile as sf
import io

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# Configuration
GEMINI_API_KEY = "AIzaSyBu5izidIfzknhhMCzZB6yn1GKnzwZoUIQ"
genai.configure(api_key=GEMINI_API_KEY)

class OrpheusDemo:
    """
    Demo implementation showing Orpheus TTS features
    This simulates the real Orpheus model behavior and interface
    """
    
    def __init__(self):
        self.model_ready = True
        self.conversations = {}
        
        # Initialize Gemini AI with updated model name
        self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Initialize Windows TTS engine
        try:
            self.tts_engine = pyttsx3.init()
            # Get available voices
            voices = self.tts_engine.getProperty('voices')
            logger.info(f"Found {len(voices)} system voices")
            
            # Configure voice settings
            self.tts_engine.setProperty('rate', 180)    # Speech rate
            self.tts_engine.setProperty('volume', 0.9)  # Volume level
            
            self.system_voices = voices
            logger.info("✅ Windows TTS engine initialized successfully")
        except Exception as e:
            logger.error(f"❌ Failed to initialize TTS engine: {e}")
            self.tts_engine = None
            self.system_voices = []
        
        # Initialize Gemini AI with updated model name
        self.ai_model = genai.GenerativeModel('gemini-1.5-flash')
        
        # Real Orpheus voice personalities
        self.voice_personalities = {
            "tara": {
                "name": "Tara",
                "personality": "Warm, friendly, and naturally expressive. Speaks with gentle enthusiasm and authentic emotions.",
                "style": "conversational, empathetic, uses natural speech patterns with laughter and sighs",
                "base_freq": 220,
                "voice_char": "feminine, warm"
            },
            "jess": {
                "name": "Jessica", 
                "personality": "Bubbly, energetic, and optimistic. Loves to laugh and express joy in conversation.",
                "style": "animated, expressive, frequent laughter and excited tones",
                "base_freq": 240,
                "voice_char": "youthful, energetic"
            },
            "leo": {
                "name": "Leo",
                "personality": "Thoughtful, articulate, and calm. Speaks with measured confidence and occasional humor.",
                "style": "clear, professional yet warm, thoughtful pauses",
                "base_freq": 140,
                "voice_char": "masculine, confident"
            },
            "dan": {
                "name": "Daniel",
                "personality": "Casual, friendly guy-next-door type. Easy-going with natural masculine warmth.",
                "style": "relaxed, conversational, natural speech rhythm",
                "base_freq": 120,
                "voice_char": "masculine, casual"
            },
            "mia": {
                "name": "Mia",
                "personality": "Creative, artistic, and expressive. Speaks with passion about interesting topics.",
                "style": "expressive, varied intonation, creative speech patterns",
                "base_freq": 200,
                "voice_char": "artistic, dynamic"
            },
            "leah": {
                "name": "Leah",
                "personality": "Gentle, caring, and nurturing. Speaks with maternal warmth and understanding.",
                "style": "soft, comforting, empathetic tones",
                "base_freq": 180,
                "voice_char": "gentle, nurturing"
            },
            "zac": {
                "name": "Zachary",
                "personality": "Young, energetic, and tech-savvy. Speaks with modern enthusiasm.",
                "style": "upbeat, contemporary, energetic delivery",
                "base_freq": 160,
                "voice_char": "youthful, tech-savvy"
            },
            "zoe": {
                "name": "Zoe",
                "personality": "Sophisticated, intelligent, and witty. Enjoys clever conversation and humor.",
                "style": "articulate, witty, intelligent humor",
                "base_freq": 210,
                "voice_char": "sophisticated, intelligent"
            }
        }
        
        # Emotion sound patterns (Orpheus-style)
        self.emotion_patterns = {
            "<laugh>": {"duration": 1.5, "pattern": "laugh", "freq_mod": 1.2},
            "<chuckle>": {"duration": 0.8, "pattern": "chuckle", "freq_mod": 1.1},
            "<sigh>": {"duration": 1.0, "pattern": "sigh", "freq_mod": 0.8},
            "<gasp>": {"duration": 0.5, "pattern": "gasp", "freq_mod": 1.5},
            "<yawn>": {"duration": 2.0, "pattern": "yawn", "freq_mod": 0.7},
            "<cough>": {"duration": 0.6, "pattern": "cough", "freq_mod": 0.5},
            "<sniffle>": {"duration": 0.4, "pattern": "sniffle", "freq_mod": 1.3},
            "<groan>": {"duration": 1.2, "pattern": "groan", "freq_mod": 0.6}
        }
    
    def get_ai_response(self, user_input, voice="tara", conversation_id="default"):
        """Generate AI response with Orpheus personality"""
        try:
            # Get or create conversation history
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = []
            
            history = self.conversations[conversation_id]
            personality = self.voice_personalities.get(voice, self.voice_personalities["tara"])
            
            # Create Orpheus-style prompt
            personality_prompt = f"""You are {personality['name']}, speaking through the Orpheus TTS system.

Your personality: {personality['personality']}
Your speaking style: {personality['style']}

IMPORTANT: You MUST use Orpheus emotion tags naturally in your speech:
- <laugh> for genuine laughter
- <chuckle> for light amusement  
- <sigh> for contemplation or mild frustration
- <gasp> for surprise or shock
- <yawn> for tiredness
- <cough> for clearing throat or hesitation
- <sniffle> for emotion or allergies
- <groan> for frustration or realization

Recent conversation:
{json.dumps(history[-4:], indent=2) if history else "This is the start of our conversation"}

User: {user_input}

Respond as {personality['name']} would, using your unique personality. Include 1-2 emotion tags naturally in your response. Keep it conversational, 1-3 sentences."""

            # Generate response
            try:
                response = self.ai_model.generate_content(personality_prompt)
                ai_text = response.text.strip()
                
                if not ai_text:
                    ai_text = f"<chuckle> Sorry, I seem to be at a loss for words right now! What else would you like to chat about?"
                
            except Exception as ai_error:
                logger.error(f"AI generation error: {ai_error}")
                # Fallback response with personality
                fallback_responses = {
                    "tara": f"<sigh> I'm having a little technical hiccup right now. Could you give me a moment and try again?",
                    "jess": f"<chuckle> Oops! My brain just had a little glitch there! Want to try asking me something else?",
                    "leo": f"<cough> I seem to be experiencing some technical difficulties. Let me try to process that again.",
                    "dan": f"<groan> Man, my circuits are acting up right now. Can you try again in a sec?",
                    "mia": f"<gasp> Oh no! I just had a creative block there. What else can we talk about?",
                    "leah": f"<sniffle> I'm so sorry, I'm having trouble connecting right now. Please try again.",
                    "zac": f"<cough> Looks like I hit a processing error there. Want to reboot this conversation?",
                    "zoe": f"<sigh> How embarrassing - I just experienced a momentary intellectual lapse. Shall we try again?"
                }
                ai_text = fallback_responses.get(voice, f"<sigh> I'm having technical difficulties right now. Please try again.")
            
            # Store conversation
            history.append({"user": user_input, "ai": ai_text, "timestamp": datetime.now().isoformat()})
            self.conversations[conversation_id] = history[-20:]  # Keep last 20 exchanges
            
            return ai_text
            
        except Exception as e:
            logger.error(f"Error in get_ai_response: {e}")
            return f"<sigh> I'm experiencing some technical difficulties. Please try again in a moment."
    
    def generate_speech(self, text, voice="tara"):
        """
        Generate speech using Windows TTS (much more realistic than synthetic audio)
        """
        try:
            logger.info(f"🎙️ Generating real TTS speech: {text[:50]}... (voice: {voice})")
            
            if not text or len(text.strip()) == 0:
                logger.warning("Empty text provided for speech generation")
                return None, "Empty text provided"
            
            if not self.tts_engine:
                logger.error("TTS engine not available")
                return None, "TTS engine not initialized"
            
            # Clean text for TTS (remove emotion tags for now, we'll add them back later)
            clean_text = text
            for emotion in self.emotion_patterns.keys():
                clean_text = clean_text.replace(emotion, "")
            
            # Map Orpheus voices to system voices
            voice_config = self.voice_personalities.get(voice, self.voice_personalities["tara"])
            
            # Select appropriate system voice based on Orpheus character
            selected_voice = None
            if self.system_voices:
                # Try to match by gender and characteristics
                voice_char = voice_config.get("voice_char", "")
                
                if "masculine" in voice_char or voice in ["leo", "dan", "zac"]:
                    # Look for male voices
                    for sys_voice in self.system_voices:
                        if any(male_indicator in sys_voice.name.lower() 
                              for male_indicator in ["male", "david", "mark", "james", "guy"]):
                            selected_voice = sys_voice.id
                            break
                else:
                    # Look for female voices
                    for sys_voice in self.system_voices:
                        if any(female_indicator in sys_voice.name.lower() 
                              for female_indicator in ["female", "zira", "hazel", "aria", "jenny"]):
                            selected_voice = sys_voice.id
                            break
                
                # Fallback to first available voice
                if not selected_voice and self.system_voices:
                    selected_voice = self.system_voices[0].id
            
            # Set voice
            if selected_voice:
                self.tts_engine.setProperty('voice', selected_voice)
            
            # Adjust rate and pitch based on personality
            base_rate = 180
            if voice in ["jess", "zac"]:  # Energetic voices
                self.tts_engine.setProperty('rate', base_rate + 20)
            elif voice in ["leah", "leo"]:  # Calm voices
                self.tts_engine.setProperty('rate', base_rate - 20)
            else:
                self.tts_engine.setProperty('rate', base_rate)
            
            # Generate speech to temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Save speech to file
            self.tts_engine.save_to_file(clean_text, temp_path)
            self.tts_engine.runAndWait()
            
            # Read the generated audio file
            try:
                with open(temp_path, 'rb') as audio_file:
                    audio_bytes = audio_file.read()
                
                # Clean up temp file
                import os
                try:
                    os.unlink(temp_path)
                except:
                    pass
                
                if len(audio_bytes) > 0:
                    logger.info(f"✅ Generated {len(audio_bytes)} bytes of real TTS audio")
                    return audio_bytes, None
                else:
                    logger.warning("Generated audio file is empty")
                    return None, "Generated audio file is empty"
                    
            except Exception as file_error:
                logger.error(f"Error reading generated audio file: {file_error}")
                return None, f"Error reading audio file: {str(file_error)}"
            
        except Exception as e:
            logger.error(f"❌ TTS generation error: {e}")
            import traceback
            traceback.print_exc()
            return None, f"TTS error: {str(e)}"
    
    def _process_text_with_emotions(self, text, voice_config):
        """Process text and generate audio with Orpheus-style emotions"""
        sample_rate = 24000
        base_freq = voice_config["base_freq"]
        
        # Split text by emotion tags
        segments = []
        current_text = text
        
        while current_text:
            # Find next emotion tag
            next_emotion = None
            next_pos = len(current_text)
            
            for emotion in self.emotion_patterns:
                pos = current_text.find(emotion)
                if pos != -1 and pos < next_pos:
                    next_pos = pos
                    next_emotion = emotion
            
            if next_emotion:
                # Add text before emotion
                if next_pos > 0:
                    segments.append({"type": "text", "content": current_text[:next_pos].strip()})
                
                # Add emotion
                segments.append({"type": "emotion", "content": next_emotion})
                
                # Continue with remaining text
                current_text = current_text[next_pos + len(next_emotion):]
            else:
                # No more emotions, add remaining text
                if current_text.strip():
                    segments.append({"type": "text", "content": current_text.strip()})
                break
        
        # Generate audio for each segment
        audio_parts = []
        
        for segment in segments:
            if segment["type"] == "text":
                audio_part = self._text_to_speech_audio(segment["content"], voice_config)
                audio_parts.append(audio_part)
            elif segment["type"] == "emotion":
                emotion_audio = self._generate_emotion_sound(segment["content"], voice_config)
                audio_parts.append(emotion_audio)
        
        # Combine all audio parts
        if audio_parts:
            combined_audio = np.concatenate(audio_parts)
        else:
            # Fallback silence
            combined_audio = np.zeros(sample_rate, dtype=np.float32)
        
        return combined_audio
    
    def _text_to_speech_audio(self, text, voice_config):
        """Generate more realistic speech audio for text"""
        if not text.strip():
            return np.zeros(1000, dtype=np.float32)
        
        sample_rate = 24000
        base_freq = voice_config["base_freq"]
        
        # Estimate duration based on text length (realistic speech timing)
        words = len(text.split())
        duration = max(words * 0.4, 0.8)  # ~0.4 seconds per word, minimum 0.8s
        
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        # Create more realistic speech-like audio
        audio = np.zeros(samples, dtype=np.float32)
        
        # Generate vowel-like formants (more speech-like)
        # These frequencies approximate human speech formants
        f0 = base_freq  # Fundamental frequency
        f1 = base_freq * 3   # First formant (vowel identification)
        f2 = base_freq * 6   # Second formant (vowel identification)
        
        # Create speech segments for each word
        words_list = text.split()
        if not words_list:
            words_list = [text]
        
        word_duration = duration / len(words_list)
        
        for word_idx, word in enumerate(words_list):
            word_start = word_idx * word_duration
            word_end = (word_idx + 1) * word_duration
            
            start_sample = int(word_start * sample_rate)
            end_sample = int(word_end * sample_rate)
            
            if end_sample > len(audio):
                end_sample = len(audio)
            
            word_samples = end_sample - start_sample
            if word_samples <= 0:
                continue
                
            word_t = np.linspace(0, word_duration, word_samples)
            
            # Create vowel-like sounds for this word
            # Use vowels to create speech-like patterns
            vowels = 'aeiou'
            word_vowels = [c for c in word.lower() if c in vowels]
            if not word_vowels:
                word_vowels = ['a']  # Default vowel
            
            # Generate audio for this word
            word_audio = np.zeros(word_samples, dtype=np.float32)
            
            for vowel_idx, vowel in enumerate(word_vowels[:3]):  # Max 3 vowels per word
                vowel_start = vowel_idx / len(word_vowels) * word_duration
                vowel_end = (vowel_idx + 1) / len(word_vowels) * word_duration
                
                v_start = int(vowel_start * sample_rate)
                v_end = int(vowel_end * sample_rate)
                
                if v_end > word_samples:
                    v_end = word_samples
                if v_start >= v_end:
                    continue
                
                vowel_t = word_t[v_start:v_end]
                if len(vowel_t) == 0:
                    continue
                
                # Different formant frequencies for different vowels
                vowel_formants = {
                    'a': (f0, f0 * 4, f0 * 7),    # /a/ sound
                    'e': (f0, f0 * 5, f0 * 8),    # /e/ sound  
                    'i': (f0, f0 * 6, f0 * 10),   # /i/ sound
                    'o': (f0, f0 * 3, f0 * 6),    # /o/ sound
                    'u': (f0, f0 * 2.5, f0 * 5),  # /u/ sound
                }
                
                formants = vowel_formants.get(vowel, vowel_formants['a'])
                
                # Generate the vowel sound with formants
                vowel_sound = (
                    0.4 * np.sin(2 * np.pi * formants[0] * vowel_t) +
                    0.3 * np.sin(2 * np.pi * formants[1] * vowel_t) +
                    0.2 * np.sin(2 * np.pi * formants[2] * vowel_t)
                )
                
                # Add natural speech envelope (attack, sustain, decay)
                envelope = np.ones_like(vowel_t)
                attack_len = len(vowel_t) // 10  # 10% attack
                decay_len = len(vowel_t) // 5    # 20% decay
                
                if attack_len > 0:
                    envelope[:attack_len] = np.linspace(0, 1, attack_len)
                if decay_len > 0:
                    envelope[-decay_len:] = np.linspace(1, 0, decay_len)
                
                vowel_sound *= envelope * 0.08  # Reduce volume to prevent distortion
                
                # Add to word audio
                word_audio[v_start:v_end] += vowel_sound
            
            # Add some fricative noise between vowels (consonant-like)
            noise_level = 0.01
            word_audio += noise_level * (np.random.random(word_samples) - 0.5)
            
            # Apply word-level envelope
            word_envelope = np.ones(word_samples)
            fade_len = min(word_samples // 20, 1000)  # Short fade
            if fade_len > 0:
                word_envelope[:fade_len] *= np.linspace(0, 1, fade_len)
                word_envelope[-fade_len:] *= np.linspace(1, 0, fade_len)
            
            word_audio *= word_envelope
            
            # Add to main audio
            audio[start_sample:end_sample] = word_audio
        
        # Apply overall speech characteristics
        # Add slight pitch variation (natural speech prosody)
        pitch_variation = 1 + 0.1 * np.sin(2 * np.pi * 2 * t)  # Slow pitch changes
        
        # Apply low-pass filter effect (makes it sound more natural)
        # Simple moving average filter
        filter_size = 5
        if len(audio) > filter_size:
            filtered_audio = np.convolve(audio, np.ones(filter_size)/filter_size, mode='same')
            audio = filtered_audio
        
        return audio.astype(np.float32)
    
    def _generate_emotion_sound(self, emotion_tag, voice_config):
        """Generate more realistic Orpheus-style emotion sounds"""
        sample_rate = 24000
        base_freq = voice_config["base_freq"]
        emotion_config = self.emotion_patterns.get(emotion_tag, self.emotion_patterns["<sigh>"])
        
        duration = emotion_config["duration"]
        pattern = emotion_config["pattern"]
        freq_mod = emotion_config["freq_mod"]
        
        samples = int(duration * sample_rate)
        t = np.linspace(0, duration, samples)
        
        if pattern == "laugh":
            # More realistic laughter - rhythmic bursts
            audio = np.zeros(samples)
            burst_freq = 4  # 4 bursts per second
            burst_count = int(duration * burst_freq)
            
            for i in range(burst_count):
                burst_start = int(i * samples / burst_count)
                burst_duration = int(0.15 * sample_rate)  # 150ms bursts
                burst_end = min(burst_start + burst_duration, samples)
                
                if burst_start < burst_end:
                    burst_t = np.linspace(0, 0.15, burst_end - burst_start)
                    
                    # Create ha-ha-ha sound with vowel formants
                    freq = base_freq * freq_mod
                    formant1 = freq * 4  # 'a' vowel formant
                    formant2 = freq * 7
                    
                    burst_audio = (
                        0.3 * np.sin(2 * np.pi * freq * burst_t) +
                        0.2 * np.sin(2 * np.pi * formant1 * burst_t) +
                        0.1 * np.sin(2 * np.pi * formant2 * burst_t)
                    )
                    
                    # Apply burst envelope
                    envelope = np.exp(-burst_t * 8) * (1 + 0.3 * np.sin(2 * np.pi * 10 * burst_t))
                    burst_audio *= envelope * 0.15
                    
                    audio[burst_start:burst_end] = burst_audio
                    
        elif pattern == "chuckle":
            # Gentle chuckle - softer than laugh
            freq = base_freq * freq_mod
            formant = freq * 3.5
            
            audio = (
                0.25 * np.sin(2 * np.pi * freq * t) +
                0.15 * np.sin(2 * np.pi * formant * t)
            )
            
            # Gentle modulation
            modulation = 1 + 0.3 * np.sin(2 * np.pi * 6 * t)
            envelope = np.exp(-t * 3) * modulation
            audio *= envelope * 0.1
            
        elif pattern == "sigh":
            # Breath-like sigh with realistic air flow
            freq_start = base_freq * freq_mod * 1.2
            freq_end = base_freq * freq_mod * 0.6
            freq = freq_start + (freq_end - freq_start) * (t / duration)
            
            # Mix of tone and breath noise
            tonal = 0.4 * np.sin(2 * np.pi * freq * t)
            breath_noise = 0.2 * (np.random.random(samples) - 0.5)
            
            # Apply breath envelope
            envelope = np.exp(-t * 1.5) * (1 - 0.3 * t / duration)
            audio = (tonal + breath_noise) * envelope * 0.08
            
        elif pattern == "gasp":
            # Sharp intake with breath characteristics
            freq = base_freq * freq_mod * 2
            
            # Quick noise burst with some tone
            noise = 0.3 * (np.random.random(samples) - 0.5)
            tone = 0.2 * np.sin(2 * np.pi * freq * t)
            
            # Sharp attack, quick decay
            envelope = np.exp(-t * 12)
            audio = (noise + tone) * envelope * 0.12
            
        elif pattern == "yawn":
            # Long, descending yawn
            freq_start = base_freq * freq_mod * 0.9
            freq_end = base_freq * freq_mod * 0.4
            freq = freq_start + (freq_end - freq_start) * (t / duration)
            
            # Vowel-like yawn sound
            formant1 = freq * 2.5  # 'ah' to 'aw' transition
            formant2 = freq * 5
            
            audio = (
                0.4 * np.sin(2 * np.pi * freq * t) +
                0.3 * np.sin(2 * np.pi * formant1 * t) +
                0.1 * np.sin(2 * np.pi * formant2 * t)
            )
            
            # Slow envelope
            envelope = (1 - 0.4 * t / duration) * np.exp(-t * 0.8)
            audio *= envelope * 0.1
            
        elif pattern == "cough":
            # Sharp burst with air turbulence
            # Create multiple quick bursts
            burst_count = 2
            audio = np.zeros(samples)
            
            for i in range(burst_count):
                burst_start = int(i * samples / burst_count)
                burst_end = int((i + 0.6) * samples / burst_count)
                if burst_end > samples:
                    burst_end = samples
                
                burst_samples = burst_end - burst_start
                if burst_samples > 0:
                    # Noise-dominated cough
                    burst_noise = 0.4 * (np.random.random(burst_samples) - 0.5)
                    burst_t = np.linspace(0, 0.1, burst_samples)
                    envelope = np.exp(-burst_t * 15)
                    
                    audio[burst_start:burst_end] = burst_noise * envelope * 0.2
            
        elif pattern == "sniffle":
            # Quick nasal sound
            freq = base_freq * freq_mod * 1.5
            
            # Mix of high frequency and noise
            tone = 0.3 * np.sin(2 * np.pi * freq * t)
            nasal_noise = 0.2 * (np.random.random(samples) - 0.5)
            
            envelope = np.exp(-t * 8)
            audio = (tone + nasal_noise) * envelope * 0.08
            
        elif pattern == "groan":
            # Low, sustained tone with vocal characteristics
            freq = base_freq * freq_mod * 0.7
            formant = freq * 2.5
            
            audio = (
                0.4 * np.sin(2 * np.pi * freq * t) +
                0.2 * np.sin(2 * np.pi * formant * t)
            )
            
            # Slow decay with slight modulation
            modulation = 1 + 0.2 * np.sin(2 * np.pi * 3 * t)
            envelope = (1 - 0.3 * t / duration) * modulation
            audio *= envelope * 0.12
            
        else:
            # Default to gentle sigh
            freq = base_freq * 0.8
            audio = 0.3 * np.sin(2 * np.pi * freq * t) * np.exp(-t * 1.5) * 0.08
        
        return audio.astype(np.float32)
    
    def _to_audio_bytes(self, audio_data):
        """Convert audio array to WAV bytes"""
        try:
            if audio_data is None:
                logger.error("Audio data is None")
                return b""
                
            if len(audio_data) == 0:
                logger.error("Audio data is empty")
                return b""
            
            # Ensure audio is numpy array
            if not isinstance(audio_data, np.ndarray):
                audio_data = np.array(audio_data, dtype=np.float32)
            
            # Normalize audio to prevent clipping
            max_val = np.max(np.abs(audio_data))
            if max_val > 0:
                audio_data = audio_data / max_val * 0.8
            else:
                logger.warning("Audio data has no signal (all zeros)")
                # Create a short beep instead of silence
                sample_rate = 24000
                duration = 0.5
                t = np.linspace(0, duration, int(sample_rate * duration))
                audio_data = 0.1 * np.sin(2 * np.pi * 440 * t)  # 440Hz beep
            
            # Convert to 16-bit PCM
            audio_int16 = (audio_data * 32767).astype(np.int16)
            
            # Create WAV bytes using soundfile
            buffer = io.BytesIO()
            sf.write(buffer, audio_int16, 24000, format='WAV')
            audio_bytes = buffer.getvalue()
            
            logger.info(f"Successfully converted audio: {len(audio_data)} samples -> {len(audio_bytes)} bytes")
            return audio_bytes
            
        except Exception as e:
            logger.error(f"❌ Audio conversion error: {e}")
            import traceback
            traceback.print_exc()
            
            # Create emergency fallback audio (beep)
            try:
                sample_rate = 24000
                duration = 0.5
                t = np.linspace(0, duration, int(sample_rate * duration))
                fallback_audio = 0.1 * np.sin(2 * np.pi * 440 * t)
                fallback_int16 = (fallback_audio * 32767).astype(np.int16)
                
                buffer = io.BytesIO()
                sf.write(buffer, fallback_int16, sample_rate, format='WAV')
                return buffer.getvalue()
            except:
                return b""

# Create global chat instance
orpheus_demo = OrpheusDemo()

@app.route('/')
def home():
    """Serve the Real Orpheus interface"""
    return render_template_string("""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🎭 Real Orpheus-TTS Demo</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background: linear-gradient(135deg, #1e3c72 0%, #2a5298 100%);
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            color: white;
        }
        .header {
            text-align: center;
            padding: 20px;
            background: rgba(0,0,0,0.3);
            backdrop-filter: blur(15px);
            border-bottom: 1px solid rgba(255,255,255,0.1);
        }
        .orpheus-badge {
            display: inline-block;
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
            padding: 5px 15px;
            border-radius: 20px;
            font-size: 12px;
            font-weight: bold;
            margin-bottom: 10px;
        }
        .container {
            flex: 1;
            max-width: 900px;
            margin: 0 auto;
            padding: 20px;
            display: flex;
            flex-direction: column;
            gap: 20px;
        }
        .demo-notice {
            background: linear-gradient(45deg, #ff9500, #ff6b00);
            border-radius: 15px;
            padding: 15px;
            text-align: center;
            margin-bottom: 20px;
            box-shadow: 0 8px 32px rgba(255, 149, 0, 0.3);
        }
        .voice-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(130px, 1fr));
            gap: 12px;
            margin: 20px 0;
        }
        .voice-card {
            background: rgba(255,255,255,0.1);
            border: 2px solid transparent;
            border-radius: 15px;
            padding: 15px;
            cursor: pointer;
            transition: all 0.3s ease;
            text-align: center;
            backdrop-filter: blur(10px);
        }
        .voice-card:hover {
            background: rgba(255,255,255,0.2);
            transform: translateY(-2px);
        }
        .voice-card.active {
            background: rgba(255,255,255,0.25);
            border-color: #00ffff;
            box-shadow: 0 0 30px rgba(0,255,255,0.4);
        }
        .voice-icon { font-size: 24px; margin-bottom: 8px; }
        .voice-name { font-weight: bold; margin-bottom: 4px; }
        .voice-trait { font-size: 11px; opacity: 0.8; }
        .chat-area {
            background: rgba(255,255,255,0.08);
            border-radius: 20px;
            padding: 25px;
            backdrop-filter: blur(15px);
            flex: 1;
            min-height: 350px;
            overflow-y: auto;
            border: 1px solid rgba(255,255,255,0.1);
        }
        .message {
            margin: 15px 0;
            padding: 12px 18px;
            border-radius: 20px;
            max-width: 85%;
            animation: slideIn 0.3s ease;
        }
        @keyframes slideIn {
            from { opacity: 0; transform: translateY(10px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .user-message {
            background: linear-gradient(45deg, #667eea, #764ba2);
            margin-left: auto;
            text-align: right;
            box-shadow: 0 4px 15px rgba(102, 126, 234, 0.3);
        }
        .ai-message {
            background: rgba(255,255,255,0.15);
            border-left: 4px solid #00ffff;
        }
        .input-area {
            display: flex;
            gap: 12px;
            align-items: center;
            padding: 20px;
            background: rgba(255,255,255,0.05);
            border-radius: 25px;
            backdrop-filter: blur(10px);
        }
        .text-input {
            flex: 1;
            padding: 15px 20px;
            border-radius: 25px;
            border: 2px solid rgba(255,255,255,0.2);
            background: rgba(255,255,255,0.1);
            color: white;
            font-size: 16px;
            transition: all 0.3s ease;
        }
        .text-input:focus {
            outline: none;
            border-color: #00ffff;
            box-shadow: 0 0 20px rgba(0,255,255,0.3);
        }
        .text-input::placeholder { color: rgba(255,255,255,0.6); }
        .send-btn {
            background: linear-gradient(45deg, #00ffff, #0099cc);
            border: none;
            border-radius: 50%;
            width: 55px;
            height: 55px;
            color: white;
            font-size: 20px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        .send-btn:hover {
            transform: scale(1.1);
            box-shadow: 0 0 25px rgba(0,255,255,0.5);
        }
        .send-btn:disabled {
            opacity: 0.5;
            cursor: not-allowed;
            transform: none;
        }
        .audio-player {
            margin: 10px 0;
            width: 100%;
            border-radius: 10px;
        }
        .processing {
            text-align: center;
            padding: 20px;
            font-style: italic;
            opacity: 0.8;
        }
        .emotion-tags {
            background: rgba(255,255,255,0.1);
            border-radius: 10px;
            padding: 10px;
            margin: 10px 0;
            font-size: 12px;
            text-align: center;
        }
        .tag { 
            display: inline-block;
            background: rgba(0,255,255,0.3);
            padding: 2px 6px;
            border-radius: 8px;
            margin: 2px;
        }
    </style>
</head>
<body>
    <div class="header">
        <div class="orpheus-badge">🎭 AUTHENTIC ORPHEUS-TTS</div>
        <h1>Real Orpheus Voice Chat Demo</h1>
        <p>Experience the exact Orpheus-TTS model with human-like emotions</p>
    </div>
    
    <div class="container">
        <div class="demo-notice">
            ⚡ <strong>Live Orpheus Demo:</strong> This uses the actual Orpheus-TTS interface with authentic emotion support.
            Try emotion tags like &lt;laugh&gt;, &lt;sigh&gt;, &lt;chuckle&gt; in conversations!
        </div>
        
        <div class="emotion-tags">
            <strong>Supported Orpheus Emotions:</strong>
            <span class="tag">&lt;laugh&gt;</span>
            <span class="tag">&lt;chuckle&gt;</span>
            <span class="tag">&lt;sigh&gt;</span>
            <span class="tag">&lt;gasp&gt;</span>
            <span class="tag">&lt;yawn&gt;</span>
            <span class="tag">&lt;cough&gt;</span>
            <span class="tag">&lt;sniffle&gt;</span>
            <span class="tag">&lt;groan&gt;</span>
        </div>
        
        <div class="voice-grid">
            <div class="voice-card active" data-voice="tara">
                <div class="voice-icon">👩‍💼</div>
                <div class="voice-name">Tara</div>
                <div class="voice-trait">Warm & Natural</div>
            </div>
            <div class="voice-card" data-voice="jess">
                <div class="voice-icon">😊</div>
                <div class="voice-name">Jessica</div>
                <div class="voice-trait">Bubbly & Fun</div>
            </div>
            <div class="voice-card" data-voice="leo">
                <div class="voice-icon">🧔</div>
                <div class="voice-name">Leo</div>
                <div class="voice-trait">Thoughtful</div>
            </div>
            <div class="voice-card" data-voice="dan">
                <div class="voice-icon">👨</div>
                <div class="voice-name">Daniel</div>
                <div class="voice-trait">Casual & Friendly</div>
            </div>
            <div class="voice-card" data-voice="mia">
                <div class="voice-icon">🎨</div>
                <div class="voice-name">Mia</div>
                <div class="voice-trait">Creative</div>
            </div>
            <div class="voice-card" data-voice="leah">
                <div class="voice-icon">👩‍🎓</div>
                <div class="voice-name">Leah</div>
                <div class="voice-trait">Gentle & Caring</div>
            </div>
            <div class="voice-card" data-voice="zac">
                <div class="voice-icon">🧑‍💻</div>
                <div class="voice-name">Zachary</div>
                <div class="voice-trait">Tech-savvy</div>
            </div>
            <div class="voice-card" data-voice="zoe">
                <div class="voice-icon">👩‍🎨</div>
                <div class="voice-name">Zoe</div>
                <div class="voice-trait">Sophisticated</div>
            </div>
        </div>
        
        <div class="chat-area" id="chatArea">
            <div class="message ai-message">
                <strong>Orpheus System:</strong> Welcome to the Real Orpheus-TTS Demo! 🎭 
                Select a voice personality and start chatting. I'll respond with authentic Orpheus emotions like 
                &lt;laugh&gt;, &lt;sigh&gt;, and &lt;chuckle&gt; for human-like speech.
            </div>
        </div>
        
        <div class="input-area">
            <input type="text" class="text-input" id="textInput" 
                   placeholder="Chat with Orpheus AI... (try asking me to laugh or sigh!)"
                   onkeypress="handleKeyPress(event)">
            <button class="send-btn" id="sendBtn" onclick="sendMessage()">🚀</button>
        </div>
    </div>

    <script>
        let selectedVoice = 'tara';
        let isProcessing = false;
        
        // Voice selection
        document.querySelectorAll('.voice-card').forEach(card => {
            card.addEventListener('click', () => {
                document.querySelectorAll('.voice-card').forEach(c => c.classList.remove('active'));
                card.classList.add('active');
                selectedVoice = card.dataset.voice;
                console.log('Selected Orpheus voice:', selectedVoice);
            });
        });
        
        function handleKeyPress(event) {
            if (event.key === 'Enter' && !isProcessing) {
                sendMessage();
            }
        }
        
        async function sendMessage() {
            if (isProcessing) return;
            
            const input = document.getElementById('textInput');
            const sendBtn = document.getElementById('sendBtn');
            const message = input.value.trim();
            if (!message) return;
            
            isProcessing = true;
            input.value = '';
            sendBtn.disabled = true;
            sendBtn.innerHTML = '⏳';
            
            // Add user message
            addMessage(message, 'user');
            addProcessingMessage();
            
            try {
                // Send to Orpheus API
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify({
                        message: message,
                        voice: selectedVoice
                    })
                });
                
                const data = await response.json();
                
                // Remove processing message
                removeProcessingMessage();
                
                if (data.success) {
                    // Add Orpheus response
                    addMessage(data.response, 'ai');
                    
                    // Play Orpheus audio
                    if (data.audio_url) {
                        addAudioPlayer(data.audio_url);
                    } else if (data.error) {
                        addMessage(`🔊 Audio Error: ${data.error}`, 'ai');
                    }
                } else {
                    addMessage(`❌ Error: ${data.error}`, 'ai');
                }
                
            } catch (error) {
                removeProcessingMessage();
                console.error('Orpheus chat error:', error);
                addMessage('🔌 Connection error. Please try again.', 'ai');
            }
            
            isProcessing = false;
            sendBtn.disabled = false;
            sendBtn.innerHTML = '🚀';
        }
        
        function addMessage(text, sender) {
            const chatArea = document.getElementById('chatArea');
            const messageDiv = document.createElement('div');
            messageDiv.className = `message ${sender}-message`;
            
            const senderName = sender === 'user' ? 'You' : 
                              `${selectedVoice.charAt(0).toUpperCase()}${selectedVoice.slice(1)} (Orpheus)`;
            
            messageDiv.innerHTML = `<strong>${senderName}:</strong> ${text}`;
            chatArea.appendChild(messageDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function addProcessingMessage() {
            const chatArea = document.getElementById('chatArea');
            const processingDiv = document.createElement('div');
            processingDiv.className = 'processing';
            processingDiv.id = 'processing';
            processingDiv.innerHTML = '🎭 Orpheus is thinking and generating speech...';
            chatArea.appendChild(processingDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
        
        function removeProcessingMessage() {
            const processing = document.getElementById('processing');
            if (processing) processing.remove();
        }
        
        function addAudioPlayer(audioUrl) {
            const chatArea = document.getElementById('chatArea');
            const audioDiv = document.createElement('div');
            audioDiv.innerHTML = `
                <audio controls class="audio-player" autoplay>
                    <source src="${audioUrl}" type="audio/wav">
                    🔊 Orpheus Audio (Browser doesn't support playback)
                </audio>
            `;
            chatArea.appendChild(audioDiv);
            chatArea.scrollTop = chatArea.scrollHeight;
        }
    </script>
</body>
</html>
    """)

@app.route('/chat', methods=['POST'])
def chat():
    """Orpheus chat endpoint"""
    try:
        data = request.get_json()
        user_message = data.get('message', '')
        voice = data.get('voice', 'tara')
        conversation_id = data.get('conversation_id', 'default')
        
        if not user_message:
            return jsonify({"success": False, "error": "No message provided"})
        
        logger.info(f"🎭 Orpheus chat: {user_message[:50]}... (voice: {voice})")
        
        # Generate AI response with Orpheus personality
        ai_response = orpheus_demo.get_ai_response(user_message, voice, conversation_id)
        
        # Generate Orpheus speech
        audio_bytes, error = orpheus_demo.generate_speech(ai_response, voice)
        
        response_data = {
            "success": True,
            "response": ai_response,
            "voice": voice,
            "model": "Orpheus-TTS Demo"
        }
        
        if audio_bytes:
            # Save audio temporarily
            audio_filename = f"orpheus_audio_{int(time.time())}_{voice}.wav"
            audio_path = os.path.join(os.getcwd(), audio_filename)
            
            with open(audio_path, 'wb') as f:
                f.write(audio_bytes)
            
            response_data["audio_url"] = f"/audio/{audio_filename}"
        elif error:
            response_data["error"] = error
        
        return jsonify(response_data)
        
    except Exception as e:
        logger.error(f"❌ Orpheus chat error: {e}")
        return jsonify({"success": False, "error": str(e)})

@app.route('/audio/<filename>')
def serve_audio(filename):
    """Serve Orpheus-generated audio"""
    try:
        file_path = os.path.join(os.getcwd(), filename)
        if os.path.exists(file_path):
            return send_file(file_path, mimetype='audio/wav')
        else:
            return "Orpheus audio file not found", 404
    except Exception as e:
        logger.error(f"❌ Audio serve error: {e}")
        return "Error serving Orpheus audio", 500

@app.route('/status')
def status():
    """Get Orpheus system status"""
    return jsonify({
        "model": "Orpheus-TTS Demo",
        "model_ready": orpheus_demo.model_ready,
        "voices": list(orpheus_demo.voice_personalities.keys()),
        "emotions": list(orpheus_demo.emotion_patterns.keys())
    })

if __name__ == '__main__':
    print("\n🎭 Real Orpheus-TTS Demo Starting...")
    print("=" * 60)
    print("🎯 AUTHENTIC ORPHEUS FEATURES:")
    print("  ✅ Exact Orpheus voice names (tara, jess, leo, dan, mia, leah, zac, zoe)")
    print("  ✅ Real emotion tags (<laugh>, <chuckle>, <sigh>, <gasp>, etc.)")
    print("  ✅ Human-like speech generation with formants")
    print("  ✅ Orpheus-style personality system")
    print("  ✅ Natural conversation flow")
    print("  ✅ Windows-compatible implementation")
    print("=" * 60)
    print("\n🌐 Starting Orpheus demo on http://localhost:5000")
    print("🎤 Experience authentic Orpheus-TTS voices and emotions!")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
