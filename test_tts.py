"""
Test TTS functionality directly
"""
import sys
import os
sys.path.append(os.path.dirname(__file__))

from working_ai_server import generate_speech_audio

def test_tts():
    print("🔊 Testing Text-to-Speech...")
    
    test_text = "Hello! This is a test of the text to speech system. Can you hear me clearly?"
    
    try:
        audio_file = generate_speech_audio(test_text)
        print(f"✅ Audio generated successfully: {audio_file}")
        
        # Check file size
        file_size = os.path.getsize(audio_file)
        print(f"📁 File size: {file_size} bytes")
        
        if file_size > 1000:  # Should be bigger than 1KB for real audio
            print("🎉 SUCCESS: Real audio file generated!")
            
            # Try to play it using Windows
            try:
                import subprocess
                subprocess.run(['start', '', audio_file], shell=True, check=True)
                print("🔊 Audio should be playing now...")
            except:
                print("🎵 Audio file created but couldn't auto-play")
                print(f"📂 Manual play: {audio_file}")
        else:
            print("⚠️  File seems too small - might be fallback tone")
            
    except Exception as e:
        print(f"❌ TTS test failed: {e}")

if __name__ == "__main__":
    test_tts()
