"""
Enhanced Orpheus TTS API with Real-time Conversation
Combines simple TTS demo with intelligent AI chat capabilities
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
import tempfile
import wave
import numpy as np
from datetime import datetime
import requests
import json

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'canopylabs/orpheus-tts-0.1-finetune-prod')
PORT = int(os.getenv('PORT', 8080))

# Available voices
VOICES = {
    "tara": {"id": "tara", "name": "Tara", "gender": "female"},
    "alex": {"id": "alex", "name": "Alex", "gender": "male"},
    "sarah": {"id": "sarah", "name": "Sarah", "gender": "female"}
}

# Conversation memory for each user
conversations = {}

def generate_orpheus_tts(text, voice="tara"):
    """
    Generate speech using Orpheus TTS model
    For demo purposes, this creates a synthetic audio file
    """
    # Remove voice prefix if present (e.g., "tara: Hello" -> "Hello")
    if ":" in text:
        voice_prefix, clean_text = text.split(":", 1)
        voice = voice_prefix.strip().lower()
        text = clean_text.strip()
    
    # Create synthetic audio based on text characteristics
    sample_rate = 22050
    duration = len(text) * 0.08  # Roughly 80ms per character
    duration = max(1.0, min(duration, 10.0))  # Between 1-10 seconds
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Base frequency varies by voice
    voice_frequencies = {
        "tara": 220,   # Lower female voice
        "sarah": 250,  # Higher female voice  
        "alex": 150    # Male voice
    }
    
    base_freq = voice_frequencies.get(voice, 220)
    
    # Create speech-like waveform with multiple harmonics
    audio_data = np.zeros_like(t)
    
    # Add fundamental frequency and harmonics
    for i, harmonic in enumerate([1.0, 0.5, 0.3, 0.2, 0.1]):
        freq = base_freq * (i + 1)
        audio_data += harmonic * np.sin(2 * np.pi * freq * t)
    
    # Add speech-like modulation
    modulation = 1 + 0.3 * np.sin(2 * np.pi * 4 * t)  # 4Hz modulation
    audio_data *= modulation
    
    # Add some speech-like variation based on text
    for i, char in enumerate(text.lower()):
        if char in 'aeiou':  # Vowels create formants
            formant_freq = base_freq * (2 + ord(char) % 3)
            formant_pos = int((i / len(text)) * len(t))
            formant_width = int(0.1 * sample_rate)
            start = max(0, formant_pos - formant_width // 2)
            end = min(len(t), formant_pos + formant_width // 2)
            audio_data[start:end] += 0.2 * np.sin(2 * np.pi * formant_freq * t[start:end])
    
    # Normalize and apply envelope
    audio_data = audio_data / np.max(np.abs(audio_data)) * 0.7
    
    # Apply fade in/out
    fade_samples = int(sample_rate * 0.05)  # 50ms fade
    if len(audio_data) > 2 * fade_samples:
        audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
        audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    # Convert to 16-bit PCM
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Save to temporary WAV file
    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
    with wave.open(temp_file.name, 'wb') as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(sample_rate)
        wav_file.writeframes(audio_data.tobytes())
    
    return temp_file.name

def get_ai_response(user_message, user_id="default"):
    """
    Generate intelligent AI response for conversation
    """
    # Initialize conversation history for new users
    if user_id not in conversations:
        conversations[user_id] = []
    
    # Add user message to history
    conversations[user_id].append({"role": "user", "content": user_message})
    
    # Simple AI response logic (you can replace with OpenAI API, Ollama, etc.)
    responses = {
        "hello": "Hello! I'm your AI voice assistant. How can I help you today?",
        "hi": "Hi there! What would you like to talk about?",
        "how are you": "I'm doing great! I'm an AI assistant ready to help with any questions or have a conversation.",
        "what's your name": "I'm your AI voice assistant powered by Orpheus TTS. You can call me whatever you'd like!",
        "weather": "I don't have access to real-time weather data, but I'd be happy to chat about weather in general!",
        "time": f"The current time is {datetime.now().strftime('%I:%M %p')}",
        "date": f"Today is {datetime.now().strftime('%A, %B %d, %Y')}",
        "joke": "Why don't scientists trust atoms? Because they make up everything!",
        "help": "I can help with conversations, answer questions, tell jokes, or just chat! What would you like to do?",
        "bye": "Goodbye! It was nice talking with you. Feel free to come back anytime!",
        "goodbye": "See you later! Thanks for the chat!"
    }
    
    # Check for simple keyword matches
    user_lower = user_message.lower().strip()
    for keyword, response in responses.items():
        if keyword in user_lower:
            ai_response = response
            break
    else:
        # Default intelligent responses based on message content
        if "?" in user_message:
            ai_response = f"That's an interesting question about '{user_message}'. I'd love to explore that topic with you!"
        elif len(user_message.split()) > 10:
            ai_response = "I appreciate you sharing that detailed message with me. What aspect would you like to discuss further?"
        elif any(word in user_lower for word in ["love", "like", "enjoy"]):
            ai_response = "That sounds wonderful! I'd love to hear more about what you enjoy."
        elif any(word in user_lower for word in ["problem", "issue", "help", "trouble"]):
            ai_response = "I'm here to help! Can you tell me more about what you're dealing with?"
        else:
            ai_response = f"Interesting! You mentioned '{user_message}'. Can you tell me more about that?"
    
    # Add AI response to history
    conversations[user_id].append({"role": "assistant", "content": ai_response})
    
    # Keep conversation history reasonable (last 20 messages)
    if len(conversations[user_id]) > 20:
        conversations[user_id] = conversations[user_id][-20:]
    
    return ai_response

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Enhanced Orpheus TTS API with AI Chat",
        "model": MODEL_NAME,
        "timestamp": datetime.now().isoformat(),
        "version": "1.0.0",
        "features": ["tts", "conversation", "multi-voice"]
    })

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available voices"""
    return jsonify({
        "voices": list(VOICES.values())
    })

@app.route('/speak', methods=['POST'])
def generate_speech():
    """Generate speech from text input (original demo endpoint)"""
    try:
        # Parse request
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        text = data.get('text', '').strip()
        voice = data.get('voice', 'tara').lower()
        
        # Validate input
        if not text:
            return jsonify({"error": "Text field is required"}), 400
        
        if len(text) > 1000:
            return jsonify({"error": "Text too long (max 1000 characters)"}), 400
        
        if voice not in VOICES:
            return jsonify({"error": f"Unknown voice '{voice}'. Available: {list(VOICES.keys())}"}), 400
        
        # Generate speech
        audio_file = generate_orpheus_tts(text, voice)
        
        # Return audio file
        return send_file(
            audio_file, 
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'speech_{voice}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        )
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/chat', methods=['POST'])
def chat_text():
    """Text-only chat endpoint for real-time conversation"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        user_id = data.get('user_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message field is required"}), 400
        
        # Get AI response
        ai_response = get_ai_response(user_message, user_id)
        
        return jsonify({
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        })
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    """Voice chat endpoint - combines conversation + TTS"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No JSON data provided"}), 400
        
        user_message = data.get('message', '').strip()
        voice = data.get('voice', 'tara').lower()
        user_id = data.get('user_id', 'default')
        
        if not user_message:
            return jsonify({"error": "Message field is required"}), 400
        
        if voice not in VOICES:
            return jsonify({"error": f"Unknown voice '{voice}'. Available: {list(VOICES.keys())}"}), 400
        
        # Get AI response
        ai_response = get_ai_response(user_message, user_id)
        
        # Generate speech for AI response
        audio_file = generate_orpheus_tts(ai_response, voice)
        
        # Return audio file with metadata
        response_headers = {
            'X-User-Message': user_message,
            'X-AI-Response': ai_response,
            'X-Voice': voice,
            'X-User-ID': user_id,
            'X-Timestamp': datetime.now().isoformat()
        }
        
        return send_file(
            audio_file,
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'chat_{voice}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        ), 200, response_headers
        
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conversation/<user_id>', methods=['GET'])
def get_conversation_history(user_id):
    """Get conversation history for a user"""
    try:
        history = conversations.get(user_id, [])
        return jsonify({
            "user_id": user_id,
            "conversation": history,
            "message_count": len(history)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/conversation/<user_id>', methods=['DELETE'])
def clear_conversation(user_id):
    """Clear conversation history for a user"""
    try:
        if user_id in conversations:
            del conversations[user_id]
        return jsonify({
            "message": f"Conversation cleared for user {user_id}",
            "user_id": user_id
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print(f"🎤 Starting Enhanced Orpheus TTS API...")
    print(f"📡 Model: {MODEL_NAME}")
    print(f"🔊 Available voices: {list(VOICES.keys())}")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"📚 Endpoints:")
    print(f"   GET  / - Health check")
    print(f"   GET  /voices - List voices")
    print(f"   POST /speak - Generate speech (demo)")
    print(f"   POST /chat - Text conversation")
    print(f"   POST /voice_chat - Voice conversation")
    print(f"   GET  /conversation/<user_id> - Get chat history")
    print(f"   DELETE /conversation/<user_id> - Clear chat history")
    print(f"🚀 Features: Simple TTS Demo + Real-time AI Conversation!")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
