"""
Quick fix for AI assistant connection issues
"""

import subprocess
import time
import requests
import sys
import os

def check_server_running():
    """Check if server is running on port 8080"""
    try:
        response = requests.get("http://localhost:8080/", timeout=2)
        return response.status_code == 200
    except:
        return False

def start_server():
    """Start the AI assistant server"""
    print("🚀 Starting AI Voice Assistant server...")
    
    # Change to the correct directory
    os.chdir(r"k:\full stack\AI\voice model\voice-ai-orpheus")
    
    # Start the server
    try:
        # Use subprocess to start server in background
        process = subprocess.Popen([
            sys.executable, "ai_voice_assistant.py"
        ], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        print("⏳ Waiting for server to start...")
        time.sleep(5)
        
        if check_server_running():
            print("✅ Server started successfully!")
            print("🌐 Server is running on http://localhost:8080")
            return True
        else:
            print("❌ Server failed to start properly")
            return False
            
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False

def main():
    print("🔧 AI Assistant Connection Fixer")
    print("=" * 40)
    
    # Check if server is already running
    if check_server_running():
        print("✅ Server is already running!")
        print("🎤 Go back to your browser and try the microphone again")
        return
    
    print("🔍 Server not running, starting it now...")
    
    if start_server():
        print("\n🎉 SUCCESS! Your AI assistant is now ready!")
        print("\nNext steps:")
        print("1. Go back to your browser")
        print("2. Click '🔗 Test Connection' - should show green")
        print("3. Click the 🎤 microphone button")
        print("4. Start talking to your AI!")
        print("\nKeep this window open to keep the server running.")
        
        # Keep the script running
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n👋 Server stopped")
    else:
        print("\n❌ Could not start server automatically")
        print("\n🛠️ Manual fix:")
        print("1. Open Command Prompt")
        print('2. Run: cd "k:\\full stack\\AI\\voice model\\voice-ai-orpheus"')
        print("3. Run: python ai_voice_assistant.py")

if __name__ == "__main__":
    main()
