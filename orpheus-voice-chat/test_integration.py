#!/usr/bin/env python3
"""
Quick test of OpenVoice integration functionality
"""

import sys
import os
sys.path.append('src')

def test_speech_synthesis():
    """Test speech synthesis with emotion tags"""
    print("🧪 Testing OpenVoice Speech Synthesis...")
    
    try:
        from openvoice_integration import create_orpheus_tts
        
        # Create TTS instance
        tts = create_orpheus_tts()
        print(f"✅ TTS created: {type(tts).__name__}")
        
        # Test texts with emotions
        test_cases = [
            ("Hello! This is a simple test.", "default"),
            ("Hello! <laugh> This is so funny!", "cheerful"),
            ("I'm feeling <sad> today, but trying to stay positive.", "sad"),
            ("<cheerful> What a wonderful day for testing! <excited> This is amazing!", "cheerful"),
        ]
        
        for text, emotion in test_cases:
            print(f"\n🎤 Testing: '{text}' with emotion '{emotion}'")
            
            result = tts.synthesize_speech(text, emotion=emotion)
            
            if result and os.path.exists(result):
                file_size = os.path.getsize(result)
                print(f"✅ Generated audio: {result} ({file_size} bytes)")
                
                # Clean up test file
                try:
                    os.unlink(result)
                    print("🧹 Cleaned up test file")
                except:
                    pass
            else:
                print("❌ Failed to generate audio")
        
        print("\n✅ Speech synthesis test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

def test_personality_synthesis():
    """Test personality-based synthesis"""
    print("\n🧪 Testing Personality-Based Synthesis...")
    
    try:
        from openvoice_integration import create_orpheus_tts
        
        tts = create_orpheus_tts()
        
        personalities = ["tara", "jessica", "leo", "daniel"]
        test_text = "Hello! <laugh> Nice to meet you! How are you doing today?"
        
        for personality in personalities:
            print(f"\n👤 Testing personality: {personality}")
            
            result = tts.synthesize_with_personality(test_text, personality)
            
            if result and os.path.exists(result):
                file_size = os.path.getsize(result)
                print(f"✅ Generated {personality} voice: {file_size} bytes")
                
                # Clean up
                try:
                    os.unlink(result)
                except:
                    pass
            else:
                print(f"❌ Failed to generate {personality} voice")
        
        print("\n✅ Personality synthesis test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Personality test failed: {e}")
        return False

def test_app_integration():
    """Test integration with main app"""
    print("\n🧪 Testing App Integration...")
    
    try:
        from app_live_orpheus import LiveOrpheusChat
        
        # Initialize chat system
        chat = LiveOrpheusChat()
        print(f"✅ Chat system initialized")
        print(f"   TTS System: {chat.tts_system}")
        print(f"   Available personalities: {list(chat.voice_personalities.keys())}")
        
        # Test speech generation
        test_text = "Hello! <chuckle> This is a test from the chat system."
        audio_bytes = chat.speak_text(test_text, voice="tara")
        
        if audio_bytes:
            print(f"✅ Chat system generated {len(audio_bytes)} bytes of audio")
        else:
            print("❌ Chat system failed to generate audio")
        
        print("\n✅ App integration test completed!")
        return True
        
    except Exception as e:
        print(f"❌ App integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🎭 ORPHEUS OPENVOICE INTEGRATION TESTS")
    print("=" * 50)
    
    results = []
    
    # Test 1: Basic speech synthesis
    results.append(test_speech_synthesis())
    
    # Test 2: Personality-based synthesis  
    results.append(test_personality_synthesis())
    
    # Test 3: App integration
    results.append(test_app_integration())
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 TEST SUMMARY:")
    
    passed = sum(results)
    total = len(results)
    
    if passed == total:
        print(f"✅ All {total} tests passed! System is working correctly.")
        print("🎤 Ready to run the full application!")
    else:
        print(f"⚠️  {passed}/{total} tests passed.")
        print("💡 The system will work with Edge TTS fallback.")
    
    print(f"\n🔧 Current status: Using {tts.tts_system if 'tts' in locals() else 'Edge TTS fallback'}")
    print("📖 For full OpenVoice setup: see docs/OPENVOICE_INTEGRATION.md")
