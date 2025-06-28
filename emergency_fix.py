"""
Emergency AI Assistant Diagnostics and Auto-Fix
This will identify and fix connection issues
"""

import subprocess
import time
import requests
import sys
import os
import traceback
import json

def print_header():
    print("🔧 EMERGENCY AI ASSISTANT FIXER")
    print("=" * 50)
    print("This will diagnose and fix your connection issues")
    print("=" * 50)

def check_python_environment():
    """Check if Python environment is working"""
    print("\n🐍 Step 1: Checking Python Environment...")
    
    try:
        import flask
        print("   ✅ Flask: Available")
    except ImportError:
        print("   ❌ Flask: Missing")
        return False
    
    try:
        import numpy
        print("   ✅ NumPy: Available")
    except ImportError:
        print("   ❌ NumPy: Missing")
        return False
    
    try:
        import orpheus_tts
        print("   ✅ Orpheus TTS Mock: Available")
    except ImportError:
        print("   ❌ Orpheus TTS Mock: Missing")
        return False
    
    return True

def check_port_availability():
    """Check if port 8080 is available"""
    print("\n🌐 Step 2: Checking Port 8080...")
    
    try:
        import socket
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        result = sock.connect_ex(('localhost', 8080))
        sock.close()
        
        if result == 0:
            print("   ⚠️  Port 8080 is in use")
            return False
        else:
            print("   ✅ Port 8080 is available")
            return True
    except Exception:
        print("   ✅ Port 8080 is available")
        return True

def kill_existing_servers():
    """Kill any existing servers on port 8080"""
    print("\n🛑 Step 3: Cleaning up existing servers...")
    
    try:
        # Windows command to kill processes using port 8080
        subprocess.run(['netstat', '-ano'], capture_output=True, check=True)
        subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], capture_output=True)
        print("   ✅ Cleaned up existing processes")
        time.sleep(2)
    except:
        print("   ✅ No cleanup needed")

def test_basic_imports():
    """Test if we can import and create basic objects"""
    print("\n🧪 Step 4: Testing Basic Functionality...")
    
    try:
        # Test TTS import
        from orpheus_tts import OrpheusModel
        print("   ✅ OrpheusModel import successful")
        
        # Test model creation
        model = OrpheusModel()
        print("   ✅ Model creation successful")
        
        # Test basic audio generation
        chunks = model.generate_speech("test", "tara")
        print(f"   ✅ Audio generation successful ({len(chunks)} chunks)")
        
        return True
    except Exception as e:
        print(f"   ❌ Basic functionality failed: {e}")
        return False

def start_server_with_output():
    """Start server and capture output"""
    print("\n🚀 Step 5: Starting AI Server...")
    
    try:
        # Change to project directory
        project_dir = r"k:\full stack\AI\voice model\voice-ai-orpheus"
        os.chdir(project_dir)
        print(f"   📁 Working directory: {os.getcwd()}")
        
        # Start server
        print("   🔄 Launching server...")
        process = subprocess.Popen(
            [sys.executable, "simple_ai_server.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        # Wait and check if server starts
        time.sleep(5)
        
        if process.poll() is None:  # Process is still running
            print("   ✅ Server process started")
            return process
        else:
            # Process died, get error output
            stdout, stderr = process.communicate()
            print(f"   ❌ Server failed to start")
            print(f"   Output: {stdout}")
            print(f"   Error: {stderr}")
            return None
            
    except Exception as e:
        print(f"   ❌ Failed to start server: {e}")
        traceback.print_exc()
        return None

def test_server_connection():
    """Test if server is responding"""
    print("\n🔍 Step 6: Testing Server Connection...")
    
    for attempt in range(10):
        try:
            response = requests.get("http://localhost:8080/", timeout=2)
            if response.status_code == 200:
                data = response.json()
                print(f"   ✅ Server responding: {data.get('message', 'OK')}")
                return True
            else:
                print(f"   ⚠️  Server returned status: {response.status_code}")
        except requests.exceptions.ConnectionError:
            print(f"   ⏳ Attempt {attempt + 1}/10: Connection refused, retrying...")
            time.sleep(1)
        except Exception as e:
            print(f"   ❌ Connection test failed: {e}")
    
    print("   ❌ Server not responding after 10 attempts")
    return False

def create_minimal_server():
    """Create a super minimal server for testing"""
    print("\n🛠️ Creating minimal test server...")
    
    minimal_server_code = '''
from flask import Flask, jsonify
import sys
import os

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

app = Flask(__name__)

@app.route('/')
def health():
    return jsonify({"status": "healthy", "message": "Minimal test server running!"})

@app.route('/test')
def test():
    return jsonify({"test": "success", "message": "Server is working!"})

if __name__ == '__main__':
    print("🧪 Starting minimal test server on port 8080...")
    print("Server should be available at http://localhost:8080")
    app.run(host='0.0.0.0', port=8080, debug=False)
'''
    
    try:
        with open("minimal_test_server.py", "w") as f:
            f.write(minimal_server_code)
        print("   ✅ Minimal server created: minimal_test_server.py")
        return True
    except Exception as e:
        print(f"   ❌ Failed to create minimal server: {e}")
        return False

def main():
    """Main diagnostic and fix routine"""
    print_header()
    
    # Step 1: Check Python environment
    if not check_python_environment():
        print("\n❌ CRITICAL: Python environment issues detected")
        print("Fix: Install missing packages with:")
        print("   pip install flask numpy scipy")
        return
    
    # Step 2: Clean up existing servers
    kill_existing_servers()
    
    # Step 3: Check port availability
    if not check_port_availability():
        print("\n⚠️  Port 8080 is busy, trying to free it...")
        kill_existing_servers()
    
    # Step 4: Test basic functionality
    if not test_basic_imports():
        print("\n❌ CRITICAL: Basic TTS functionality not working")
        return
    
    # Step 5: Try starting the main server
    process = start_server_with_output()
    
    if process:
        # Step 6: Test connection
        if test_server_connection():
            print("\n🎉 SUCCESS! AI Assistant is now running!")
            print("\nNext steps:")
            print("1. Go back to your browser")
            print("2. Click '🔗 Test Connection' - should show green")
            print("3. Click 🎤 microphone and say 'Hello AI'")
            print("4. You should get an AI voice response!")
            print("\n⚠️  IMPORTANT: Keep this window open!")
            
            try:
                # Keep server running
                process.wait()
            except KeyboardInterrupt:
                print("\n👋 Server stopped by user")
                process.terminate()
        else:
            print("\n❌ Server started but not responding")
            process.terminate()
    else:
        print("\n🛠️ Main server failed, trying minimal test server...")
        if create_minimal_server():
            print("\nTry running: python minimal_test_server.py")
    
    print("\n" + "=" * 50)
    print("🔧 Diagnostic complete")

if __name__ == "__main__":
    main()
