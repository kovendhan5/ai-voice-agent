"""
Quick test of the fixed Orpheus TTS synthesis
"""
import requests
import json

def test_synthesis():
    """Test the synthesis endpoint with fixed parameters"""
    
    print("🎭 Testing Fixed Orpheus TTS Synthesis")
    print("="*50)
    
    # Test data
    test_data = {
        "text": "Hello! This is a test of the fixed Orpheus TTS system. <chuckle> Let's see if it works now!",
        "voice": "tara",
        "add_emotions": True
    }
    
    try:
        print("🔄 Sending synthesis request...")
        response = requests.post(
            'http://localhost:8080/synthesize', 
            json=test_data,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("✅ SUCCESS! Synthesis working!")
            print(f"📦 Response headers: {dict(response.headers)}")
            print(f"📏 Audio data size: {len(response.content)} bytes")
            
            # Save test audio
            with open('test_synthesis_output.wav', 'wb') as f:
                f.write(response.content)
            print("💾 Saved audio to test_synthesis_output.wav")
            
        else:
            print(f"❌ ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error text: {response.text}")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")

def test_chat():
    """Test the chat endpoint"""
    
    print("\n🤖 Testing Chat Endpoint")
    print("="*50)
    
    chat_data = {
        "message": "Hello! How are you doing today?",
        "voice": "jess"
    }
    
    try:
        print("🔄 Sending chat request...")
        response = requests.post(
            'http://localhost:8080/chat',
            json=chat_data,
            timeout=30
        )
        
        print(f"📊 Status Code: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("✅ SUCCESS! Chat working!")
            print(f"🤖 AI Response: {data.get('response', 'N/A')}")
            print(f"🎭 Voice: {data.get('voice', 'N/A')}")
            print(f"🎨 Personality: {data.get('personality', 'N/A')}")
            print(f"🔧 Generation Method: {data.get('generation_method', 'N/A')}")
        else:
            print(f"❌ ERROR: {response.status_code}")
            try:
                error_data = response.json()
                print(f"Error details: {error_data}")
            except:
                print(f"Error text: {response.text}")
                
    except Exception as e:
        print(f"❌ Connection error: {e}")

if __name__ == "__main__":
    test_synthesis()
    test_chat()
    print("\n🎯 Quick Test Complete!")
