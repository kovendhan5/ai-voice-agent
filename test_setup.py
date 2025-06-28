"""
Simple test script to verify the Orpheus TTS API setup
"""

def test_imports():
    """Test all required imports"""
    try:
        import flask
        print("✓ Flask imported successfully")
        
        import numpy
        print("✓ NumPy imported successfully")
        
        import scipy
        print("✓ SciPy imported successfully")
        
        import orpheus_tts
        print("✓ Orpheus TTS mock imported successfully")
        
        # Test model creation
        model = orpheus_tts.OrpheusModel()
        print("✓ OrpheusModel created successfully")
        
        # Test speech generation
        chunks = model.generate_speech("tara: Hello world test!")
        print(f"✓ Speech generation test completed - generated {len(chunks)} chunks")
        
        return True
        
    except Exception as e:
        print(f"✗ Import test failed: {e}")
        return False

def test_flask_app():
    """Test Flask app creation"""
    try:
        from app import app
        print("✓ Flask app imported successfully")
        
        with app.test_client() as client:
            # Test health check
            response = client.get('/')
            print(f"✓ Health check: {response.status_code}")
            
            # Test voices endpoint
            response = client.get('/voices')
            print(f"✓ Voices endpoint: {response.status_code}")
            
        return True
        
    except Exception as e:
        print(f"✗ Flask app test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Orpheus TTS API Setup")
    print("=" * 40)
    
    if test_imports():
        print("\n🧪 Testing Flask App")
        print("=" * 40)
        test_flask_app()
    
    print("\n✅ Setup test completed!")
