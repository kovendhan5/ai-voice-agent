#!/usr/bin/env python3
"""
Test Real Orpheus-TTS Integration
"""

import sys
import os
sys.path.append('src')

def test_orpheus_availability():
    """Test if Orpheus-TTS package is available"""
    print("🎭 Testing Real Orpheus-TTS Availability")
    print("=" * 50)
    
    try:
        import orpheus_tts
        print("✅ orpheus_tts package available")
        
        try:
            from orpheus_tts import OrpheusModel, tokens_decoder_sync
            print("✅ OrpheusModel class available")
            print("✅ tokens_decoder_sync available")
            return True
        except ImportError as e:
            print(f"❌ OrpheusModel components not available: {e}")
            return False
            
    except ImportError as e:
        print(f"❌ orpheus_tts not available: {e}")
        return False

def test_orpheus_basic():
    """Test basic Orpheus-TTS functionality"""
    print("\n🎤 Testing Basic Orpheus-TTS Functionality")
    print("-" * 50)
    
    try:
        from orpheus_real_integration import create_orpheus_tts
        
        # Create TTS instance
        tts = create_orpheus_tts(prefer_real_orpheus=True)
        print(f"✅ TTS instance created: {type(tts).__name__}")
        print(f"   System: {tts.tts_system}")
        
        # Test if it's the real Orpheus-TTS
        if "Orpheus-TTS" in tts.tts_system:
            print("🎉 Real Orpheus-TTS system active!")
            
            # Test speech synthesis
            test_text = "Hello! <laugh> This is the real Orpheus-TTS providing ultra-realistic speech."
            
            print(f"\n🎤 Testing synthesis: '{test_text}'")
            result = tts.synthesize_speech(test_text, voice="tara")
            
            if result and os.path.exists(result):
                size = os.path.getsize(result)
                print(f"✅ Real Orpheus-TTS generated {size} bytes of audio!")
                print(f"   Audio file: {result}")
                
                # Don't delete - let user hear the quality
                print("🎧 Play this file to hear the ultra-realistic quality!")
                return True
            else:
                print("❌ Synthesis failed")
                return False
        else:
            print("⚠️  Using fallback system (not real Orpheus-TTS)")
            return False
            
    except Exception as e:
        print(f"❌ Orpheus-TTS test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Run Orpheus-TTS tests"""
    print("🎭 REAL ORPHEUS-TTS INTEGRATION TEST")
    print("=" * 60)
    
    # Test availability
    available = test_orpheus_availability()
    
    if available:
        # Test functionality
        working = test_orpheus_basic()
        
        if working:
            print("\n🎉 SUCCESS! Real Orpheus-TTS is working!")
            print("🔥 You now have access to ultra-realistic human-like speech synthesis!")
            print("🎤 The quality should be indistinguishable from human speech.")
        else:
            print("\n⚠️  Orpheus-TTS available but needs configuration")
    else:
        print("\n⚠️  Orpheus-TTS package needs to finish installing")
        print("💡 The system will use enhanced Edge TTS fallback for now")
    
    print("\n🚀 Ready to integrate with your voice chat application!")

if __name__ == "__main__":
    main()
