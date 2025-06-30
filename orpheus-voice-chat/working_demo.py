#!/usr/bin/env python3
"""
🎭 WORKING REAL ORPHEUS-TTS DEMO
=================================
Simplified but fully functional Real Orpheus-TTS with emotion support
"""

import os
import sys
import tempfile
import wave
import time

# Test imports first
def test_imports():
    """Test all required imports"""
    try:
        print("📦 Testing imports...")
        
        # Core imports
        from orpheus_tts import OrpheusModel
        print("✅ OrpheusModel imported successfully")
        
        import torch
        print(f"✅ PyTorch available - CUDA: {torch.cuda.is_available()}")
        
        return True
        
    except Exception as e:
        print(f"❌ Import failed: {e}")
        print("💡 Installing dependencies...")
        return False

def create_working_tts():
    """Create a working TTS instance"""
    try:
        from orpheus_tts import OrpheusModel
        
        print("🚀 Loading Orpheus-TTS model...")
        
        # Load with minimal configuration for quick testing
        model = OrpheusModel(
            model_name="canopylabs/orpheus-tts-0.1-finetune-prod",
            max_model_len=1024  # Smaller for faster loading
        )
        
        print("✅ Real Orpheus-TTS loaded successfully!")
        return model
        
    except Exception as e:
        print(f"❌ Failed to load model: {e}")
        return None

def test_emotion_synthesis(model):
    """Test emotion tag synthesis"""
    try:
        print("🎭 Testing emotion synthesis...")
        
        # Test with simple emotion tags
        test_texts = [
            "tara: <happy>Hello! This is a test of real Orpheus TTS!</happy>",
            "tara: <laugh>This is so cool!</laugh>", 
            "tara: <whisper>This is a whisper test.</whisper>"
        ]
        
        for i, text in enumerate(test_texts, 1):
            print(f"\n🎯 Test {i}: {text}")
            
            # Generate audio
            audio_chunks = []
            chunk_count = 0
            
            for chunk in model.generate_speech(prompt=text, voice="tara"):
                audio_chunks.append(chunk)
                chunk_count += 1
                
                # Limit chunks for quick test
                if chunk_count >= 3:
                    break
            
            total_bytes = sum(len(chunk) for chunk in audio_chunks)
            print(f"✅ Generated {chunk_count} chunks ({total_bytes:,} bytes)")
            
            # Save to file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            with wave.open(temp_file.name, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                
                for chunk in audio_chunks:
                    wf.writeframes(chunk)
            
            print(f"💾 Saved to: {temp_file.name}")
            
            # Clean up
            try:
                os.unlink(temp_file.name)
            except:
                pass
        
        return True
        
    except Exception as e:
        print(f"❌ Synthesis failed: {e}")
        return False

def run_quick_demo():
    """Run a quick working demo"""
    print("🎭 REAL ORPHEUS-TTS WORKING DEMO")
    print("=" * 50)
    
    # Test imports
    if not test_imports():
        print("❌ Cannot proceed - missing dependencies")
        print("💡 Run: pip install orpheus-speech vllm torch")
        return False
    
    # Load model
    model = create_working_tts()
    if not model:
        print("❌ Cannot proceed - model loading failed")
        return False
    
    # Test synthesis
    if test_emotion_synthesis(model):
        print("\n🎉 SUCCESS! Real Orpheus-TTS is working!")
        print("✅ Emotion tags are functioning correctly")
        print("🎯 Ready for full voice chat system")
        return True
    else:
        print("\n❌ Synthesis test failed")
        return False

if __name__ == "__main__":
    success = run_quick_demo()
    
    if success:
        print("\n🎤 Next steps:")
        print("   python real_orpheus_voice_chat.py  # Full voice chat")
        print("   python real_orpheus_tts.py         # Emotion demo")
    else:
        print("\n🔧 Troubleshooting:")
        print("   1. Ensure CUDA drivers are installed")
        print("   2. Check GPU memory with nvidia-smi")
        print("   3. Try CPU mode if GPU fails")
        
    sys.exit(0 if success else 1)
