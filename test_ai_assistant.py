"""
Test the AI Voice Assistant functionality
"""

import requests
import json
import time

def test_ai_assistant():
    """Test the AI assistant endpoints"""
    base_url = "http://localhost:8080"
    
    print("🤖 Testing AI Voice Assistant")
    print("=" * 50)
    
    try:
        # Test health check
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   Response: {data}")
        
        # Test text chat
        print("\n2. Testing AI chat conversation...")
        test_conversations = [
            "Hello, how are you today?",
            "What can you help me with?",
            "Tell me a joke",
            "What's your name?"
        ]
        
        for i, message in enumerate(test_conversations, 1):
            print(f"\n   Test {i}: '{message}'")
            response = requests.post(
                f"{base_url}/chat",
                json={"message": message, "user_id": "TestUser"},
                headers={"Content-Type": "application/json"},
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                print(f"   AI Response: {data['ai_response']}")
            else:
                print(f"   ❌ Failed: {response.status_code}")
        
        # Test voice chat
        print("\n3. Testing voice chat (audio generation)...")
        response = requests.post(
            f"{base_url}/voice_chat",
            json={"message": "Hello AI, generate some speech for me!", "user_id": "TestUser", "voice": "tara"},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            filename = "ai_test_response.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"   ✅ Voice response saved to: {filename}")
            print(f"   📊 Audio size: {len(response.content)} bytes")
        else:
            print(f"   ❌ Voice chat failed: {response.status_code}")
        
        # Test conversation history
        print("\n4. Testing conversation history...")
        response = requests.get(f"{base_url}/conversation_history", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Total interactions: {data['total_interactions']}")
            print(f"   Recent history entries: {len(data['conversation_history'])}")
        
        # Test stats
        print("\n5. Testing stats endpoint...")
        response = requests.get(f"{base_url}/stats", timeout=5)
        if response.status_code == 200:
            data = response.json()
            print(f"   Stats: {data}")
        
        print("\n🎉 AI Assistant tests completed!")
        print("\nNext steps:")
        print("1. Start the server: python ai_voice_assistant.py")
        print("2. Open the interface: ai_voice_interface.html")
        print("3. Talk to your AI assistant!")
        
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("💡 Start the server first:")
        print("   python ai_voice_assistant.py")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_ai_assistant()
