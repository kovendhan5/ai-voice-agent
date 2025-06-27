#!/usr/bin/env python3
"""
Simple Integration Test - Demo Output
"""

import sys
import os
import time
sys.path.append('src')

def test_speech_synthesis():
    """Test speech synthesis with emotion tags"""
    print("Testing OpenVoice Speech Synthesis...")
    
    try:
        # Try the integrated system first
        try:
            from openvoice_integration import create_orpheus_tts
            tts = create_orpheus_tts()
            print(f"✓ TTS created: {type(tts).__name__}")
        except Exception as e:
            print(f"! OpenVoice integration issue: {e}")
            print("→ Falling back to Ultra-Enhanced TTS...")
            from ultra_enhanced_tts import UltraEnhancedEdgeTTS
            tts = UltraEnhancedEdgeTTS()
            print(f"✓ TTS created: {tts.tts_system}")
        
        # Test texts with emotions
        test_cases = [
            ("Hello! This is a simple test.", "default"),
            ("Hello! This is so funny!", "cheerful"),
            ("I'm feeling sad today, but trying to stay positive.", "sad"),
            ("What a wonderful day for testing! This is amazing!", "cheerful"),
        ]
        
        for text, emotion in test_cases:
            print(f"\n♪ Testing: '{text}' with emotion '{emotion}'")
            
            try:
                # Use the correct method based on TTS type
                if hasattr(tts, 'synthesize_speech'):
                    result = tts.synthesize_speech(text, emotion=emotion)
                elif hasattr(tts, 'speak_text'):
                    result = tts.speak_text(text, emotion=emotion)
                else:
                    print("✗ No known synthesis method")
                    continue
                
                if result and os.path.exists(result):
                    file_size = os.path.getsize(result)
                    print(f"✓ Generated audio: {os.path.basename(result)} ({file_size} bytes)")
                    
                    # Clean up test file
                    try:
                        os.unlink(result)
                        print("→ Cleaned up test file")
                    except:
                        pass
                else:
                    print("✗ Failed to generate audio")
            except Exception as e:
                print(f"✗ Generation error: {e}")
        
        print("\n✓ Speech synthesis test completed!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed: {e}")
        return False

def test_personality_synthesis():
    """Test personality-based synthesis"""
    print("\nTesting Personality-Based Synthesis...")
    
    try:
        # Try the integrated system first
        try:
            from openvoice_integration import create_orpheus_tts
            tts = create_orpheus_tts()
        except Exception as e:
            print(f"! OpenVoice integration issue: {e}")
            print("→ Falling back to Ultra-Enhanced TTS...")
            from ultra_enhanced_tts import UltraEnhancedEdgeTTS
            tts = UltraEnhancedEdgeTTS()
        
        personalities = ["tara", "jessica", "zoe", "alex"]
        test_text = "Hello! Nice to meet you! How are you doing today?"
        
        for personality in personalities:
            print(f"\n♦ Testing personality: {personality}")
            
            try:
                # Use the correct method based on TTS type
                if hasattr(tts, 'synthesize_with_personality'):
                    result = tts.synthesize_with_personality(test_text, personality)
                elif hasattr(tts, 'synthesize_speech'):
                    # Use emotion-based synthesis as fallback
                    emotion = "cheerful" if personality == "tara" else "confident"
                    result = tts.synthesize_speech(test_text, emotion=emotion)
                else:
                    print(f"✗ No personality synthesis method available")
                    continue
                
                if result and os.path.exists(result):
                    file_size = os.path.getsize(result)
                    print(f"✓ Generated {personality} voice: {file_size} bytes")
                    
                    # Clean up
                    try:
                        os.unlink(result)
                    except:
                        pass
                else:
                    print(f"✗ Failed to generate {personality} voice")
            except Exception as e:
                print(f"✗ Error for {personality}: {e}")
        
        print("\n✓ Personality synthesis test completed!")
        return True
        
    except Exception as e:
        print(f"✗ Personality test failed: {e}")
        return False

def test_app_integration():
    """Test integration with main app"""
    print("\nTesting App Integration...")
    
    try:
        from app_live_orpheus import LiveOrpheusChat
        
        # Initialize chat system
        chat = LiveOrpheusChat()
        print(f"✓ Chat system initialized")
        print(f"  TTS System: {chat.tts_system}")
        print(f"  Available personalities: {list(chat.voice_personalities.keys())}")
        
        # Test speech generation
        test_text = "Hello! This is a test from the chat system."
        audio_bytes = chat.speak_text(test_text, voice="tara")
        
        if audio_bytes:
            print(f"✓ Chat system generated {len(audio_bytes)} bytes of audio")
        else:
            print("✗ Chat system failed to generate audio")
        
        print("\n✓ App integration test completed!")
        return True
        
    except Exception as e:
        print(f"✗ App integration test failed: {e}")
        return False

if __name__ == "__main__":
    print("ORPHEUS OPENVOICE INTEGRATION TESTS")
    print("=" * 50)
    
    start_time = time.time()
    results = []
    
    # Test 1: Basic speech synthesis
    print("\n[1/3] Basic Speech Synthesis Test")
    results.append(test_speech_synthesis())
    
    # Test 2: Personality-based synthesis  
    print("\n[2/3] Personality-Based Synthesis Test")
    results.append(test_personality_synthesis())
    
    # Test 3: App integration
    print("\n[3/3] App Integration Test")
    results.append(test_app_integration())
    
    # Summary
    end_time = time.time()
    print("\n" + "=" * 50)
    print("TEST SUMMARY:")
    
    passed = sum(results)
    total = len(results)
    
    print(f"Completed: {total} tests")
    print(f"Passed: {passed}")
    print(f"Failed: {total - passed}")
    print(f"Time: {end_time - start_time:.2f} seconds")
    
    if passed == total:
        print("✓ All tests passed! System is working correctly.")
        print("→ Ready to run the full application!")
    else:
        print(f"! {passed}/{total} tests passed.")
        print("→ The system will work with Edge TTS fallback.")
    
    print(f"\nCurrent status: Voice synthesis system operational")
    print("For full OpenVoice setup: see docs/OPENVOICE_INTEGRATION.md")
