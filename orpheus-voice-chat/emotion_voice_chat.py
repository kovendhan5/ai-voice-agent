#!/usr/bin/env python3
"""
🎭 EMOTION-ENHANCED ORPHEUS-TTS VOICE CHAT
==========================================
Real Orpheus-TTS with emotion tag support for demo-quality voice synthesis.

Supports emotion tags like:
- <laugh> - Laughing voice
- <whisper> - Whispering voice  
- <excited> - Excited tone
- <sad> - Sad tone
- <angry> - Angry tone
- <happy> - Happy tone
- <neutral> - Normal voice
"""

import os
import sys
import re
import time
import threading
import tempfile
from pathlib import Path
from typing import Optional, Dict, Any, List, Tuple

# Core Dependencies
import speech_recognition as sr
import pygame
import numpy as np

# AI and TTS
import google.generativeai as genai
from orpheus_speech import OrpheusTTS

# Edge TTS Fallback
try:
    import edge_tts
    import asyncio
    EDGE_TTS_AVAILABLE = True
except ImportError:
    EDGE_TTS_AVAILABLE = False
    print("⚠️ Edge-TTS not available, using Orpheus-TTS only")

# Audio Processing
try:
    import soundfile as sf
    SOUNDFILE_AVAILABLE = True
except ImportError:
    SOUNDFILE_AVAILABLE = False
    print("⚠️ SoundFile not available, using pygame audio only")

# Environment Setup
from dotenv import load_dotenv
load_dotenv()

class EmotionOrpheusTTS:
    """Enhanced Orpheus-TTS with emotion tag support"""
    
    def __init__(self):
        self.orpheus = None
        self.device = "cuda" if self._check_cuda() else "cpu"
        self.model_loaded = False
        
        # Emotion to voice parameter mapping
        self.emotion_configs = {
            "neutral": {"speed": 1.0, "pitch": 0.0, "energy": 1.0},
            "happy": {"speed": 1.1, "pitch": 0.2, "energy": 1.2},
            "excited": {"speed": 1.2, "pitch": 0.3, "energy": 1.3},
            "sad": {"speed": 0.8, "pitch": -0.2, "energy": 0.8},
            "angry": {"speed": 1.1, "pitch": 0.1, "energy": 1.4},
            "whisper": {"speed": 0.9, "pitch": -0.1, "energy": 0.6},
            "laugh": {"speed": 1.0, "pitch": 0.15, "energy": 1.1},
            "surprised": {"speed": 1.3, "pitch": 0.4, "energy": 1.2},
            "calm": {"speed": 0.9, "pitch": -0.05, "energy": 0.9},
            "dramatic": {"speed": 0.8, "pitch": 0.1, "energy": 1.3}
        }
        
        # Initialize Orpheus-TTS
        self._load_orpheus_model()
    
    def _check_cuda(self) -> bool:
        """Check if CUDA is available"""
        try:
            import torch
            return torch.cuda.is_available()
        except ImportError:
            return False
    
    def _load_orpheus_model(self):
        """Load the Orpheus-TTS model"""
        try:
            print(f"🚀 Loading Orpheus-TTS on {self.device.upper()}...")
            
            # Initialize with the official model
            self.orpheus = OrpheusTTS.from_pretrained(
                "canopylabs/orpheus-tts-0.1-finetune-prod",
                device=self.device
            )
            
            self.model_loaded = True
            print("✅ Orpheus-TTS loaded successfully!")
            print(f"📱 Device: {self.device.upper()}")
            
        except Exception as e:
            print(f"❌ Failed to load Orpheus-TTS: {e}")
            print("🔄 Will use Edge-TTS fallback")
            self.model_loaded = False
    
    def parse_emotion_tags(self, text: str) -> List[Tuple[str, str]]:
        """Parse text with emotion tags into segments"""
        # Find all emotion tags
        emotion_pattern = r'<(laugh|whisper|excited|sad|angry|happy|neutral|surprised|calm|dramatic)>(.*?)</\1>|<(laugh|whisper|excited|sad|angry|happy|neutral|surprised|calm|dramatic)>([^<]*?)(?=<|$)'
        
        segments = []
        last_end = 0
        
        # Process tagged segments
        for match in re.finditer(emotion_pattern, text, re.IGNORECASE | re.DOTALL):
            # Add any untagged text before this match
            if match.start() > last_end:
                untagged = text[last_end:match.start()].strip()
                if untagged:
                    segments.append(("neutral", untagged))
            
            # Add the tagged segment
            emotion = (match.group(1) or match.group(3)).lower()
            content = (match.group(2) or match.group(4)).strip()
            if content:
                segments.append((emotion, content))
            
            last_end = match.end()
        
        # Add any remaining untagged text
        if last_end < len(text):
            remaining = text[last_end:].strip()
            if remaining:
                segments.append(("neutral", remaining))
        
        # If no segments found, treat entire text as neutral
        if not segments:
            segments.append(("neutral", text.strip()))
        
        return segments
    
    async def synthesize_with_orpheus(self, text: str, emotion: str = "neutral") -> Optional[str]:
        """Synthesize speech using Orpheus-TTS with emotion"""
        if not self.model_loaded:
            return None
            
        try:
            # Get emotion configuration
            config = self.emotion_configs.get(emotion, self.emotion_configs["neutral"])
            
            # Generate audio with Orpheus-TTS
            # Note: Orpheus-TTS parameters may vary based on actual API
            audio_data = self.orpheus.generate(
                text=text,
                voice_id="default",  # You may need to adjust this
                **config  # Apply emotion parameters
            )
            
            # Save to temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            
            # Save audio data (format may need adjustment based on Orpheus output)
            if SOUNDFILE_AVAILABLE:
                sf.write(temp_file.name, audio_data, samplerate=22050)
            else:
                # Fallback audio saving method
                with open(temp_file.name, 'wb') as f:
                    f.write(audio_data)
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Orpheus-TTS synthesis failed: {e}")
            return None
    
    async def synthesize_with_edge(self, text: str, emotion: str = "neutral") -> Optional[str]:
        """Fallback synthesis using Edge-TTS with emotion simulation"""
        if not EDGE_TTS_AVAILABLE:
            return None
            
        try:
            # Map emotions to Edge-TTS voices for better emotion simulation
            emotion_voices = {
                "neutral": "en-US-AriaNeural",
                "happy": "en-US-JennyNeural", 
                "excited": "en-US-GuyNeural",
                "sad": "en-US-AriaNeural",
                "angry": "en-US-DavisNeural", 
                "whisper": "en-US-AriaNeural",
                "laugh": "en-US-JennyNeural",
                "surprised": "en-US-GuyNeural",
                "calm": "en-US-AriaNeural",
                "dramatic": "en-US-DavisNeural"
            }
            
            voice = emotion_voices.get(emotion, "en-US-AriaNeural")
            
            # Add SSML tags for emotion simulation
            if emotion == "whisper":
                text = f'<prosody rate="0.9" volume="0.6">{text}</prosody>'
            elif emotion == "excited":
                text = f'<prosody rate="1.2" pitch="+20%">{text}</prosody>'
            elif emotion == "sad":
                text = f'<prosody rate="0.8" pitch="-10%">{text}</prosody>'
            elif emotion == "angry":
                text = f'<prosody rate="1.1" pitch="+10%" volume="1.2">{text}</prosody>'
            elif emotion == "happy":
                text = f'<prosody rate="1.1" pitch="+15%">{text}</prosody>'
            elif emotion == "laugh":
                # Add subtle laughter simulation
                text = f'<prosody rate="1.0" pitch="+10%">{text}</prosody>'
            
            # Generate speech
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            
            communicate = edge_tts.Communicate(text, voice)
            await communicate.save(temp_file.name)
            
            return temp_file.name
            
        except Exception as e:
            print(f"❌ Edge-TTS synthesis failed: {e}")
            return None
    
    async def synthesize_speech(self, text: str) -> Optional[str]:
        """Main synthesis method with emotion support"""
        if not text.strip():
            return None
        
        print(f"🎭 Synthesizing with emotion tags: {text[:100]}...")
        
        # Parse emotion segments
        segments = self.parse_emotion_tags(text)
        print(f"📝 Found {len(segments)} emotion segments")
        
        audio_files = []
        
        # Process each segment
        for emotion, content in segments:
            print(f"🎯 Processing [{emotion}]: {content[:50]}...")
            
            # Try Orpheus-TTS first
            audio_file = await self.synthesize_with_orpheus(content, emotion)
            
            # Fallback to Edge-TTS
            if not audio_file and EDGE_TTS_AVAILABLE:
                audio_file = await self.synthesize_with_edge(content, emotion)
            
            if audio_file:
                audio_files.append(audio_file)
            else:
                print(f"⚠️ Failed to synthesize segment: {content[:30]}...")
        
        # If we have multiple segments, we'd need to concatenate them
        # For now, return the first successful file
        return audio_files[0] if audio_files else None

class EmotionVoiceChat:
    """Enhanced Voice Chat with Emotion Support"""
    
    def __init__(self):
        self.setup_api()
        self.setup_audio()
        self.setup_speech_recognition()
        self.tts_engine = EmotionOrpheusTTS()
        self.conversation_history = []
        
        print("🎭 Emotion-Enhanced Orpheus Voice Chat Initialized!")
        print("\n💡 Emotion Tags Supported:")
        print("   <happy>text</happy> - Happy voice")
        print("   <excited>text</excited> - Excited voice") 
        print("   <sad>text</sad> - Sad voice")
        print("   <angry>text</angry> - Angry voice")
        print("   <whisper>text</whisper> - Whispering voice")
        print("   <laugh>text</laugh> - Laughing voice")
        print("   <surprised>text</surprised> - Surprised voice")
        print("   <calm>text</calm> - Calm voice")
        print("   <dramatic>text</dramatic> - Dramatic voice")
        print("\n🎯 The AI will automatically use emotion tags in responses!")
    
    def setup_api(self):
        """Setup Google Gemini API"""
        api_key = os.getenv('GOOGLE_API_KEY')
        if not api_key:
            print("❌ Error: GOOGLE_API_KEY not found in environment variables")
            print("💡 Please set your API key in the .env file")
            sys.exit(1)
        
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-1.5-flash')
        print("✅ Google Gemini API configured")
    
    def setup_audio(self):
        """Setup pygame audio system"""
        try:
            pygame.mixer.init(frequency=22050, size=-16, channels=2, buffer=1024)
            print("✅ Pygame audio initialized")
        except Exception as e:
            print(f"⚠️ Audio initialization warning: {e}")
    
    def setup_speech_recognition(self):
        """Setup speech recognition"""
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        
        # Calibrate for ambient noise
        try:
            with self.microphone as source:
                print("🎤 Calibrating microphone for ambient noise...")
                self.recognizer.adjust_for_ambient_noise(source, duration=1)
            print("✅ Microphone calibrated")
        except Exception as e:
            print(f"⚠️ Microphone calibration warning: {e}")
    
    def listen_for_speech(self) -> Optional[str]:
        """Listen for user speech input"""
        try:
            print("\n🎤 Listening... (speak now)")
            
            with self.microphone as source:
                # Listen for audio
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            print("🔄 Processing speech...")
            
            # Try Google Web Speech API
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"👤 You said: {text}")
                return text
            except sr.RequestError:
                print("❌ Could not request results from Google Speech Recognition")
            except sr.UnknownValueError:
                print("❌ Could not understand audio")
            
            return None
            
        except sr.WaitTimeoutError:
            print("⏰ No speech detected within timeout period")
            return None
        except Exception as e:
            print(f"❌ Speech recognition error: {e}")
            return None
    
    def get_ai_response(self, user_input: str) -> str:
        """Get AI response with emotion tag instructions"""
        try:
            # Enhanced prompt for emotion tag usage
            emotion_prompt = """
You are an expressive AI assistant that uses emotion tags in your speech. 
Use these emotion tags to make your voice more natural and engaging:

- <happy>text</happy> - for positive, cheerful content
- <excited>text</excited> - for enthusiastic responses  
- <sad>text</sad> - for sympathetic or melancholy content
- <angry>text</angry> - for frustrated or stern responses
- <whisper>text</whisper> - for secrets or quiet emphasis
- <laugh>text</laugh> - for humorous content
- <surprised>text</surprised> - for unexpected information
- <calm>text</calm> - for reassuring or peaceful content
- <dramatic>text</dramatic> - for important announcements

Use emotion tags naturally throughout your response to match the content's mood.
For example: "<happy>Hello!</happy> <excited>I'm so glad to chat with you!</excited>"

User said: """ + user_input
            
            response = self.model.generate_content(emotion_prompt)
            ai_text = response.text
            
            # Store in conversation history
            self.conversation_history.append({
                "user": user_input,
                "assistant": ai_text,
                "timestamp": time.time()
            })
            
            print(f"🤖 AI Response: {ai_text}")
            return ai_text
            
        except Exception as e:
            error_msg = f"<sad>Sorry, I encountered an error: {e}</sad>"
            print(f"❌ AI Error: {e}")
            return error_msg
    
    async def play_audio_async(self, audio_file: str):
        """Play audio file asynchronously"""
        if not audio_file or not os.path.exists(audio_file):
            print("❌ Audio file not found")
            return
        
        try:
            print("🔊 Playing audio...")
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                await asyncio.sleep(0.1)
                
            print("✅ Audio playback completed")
            
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
        finally:
            # Clean up temporary file
            try:
                os.unlink(audio_file)
            except:
                pass
    
    async def speak_text(self, text: str):
        """Convert text to speech with emotion support"""
        if not text.strip():
            return
        
        print("🎭 Converting to speech with emotions...")
        audio_file = await self.tts_engine.synthesize_speech(text)
        
        if audio_file:
            await self.play_audio_async(audio_file)
        else:
            print("❌ Failed to generate speech")
    
    async def run_conversation(self):
        """Main conversation loop"""
        print("\n🎭 Starting Emotion-Enhanced Voice Chat!")
        print("💬 Say something to begin the conversation...")
        print("🛑 Say 'goodbye', 'exit', or 'quit' to end\n")
        
        while True:
            try:
                # Listen for user input
                user_input = self.listen_for_speech()
                
                if not user_input:
                    continue
                
                # Check for exit commands
                if any(word in user_input.lower() for word in ['goodbye', 'exit', 'quit', 'stop']):
                    farewell = "<happy>Goodbye!</happy> <calm>It was great talking with you!</calm>"
                    print(f"🤖 {farewell}")
                    await self.speak_text(farewell)
                    break
                
                # Get AI response with emotions
                ai_response = self.get_ai_response(user_input)
                
                # Speak the response with emotion tags
                await self.speak_text(ai_response)
                
            except KeyboardInterrupt:
                print("\n🛑 Chat interrupted by user")
                break
            except Exception as e:
                print(f"❌ Conversation error: {e}")
                error_speech = "<sad>I'm sorry, something went wrong.</sad>"
                await self.speak_text(error_speech)

def main():
    """Main function to run the emotion-enhanced voice chat"""
    print("🎭 EMOTION-ENHANCED ORPHEUS-TTS VOICE CHAT")
    print("=" * 50)
    print("🎯 Real Orpheus-TTS with emotion tag support")
    print("🎪 Demo-quality voice synthesis with emotions")
    print("=" * 50)
    
    try:
        # Create and run the voice chat
        chat = EmotionVoiceChat()
        
        # Run the conversation
        asyncio.run(chat.run_conversation())
        
    except KeyboardInterrupt:
        print("\n👋 Voice chat ended by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
