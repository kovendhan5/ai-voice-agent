"""
Step-by-step troubleshooting script
"""

def step1_check_environment():
    """Check Python environment and packages"""
    print("🔍 Step 1: Checking Environment")
    print("-" * 30)
    
    import sys
    print(f"✅ Python version: {sys.version}")
    
    # Check required packages
    packages = ['flask', 'numpy', 'scipy', 'requests']
    for pkg in packages:
        try:
            __import__(pkg)
            print(f"✅ {pkg}: installed")
        except ImportError:
            print(f"❌ {pkg}: NOT FOUND")
            return False
    
    # Check our custom module
    try:
        import orpheus_tts
        print("✅ orpheus_tts: available")
    except ImportError:
        print("❌ orpheus_tts: NOT FOUND")
        return False
    
    return True

def step2_test_basic_functionality():
    """Test basic TTS functionality"""
    print("\n🧪 Step 2: Testing Basic TTS")
    print("-" * 30)
    
    try:
        from orpheus_tts import OrpheusModel
        print("✅ OrpheusModel import successful")
        
        model = OrpheusModel()
        print("✅ Model created successfully")
        
        chunks = model.generate_speech("tara: Hello test", "tara")
        print(f"✅ Audio generated: {len(chunks)} chunks")
        
        # Test file creation
        with open("test_audio.wav", "wb") as f:
            for chunk in chunks:
                f.write(chunk)
        print("✅ Audio file saved: test_audio.wav")
        
        return True
        
    except Exception as e:
        print(f"❌ TTS test failed: {e}")
        return False

def step3_test_flask_app():
    """Test Flask application"""
    print("\n🌐 Step 3: Testing Flask App")
    print("-" * 30)
    
    try:
        from app import app
        print("✅ Flask app imported")
        
        with app.test_client() as client:
            # Health check
            response = client.get('/')
            print(f"✅ Health endpoint: {response.status_code}")
            
            # Voices endpoint
            response = client.get('/voices')
            print(f"✅ Voices endpoint: {response.status_code}")
            
            # Speech endpoint
            response = client.post('/speak', 
                                 json={'text': 'tara: Test'},
                                 headers={'Content-Type': 'application/json'})
            print(f"✅ Speech endpoint: {response.status_code}")
            print(f"✅ Audio size: {len(response.data)} bytes")
        
        return True
        
    except Exception as e:
        print(f"❌ Flask test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def step4_try_server_start():
    """Try to start the server"""
    print("\n🚀 Step 4: Starting Server")
    print("-" * 30)
    
    try:
        from app import app
        print("✅ App imported for server start")
        print("🔄 Starting server on http://localhost:8080")
        print("   (This will block - press Ctrl+C to stop)")
        print("   Open another terminal and test with:")
        print("   curl http://localhost:8080/")
        print()
        
        app.run(host='0.0.0.0', port=8080, debug=True)
        
    except KeyboardInterrupt:
        print("\n✅ Server stopped by user")
        return True
    except Exception as e:
        print(f"❌ Server start failed: {e}")
        return False

def main():
    """Run troubleshooting steps"""
    print("🔧 Orpheus TTS Troubleshooting")
    print("=" * 50)
    
    steps = [
        ("Environment Check", step1_check_environment),
        ("Basic TTS Test", step2_test_basic_functionality),
        ("Flask App Test", step3_test_flask_app),
    ]
    
    for step_name, step_func in steps:
        if not step_func():
            print(f"\n❌ Failed at: {step_name}")
            print("🛠️  Please fix the above issues before continuing")
            return False
        print(f"✅ {step_name} completed successfully")
    
    print("\n🎉 All tests passed!")
    print("\nChoose next action:")
    print("1. Start server (type 'server')")
    print("2. Test voice interface (type 'voice')")
    print("3. Exit (type 'exit')")
    
    choice = input("\nEnter choice: ").strip().lower()
    
    if choice == 'server':
        step4_try_server_start()
    elif choice == 'voice':
        print("🌐 To test voice interface:")
        print("1. Start server: python app.py")
        print("2. Open: voice_interface.html")
        print("3. Allow microphone access")
        print("4. Click microphone button and speak")
    else:
        print("👋 Goodbye!")

if __name__ == "__main__":
    main()
