"""
Simple API test without browser dependencies
"""

import requests
import json

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Orpheus TTS API")
    print("=" * 40)
    
    try:
        # Test health check
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/", timeout=5)
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test speech generation
        print("\n2. Testing speech generation...")
        data = {"text": "tara: Hello from the API test!", "voice": "tara"}
        response = requests.post(
            f"{base_url}/speak", 
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            filename = "api_test_output.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            print(f"   ✅ Success! Audio saved to: {filename}")
            print(f"   📊 File size: {len(response.content)} bytes")
        else:
            print(f"   ❌ Failed: {response.status_code}")
            print(f"   Response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("💡 Make sure the server is running:")
        print("   python simple_server.py")
    except Exception as e:
        print(f"❌ Test failed: {e}")

if __name__ == "__main__":
    test_api()
