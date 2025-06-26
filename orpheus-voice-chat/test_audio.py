"""
Quick test of audio generation
"""
import sys
import os
sys.path.append('src')

from app_orpheus_demo import OrpheusDemo

def test_audio():
    print("🎭 Testing Orpheus Audio Generation...")
    
    # Create demo instance
    demo = OrpheusDemo()
    
    # Test simple text
    test_text = "Hello there! <laugh> This is a test of Orpheus voice generation."
    print(f"Testing: {test_text}")
    
    # Generate audio
    audio_bytes, error = demo.generate_speech(test_text, "tara")
    
    if error:
        print(f"❌ Error: {error}")
        return False
    
    if audio_bytes and len(audio_bytes) > 0:
        print(f"✅ Success! Generated {len(audio_bytes)} bytes of audio")
        
        # Save test file
        with open("test_output.wav", "wb") as f:
            f.write(audio_bytes)
        print("✅ Saved as test_output.wav")
        return True
    else:
        print("❌ No audio generated")
        return False

if __name__ == "__main__":
    test_audio()
