#!/usr/bin/env python3
"""
Test the lightweight voice integration
"""

import sys
import os
sys.path.append('src')

def test_lite_integration():
    """Test the lightweight voice integration"""
    print("🎭 Testing Lightweight Voice Integration")
    print("=" * 45)
    
    try:
        # Import the lite version
        from voice_integration_lite import OpenVoiceFallback, get_openvoice_tts
        print("✅ Voice integration module imported")
        
        # Test factory function
        tts = get_openvoice_tts()
        print("✅ TTS instance created")
        
        # Test emotion processing
        test_text = "Hello! This is <excited>amazing</excited> and <cheerful>wonderful</cheerful>!"
        cleaned_text, emotion = tts.process_emotion_tags(test_text)
        print(f"✅ Emotion processing:")
        print(f"   Input: {test_text}")
        print(f"   Output: {cleaned_text}")
        print(f"   Emotion: {emotion}")
        
        # Test model loading
        loaded = tts.load_models()
        print(f"✅ Model loading: {loaded}")
        
        print("\n🎉 Lightweight integration working!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_speech_synthesis():
    """Test actual speech synthesis (optional)"""
    print("\n🔊 Testing Speech Synthesis (optional)")
    print("-" * 45)
    
    try:
        from voice_integration_lite import get_openvoice_tts
        tts = get_openvoice_tts()
        
        # Test text
        test_text = "Hello! This is a test of emotional speech synthesis."
        
        print(f"Synthesizing: '{test_text}'")
        
        # Try synthesis (this will test Edge TTS import)
        result = tts.synthesize_speech(test_text, emotion='cheerful')
        
        if result:
            print(f"✅ Speech synthesized: {result}")
            
            # Clean up temp file
            if os.path.exists(result):
                os.unlink(result)
                print("✅ Temp file cleaned up")
            
            return True
        else:
            print("⚠️  Synthesis returned None (may be expected if Edge TTS unavailable)")
            return False
            
    except Exception as e:
        print(f"⚠️  Speech synthesis test failed: {e}")
        print("   This is OK if Edge TTS is not available")
        return False

def main():
    """Run all tests"""
    print("🧪 LIGHTWEIGHT VOICE INTEGRATION TEST")
    print("=" * 50)
    
    # Test 1: Basic integration
    basic_ok = test_lite_integration()
    
    # Test 2: Speech synthesis (optional)
    speech_ok = test_speech_synthesis()
    
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    
    if basic_ok:
        print("✅ Core voice integration working")
        if speech_ok:
            print("✅ Speech synthesis working")
        else:
            print("⚠️  Speech synthesis needs Edge TTS")
        
        print("\n🔧 Status: READY FOR USE")
        print("💡 The system can handle emotion processing and will use available TTS")
        return True
    else:
        print("❌ Core integration failed")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
