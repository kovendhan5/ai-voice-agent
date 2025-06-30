#!/usr/bin/env python3
"""
🧪 QUICK TEST - REAL ORPHEUS-TTS
=================================
Simple test to verify Real Orpheus-TTS is working correctly
"""

import os
import time

def test_orpheus_import():
    """Test if we can import the Orpheus TTS"""
    try:
        from orpheus_tts import OrpheusModel
        print("✅ OrpheusModel import successful")
        return True
    except Exception as e:
        print(f"❌ Import failed: {e}")
        return False

def test_orpheus_model():
    """Test if we can load the Orpheus model"""
    try:
        from orpheus_tts import OrpheusModel
        
        print("🚀 Loading Orpheus-TTS model...")
        model = OrpheusModel(
            model_name="canopylabs/orpheus-tts-0.1-finetune-prod",
            max_model_len=512  # Small for quick test
        )
        print("✅ Model loaded successfully!")
        return model
        
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return None

def test_simple_generation():
    """Test a simple text generation"""
    model = test_orpheus_model()
    if not model:
        return False
    
    try:
        print("🎭 Testing simple text generation...")
        
        # Simple test text with emotion
        text = "tara: <happy>Hello! This is a test of the real Orpheus TTS!</happy>"
        
        print(f"📝 Input: {text}")
        
        # Generate speech
        audio_chunks = []
        for chunk in model.generate_speech(prompt=text, voice="tara"):
            audio_chunks.append(chunk)
            if len(audio_chunks) >= 3:  # Just test first few chunks
                break
        
        print(f"✅ Generated {len(audio_chunks)} audio chunks successfully!")
        total_bytes = sum(len(chunk) for chunk in audio_chunks)
        print(f"📊 Total audio data: {total_bytes:,} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Generation failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 REAL ORPHEUS-TTS QUICK TEST")
    print("=" * 40)
    
    # Test 1: Import
    print("\n1️⃣ Testing imports...")
    if not test_orpheus_import():
        print("❌ Cannot proceed - import failed")
        return
    
    # Test 2: Model loading  
    print("\n2️⃣ Testing model loading...")
    model = test_orpheus_model()
    if not model:
        print("❌ Cannot proceed - model loading failed")
        return
    
    # Test 3: Simple generation
    print("\n3️⃣ Testing speech generation...")
    if test_simple_generation():
        print("\n🎉 ALL TESTS PASSED!")
        print("✅ Real Orpheus-TTS is working correctly!")
        print("🎯 Ready for emotion-enhanced voice chat!")
    else:
        print("\n❌ Generation test failed")
        print("💡 Check your GPU/CUDA setup or model permissions")

if __name__ == "__main__":
    main()
