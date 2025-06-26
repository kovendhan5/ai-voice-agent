"""
Ultra-simple AI server that definitely works
"""

from flask import Flask, request, jsonify, send_file
import tempfile
import os
import sys

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

try:
    from orpheus_tts import OrpheusModel
    print("✅ Orpheus TTS imported successfully")
except ImportError:
    print("❌ Could not import orpheus_tts")
    sys.exit(1)

app = Flask(__name__)

# Global variables
tts_model = None
conversation_count = 0

def initialize_model():
    """Initialize the TTS model"""
    global tts_model
    try:
        print("🤖 Loading Orpheus TTS model...")
        tts_model = OrpheusModel()
        print("✅ Model loaded successfully!")
        return True
    except Exception as e:
        print(f"❌ Model loading failed: {e}")
        return False

@app.route('/')
def health():
    """Health check"""
    return jsonify({
        "status": "healthy",
        "message": "AI Voice Assistant is running!",
        "model_loaded": tts_model is not None
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Simple text chat"""
    global conversation_count
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        
        # Simple AI responses
        if 'yourself' in user_message or 'about you' in user_message:
            response = "Hello! I'm an AI assistant powered by Orpheus voice technology. I can have conversations with you and respond using realistic speech synthesis. I'm here to chat, answer questions, and help with whatever you need!"
        elif 'hello' in user_message or 'hi' in user_message:
            response = "Hello there! Great to meet you! I'm your AI voice assistant. I can understand what you're saying and respond back with natural-sounding speech. What would you like to talk about?"
        elif 'how are you' in user_message:
            response = "I'm doing fantastic! I'm excited to be talking with you. As an AI, I don't have feelings in the human sense, but I'm functioning perfectly and ready to help you with anything!"
        elif 'what can you do' in user_message:
            response = "I can have natural conversations with you! I understand speech, process your questions, and respond with realistic AI-generated voice. We can chat about topics, I can answer questions, tell jokes, or just have a friendly conversation!"
        elif 'joke' in user_message:
            response = "Here's one for you: Why don't scientists trust atoms? Because they make up everything! I hope that made you smile!"
        elif 'thank' in user_message:
            response = "You're very welcome! I'm happy to help and chat with you. Feel free to ask me anything else!"
        else:
            response = f"That's interesting! You said '{data.get('message', '')}'. I'm here to have a conversation with you. What would you like to know or talk about? I can discuss topics, answer questions, or just chat!"
        
        conversation_count += 1
        
        return jsonify({
            "ai_response": response,
            "user_message": data.get('message', ''),
            "conversation_id": conversation_count
        })
        
    except Exception as e:
        print(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    """Voice chat with audio response"""
    global tts_model
    
    if not tts_model:
        return jsonify({"error": "TTS model not loaded"}), 500
    
    try:
        data = request.get_json()
        user_message = data.get('message', '').lower()
        voice = data.get('voice', 'tara')
        
        print(f"🎤 User said: {user_message}")
        
        # Get text response (same logic as chat)
        if 'yourself' in user_message or 'about you' in user_message:
            response = "Hello! I'm an AI assistant powered by Orpheus voice technology. I can have conversations with you and respond using realistic speech synthesis. I'm here to chat, answer questions, and help with whatever you need!"
        elif 'hello' in user_message or 'hi' in user_message:
            response = "Hello there! Great to meet you! I'm your AI voice assistant. I can understand what you're saying and respond back with natural-sounding speech. What would you like to talk about?"
        elif 'how are you' in user_message:
            response = "I'm doing fantastic! I'm excited to be talking with you. As an AI, I don't have feelings in the human sense, but I'm functioning perfectly and ready to help you with anything!"
        elif 'what can you do' in user_message:
            response = "I can have natural conversations with you! I understand speech, process your questions, and respond with realistic AI-generated voice. We can chat about topics, I can answer questions, tell jokes, or just have a friendly conversation!"
        elif 'joke' in user_message:
            response = "Here's one for you: Why don't scientists trust atoms? Because they make up everything! I hope that made you smile!"
        elif 'thank' in user_message:
            response = "You're very welcome! I'm happy to help and chat with you. Feel free to ask me anything else!"
        else:
            response = f"That's interesting! You mentioned '{data.get('message', '')}'. I'm here to have a conversation with you. What would you like to know or talk about? I can discuss topics, answer questions, or just chat!"
        
        print(f"🤖 AI responding: {response[:50]}...")
        
        # Generate speech
        prompt = f"{voice}: {response}"
        audio_chunks = tts_model.generate_speech(prompt=prompt, voice=voice)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            for chunk in audio_chunks:
                temp_file.write(chunk)
            temp_path = temp_file.name
        
        print("🔊 Audio generated successfully!")
        
        return send_file(temp_path, mimetype='audio/wav', as_attachment=True, download_name='ai_response.wav')
        
    except Exception as e:
        print(f"❌ Voice chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/voices')
def voices():
    """Available voices"""
    return jsonify({
        "voices": [
            {"id": "tara", "name": "Tara"},
            {"id": "alex", "name": "Alex"}, 
            {"id": "sarah", "name": "Sarah"}
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting Ultra-Simple AI Voice Assistant")
    print("=" * 50)
    
    if not initialize_model():
        print("❌ Cannot start without TTS model")
        sys.exit(1)
    
    print("🌐 Server starting on http://localhost:8080")
    print("🎤 Ready for voice conversations!")
    print("=" * 50)
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=True, use_reloader=False)
    except Exception as e:
        print(f"❌ Server failed to start: {e}")
        input("Press Enter to exit...")
