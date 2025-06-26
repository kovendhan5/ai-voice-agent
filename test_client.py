"""
Simple API test client for the Orpheus TTS API
"""

import requests
import json
import sys
import time

def test_api():
    """Test the API endpoints"""
    base_url = "http://localhost:8080"
    
    print("🧪 Testing Orpheus TTS API")
    print("=" * 40)
    
    # Wait a moment for server to be ready
    print("⏳ Waiting for server to be ready...")
    time.sleep(2)
    
    try:
        # Test health check
        print("📡 Testing health check endpoint...")
        response = requests.get(f"{base_url}/", timeout=10)
        if response.status_code == 200:
            print("✓ Health check passed")
            print(f"  Response: {response.json()}")
        else:
            print(f"✗ Health check failed: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"✗ Cannot connect to server: {e}")
        print("  Make sure the server is running with: python app.py")
        return False
    
    try:
        # Test voices endpoint
        print("\n📢 Testing voices endpoint...")
        response = requests.get(f"{base_url}/voices", timeout=10)
        if response.status_code == 200:
            print("✓ Voices endpoint passed")
            print(f"  Available voices: {response.json()}")
        else:
            print(f"✗ Voices endpoint failed: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Voices endpoint error: {e}")
    
    try:
        # Test speech generation
        print("\n🎤 Testing speech generation...")
        data = {"text": "tara: Hello from Orpheus TTS! This is a test."}
        response = requests.post(
            f"{base_url}/speak", 
            json=data, 
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            # Save the audio file
            filename = "test_speech.wav"
            with open(filename, "wb") as f:
                f.write(response.content)
            print("✓ Speech generation passed")
            print(f"  Audio saved to: {filename}")
            print(f"  File size: {len(response.content)} bytes")
        else:
            print(f"✗ Speech generation failed: {response.status_code}")
            print(f"  Response: {response.text}")
    except requests.exceptions.RequestException as e:
        print(f"✗ Speech generation error: {e}")
    
    print("\n✅ API tests completed!")
    return True

if __name__ == "__main__":
    test_api()
