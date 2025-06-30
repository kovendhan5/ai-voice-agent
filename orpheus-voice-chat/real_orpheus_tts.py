#!/usr/bin/env python3
"""
🎭 REAL ORPHEUS-TTS WITH EMOTION TAGS
=====================================
Authentic Orpheus-TTS implementation with emotion tag support for demo-quality voice synthesis.

Features:
- Real Orpheus-TTS from canopylabs/orpheus-tts-0.1-finetune-prod
- Emotion tags: <laugh>, <whisper>, <excited>, <sad>, <angry>, <happy>, etc.
- Streaming audio generation
- Multiple voice options: tara, leah, jess, leo, dan, mia, zac, zoe
"""

import os
import re
import time
import wave
import tempfile
import asyncio
from typing import List, Tuple, Optional, Dict, Any

# Real Orpheus-TTS
from orpheus_tts import OrpheusModel
import torch

# Audio processing
import numpy as np

# Environment setup
from dotenv import load_dotenv
load_dotenv()

class RealOrpheusTTS:
    """Real Orpheus-TTS with emotion tag support"""
    
    def __init__(self, voice: str = "tara", model_name: str = "canopylabs/orpheus-tts-0.1-finetune-prod"):
        """
        Initialize the real Orpheus-TTS model
        
        Args:
            voice: Voice to use (tara, leah, jess, leo, dan, mia, zac, zoe)
            model_name: Orpheus model to load
        """
        self.voice = voice
        self.model_name = model_name
        self.model = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Emotion tag mapping for natural speech
        self.emotion_tags = {
            "laugh": "<laugh>",
            "chuckle": "<chuckle>", 
            "whisper": "<whisper>",
            "excited": "<excited>",
            "sad": "<sad>",
            "angry": "<angry>",
            "happy": "<happy>",
            "neutral": "",
            "sigh": "<sigh>",
            "cough": "<cough>",
            "sniffle": "<sniffle>",
            "groan": "<groan>",
            "yawn": "<yawn>",
            "gasp": "<gasp>",
            "surprised": "<gasp>",  # Map to gasp for Orpheus
            "calm": "",  # Use neutral voice for calm
            "dramatic": ""  # Use neutral with different formatting
        }
        
        # Initialize the model
        self._load_model()
    
    def _load_model(self):
        """Load the Orpheus-TTS model"""
        try:
            print(f"🚀 Loading Real Orpheus-TTS on {self.device.upper()}...")
            print(f"📦 Model: {self.model_name}")
            print(f"🎤 Voice: {self.voice}")
            
            # Load the real Orpheus model with proper configuration
            self.model = OrpheusModel(
                model_name=self.model_name,
                max_model_len=2048,  # Optimize for memory usage
                device=self.device
            )
            
            print("✅ Real Orpheus-TTS loaded successfully!")
            print("🎭 Emotion tags ready: <laugh>, <whisper>, <excited>, etc.")
            
        except Exception as e:
            print(f"❌ Failed to load Orpheus-TTS: {e}")
            print("💡 Make sure you have: pip install orpheus-speech vllm")
            raise
    
    def parse_emotion_text(self, text: str) -> str:
        """
        Parse and convert emotion tags to Orpheus-compatible format
        
        Args:
            text: Text with emotion tags like <happy>text</happy>
            
        Returns:
            Text formatted for Orpheus-TTS with proper emotion tags
        """
        # Find emotion segments
        emotion_pattern = r'<(laugh|chuckle|whisper|excited|sad|angry|happy|neutral|sigh|cough|sniffle|groan|yawn|gasp|surprised|calm|dramatic)>(.*?)</\1>'
        
        def replace_emotion(match):
            emotion = match.group(1).lower()
            content = match.group(2)
            
            # Get the Orpheus emotion tag
            orpheus_tag = self.emotion_tags.get(emotion, "")
            
            # Format for Orpheus
            if orpheus_tag:
                return f"{orpheus_tag}{content}"
            else:
                return content
        
        # Replace emotion tags
        processed_text = re.sub(emotion_pattern, replace_emotion, text, flags=re.IGNORECASE | re.DOTALL)
        
        # Also handle single tags without closing (e.g., <laugh>text)
        single_tag_pattern = r'<(laugh|chuckle|whisper|excited|sad|angry|happy|neutral|sigh|cough|sniffle|groan|yawn|gasp|surprised|calm|dramatic)>([^<]*?)(?=<|$)'
        
        def replace_single_emotion(match):
            emotion = match.group(1).lower()
            content = match.group(2)
            
            orpheus_tag = self.emotion_tags.get(emotion, "")
            if orpheus_tag:
                return f"{orpheus_tag}{content}"
            else:
                return content
        
        processed_text = re.sub(single_tag_pattern, replace_single_emotion, processed_text, flags=re.IGNORECASE | re.DOTALL)
        
        return processed_text.strip()
    
    def format_prompt(self, text: str) -> str:
        """
        Format text with proper Orpheus prompt format
        
        Args:
            text: Input text (can contain emotion tags)
            
        Returns:
            Properly formatted prompt for Orpheus-TTS
        """
        # Process emotion tags first
        processed_text = self.parse_emotion_text(text)
        
        # Format with voice name as required by Orpheus
        formatted_prompt = f"{self.voice}: {processed_text}"
        
        return formatted_prompt
    
    def generate_speech_streaming(self, text: str, **kwargs) -> List[bytes]:
        """
        Generate speech using real Orpheus-TTS with streaming
        
        Args:
            text: Text to synthesize (can contain emotion tags)
            **kwargs: Additional generation parameters
            
        Returns:
            List of audio chunks as bytes
        """
        if not self.model:
            raise RuntimeError("Orpheus model not loaded")
        
        # Format the prompt properly
        prompt = self.format_prompt(text)
        
        print(f"🎭 Generating speech with Real Orpheus-TTS...")
        print(f"📝 Prompt: {prompt[:100]}...")
        
        try:
            # Default generation parameters optimized for quality
            generation_params = {
                "voice": self.voice,
                "temperature": 0.7,
                "top_p": 0.9,
                "repetition_penalty": 1.1,
                "max_tokens": 4096,
                **kwargs
            }
            
            # Generate speech with streaming
            audio_chunks = []
            
            start_time = time.time()
            
            # Use the real Orpheus streaming generation
            for audio_chunk in self.model.generate_speech(prompt=prompt, **generation_params):
                audio_chunks.append(audio_chunk)
            
            generation_time = time.time() - start_time
            total_audio_bytes = sum(len(chunk) for chunk in audio_chunks)
            
            print(f"✅ Generated {len(audio_chunks)} chunks ({total_audio_bytes:,} bytes) in {generation_time:.2f}s")
            
            return audio_chunks
            
        except Exception as e:
            print(f"❌ Speech generation failed: {e}")
            raise
    
    def generate_speech_file(self, text: str, output_file: Optional[str] = None, **kwargs) -> str:
        """
        Generate speech and save to file
        
        Args:
            text: Text to synthesize (can contain emotion tags)
            output_file: Output file path (optional, will create temp file if None)
            **kwargs: Additional generation parameters
            
        Returns:
            Path to the generated audio file
        """
        # Generate audio chunks
        audio_chunks = self.generate_speech_streaming(text, **kwargs)
        
        # Create output file
        if output_file is None:
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            output_file = temp_file.name
            temp_file.close()
        
        # Write to WAV file
        print(f"💾 Saving audio to: {output_file}")
        
        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(1)  # Mono
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(24000)  # 24kHz sample rate
            
            total_frames = 0
            for audio_chunk in audio_chunks:
                frame_count = len(audio_chunk) // (wf.getsampwidth() * wf.getnchannels())
                total_frames += frame_count
                wf.writeframes(audio_chunk)
            
            duration = total_frames / wf.getframerate()
            print(f"🎵 Generated {duration:.2f} seconds of audio")
        
        return output_file
    
    def set_voice(self, voice: str):
        """Change the voice"""
        available_voices = ["tara", "leah", "jess", "leo", "dan", "mia", "zac", "zoe"]
        if voice.lower() in available_voices:
            self.voice = voice.lower()
            print(f"🎤 Voice changed to: {self.voice}")
        else:
            print(f"❌ Voice '{voice}' not available. Available: {', '.join(available_voices)}")

def demo_real_orpheus():
    """Demo the real Orpheus-TTS with emotion tags"""
    print("🎭 REAL ORPHEUS-TTS EMOTION DEMO")
    print("=" * 50)
    
    # Initialize with tara voice (most natural)
    tts = RealOrpheusTTS(voice="tara")
    
    # Demo texts with various emotion combinations
    demo_texts = [
        "<happy>Hello! Welcome to the real Orpheus-TTS demo!</happy>",
        
        "<excited>This is amazing!</excited> <laugh>I can't believe how natural this sounds!</laugh>",
        
        "<whisper>Let me tell you a secret...</whisper> <excited>This voice model is incredibly realistic!</excited>",
        
        "<sad>I'm sorry to hear about that.</sad> <calm>But everything will work out fine.</calm>",
        
        "<laugh>That's hilarious!</laugh> <happy>You have such a great sense of humor!</happy>",
        
        "This is regular speech without any emotion tags, but it still sounds incredibly natural.",
        
        "<gasp>Oh my goodness!</gasp> <excited>I didn't expect it to sound this good!</excited>",
        
        "<chuckle>Well, that was unexpected.</chuckle> <happy>But I'm glad it worked out!</happy>"
    ]
    
    print(f"🎯 Testing {len(demo_texts)} emotion examples with real Orpheus-TTS...\n")
    
    for i, text in enumerate(demo_texts, 1):
        print(f"🎪 Demo {i}/{len(demo_texts)}")
        print(f"📝 Text: {text}")
        
        try:
            # Generate speech with emotion tags
            audio_file = tts.generate_speech_file(text)
            print(f"✅ Generated: {audio_file}")
            
            # Clean up
            try:
                os.unlink(audio_file)
            except:
                pass
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 50)
        time.sleep(1)  # Brief pause between demos
    
    print("🎉 Real Orpheus-TTS emotion demo completed!")

if __name__ == "__main__":
    # Run the demo
    demo_real_orpheus()
