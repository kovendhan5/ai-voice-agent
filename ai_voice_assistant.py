from flask import Flask, request, send_file, jsonify
import os
import tempfile
import logging
from datetime import datetime
import json

# For now, we'll use a simple AI response system
# You can replace this with GPT, Claude, or any other LLM API
from orpheus_tts import OrpheusModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the TTS model
logger.info("Loading Orpheus TTS model...")
try:
    tts_model = OrpheusModel(model_name="canopylabs/orpheus-tts-0.1-finetune-prod")
    logger.info("Orpheus TTS model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load TTS model: {e}")
    tts_model = None

# Simple AI response system (replace with real LLM later)
class SimpleAI:
    def __init__(self):
        self.conversation_history = []
        self.personality = "friendly and helpful assistant"
    
    def get_response(self, user_input, user_id=None):
        """Generate AI response based on user input"""
        user_input = user_input.lower().strip()
        
        # Add to conversation history
        self.conversation_history.append({
            "user_id": user_id,
            "user_input": user_input,
            "timestamp": datetime.now().isoformat()
        })
        
        # Simple response logic (replace with real AI)
        if "hello" in user_input or "hi" in user_input:
            responses = [
                "Hello! I'm your AI assistant. How can I help you today?",
                "Hi there! Great to meet you. What would you like to talk about?",
                "Hello! I'm here and ready to chat. What's on your mind?"
            ]
        elif "how are you" in user_input:
            responses = [
                "I'm doing great, thank you! I'm excited to be talking with you.",
                "I'm wonderful! Ready to help you with anything you need.",
                "I'm doing fantastic! How are you doing today?"
            ]
        elif "what can you do" in user_input or "capabilities" in user_input:
            responses = [
                "I can have conversations with you, answer questions, and speak back to you using advanced text-to-speech technology!",
                "I'm an AI assistant that can chat with you naturally. I can discuss topics, answer questions, and respond with realistic speech!",
                "I can engage in conversations, provide information, and communicate through both text and speech!"
            ]
        elif "weather" in user_input:
            responses = [
                "I don't have access to real-time weather data, but I'd be happy to chat about weather in general or help you with something else!",
                "I can't check the current weather, but I'm here to help with other questions or just have a friendly conversation!"
            ]
        elif "joke" in user_input or "funny" in user_input:
            responses = [
                "Why don't scientists trust atoms? Because they make up everything!",
                "I told my wife she was drawing her eyebrows too high. She looked surprised!",
                "Why did the scarecrow win an award? He was outstanding in his field!"
            ]
        elif "goodbye" in user_input or "bye" in user_input:
            responses = [
                "Goodbye! It was great talking with you. Come back anytime!",
                "See you later! Thanks for the wonderful conversation.",
                "Bye! I enjoyed our chat. Hope to talk again soon!"
            ]
        elif "name" in user_input and ("my" in user_input or "i am" in user_input):
            responses = [
                "Nice to meet you! I'm your AI assistant, and I'm happy to be chatting with you.",
                "Great to meet you! I'm an AI powered by Orpheus voice technology.",
                "Pleased to meet you! I'm here to have conversations and help however I can."
            ]
        elif "thank" in user_input:
            responses = [
                "You're very welcome! I'm happy to help.",
                "My pleasure! That's what I'm here for.",
                "You're welcome! Feel free to ask me anything else."
            ]
        else:
            # Generic responses for other inputs
            responses = [
                f"That's interesting! You mentioned: '{user_input}'. Can you tell me more about that?",
                f"I heard you say '{user_input}'. That's fascinating! What would you like to explore about this topic?",
                f"Thanks for sharing that! '{user_input}' is something I'd love to discuss further. What specifically interests you about it?",
                "That's a great point! I find conversations like this really engaging. What else would you like to talk about?",
                "Interesting perspective! I enjoy learning from these conversations. Is there anything specific you'd like to know or discuss?"
            ]
        
        # Select a response (you could make this more sophisticated)
        import random
        response = random.choice(responses)
        
        # Add AI response to history
        self.conversation_history.append({
            "ai_response": response,
            "timestamp": datetime.now().isoformat()
        })
        
        return response

# Initialize AI
ai_assistant = SimpleAI()

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    if tts_model is None:
        return jsonify({"status": "error", "message": "TTS model not loaded"}), 500
    return jsonify({
        "status": "healthy", 
        "message": "Orpheus AI Voice Assistant is running",
        "version": "1.0",
        "features": ["voice_conversation", "multi_user", "real_time_ai"]
    })

@app.route("/chat", methods=["POST"])
def chat_with_ai():
    """Have a conversation with the AI (text only)"""
    try:
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400
        
        user_message = data.get("message", "")
        user_id = data.get("user_id", "anonymous")
        
        # Get AI response
        ai_response = ai_assistant.get_response(user_message, user_id)
        
        return jsonify({
            "user_message": user_message,
            "ai_response": ai_response,
            "timestamp": datetime.now().isoformat(),
            "user_id": user_id
        })
    
    except Exception as e:
        logger.error(f"Chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/voice_chat", methods=["POST"])
def voice_chat():
    """Complete voice conversation: speech input -> AI response -> speech output"""
    try:
        if tts_model is None:
            return jsonify({"error": "TTS model not loaded"}), 500
        
        data = request.get_json()
        if not data or "message" not in data:
            return jsonify({"error": "Missing 'message' field"}), 400
        
        user_message = data.get("message", "")
        user_id = data.get("user_id", "anonymous")
        voice = data.get("voice", "tara")
        
        logger.info(f"Voice chat from {user_id}: {user_message[:50]}...")
        
        # Get AI response
        ai_response = ai_assistant.get_response(user_message, user_id)
        
        # Generate speech for AI response
        prompt = f"{voice}: {ai_response}"
        audio_chunks = tts_model.generate_speech(prompt=prompt, voice=voice)
        
        # Create temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            for chunk in audio_chunks:
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        logger.info(f"AI response generated: {ai_response[:50]}...")
        
        return send_file(
            temp_file_path,
            mimetype="audio/wav",
            as_attachment=True,
            download_name="ai_response.wav"
        )
    
    except Exception as e:
        logger.error(f"Voice chat error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/conversation_history", methods=["GET"])
def get_conversation_history():
    """Get recent conversation history"""
    try:
        # Return last 20 conversation entries
        recent_history = ai_assistant.conversation_history[-20:]
        return jsonify({
            "conversation_history": recent_history,
            "total_interactions": len(ai_assistant.conversation_history)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/voices", methods=["GET"])
def list_voices():
    """List available voices"""
    voices = [
        {"id": "tara", "name": "Tara", "description": "Friendly female voice"},
        {"id": "alex", "name": "Alex", "description": "Professional male voice"},
        {"id": "sarah", "name": "Sarah", "description": "Warm female voice"}
    ]
    return jsonify({"voices": voices})

@app.route("/stats", methods=["GET"])
def get_stats():
    """Get usage statistics"""
    return jsonify({
        "total_conversations": len(ai_assistant.conversation_history),
        "server_uptime": "Running",
        "model_status": "Loaded" if tts_model else "Error",
        "timestamp": datetime.now().isoformat()
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    debug_mode = os.environ.get("DEBUG", "false").lower() == "true"
    
    logger.info(f"🤖 Starting Orpheus AI Voice Assistant on port {port}")
    logger.info("🎤 Features: Real-time AI conversations with voice")
    logger.info("🌐 Endpoints:")
    logger.info("   GET  /                 - Health check")
    logger.info("   POST /chat            - Text conversation")
    logger.info("   POST /voice_chat      - Voice conversation")
    logger.info("   GET  /conversation_history - Chat history")
    logger.info("   GET  /voices          - Available voices")
    logger.info("   GET  /stats           - Usage statistics")
    
    app.run(host="0.0.0.0", port=port, debug=debug_mode)
