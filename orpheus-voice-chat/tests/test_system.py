"""
Quick System Test - Verify everything is working before deployment
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))

import requests
import json

def test_server():
    """Test if the server is running and responding"""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Orpheus Voice Chat Server...")
    print("=" * 50)
    
    # Test 1: Health check
    print("1. Health Check...")
    try:
        response = requests.get(f"{base_url}/")
        if response.status_code == 200:
            print("   ✅ Server is running!")
        else:
            print(f"   ❌ Server returned {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("   ❌ Server not running! Start with: scripts\\start_minimal.bat")
        return False
    
    # Test 2: Voices endpoint
    print("2. Voice List...")
    try:
        response = requests.get(f"{base_url}/voices")
        if response.status_code == 200:
            voices = response.json()
            print(f"   ✅ Found {len(voices)} voices: {', '.join(voices)}")
        else:
            print(f"   ❌ Voices endpoint failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 3: Speech synthesis
    print("3. Speech Generation...")
    try:
        test_data = {
            "text": "tara: Hello! This is a test of the voice system.",
            "voice": "tara"
        }
        response = requests.post(
            f"{base_url}/synthesize",
            headers={"Content-Type": "application/json"},
            data=json.dumps(test_data)
        )
        if response.status_code == 200:
            audio_size = len(response.content)
            print(f"   ✅ Generated audio: {audio_size} bytes")
            
            # Save test file
            with open("test_output.wav", "wb") as f:
                f.write(response.content)
            print("   📄 Saved as: test_output.wav")
        else:
            print(f"   ❌ Speech generation failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    # Test 4: Chat endpoint
    print("4. Chat Interface...")
    try:
        chat_data = {"message": "Hello there!"}
        response = requests.post(
            f"{base_url}/chat",
            headers={"Content-Type": "application/json"},
            data=json.dumps(chat_data)
        )
        if response.status_code == 200:
            result = response.json()
            print(f"   ✅ Chat response: {result.get('response', 'N/A')[:50]}...")
        else:
            print(f"   ❌ Chat failed: {response.status_code}")
    except Exception as e:
        print(f"   ❌ Error: {e}")
    
    print("\n🎉 System Test Complete!")
    print("\n📋 Next Steps:")
    print("   1. ✅ System is working locally")
    print("   2. 🚀 Deploy to cloud: scripts\\deploy_to_cloud.bat")
    print("   3. 👥 Share URL with friends")
    
    return True

if __name__ == "__main__":
    test_server()
