"""
Quick test of the enhanced Orpheus TTS API
"""
import requests
import json

def test_enhanced_api():
    print("🎭 Testing Enhanced Orpheus TTS API")
    print("="*50)
    
    # Test 1: Status endpoint
    try:
        print("1. Testing status endpoint...")
        response = requests.get('http://localhost:8080/status', timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            status = response.json()
            print(f"   ✅ Server Status: {status['status']}")
            print(f"   🎯 Model: {status['model']}")
            print(f"   📦 Repo: {status['repo']}")
            print(f"   🎤 Voices: {status['voices']}")
            print(f"   😊 Emotions: {status['emotions']}")
            print(f"   🤖 Text Generation: {status.get('text_generation', 'unknown')}")
            print(f"   🔄 Model Loaded: {status['model_loaded']}")
        else:
            print(f"   ❌ Status error: {response.text}")
    except Exception as e:
        print(f"   ❌ Status connection error: {e}")
    
    print()
    
    # Test 2: Voices endpoint
    try:
        print("2. Testing voices endpoint...")
        response = requests.get('http://localhost:8080/voices', timeout=10)
        print(f"   Status Code: {response.status_code}")
        if response.status_code == 200:
            voices = response.json()
            print(f"   ✅ Available voices: {len(voices['voices'])}")
            for voice, desc in list(voices['voices'].items())[:3]:  # Show first 3
                print(f"      • {voice}: {desc}")
        else:
            print(f"   ❌ Voices error: {response.text}")
    except Exception as e:
        print(f"   ❌ Voices connection error: {e}")
    
    print()
    
    # Test 3: Speech synthesis (this will trigger model loading)
    try:
        print("3. Testing speech synthesis (may trigger model loading)...")
        data = {
            'text': 'Hello! <laugh> This is a test of our enhanced Orpheus TTS system!',
            'voice': 'tara'
        }
        
        print("   Sending synthesis request...")
        response = requests.post('http://localhost:8080/synthesize', json=data, timeout=60)  # Longer timeout for model loading
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Synthesis successful!")
            print(f"   🎤 Voice: {result['voice']}")
            print(f"   📝 Text: {result['text'][:50]}...")
            print(f"   🎵 Audio URL: {result.get('audio_url', 'N/A')}")
            print(f"   🎭 Emotions Added: {result.get('emotions_added', 'unknown')}")
        else:
            print(f"   ❌ Synthesis error: {response.text}")
    except Exception as e:
        print(f"   ❌ Synthesis connection error: {e}")
    
    print()
    
    # Test 4: Chat endpoint (enhanced text generation)
    try:
        print("4. Testing enhanced chat endpoint...")
        data = {
            'message': 'Tell me about the weather today!',
            'voice': 'jess'
        }
        
        print("   Sending chat request...")
        response = requests.post('http://localhost:8080/chat', json=data, timeout=60)
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Chat successful!")
            print(f"   🎤 Voice: {result['voice']}")
            print(f"   👤 Personality: {result.get('personality', 'unknown')}")
            print(f"   🤖 Generation Method: {result.get('generation_method', 'unknown')}")
            print(f"   💬 Response: {result['response'][:100]}...")
        else:
            print(f"   ❌ Chat error: {response.text}")
    except Exception as e:
        print(f"   ❌ Chat connection error: {e}")
    
    print("\n🎯 Enhanced API Test Complete!")

if __name__ == "__main__":
    test_enhanced_api()
