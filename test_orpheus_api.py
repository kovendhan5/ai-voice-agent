"""
Test Authentic Orpheus TTS API
"""

import requests
import json
import time

def test_orpheus_api():
    base_url = "http://localhost:8080"
    
    print("🎭 Testing Authentic Orpheus TTS API")
    print("="*50)
    
    # Test 1: Status check
    print("\n1. 📊 Testing status endpoint...")
    try:
        response = requests.get(f"{base_url}/status")
        if response.status_code == 200:
            status_data = response.json()
            print(f"✅ Status: {status_data['status']}")
            print(f"🎯 Model: {status_data['model']}")
            print(f"📦 Repo: {status_data['repo']}")
            print(f"🎭 Voices: {status_data['voices']}")
            print(f"😄 Emotions: {status_data['emotions']}")
            print(f"🔧 Mock Model: {status_data.get('is_mock', False)}")
        else:
            print(f"❌ Status check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Status check error: {e}")
        return False
    
    # Test 2: Get voices
    print("\n2. 🎭 Testing voices endpoint...")
    try:
        response = requests.get(f"{base_url}/voices")
        if response.status_code == 200:
            voices_data = response.json()
            print(f"✅ Found {voices_data['total_voices']} voices")
            for voice, desc in list(voices_data['voices'].items())[:3]:
                print(f"   🎤 {voice}: {desc}")
            print(f"   ... and {voices_data['total_voices'] - 3} more")
        else:
            print(f"❌ Voices check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Voices check error: {e}")
    
    # Test 3: Text-to-Speech synthesis
    print("\n3. 🎤 Testing speech synthesis...")
    try:
        test_data = {
            "text": "Hey there! <chuckle> This is a test of the authentic Orpheus TTS system. <laugh> Pretty cool, right?",
            "voice": "tara",
            "add_emotions": True
        }
        
        print(f"📝 Text: {test_data['text']}")
        print(f"🎭 Voice: {test_data['voice']}")
        print("⏳ Generating speech...")
        
        start_time = time.time()
        response = requests.post(
            f"{base_url}/synthesize",
            json=test_data,
            timeout=60  # Give it time to download model if needed
        )
        
        if response.status_code == 200:
            generation_time = time.time() - start_time
            audio_size = len(response.content)
            print(f"✅ Speech generated successfully!")
            print(f"📊 Generation time: {generation_time:.2f}s")
            print(f"📁 Audio size: {audio_size:,} bytes")
            print(f"🎵 Format: WAV audio")
            
            # Save the audio file for testing
            with open("test_orpheus_output.wav", "wb") as f:
                f.write(response.content)
            print(f"💾 Saved to: test_orpheus_output.wav")
            
        else:
            print(f"❌ Speech synthesis failed: {response.status_code}")
            print(f"Error: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Speech synthesis error: {e}")
        return False
    
    # Test 4: Quick voice test
    print("\n4. 🎯 Testing quick voice test...")
    try:
        response = requests.get(f"{base_url}/test?voice=zac")
        if response.status_code == 200:
            audio_size = len(response.content)
            print(f"✅ Voice test successful!")
            print(f"📁 Test audio size: {audio_size:,} bytes")
            
            # Save the test audio
            with open("test_voice_zac.wav", "wb") as f:
                f.write(response.content)
            print(f"💾 Saved test to: test_voice_zac.wav")
        else:
            print(f"❌ Voice test failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Voice test error: {e}")
    
    print("\n" + "="*50)
    print("🎉 Authentic Orpheus TTS API Test Complete!")
    print("\nGenerated files:")
    print("  📁 test_orpheus_output.wav - Custom text synthesis")
    print("  📁 test_voice_zac.wav - Voice test sample")
    print("\n🎧 Play these files to hear the authentic Orpheus TTS in action!")
    
    return True

if __name__ == "__main__":
    test_orpheus_api()
