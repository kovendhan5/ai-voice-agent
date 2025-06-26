"""
Production Orpheus Voice Chat for Google Cloud Run
EXACT copy of the app running on http://127.0.0.1:5000/
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

# Import the exact same app that runs locally
from app_live_orpheus import app, live_chat

# Expose the app for gunicorn
application = app

if __name__ == '__main__':
    print("\n🎙️ LIVE ORPHEUS VOICE CHAT - CLOUD DEPLOYMENT")
    print("=" * 60)
    print("🎯 EXACT COPY OF LOCAL http://127.0.0.1:5000/ SERVER")
    print("  ✅ Real-time voice conversation")
    print("  ✅ Speech-to-text input")
    print("  ✅ Enhanced personality responses") 
    print("  ✅ Live conversation flow")
    print("  ✅ Interactive voice controls")
    print("  ✅ Natural dialogue patterns")
    print("  ✅ Continuous chat mode")
    print("  ✅ 8 unique AI personalities")
    print("=" * 60)
    
    # Cloud Run uses PORT environment variable
    port = int(os.environ.get('PORT', 5000))
    print(f"\n🌐 Starting on port {port}")
    print("🎤 Experience truly interactive Orpheus conversations!")
    
    # Run with the same settings as local
    app.run(
        debug=False,
        host='0.0.0.0',
        port=port,
        threaded=True
    )
    print("🚀 ORPHEUS VOICE CHAT - CLOUD DEPLOYMENT")
    print("=" * 50)
    print("✅ Live Interactive Voice Chat")
    print("✅ 8 AI Personalities")
    print("✅ Real-time Speech Processing")
    print("✅ Multi-user Support")
    print("=" * 50)
    
    # Cloud Run uses PORT environment variable
    port = int(os.environ.get('PORT', 8080))
    print(f"🌐 Starting on port {port}")
    
    app.run(
        debug=False,
        host='0.0.0.0',
        port=port,
        threaded=True
    )
