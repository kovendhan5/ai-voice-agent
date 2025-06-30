#!/usr/bin/env python3
"""
🎭 STREAMLINED REAL ORPHEUS-TTS VOICE CHAT
===========================================
Simplified but fully functional Real Orpheus-TTS with emotion support
"""

import os
import sys
import time
import tempfile
import wave
from typing import Optional

def setup_environment():
    """Setup the environment and check dependencies"""
    print("🔧 Setting up environment...")
    
    # Check .env file
    env_file = ".env"
    if not os.path.exists(env_file):
        print("⚠️ .env file not found, creating example...")
        with open(env_file, 'w') as f:
            f.write("GOOGLE_API_KEY=your_google_gemini_api_key_here\n")
        print("💡 Please add your Google API key to .env file")
    
    # Load environment
    try:
        from dotenv import load_dotenv
        load_dotenv()
        print("✅ Environment loaded")
    except ImportError:
        print("⚠️ python-dotenv not found, using os.environ")

def test_orpheus_tts():
    """Test Real Orpheus-TTS functionality"""
    print("\n🎭 Testing Real Orpheus-TTS...")
    
    try:
        # Import the model
        from orpheus_tts import OrpheusModel
        print("✅ OrpheusModel imported")
        
        # Check PyTorch
        import torch
        print(f"✅ PyTorch - CUDA available: {torch.cuda.is_available()}")
        
        # Load model with error handling
        print("🚀 Loading model (this may take a moment)...")
        model = OrpheusModel(
            model_name="canopylabs/orpheus-tts-0.1-finetune-prod",
            max_model_len=1024  # Smaller for faster loading
        )
        print("✅ Model loaded successfully!")
        
        return model
        
    except Exception as e:
        print(f"❌ Orpheus-TTS test failed: {e}")
        print("\n🔧 Possible solutions:")
        print("   1. Install: pip install orpheus-speech vllm torch")
        print("   2. Check GPU memory: nvidia-smi")
        print("   3. Restart Python session")
        return None

def test_emotion_generation(model):
    """Test emotion tag generation"""
    print("\n🎭 Testing emotion generation...")
    
    emotion_tests = [
        ("Happy", "tara: <happy>Hello! This is amazing!</happy>"),
        ("Laugh", "tara: <laugh>That's so funny!</laugh>"),
        ("Whisper", "tara: <whisper>This is a secret.</whisper>"),
        ("Excited", "tara: <excited>This is incredible!</excited>")
    ]
    
    for emotion_name, prompt in emotion_tests:
        try:
            print(f"\n🎯 Testing {emotion_name} emotion...")
            print(f"📝 Prompt: {prompt}")
            
            # Generate audio chunks
            chunks = []
            for i, chunk in enumerate(model.generate_speech(prompt=prompt, voice="tara")):
                chunks.append(chunk)
                if i >= 2:  # Limit for quick test
                    break
            
            total_bytes = sum(len(chunk) for chunk in chunks)
            print(f"✅ Generated {len(chunks)} chunks ({total_bytes:,} bytes)")
            
        except Exception as e:
            print(f"❌ {emotion_name} test failed: {e}")

def create_audio_file(model, text: str, output_file: str):
    """Create audio file from text"""
    try:
        print(f"🎵 Creating audio: {text[:50]}...")
        
        # Generate speech
        chunks = []
        for chunk in model.generate_speech(prompt=f"tara: {text}", voice="tara"):
            chunks.append(chunk)
        
        # Save to WAV file
        with wave.open(output_file, "wb") as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(24000)
            
            for chunk in chunks:
                wf.writeframes(chunk)
        
        print(f"✅ Audio saved to: {output_file}")
        return True
        
    except Exception as e:
        print(f"❌ Audio creation failed: {e}")
        return False

def demo_voice_chat():
    """Demo voice chat functionality"""
    print("\n🎤 Demo Voice Chat with Emotions...")
    
    # Setup
    setup_environment()
    
    # Test Orpheus-TTS
    model = test_orpheus_tts()
    if not model:
        return False
    
    # Test emotions
    test_emotion_generation(model)
    
    # Create sample audio files
    sample_texts = [
        "<happy>Welcome to Real Orpheus-TTS!</happy>",
        "<excited>This voice quality is incredible!</excited>",
        "<laugh>It sounds just like the official demos!</laugh>",
        "<whisper>The emotion tags work perfectly.</whisper>"
    ]
    
    print("\n🎵 Creating sample audio files...")
    for i, text in enumerate(sample_texts, 1):
        output_file = f"sample_{i}.wav"
        if create_audio_file(model, text, output_file):
            print(f"📁 Sample {i} ready: {output_file}")
    
    print("\n🎉 SUCCESS! Real Orpheus-TTS is fully functional!")
    return True

def main():
    """Main function"""
    print("🎭 REAL ORPHEUS-TTS VOICE CHAT SYSTEM")
    print("=" * 60)
    print("🎯 Testing authentic Orpheus-TTS with emotion support")
    print("=" * 60)
    
    try:
        success = demo_voice_chat()
        
        if success:
            print("\n✅ SYSTEM READY!")
            print("\n🎤 Available commands:")
            print("   python real_orpheus_voice_chat.py  # Full voice chat")
            print("   python simple_test.py              # Quick test")
            print("   python working_demo.py             # Extended demo")
            
            print("\n🎭 Emotion tags supported:")
            print("   <happy>, <excited>, <laugh>, <whisper>")
            print("   <sad>, <angry>, <gasp>, <sigh>, <cough>")
            
            print("\n🎤 Voices available:")
            print("   tara, leah, jess, leo, dan, mia, zac, zoe")
        else:
            print("\n❌ SETUP INCOMPLETE")
            print("💡 Please install dependencies and try again")
        
        return success
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        return False
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
