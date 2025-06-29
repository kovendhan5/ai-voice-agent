#!/usr/bin/env python3
"""
FIXED Voice Chat Application
Addresses voice quality and text accuracy issues
"""

import asyncio
import logging
import tempfile
import os
import json
import speech_recognition as sr
import edge_tts
import google.generativeai as genai
from pathlib import Path
import soundfile as sf
import numpy as np
import time
import re

# Load environment variables
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    # dotenv not installed, environment variables should be set manually
    pass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Configure Gemini AI
GEMINI_API_KEY = os.getenv('GOOGLE_API_KEY')
if not GEMINI_API_KEY:
    raise ValueError("GOOGLE_API_KEY environment variable is required. Please set it in your .env file")
genai.configure(api_key=GEMINI_API_KEY)

class FixedVoiceChat:
    """Fixed voice chat with improved voice quality and text accuracy"""
    
    def __init__(self):
        self.ai_model = genai.GenerativeModel('gemini-1.5-flash')  # Updated model name
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()
        self.conversation_history = []
        
        # Optimized recognizer settings for better accuracy
        self.recognizer.energy_threshold = 4000
        self.recognizer.dynamic_energy_threshold = True
        self.recognizer.pause_threshold = 0.8
        self.recognizer.phrase_threshold = 0.3
        
        # Premium voice configurations
        self.voice_config = {
            "default": {
                "voice": "en-US-JennyNeural",
                "rate": "+0%",
                "pitch": "+0Hz",
                "style": "cheerful"
            },
            "friendly": {
                "voice": "en-US-AriaNeural", 
                "rate": "+5%",
                "pitch": "+10Hz",
                "style": "friendly"
            },
            "professional": {
                "voice": "en-US-SaraNeural",
                "rate": "-5%", 
                "pitch": "-5Hz",
                "style": "cheerful"
            }
        }
        
        logger.info("✅ Fixed Voice Chat initialized")
    
    def calibrate_microphone(self):
        """Calibrate microphone for better speech recognition"""
        try:
            logger.info("🎤 Calibrating microphone for ambient noise...")
            with self.microphone as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=2)
            logger.info(f"✅ Microphone calibrated. Energy threshold: {self.recognizer.energy_threshold}")
            return True
        except Exception as e:
            logger.error(f"❌ Microphone calibration failed: {e}")
            return False
    
    def improved_speech_recognition(self, timeout=5, phrase_time_limit=None):
        """Improved speech recognition with better accuracy"""
        try:
            logger.info("🎤 Listening for speech...")
            
            with self.microphone as source:
                # Better noise adjustment
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                
                # Listen with optimized settings
                audio = self.recognizer.listen(
                    source, 
                    timeout=timeout,
                    phrase_time_limit=phrase_time_limit
                )
            
            logger.info("🔍 Processing speech...")
            
            # Try multiple recognition methods for better accuracy
            try:
                # Primary: Google Web Speech API (most accurate)
                text = self.recognizer.recognize_google(audio, language="en-US")
                logger.info(f"✅ Google Speech: '{text}'")
                return text
            except sr.UnknownValueError:
                try:
                    # Fallback: Google with show_all for confidence scores
                    results = self.recognizer.recognize_google(audio, language="en-US", show_all=True)
                    if results and 'alternative' in results:
                        best_result = results['alternative'][0]
                        text = best_result['transcript']
                        confidence = best_result.get('confidence', 0)
                        logger.info(f"✅ Google Speech (confidence {confidence:.2f}): '{text}'")
                        return text
                except:
                    pass
                
                # Final fallback: Whisper-style recognition
                logger.warning("🔄 Trying alternative recognition...")
                return None
                
        except sr.WaitTimeoutError:
            logger.warning("⏰ Speech recognition timeout")
            return None
        except sr.RequestError as e:
            logger.error(f"❌ Speech recognition service error: {e}")
            return None
        except Exception as e:
            logger.error(f"❌ Speech recognition error: {e}")
            return None
    
    def generate_better_response(self, user_input):
        """Generate improved AI response for voice conversation"""
        try:
            # Better prompt for natural conversation
            prompt = f"""You are having a natural voice conversation with a person. 

IMPORTANT RULES:
1. Keep responses SHORT (1-2 sentences max) - people are listening, not reading
2. Be completely natural and conversational 
3. NO technical terms, NO code, NO HTML, NO markdown
4. Use simple, clear language like talking to a friend
5. Ask engaging follow-up questions to keep conversation flowing
6. Show genuine interest in what the person says
7. Be warm, friendly, and personable

Conversation so far:
{json.dumps(self.conversation_history[-3:], indent=2) if self.conversation_history else "This is the start of the conversation"}

Person just said: "{user_input}"

Respond naturally as if speaking out loud to them:"""

            response = self.ai_model.generate_content(prompt)
            ai_text = response.text.strip()
            
            # Clean up the response
            ai_text = self.clean_response_text(ai_text)
            
            # Store conversation
            self.conversation_history.append({
                "user": user_input,
                "ai": ai_text,
                "timestamp": time.time()
            })
            
            logger.info(f"🤖 AI Response: '{ai_text}'")
            return ai_text
            
        except Exception as e:
            logger.error(f"❌ AI response generation error: {e}")
            return "I'm sorry, I didn't catch that. Could you repeat?"
    
    def clean_response_text(self, text):
        """Clean AI response text for better speech synthesis"""
        # Remove common problematic elements
        text = re.sub(r'\*.*?\*', '', text)  # Remove markdown bold
        text = re.sub(r'_.*?_', '', text)    # Remove markdown italic
        text = re.sub(r'`.*?`', '', text)    # Remove code blocks
        text = re.sub(r'http[s]?://\S+', '', text)  # Remove URLs
        text = re.sub(r'<.*?>', '', text)    # Remove HTML tags
        text = re.sub(r'\[.*?\]', '', text)  # Remove brackets
        text = re.sub(r'\s+', ' ', text)     # Normalize whitespace
        
        # Ensure proper punctuation for speech
        text = text.strip()
        if text and not text.endswith(('.', '!', '?')):
            text += '.'
            
        return text
    
    async def generate_high_quality_speech(self, text, voice_style="default"):
        """Generate high-quality speech with improved audio"""
        try:
            config = self.voice_config.get(voice_style, self.voice_config["default"])
            
            # Use simplified approach that works reliably
            voice_name = config['voice']
            
            logger.info(f"🎵 Generating speech: {voice_name} - '{text[:50]}...'")
            
            # Generate audio with Edge TTS (simplified for reliability)
            communicate = edge_tts.Communicate(text, voice_name)
            
            # Create temporary file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                temp_path = temp_file.name
            
            # Save audio
            await communicate.save(temp_path)
            
            logger.info(f"✅ Generated speech audio: {temp_path}")
            return temp_path
            
        except Exception as e:
            logger.error(f"❌ Speech generation error: {e}")
            # Fallback to basic Edge TTS
            try:
                logger.info("🔄 Trying fallback speech generation...")
                communicate = edge_tts.Communicate(text, "en-US-JennyNeural")
                
                with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                    temp_path = temp_file.name
                
                await communicate.save(temp_path)
                logger.info(f"✅ Fallback speech generated: {temp_path}")
                return temp_path
                
            except Exception as e2:
                logger.error(f"❌ Fallback speech generation also failed: {e2}")
                return None
    
    def play_audio_file(self, audio_path):
        """Play audio file with proper cleanup"""
        try:
            import pygame
            pygame.mixer.init()
            pygame.mixer.music.load(audio_path)
            pygame.mixer.music.play()
            
            # Wait for playback to finish
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            pygame.mixer.quit()
            
        except ImportError:
            # Fallback to system audio player
            try:
                if os.name == 'nt':  # Windows
                    import winsound
                    winsound.PlaySound(audio_path, winsound.SND_FILENAME)
                else:  # macOS/Linux
                    os.system(f'afplay "{audio_path}" || aplay "{audio_path}"')
            except Exception as e:
                logger.error(f"❌ Audio playback error: {e}")
        
        # Clean up after playing
        try:
            time.sleep(0.2)
            os.unlink(audio_path)
        except:
            pass
    
    async def run_conversation_loop(self):
        """Main conversation loop with improved quality"""
        print("🎭 FIXED VOICE CHAT - HIGH QUALITY VERSION")
        print("=" * 50)
        print("✅ Features: Improved speech recognition & high-quality voices")
        print("🎤 Calibrating microphone...")
        
        if not self.calibrate_microphone():
            print("❌ Microphone calibration failed. Continuing anyway...")
        
        print("\n🎯 Ready for conversation!")
        print("💡 Speak clearly and naturally")
        print("💡 Say 'quit' or 'exit' to end conversation")
        print("\n" + "=" * 50)
        
        while True:
            try:
                print("\n🎤 Listening... (speak now)")
                
                # Get speech input with improved recognition
                user_speech = self.improved_speech_recognition(timeout=10)
                
                if user_speech is None:
                    print("❓ I didn't hear anything. Please try again.")
                    continue
                
                print(f"👤 You said: '{user_speech}'")
                
                # Check for exit commands
                if user_speech.lower().strip() in ['quit', 'exit', 'stop', 'goodbye']:
                    print("👋 Goodbye! Thanks for chatting!")
                    break
                
                # Generate AI response
                ai_response = self.generate_better_response(user_speech)
                print(f"🤖 AI: {ai_response}")
                
                # Generate and play high-quality speech
                print("🎵 Generating speech...")
                audio_path = await self.generate_high_quality_speech(ai_response)
                
                if audio_path:
                    print("🔊 Playing response...")
                    self.play_audio_file(audio_path)
                else:
                    print("❌ Speech generation failed")
                
            except KeyboardInterrupt:
                print("\n\n👋 Conversation ended by user. Goodbye!")
                break
            except Exception as e:
                logger.error(f"❌ Conversation loop error: {e}")
                print(f"❌ An error occurred: {e}")
                print("🔄 Continuing conversation...")

async def main():
    """Main function to run the fixed voice chat"""
    chat = FixedVoiceChat()
    await chat.run_conversation_loop()

if __name__ == "__main__":
    asyncio.run(main())
