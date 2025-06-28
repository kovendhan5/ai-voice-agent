"""
Guaranteed Working AI Voice Server
This version has minimal dependencies and should always work
"""

from flask import Flask, request, jsonify, send_file
import tempfile
import os
import sys
import json
import time
import wave
import numpy as np

# Add current directory to Python path
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, current_dir)

app = Flask(__name__)

class SimpleAI:
    """Minimal AI that always works"""
    
    def __init__(self):
        self.conversation_history = []
        
        self.responses = [
            "That's really interesting! Tell me more about that.",
            "I understand what you're saying. How does that make you feel?",
            "That's a great point! What do you think about the bigger picture?",
            "I see your perspective. Have you considered looking at it differently?",
            "Thanks for sharing that with me. What's most important to you about this?",
            "That sounds meaningful. Can you help me understand why?",
            "I appreciate you telling me that. What would you like to explore next?",
            "That's fascinating! What got you interested in this topic?",
            "I hear you. What do you think the next step should be?",
            "That makes sense. How would you explain this to someone else?"
        ]
        
    def get_response(self, text):
        """Generate AI response"""
        # Add to history
        self.conversation_history.append({"user": text, "timestamp": time.time()})
        
        # Simple response selection based on text content
        if "hello" in text.lower() or "hi" in text.lower():
            response = "Hello! I'm excited to chat with you. What's on your mind today?"
        elif "how are you" in text.lower():
            response = "I'm doing wonderful, thank you for asking! How are you doing?"
        elif "?" in text:
            response = "That's a thoughtful question! Let me think about that..."
        elif "thank" in text.lower():
            response = "You're very welcome! I enjoy our conversations."
        elif len(text.split()) < 3:
            response = "Could you tell me a bit more about that?"
        else:
            # Use response based on conversation length
            response_index = len(self.conversation_history) % len(self.responses)
            response = self.responses[response_index]
        
        # Add AI response to history
        self.conversation_history.append({"ai": response, "timestamp": time.time()})
        
        return response

class SimpleTTS:
    """Minimal TTS that generates real audio"""
    
    def generate_audio(self, text, voice="tara"):
        """Generate WAV audio from text"""
        try:
            # Calculate duration based on text length (roughly 150 words per minute)
            words = len(text.split())
            duration = max(1.0, words / 2.5)  # Minimum 1 second
            
            # Generate audio parameters
            sample_rate = 22050
            num_samples = int(duration * sample_rate)
            
            # Create simple synthetic speech (tone variations)
            t = np.linspace(0, duration, num_samples)
            
            # Base frequency varies by voice
            voice_frequencies = {"tara": 220, "alex": 150, "sarah": 250}
            base_freq = voice_frequencies.get(voice, 200)
            
            # Generate tone with some variation
            frequency_modulation = np.sin(2 * np.pi * 2 * t) * 20  # Slight vibrato
            audio = np.sin(2 * np.pi * (base_freq + frequency_modulation) * t)
            
            # Add some harmonics for richer sound
            audio += 0.3 * np.sin(2 * np.pi * (base_freq * 2 + frequency_modulation) * t)
            audio += 0.1 * np.sin(2 * np.pi * (base_freq * 3 + frequency_modulation) * t)
            
            # Apply envelope to avoid clicks
            envelope = np.exp(-3 * t / duration)
            audio *= envelope
            
            # Normalize and convert to int16
            audio = (audio * 32767 * 0.5).astype(np.int16)
            
            # Create temporary WAV file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            
            with wave.open(temp_file.name, 'wb') as wav_file:
                wav_file.setnchannels(1)  # Mono
                wav_file.setsampwidth(2)  # 2 bytes per sample
                wav_file.setframerate(sample_rate)
                wav_file.writeframes(audio.tobytes())
            
            return temp_file.name
            
        except Exception as e:
            print(f"TTS Error: {e}")
            return None

# Initialize AI and TTS
ai = SimpleAI()
tts = SimpleTTS()

@app.route('/')
def home():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "message": "AI Voice Assistant is running!",
        "version": "1.0.0",
        "endpoints": ["/", "/chat", "/voice_chat", "/conversation_history"]
    })

@app.route('/chat', methods=['POST'])
def chat():
    """Text chat endpoint"""
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message'].strip()
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        # Generate AI response
        ai_response = ai.get_response(user_message)
        
        return jsonify({
            "response": ai_response,
            "user_message": user_message,
            "timestamp": time.time()
        })
        
    except Exception as e:
        return jsonify({"error": f"Chat error: {str(e)}"}), 500

@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    """Voice chat endpoint - returns audio response"""
    try:
        data = request.json
        if not data or 'message' not in data:
            return jsonify({"error": "No message provided"}), 400
        
        user_message = data['message'].strip()
        voice = data.get('voice', 'tara')
        
        if not user_message:
            return jsonify({"error": "Empty message"}), 400
        
        # Generate AI response
        ai_response = ai.get_response(user_message)
        
        # Generate audio
        audio_file = tts.generate_audio(ai_response, voice)
        
        if audio_file:
            return send_file(
                audio_file,
                mimetype='audio/wav',
                as_attachment=True,
                download_name='response.wav'
            )
        else:
            return jsonify({"error": "Failed to generate audio"}), 500
            
    except Exception as e:
        return jsonify({"error": f"Voice chat error: {str(e)}"}), 500

@app.route('/conversation_history')
def conversation_history():
    """Get conversation history"""
    return jsonify({
        "history": ai.conversation_history[-20:],  # Last 20 exchanges
        "total_exchanges": len(ai.conversation_history)
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print("🤖 Starting AI Voice Assistant...")
    print("=" * 50)
    print("Server will be available at: http://localhost:8080")
    print("Available endpoints:")
    print("  GET  /                  - Health check")
    print("  POST /chat              - Text chat")
    print("  POST /voice_chat        - Voice chat (returns audio)")
    print("  GET  /conversation_history - Get chat history")
    print("=" * 50)
    print("✅ Server starting on port 8080...")
    
    try:
        app.run(host='0.0.0.0', port=8080, debug=False, threaded=True)
    except KeyboardInterrupt:
        print("\n👋 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Server error: {e}")
