#!/usr/bin/env python3
"""
🎯 INTEL-OPTIMIZED VOICE SYNTHESIS
==================================================
✅ Designed for Intel 12th Gen processors
✅ Works with Intel Iris integrated graphics
✅ No NVIDIA drivers required
✅ Real emotion tag support
==================================================
"""

import os
import sys
import warnings
import torch
import numpy as np
import soundfile as sf
import pygame
import time
from typing import Optional, Dict, List
import tempfile
import threading
import queue

# Force CPU-only mode for Intel systems
os.environ['CUDA_VISIBLE_DEVICES'] = ''
os.environ['FORCE_CPU'] = '1'
torch.set_num_threads(4)  # Optimize for Intel 12th gen

# Suppress warnings
warnings.filterwarnings("ignore")

class IntelOptimizedTTS:
    """
    Intel-optimized TTS system for 12th gen processors
    Uses lightweight models that work without NVIDIA drivers
    """
    
    def __init__(self):
        self.device = 'cpu'
        self.sample_rate = 22050
        self.voices = {
            'tara': {'gender': 'female', 'style': 'warm'},
            'leah': {'gender': 'female', 'style': 'professional'},
            'jess': {'gender': 'female', 'style': 'casual'},
            'leo': {'gender': 'male', 'style': 'deep'},
            'dan': {'gender': 'male', 'style': 'friendly'},
            'mia': {'gender': 'female', 'style': 'expressive'},
            'zac': {'gender': 'male', 'style': 'young'},
            'zoe': {'gender': 'female', 'style': 'energetic'}
        }
        
        self.emotion_tags = {
            '<happy>': {'pitch': 1.2, 'speed': 1.1, 'energy': 1.3},
            '<sad>': {'pitch': 0.8, 'speed': 0.9, 'energy': 0.7},
            '<excited>': {'pitch': 1.3, 'speed': 1.2, 'energy': 1.4},
            '<angry>': {'pitch': 1.1, 'speed': 1.1, 'energy': 1.2},
            '<whisper>': {'pitch': 0.9, 'speed': 0.8, 'energy': 0.5},
            '<laugh>': {'pitch': 1.2, 'speed': 1.0, 'energy': 1.3},
            '<calm>': {'pitch': 1.0, 'speed': 0.9, 'energy': 0.8},
            '<surprised>': {'pitch': 1.4, 'speed': 1.2, 'energy': 1.3}
        }
        
        self.model = None
        self.audio_queue = queue.Queue()
        pygame.mixer.init(frequency=self.sample_rate, size=-16, channels=1, buffer=1024)
        
    def initialize_intel_tts(self):
        """Initialize TTS optimized for Intel processors"""
        print("🔧 Initializing Intel-optimized TTS...")
        
        try:
            # Try Edge TTS first (lightweight, works on Intel)
            import edge_tts
            self.tts_engine = 'edge'
            print("✅ Edge TTS initialized (Intel compatible)")
            return True
            
        except ImportError:
            try:
                # Fallback to pyttsx3 (CPU-only)
                import pyttsx3
                self.model = pyttsx3.init()
                self.tts_engine = 'pyttsx3'
                print("✅ pyttsx3 initialized (CPU-only)")
                return True
                
            except:
                print("❌ Failed to initialize TTS engines")
                return False
    
    def parse_emotion_text(self, text: str) -> tuple:
        """Parse emotion tags from text"""
        emotion_params = {'pitch': 1.0, 'speed': 1.0, 'energy': 1.0}
        clean_text = text
        
        for tag, params in self.emotion_tags.items():
            if tag in text:
                emotion_params.update(params)
                clean_text = clean_text.replace(tag, '')
                print(f"🎭 Detected emotion: {tag}")
                break
                
        return clean_text.strip(), emotion_params
    
    async def generate_edge_tts(self, text: str, voice: str, emotion_params: dict) -> bytes:
        """Generate speech using Edge TTS (Intel compatible)"""
        import edge_tts
        
        # Map our voices to Edge TTS voices
        edge_voices = {
            'tara': 'en-US-AriaNeural',
            'leah': 'en-US-JennyNeural', 
            'jess': 'en-US-AmberNeural',
            'leo': 'en-US-BrandonNeural',
            'dan': 'en-US-GuyNeural',
            'mia': 'en-US-SaraNeural',
            'zac': 'en-US-DavisNeural',
            'zoe': 'en-US-MichelleNeural'
        }
        
        edge_voice = edge_voices.get(voice, 'en-US-AriaNeural')
        
        # Apply emotion parameters as SSML
        pitch_change = f"+{int((emotion_params['pitch'] - 1) * 50)}%"
        rate_change = f"+{int((emotion_params['speed'] - 1) * 50)}%"
        
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
            <voice name="{edge_voice}">
                <prosody pitch="{pitch_change}" rate="{rate_change}">
                    {text}
                </prosody>
            </voice>
        </speak>
        """
        
        communicate = edge_tts.Communicate(ssml, edge_voice)
        audio_data = b""
        async for chunk in communicate.stream():
            if chunk["type"] == "audio":
                audio_data += chunk["data"]
                
        return audio_data
    
    def generate_pyttsx3_audio(self, text: str, voice: str, emotion_params: dict) -> str:
        """Generate speech using pyttsx3 (CPU-only)"""
        if not self.model:
            return None
            
        # Apply emotion parameters
        voices = self.model.getProperty('voices')
        if voices:
            # Choose voice based on gender preference
            voice_info = self.voices.get(voice, {'gender': 'female'})
            for v in voices:
                if voice_info['gender'] in v.name.lower():
                    self.model.setProperty('voice', v.id)
                    break
        
        # Set speech parameters
        rate = int(200 * emotion_params['speed'])
        self.model.setProperty('rate', rate)
        
        volume = emotion_params['energy']
        self.model.setProperty('volume', min(volume, 1.0))
        
        # Generate audio file
        temp_file = tempfile.mktemp(suffix='.wav')
        self.model.save_to_file(text, temp_file)
        self.model.runAndWait()
        
        return temp_file
    
    def play_audio(self, audio_data: bytes = None, file_path: str = None):
        """Play audio using pygame (Intel graphics compatible)"""
        try:
            if audio_data:
                # Play from bytes
                temp_file = tempfile.mktemp(suffix='.wav')
                with open(temp_file, 'wb') as f:
                    f.write(audio_data)
                pygame.mixer.music.load(temp_file)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    
                os.unlink(temp_file)
                
            elif file_path and os.path.exists(file_path):
                # Play from file
                pygame.mixer.music.load(file_path)
                pygame.mixer.music.play()
                
                while pygame.mixer.music.get_busy():
                    time.sleep(0.1)
                    
                os.unlink(file_path)
                
        except Exception as e:
            print(f"❌ Audio playback error: {e}")
    
    async def synthesize_speech(self, text: str, voice: str = 'tara') -> bool:
        """Main synthesis function optimized for Intel systems"""
        if not text.strip():
            return False
            
        print(f"🎤 Synthesizing: '{text[:50]}...' with voice '{voice}'")
        
        # Parse emotions
        clean_text, emotion_params = self.parse_emotion_text(text)
        
        try:
            if self.tts_engine == 'edge':
                # Use Edge TTS (best quality, Intel compatible)
                audio_data = await self.generate_edge_tts(clean_text, voice, emotion_params)
                self.play_audio(audio_data=audio_data)
                
            elif self.tts_engine == 'pyttsx3':
                # Use pyttsx3 (CPU-only fallback)
                audio_file = self.generate_pyttsx3_audio(clean_text, voice, emotion_params)
                if audio_file:
                    self.play_audio(file_path=audio_file)
                    
            print("✅ Speech synthesis complete")
            return True
            
        except Exception as e:
            print(f"❌ Synthesis error: {e}")
            return False

def test_intel_tts():
    """Test Intel-optimized TTS system"""
    print("🎯 INTEL 12TH GEN TTS TEST")
    print("=" * 50)
    print("🖥️ Intel Core i5-12500H")
    print("🎮 Intel Iris Xe Graphics")
    print("🚫 No NVIDIA GPU required")
    print("=" * 50)
    
    # Initialize TTS
    tts = IntelOptimizedTTS()
    
    if not tts.initialize_intel_tts():
        print("❌ Failed to initialize TTS")
        return False
    
    # Test cases
    test_cases = [
        ("Hello! I'm running on your Intel processor.", "tara"),
        ("<happy>This is so exciting! Intel graphics work perfectly!</happy>", "jess"),
        ("<whisper>This is a quiet whisper test</whisper>", "leah"),
        ("<laugh>Haha! No NVIDIA drivers needed!</laugh>", "mia"),
        ("Your Intel 12th gen processor handles this beautifully.", "dan")
    ]
    
    print("\n🧪 Running Intel TTS tests...")
    
    import asyncio
    
    async def run_tests():
        for i, (text, voice) in enumerate(test_cases, 1):
            print(f"\n🔊 Test {i}/5: {voice}")
            success = await tts.synthesize_speech(text, voice)
            if success:
                print(f"✅ Test {i} passed")
            else:
                print(f"❌ Test {i} failed")
            
            # Wait between tests
            await asyncio.sleep(1)
    
    asyncio.run(run_tests())
    print("\n🎉 Intel TTS testing complete!")
    return True

if __name__ == "__main__":
    print("🎯 INTEL-OPTIMIZED ORPHEUS-STYLE TTS")
    print("=" * 50)
    print("💻 Designed for Intel 12th Gen processors")
    print("🎮 Compatible with Intel Iris graphics")
    print("🚫 No NVIDIA drivers required")
    print("=" * 50)
    
    # Check system
    print(f"🖥️ Device: {torch.device('cpu')}")
    print(f"🧵 Threads: {torch.get_num_threads()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Run test
    test_intel_tts()
