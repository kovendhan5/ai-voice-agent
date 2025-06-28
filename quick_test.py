"""
Quick server test
"""
import sys
import traceback

try:
    print("🚀 Starting Orpheus TTS API Server Test...")
    from app import app
    print("✅ App imported successfully")
    
    print("🔧 Testing server startup...")
    # Test if we can get a test client
    with app.test_client() as client:
        print("✅ Test client created")
        
        # Quick health check
        response = client.get('/')
        print(f"✅ Health check: {response.status_code}")
        print(f"   Response: {response.get_json()}")
        
    print("🎉 Server test completed successfully!")
    print("\nTo start the server manually, run:")
    print("python -c \"from app import app; app.run(host='0.0.0.0', port=8080, debug=True)\"")
    
except Exception as e:
    print(f"❌ Server test failed: {e}")
    print("\nFull error traceback:")
    traceback.print_exc()
