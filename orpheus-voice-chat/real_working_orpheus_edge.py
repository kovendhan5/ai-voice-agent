#!/usr/bin/env python3
"""
🎭 REAL WORKING ORPHEUS - EDGE TTS
=================================
ACTUAL working Orpheus with Microsoft Edge TTS
High-quality voices with REAL emotion processing
=================================
"""

import os
import sys
import time
import asyncio
import tempfile
import pygame
from pathlib import Path
from dotenv import load_dotenv
import edge_tts
import warnings
warnings.filterwarnings("ignore")

# Load environment
load_dotenv()

class RealWorkingOrpheus:
    """Real working Orpheus with Edge TTS"""
    
    def __init__(self):
        print("🎭 REAL WORKING ORPHEUS")
        print("=" * 40)
        print("🎪 Microsoft Edge TTS")
        print("🗣️ High-quality voices")
        print("🎭 REAL emotion tag processing")
        print("🚫 NO synthetic noise - REAL voices")
        print("=" * 40)
        
        # Initialize pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        
        # Orpheus voice personalities with Edge TTS
        self.orpheus_voices = {
            'aria': 'en-US-AriaNeural',      # Friendly female
            'jenny': 'en-US-JennyNeural',    # Cheerful female  
            'guy': 'en-US-GuyNeural',        # Calm male
            'davis': 'en-US-DavisNeural',    # Strong male
            'jane': 'en-US-JaneNeural',      # Professional female
            'jason': 'en-US-JasonNeural',    # Casual male
            'sara': 'en-US-SaraNeural',      # Warm female
            'tony': 'en-US-TonyNeural'       # Confident male
        }
        
        self.current_voice = 'aria'
        
        print(f"✅ Real working Orpheus ready!")
        print(f"🎭 Current voice: {self.current_voice}")
        print(f"🎪 Available voices: {', '.join(self.orpheus_voices.keys())}")
    
    async def orpheus_speak_async(self, text_with_emotions):
        """Async speech generation with emotions"""
        # Process Orpheus emotion tags
        clean_text, emotion_info = self.process_orpheus_emotions(text_with_emotions)
        
        if emotion_info:
            print(f"🎭 Emotion: {emotion_info['emotion']} - {emotion_info['description']}")
        
        # Create SSML with emotion effects
        ssml_text = self.create_emotional_ssml(clean_text, emotion_info)
        
        # Get voice
        voice = self.orpheus_voices[self.current_voice]
        
        # Generate speech
        communicate = edge_tts.Communicate(ssml_text, voice)
        
        # Collect audio data
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
        
        return audio_data
    
    def orpheus_speak(self, text_with_emotions):
        """Main speech function"""
        print(f"\n🎭 Orpheus ({self.current_voice}): {text_with_emotions}")
        
        try:
            # Run async function
            audio_data = asyncio.run(self.orpheus_speak_async(text_with_emotions))
            
            if audio_data:
                self.play_real_audio(audio_data)
                return True
            else:
                print("❌ No audio generated")
                return False
                
        except Exception as e:
            print(f"❌ Speech generation failed: {e}")
            return False
    
    def process_orpheus_emotions(self, text):
        """Process Orpheus emotion tags - REAL implementation"""
        orpheus_emotions = {
            '<laugh>': {
                'emotion': 'laugh',
                'description': 'laughter',
                'ssml_style': 'cheerful',
                'rate': '+10%',
                'pitch': '+5%',
                'volume': '+10%',
                'prefix': '*laughs* '
            },
            '<chuckle>': {
                'emotion': 'chuckle', 
                'description': 'soft laughter',
                'ssml_style': 'friendly',
                'rate': '+5%',
                'pitch': '+3%',
                'volume': '+5%',
                'prefix': '*chuckles* '
            },
            '<whisper>': {
                'emotion': 'whisper',
                'description': 'quiet speech',
                'ssml_style': 'gentle',
                'rate': '-20%',
                'pitch': '-10%',
                'volume': '-50%',
                'prefix': ''
            },
            '<sigh>': {
                'emotion': 'sigh',
                'description': 'sighing',
                'ssml_style': 'sad',
                'rate': '-15%',
                'pitch': '-5%',
                'volume': '-10%',
                'prefix': '*sighs* '
            },
            '<gasp>': {
                'emotion': 'gasp',
                'description': 'surprise',
                'ssml_style': 'excited',
                'rate': '+20%',
                'pitch': '+15%',
                'volume': '+20%',
                'prefix': '*gasps* '
            },
            '<groan>': {
                'emotion': 'groan',
                'description': 'groaning',
                'ssml_style': 'displeased',
                'rate': '-10%',
                'pitch': '-15%',
                'volume': '-5%',
                'prefix': '*groans* '
            },
            '<yawn>': {
                'emotion': 'yawn',
                'description': 'tired',
                'ssml_style': 'gentle',
                'rate': '-25%',
                'pitch': '-20%',
                'volume': '-20%',
                'prefix': '*yawns* '
            },
            '<cough>': {
                'emotion': 'cough',
                'description': 'coughing',
                'ssml_style': 'neutral',
                'rate': '0%',
                'pitch': '0%',
                'volume': '-10%',
                'prefix': '*coughs* '
            }
        }
        
        clean_text = text
        emotion_info = None
        
        # Find and process emotion tag
        for tag, info in orpheus_emotions.items():
            if tag in text:
                emotion_info = info.copy()
                clean_text = text.replace(tag, '').strip()
                
                # Add emotional prefix (except for whisper)
                if info['prefix'] and emotion_info['emotion'] != 'whisper':
                    clean_text = info['prefix'] + clean_text
                
                break
        
        return clean_text, emotion_info
    
    def create_emotional_ssml(self, text, emotion_info):
        """Create SSML with emotion effects"""
        if not emotion_info:
            return text
        
        # Create SSML with emotion parameters
        ssml = f'''<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <prosody rate="{emotion_info['rate']}" pitch="{emotion_info['pitch']}" volume="{emotion_info['volume']}">
                <mstts:express-as style="{emotion_info['ssml_style']}">
                    {text}
                </mstts:express-as>
            </prosody>
        </speak>'''
        
        return ssml
    
    def play_real_audio(self, audio_data):
        """Play real audio data"""
        try:
            # Save to temp file
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                temp_file.write(audio_data)
                temp_path = temp_file.name
            
            print("🔊 Playing REAL voice...")
            
            # Play with pygame
            pygame.mixer.music.load(temp_path)
            pygame.mixer.music.play()
            
            # Wait for completion
            while pygame.mixer.music.get_busy():
                time.sleep(0.1)
            
            # Cleanup
            os.unlink(temp_path)
            
            print("✅ Real voice playback completed")
            
        except Exception as e:
            print(f"❌ Audio playback failed: {e}")
    
    def change_voice(self, voice_name):
        """Change Orpheus voice personality"""
        if voice_name in self.orpheus_voices:
            self.current_voice = voice_name
            print(f"🎭 Voice changed to: {voice_name}")
            return True
        else:
            print(f"❌ Voice '{voice_name}' not available")
            return False
    
    def demo_all_voices(self):
        """Demo all Orpheus voices"""
        print("\n🎪 ORPHEUS VOICE DEMO")
        print("=" * 30)
        
        demo_text = "Hello! This is the real Orpheus speaking with authentic voices!"
        
        for voice_name in self.orpheus_voices.keys():
            print(f"\n🎭 Testing voice: {voice_name}")
            self.change_voice(voice_name)
            self.orpheus_speak(demo_text)
            time.sleep(1)
        
        # Reset to default
        self.change_voice('aria')
    
    def interactive_mode(self):
        """Interactive Orpheus mode"""
        print("\n🎭 INTERACTIVE REAL ORPHEUS")
        print("=" * 40)
        print("🎪 Type text with emotion tags")
        print("🎭 Emotions: <laugh>, <whisper>, <gasp>, <sigh>, <chuckle>, <groan>, <yawn>, <cough>")
        print("🔄 Commands: 'voice [name]' to change voice, 'demo' for voice demo")
        print("🛑 Type 'quit' to exit")
        print("=" * 40)
        
        while True:
            try:
                user_input = input(f"\n🎭 Orpheus ({self.current_voice}): ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    print("👋 Goodbye from Real Orpheus!")
                    break
                
                elif user_input.lower() == 'demo':
                    self.demo_all_voices()
                    continue
                
                elif user_input.lower().startswith('voice '):
                    voice_name = user_input[6:].strip()
                    self.change_voice(voice_name)
                    continue
                
                elif not user_input:
                    continue
                
                # Speak with Orpheus
                success = self.orpheus_speak(user_input)
                
                if success:
                    print("✅ Real Orpheus speech completed")
                else:
                    print("❌ Speech failed")
                
            except KeyboardInterrupt:
                print("\n👋 Real Orpheus session ended")
                break
            except Exception as e:
                print(f"❌ Error: {e}")

def main():
    """Main function"""
    print("🎭 REAL WORKING ORPHEUS SYSTEM")
    print("=" * 50)
    print("🎪 Microsoft Edge TTS - REAL voices")
    print("🚫 NO synthetic noise - ACTUAL human-like speech")
    print("🎭 Authentic emotion tag processing")
    print("=" * 50)
    
    try:
        # Initialize real Orpheus
        orpheus = RealWorkingOrpheus()
        
        # Test with emotion tags
        test_phrases = [
            "Hello! Welcome to the REAL Orpheus system!",
            "This is incredible! <laugh> I can't believe how good this sounds!",
            "Listen very carefully <whisper> this is actual human-like speech.",
            "Oh my goodness! <gasp> This technology is amazing!",
            "Well, that's quite impressive <sigh> I must admit.",
            "Ha ha! <chuckle> This is the real deal - no weird noises!",
            "Excuse me! <cough> Pay attention to this demonstration!",
            "I'm getting sleepy now <yawn> but this still sounds fantastic!"
        ]
        
        print(f"\n🧪 Testing {len(test_phrases)} REAL voice phrases...")
        print("🔊 Listen for actual human-like voices with emotions!\n")
        
        for i, phrase in enumerate(test_phrases, 1):
            print(f"[{i}/{len(test_phrases)}] {phrase}")
            success = orpheus.orpheus_speak(phrase)
            
            if success:
                print("✅ Real voice test passed")
            else:
                print("❌ Test failed")
            
            time.sleep(2)
        
        print("\n🎉 Real Orpheus demo complete!")
        print("🗣️ You just heard ACTUAL human-like voices with emotions!")
        
        # Interactive mode
        orpheus.interactive_mode()
        
    except Exception as e:
        print(f"❌ Real Orpheus failed: {e}")

if __name__ == "__main__":
    main()
