"""
Simple diagnostic script to identify what's not working
"""

import sys
import os

def test_step(step_name, test_func):
    """Run a test step and report results"""
    try:
        print(f"🧪 Testing: {step_name}")
        result = test_func()
        print(f"✅ {step_name}: SUCCESS")
        return True
    except Exception as e:
        print(f"❌ {step_name}: FAILED - {e}")
        return False

def test_imports():
    """Test all required imports"""
    import flask
    import orpheus_tts
    import numpy
    import scipy
    import requests
    return True

def test_orpheus_model():
    """Test OrpheusModel creation"""
    from orpheus_tts import OrpheusModel
    model = OrpheusModel()
    return True

def test_flask_app_creation():
    """Test Flask app creation"""
    from app import app
    return app is not None

def test_audio_generation():
    """Test audio generation"""
    from orpheus_tts import OrpheusModel
    model = OrpheusModel()
    chunks = model.generate_speech("tara: Test", "tara")
    return len(chunks) > 0

def test_flask_endpoints():
    """Test Flask app endpoints"""
    from app import app
    with app.test_client() as client:
        # Test health endpoint
        response = client.get('/')
        if response.status_code != 200:
            raise Exception(f"Health check failed: {response.status_code}")
        
        # Test voices endpoint
        response = client.get('/voices')
        if response.status_code != 200:
            raise Exception(f"Voices endpoint failed: {response.status_code}")
        
        return True

def test_speech_endpoint():
    """Test the main speech endpoint"""
    from app import app
    with app.test_client() as client:
        response = client.post('/speak', 
                             json={'text': 'tara: Test speech'},
                             headers={'Content-Type': 'application/json'})
        if response.status_code != 200:
            raise Exception(f"Speech endpoint failed: {response.status_code}")
        if len(response.data) < 1000:  # Audio should be substantial
            raise Exception("Generated audio too small")
        return True

def main():
    """Run all diagnostic tests"""
    print("🔍 Orpheus TTS Diagnostic Tool")
    print("=" * 50)
    
    tests = [
        ("Python Imports", test_imports),
        ("Orpheus Model Creation", test_orpheus_model),
        ("Flask App Creation", test_flask_app_creation),
        ("Audio Generation", test_audio_generation),
        ("Flask Endpoints", test_flask_endpoints),
        ("Speech Endpoint", test_speech_endpoint),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        if test_step(test_name, test_func):
            passed += 1
        print()
    
    print("=" * 50)
    print(f"📊 Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! The system should be working.")
        print("\nNext steps:")
        print("1. Start server: python app.py")
        print("2. Open voice interface: start_voice_interface.bat")
    else:
        print("❌ Some tests failed. Check the errors above.")
        print("\nTroubleshooting:")
        print("- Check if all dependencies are installed")
        print("- Verify Python environment is activated")
        print("- Make sure no other process is using port 8080")
    
    return passed == total

if __name__ == "__main__":
    main()
