"""
Simple app launcher for testing
"""
import sys
import os

# Ensure we're in the right directory
os.chdir(r"k:\full stack\AI\voice model\voice-ai-orpheus")
sys.path.insert(0, os.getcwd())

print("🚀 Starting Orpheus TTS API...")
print("=" * 40)
print(f"Working directory: {os.getcwd()}")
print("Server will start on: http://localhost:8080")
print("Press Ctrl+C to stop")
print("=" * 40)

# Import and run the app
from app import app

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
