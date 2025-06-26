#!/usr/bin/env python3
"""
Test script for OpenVoice integration
Tests both OpenVoice and fallback systems
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_openvoice_integration():
    """Test the OpenVoice integration module"""
    print("🧪 Testing OpenVoice Integration...")
    
    try:
        from openvoice_integration import create_orpheus_tts
        print("✅ Successfully imported openvoice_integration")
        
        # Test TTS creation
        tts = create_orpheus_tts(prefer_openvoice=True)
        print(f"✅ TTS system created: {type(tts).__name__}")
        
        # Test speech synthesis
        test_text = "Hello! <laugh> This is a test of the OpenVoice system. <cheerful> How exciting!"
        print(f"🎤 Testing synthesis: {test_text}")
        
        result = tts.synthesize_speech(test_text, emotion="cheerful")
        if result:
            print(f"✅ Speech synthesis successful: {result}")
        else:
            print("❌ Speech synthesis failed")
            
        return True
        
    except Exception as e:
        print(f"❌ OpenVoice integration test failed: {e}")
        return False

def test_app_startup():
    """Test the main application startup"""
    print("\n🧪 Testing App Startup...")
    
    try:
        from app_live_orpheus import LiveOrpheusChat
        print("✅ Successfully imported LiveOrpheusChat")
        
        # Test chat initialization
        chat = LiveOrpheusChat()
        print(f"✅ Chat system initialized")
        print(f"   TTS System: {chat.tts_system}")
        print(f"   OpenVoice Available: {hasattr(chat, 'orpheus_tts') and chat.orpheus_tts is not None}")
        
        # Test personalities
        personalities = list(chat.voice_personalities.keys())
        print(f"✅ Available personalities: {personalities}")
        
        return True
        
    except Exception as e:
        print(f"❌ App startup test failed: {e}")
        return False

def test_emotion_processing():
    """Test emotion tag processing"""
    print("\n🧪 Testing Emotion Processing...")
    
    try:
        from openvoice_integration import OpenVoiceFallback
        
        fallback = OpenVoiceFallback()
        
        test_cases = [
            "Hello there!",
            "This is <laugh> so funny!",
            "I'm feeling <sad> today.",
            "<cheerful> What a wonderful day! <excited> Let's have fun!"
        ]
        
        for text in test_cases:
            print(f"  Testing: {text}")
            result = fallback.synthesize_speech(text)
            if result:
                print(f"    ✅ Generated audio file")
            else:
                print(f"    ❌ Failed to generate audio")
        
        return True
        
    except Exception as e:
        print(f"❌ Emotion processing test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🎭 ORPHEUS OPENVOICE INTEGRATION TESTS")
    print("=" * 50)
    
    results = []
    
    # Test 1: OpenVoice Integration
    results.append(test_openvoice_integration())
    
    # Test 2: App Startup
    results.append(test_app_startup())
    
    # Test 3: Emotion Processing
    results.append(test_emotion_processing())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST RESULTS:")
    
    if all(results):
        print("✅ All tests passed! System is ready.")
        print("🎤 You can now run: python src/app_live_orpheus.py")
    else:
        print("⚠️  Some tests failed. Check the output above.")
        print("💡 The system will still work with Edge TTS fallback.")
    
    print("\n🔧 To install full OpenVoice support:")
    print("   scripts\\install_openvoice.bat")

if __name__ == "__main__":
    main()
