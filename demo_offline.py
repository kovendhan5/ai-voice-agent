"""
Offline demo of the Orpheus TTS functionality
This demonstrates the TTS generation without needing a running server
"""

import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orpheus_tts import OrpheusModel

def demo_tts():
    """Demonstrate TTS functionality offline"""
    print("🎤 Orpheus TTS Offline Demo")
    print("=" * 40)
    
    try:
        # Create model
        print("📡 Loading Orpheus TTS model...")
        model = OrpheusModel()
        
        # Test different voices and texts
        test_cases = [
            ("tara: Hello! Welcome to Orpheus TTS.", "tara"),
            ("alex: This is a test with Alex's voice.", "alex"),
            ("sarah: Sarah here, testing the speech synthesis.", "sarah"),
            ("tara: This is a longer test message to demonstrate the speech generation capabilities of the Orpheus TTS system.", "tara")
        ]
        
        for i, (text, voice) in enumerate(test_cases, 1):
            print(f"\n🎵 Test {i}: Generating speech...")
            print(f"   Text: {text}")
            print(f"   Voice: {voice}")
            
            # Generate speech
            chunks = model.generate_speech(prompt=text, voice=voice)
            
            # Save to file
            filename = f"demo_output_{i}_{voice}.wav"
            with open(filename, "wb") as f:
                for chunk in chunks:
                    f.write(chunk)
            
            print(f"   ✅ Saved to: {filename}")
            print(f"   📊 Generated {len(chunks)} audio chunks")
        
        print("\n🎉 Demo completed successfully!")
        print("\nGenerated files:")
        for i, (_, voice) in enumerate(test_cases, 1):
            filename = f"demo_output_{i}_{voice}.wav"
            if os.path.exists(filename):
                size = os.path.getsize(filename)
                print(f"  📁 {filename} ({size} bytes)")
        
        print("\n💡 These WAV files can be played in any audio player!")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    demo_tts()
