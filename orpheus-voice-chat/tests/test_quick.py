"""
Quick test script for Orpheus Voice Chat
Tests the main functionality to ensure everything is working
"""

import requests
import time
import os
import sys

# Add the src directory to the path to import the app
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

def test_server_status():
    """Test if the server is running and responding"""
    try:
        response = requests.get('http://localhost:8080/status', timeout=5)
        if response.status_code == 200:
            print("✅ Server is running and responsive")
            return True
        else:
            print(f"❌ Server responded with status code: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Server connection failed: {e}")
        return False

def test_voices_endpoint():
    """Test the voices endpoint"""
    try:
        response = requests.get('http://localhost:8080/voices', timeout=5)
        if response.status_code == 200:
            voices = response.json()
            print(f"✅ Voices endpoint working. Available voices: {len(voices.get('voices', []))}")
            return True
        else:
            print(f"❌ Voices endpoint failed with status: {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Voices endpoint connection failed: {e}")
        return False

def test_synthesis():
    """Test speech synthesis"""
    try:
        data = {
            "text": "Hello! This is a test of the Orpheus voice synthesis.",
            "voice": "tara"
        }
        response = requests.post('http://localhost:8080/synthesize', json=data, timeout=10)
        if response.status_code == 200:
            print("✅ Speech synthesis working")
            return True
        else:
            print(f"❌ Synthesis failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Synthesis connection failed: {e}")
        return False

def test_chat():
    """Test chat endpoint"""
    try:
        data = {
            "message": "Hello, how are you?",
            "voice": "tara"
        }
        response = requests.post('http://localhost:8080/chat', json=data, timeout=15)
        if response.status_code == 200:
            print("✅ Chat endpoint working")
            return True
        else:
            print(f"❌ Chat failed with status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Chat connection failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Starting Orpheus Voice Chat Tests")
    print("=" * 50)
    
    tests = [
        ("Server Status", test_server_status),
        ("Voices Endpoint", test_voices_endpoint),
        ("Speech Synthesis", test_synthesis),
        ("Chat Endpoint", test_chat)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n🔬 Testing {test_name}...")
        if test_func():
            passed += 1
        time.sleep(1)  # Brief pause between tests
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your Orpheus Voice Chat is working perfectly!")
    else:
        print("⚠️ Some tests failed. Check the output above for details.")
        
    print("\n💡 To start the server, run: scripts\\start.bat")
    print("🌐 Then open: http://localhost:8080")

if __name__ == "__main__":
    main()
