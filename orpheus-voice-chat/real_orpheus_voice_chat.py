#!/usr/bin/env python3
"""
🎭 REAL ORPHEUS-TTS VOICE CHAT WITH EMOTIONS
==============================================
Complete voice chat system using authentic Orpheus-TTS with emotion tag support.

Features:
- Real Orpheus-TTS for demo-quality voice synthesis
- Emotion tags: <laugh>, <whisper>, <excited>, <sad>, <angry>, <happy>, etc.
- AI conversations with Google Gemini
- Speech recognition
- Multiple voices: tara, leah, jess, leo, dan, mia, zac, zoe
"""

import os
import sys
import time
import threading
import asyncio
from typing import Optional

# Core dependencies
import speech_recognition as sr
import pygame

# AI and Real TTS
import google.generativeai as genai
from real_orpheus_tts import RealOrpheusTTS

# Environment setup
from dotenv import load_dotenv
load_dotenv()

class RealOrpheusVoiceChat:
    """Complete voice chat using Real Orpheus-TTS"""
    
    def __init__(self, voice: str = "tara"):
        """
        Initialize the voice chat system
        
        Args:
            voice: Voice to use (tara, leah, jess, leo, dan, mia, zac, zoe)
        """
        self.voice = voice
        self.setup_api()
        self.setup_audio()
        self.setup_speech_recognition()
        self.setup_tts()
        self.conversation_history = []
        
        print("🎭 Real Orpheus-TTS Voice Chat Initialized!")
        print(f"🎤 Using voice: {self.voice}")
        print("\n💡 Emotion Tags Supported by Real Orpheus-TTS:")
        print("   <laugh>text</laugh> - Laughing voice")
        print("   <chuckle>text</chuckle> - Chuckling voice") 
        print("   <whisper>text</whisper> - Whispering voice")
        print("   <excited>text</excited> - Excited voice")
        print("   <sad>text</sad> - Sad voice")
        print("   <angry>text</angry> - Angry voice")
        print("   <happy>text</happy> - Happy voice")
        print("   <sigh>text</sigh> - Sighing voice")
        print("   <gasp>text</gasp> - Gasping voice")
        print("   <cough>text</cough> - Coughing voice")
        print("\n🎯 The AI will automatically use emotion tags for natural conversations!")
    
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
            pygame.mixer.init(frequency=24000, size=-16, channels=1, buffer=1024)
            print("✅ Pygame audio initialized for 24kHz mono")
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
    
    def setup_tts(self):
        """Setup Real Orpheus-TTS"""
        try:
            self.tts = RealOrpheusTTS(voice=self.voice)
            print("✅ Real Orpheus-TTS ready")
        except Exception as e:
            print(f"❌ Failed to initialize Orpheus-TTS: {e}")
            sys.exit(1)
    
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
            # Enhanced prompt for realistic emotion tag usage
            emotion_prompt = f"""
You are an expressive AI assistant that uses emotion tags in your speech to sound more natural and human-like. 
Use these Real Orpheus-TTS emotion tags naturally in your responses:

- <happy>text</happy> - for positive, cheerful content
- <excited>text</excited> - for enthusiastic responses  
- <laugh>text</laugh> - for humorous content or when laughing
- <chuckle>text</chuckle> - for mild amusement
- <whisper>text</whisper> - for secrets, quiet emphasis, or intimate conversation
- <sad>text</sad> - for sympathetic or melancholy content
- <angry>text</angry> - for frustrated responses (use sparingly)
- <gasp>text</gasp> - for surprise or shock
- <sigh>text</sigh> - for disappointment or tiredness
- <cough>text</cough> - for clearing throat or hesitation

Use emotion tags naturally and realistically. Don't overuse them - mix tagged and untagged speech for natural conversation.
For example: "<happy>Hello there!</happy> It's great to chat with you. <excited>What would you like to talk about?</excited>"

Be conversational, friendly, and engaging. Respond to the user's emotions and match their energy level.

User said: {user_input}
"""
            
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
            error_msg = f"<sad>Sorry, I encountered an error: {str(e)}</sad>"
            print(f"❌ AI Error: {e}")
            return error_msg
    
    def play_audio(self, audio_file: str):
        """Play audio file using pygame"""
        if not audio_file or not os.path.exists(audio_file):
            print("❌ Audio file not found")
            return
        
        try:
            print("🔊 Playing Real Orpheus-TTS audio...")
            pygame.mixer.music.load(audio_file)
            pygame.mixer.music.play()
            
            # Wait for playback to complete
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
                
            print("✅ Audio playback completed")
            
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
        finally:
            # Clean up temporary file
            try:
                os.unlink(audio_file)
            except:
                pass
    
    def speak_text(self, text: str):
        """Convert text to speech using Real Orpheus-TTS"""
        if not text.strip():
            return
        
        print("🎭 Converting to speech with Real Orpheus-TTS...")
        
        try:
            # Generate speech using real Orpheus-TTS
            audio_file = self.tts.generate_speech_file(text)
            
            if audio_file:
                self.play_audio(audio_file)
            else:
                print("❌ Failed to generate speech")
                
        except Exception as e:
            print(f"❌ Speech synthesis error: {e}")
    
    def change_voice(self, voice: str):
        """Change the voice dynamically"""
        self.tts.set_voice(voice)
        self.voice = voice
        print(f"🎤 Voice changed to: {voice}")
    
    def run_conversation(self):
        """Main conversation loop"""
        print("\n🎭 Starting Real Orpheus-TTS Voice Chat!")
        print("💬 Say something to begin the conversation...")
        print("🛑 Say 'goodbye', 'exit', or 'quit' to end")
        print("🎤 Say 'change voice to [name]' to switch voices")
        print(f"🎯 Available voices: tara, leah, jess, leo, dan, mia, zac, zoe\n")
        
        while True:
            try:
                # Listen for user input
                user_input = self.listen_for_speech()
                
                if not user_input:
                    continue
                
                # Check for voice change commands
                if "change voice to" in user_input.lower():
                    voice_words = user_input.lower().split()
                    try:
                        voice_index = voice_words.index("to") + 1
                        if voice_index < len(voice_words):
                            new_voice = voice_words[voice_index]
                            self.change_voice(new_voice)
                            response = f"<happy>Voice changed to {new_voice}!</happy>"
                            self.speak_text(response)
                    except:
                        response = "<sad>Sorry, I didn't understand which voice you want.</sad>"
                        self.speak_text(response)
                    continue
                
                # Check for exit commands
                if any(word in user_input.lower() for word in ['goodbye', 'exit', 'quit', 'stop']):
                    farewell = "<happy>Goodbye!</happy> <chuckle>It was wonderful talking with you!</chuckle> <whisper>Take care!</whisper>"
                    print(f"🤖 {farewell}")
                    self.speak_text(farewell)
                    break
                
                # Get AI response with emotions
                ai_response = self.get_ai_response(user_input)
                
                # Speak the response with Real Orpheus-TTS
                self.speak_text(ai_response)
                
            except KeyboardInterrupt:
                print("\n🛑 Chat interrupted by user")
                break
            except Exception as e:
                print(f"❌ Conversation error: {e}")
                error_speech = "<sad>I'm sorry, something went wrong.</sad> <whisper>Let's try again.</whisper>"
                self.speak_text(error_speech)

def main():
    """Main function to run the Real Orpheus-TTS voice chat"""
    print("🎭 REAL ORPHEUS-TTS VOICE CHAT WITH EMOTIONS")
    print("=" * 60)
    print("🎯 Authentic Orpheus-TTS for demo-quality voice synthesis")
    print("🎪 Complete emotion tag support for natural conversations")
    print("🎤 Multiple voice options available")
    print("=" * 60)
    
    # Ask user to choose a voice
    print("\n🎤 Choose your voice:")
    print("   1. tara (recommended - most natural)")
    print("   2. leah")
    print("   3. jess") 
    print("   4. leo")
    print("   5. dan")
    print("   6. mia")
    print("   7. zac")
    print("   8. zoe")
    
    try:
        voice_choice = input("\nEnter voice name (or press Enter for 'tara'): ").strip().lower()
        if not voice_choice:
            voice_choice = "tara"
        
        # Validate voice choice
        valid_voices = ["tara", "leah", "jess", "leo", "dan", "mia", "zac", "zoe"]
        if voice_choice not in valid_voices:
            print(f"⚠️ Invalid voice '{voice_choice}', using 'tara'")
            voice_choice = "tara"
        
        print(f"🎤 Selected voice: {voice_choice}")
        
        # Create and run the voice chat
        chat = RealOrpheusVoiceChat(voice=voice_choice)
        
        # Run the conversation
        chat.run_conversation()
        
    except KeyboardInterrupt:
        print("\n👋 Voice chat ended by user")
    except Exception as e:
        print(f"❌ Application error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
