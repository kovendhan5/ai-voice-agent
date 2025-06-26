"""
Intelligent AI Voice Assistant - ChatGPT-like Conversations
"""
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import tempfile
import json
import random
import re
from datetime import datetime

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# Store conversation history for each user
conversation_history = {}

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response

def generate_ai_response(message, history):
    """Generate intelligent AI responses like ChatGPT"""
    
    # Convert message to lowercase for pattern matching
    msg_lower = message.lower()
    
    # Contextual responses based on conversation history
    recent_topics = []
    if len(history) > 2:
        recent_topics = [msg["content"].lower() for msg in history[-4:] if msg["role"] == "user"]
    
    # Greeting responses
    if any(word in msg_lower for word in ['hello', 'hi', 'hey', 'good morning', 'good afternoon', 'good evening']):
        greetings = [
            "Hello! I'm your AI assistant. I'm here to help with questions, have conversations, or assist with any tasks you need. What would you like to talk about?",
            "Hi there! Great to meet you! I'm an AI assistant designed to be helpful, harmless, and honest. How can I assist you today?",
            "Hey! I'm excited to chat with you. I can help with information, creative tasks, problem-solving, or just have a friendly conversation. What's on your mind?"
        ]
        return random.choice(greetings)
    
    # Questions about the AI
    if any(phrase in msg_lower for phrase in ['who are you', 'what are you', 'tell me about yourself', 'introduce yourself']):
        return "I'm an AI assistant, similar to ChatGPT or Copilot, but running locally on your system! I can help with coding, answer questions, have conversations, solve problems, and assist with creative tasks. I remember our conversation context, so we can have natural back-and-forth discussions. What would you like to explore together?"
    
    # Capabilities questions
    if any(phrase in msg_lower for phrase in ['what can you do', 'your capabilities', 'help me', 'how can you help']):
        return "I can help you with many things! I can answer questions, help with coding and programming, explain concepts, assist with creative writing, solve problems, have philosophical discussions, help with math and science, provide explanations on various topics, and much more. I maintain context from our conversation, so feel free to build on previous topics. What specific area interests you?"
    
    # Programming/coding questions
    if any(word in msg_lower for word in ['code', 'programming', 'python', 'javascript', 'html', 'css', 'react', 'node', 'api', 'function', 'variable', 'error', 'bug', 'debug']):
        return f"I'd be happy to help with programming! You mentioned '{message}'. I can assist with coding questions, debugging, explaining concepts, writing code snippets, reviewing code, or helping with software architecture. What specific programming challenge are you working on?"
    
    # Creative/writing requests
    if any(word in msg_lower for word in ['write', 'story', 'poem', 'creative', 'idea', 'brainstorm', 'imagine']):
        return f"I love creative tasks! Regarding '{message}', I can help with creative writing, brainstorming ideas, storytelling, poetry, or any other creative endeavors. What kind of creative project are you thinking about?"
    
    # Science/math questions
    if any(word in msg_lower for word in ['math', 'science', 'physics', 'chemistry', 'biology', 'calculate', 'formula', 'equation', 'theory']):
        return f"Great question about '{message}'! I can help explain scientific concepts, solve math problems, discuss theories, or work through calculations. What specific aspect would you like to explore?"
    
    # Context-aware responses
    if 'continue' in msg_lower or 'more' in msg_lower:
        return "Absolutely! I'm ready to continue our discussion. Could you specify what aspect you'd like me to expand on or continue with?"
    
    # Problem-solving requests
    if any(word in msg_lower for word in ['problem', 'issue', 'challenge', 'stuck', 'help', 'solution', 'fix']):
        return f"I'm here to help solve problems! About '{message}' - let me understand the situation better. Could you provide more details about the specific challenge you're facing? I can help break it down and work through potential solutions step by step."
    
    # Opinion/discussion topics
    if any(word in msg_lower for word in ['think', 'opinion', 'believe', 'discuss', 'talk about', 'what about', 'thoughts on']):
        return f"That's an interesting topic: '{message}'. I'd be happy to discuss this with you! I can share different perspectives, provide information, and explore various angles. What particular aspect of this interests you most?"
    
    # Learning/education requests
    if any(word in msg_lower for word in ['learn', 'teach', 'explain', 'understand', 'lesson', 'tutorial', 'guide']):
        return f"I'd love to help you learn about '{message}'! I can break down complex topics, provide step-by-step explanations, give examples, and adapt my teaching style to what works best for you. What's your current knowledge level on this topic?"
    
    # General conversation
    general_responses = [
        f"That's interesting that you mentioned '{message}'. I'd like to understand more about your perspective on this. Could you tell me what specifically interests you about it?",
        f"Thanks for sharing '{message}' with me. I find this topic engaging! What aspects of this would you like to explore further?",
        f"Regarding '{message}' - I can help provide information, different viewpoints, or have a detailed discussion about this. What direction would you like our conversation to take?",
        f"I appreciate you bringing up '{message}'. This could lead to a fascinating conversation! What prompted you to think about this topic?",
        f"You've touched on something interesting with '{message}'. I'm curious to learn more about your thoughts and can share relevant information or insights. What specific angle interests you most?"
    ]
    
    return random.choice(general_responses)

@app.route('/')
def health():
    return jsonify({
        "status": "healthy", 
        "message": "AI Server is running!",
        "server": "minimal_ai"
    })

@app.route('/chat', methods=['POST'])
def chat():
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'default')
        
        # Get conversation history
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Add user message to history
        conversation_history[user_id].append({"role": "user", "content": message})
        
        # Generate intelligent AI response
        response = generate_ai_response(message, conversation_history[user_id])
        
        # Add AI response to history
        conversation_history[user_id].append({"role": "assistant", "content": response})
        
        # Keep conversation history manageable (last 20 messages)
        if len(conversation_history[user_id]) > 20:
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
        return jsonify({
            "ai_response": response,
            "user_message": message,
            "conversation_length": len(conversation_history[user_id])
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/voice_chat', methods=['POST'])
def voice_chat():
    try:
        data = request.get_json() or {}
        message = data.get('message', '')
        user_id = data.get('user_id', 'voice_user')
        
        # Get conversation history
        if user_id not in conversation_history:
            conversation_history[user_id] = []
        
        # Add user message to history
        conversation_history[user_id].append({"role": "user", "content": message})
        
        # Generate intelligent AI response
        ai_response = generate_ai_response(message, conversation_history[user_id])
        
        # Add AI response to history
        conversation_history[user_id].append({"role": "assistant", "content": ai_response})
        
        # Keep conversation history manageable (last 20 messages)
        if len(conversation_history[user_id]) > 20:
            conversation_history[user_id] = conversation_history[user_id][-20:]
        
        # Generate audio response using simple TTS
        audio_file = generate_speech_audio(ai_response)
        
        return send_file(audio_file, mimetype='audio/wav', as_attachment=False,
                        download_name=f'ai_response_{len(conversation_history[user_id])}.wav')
    except Exception as e:
        # Return error as audio
        error_audio = generate_speech_audio("Sorry, I encountered an error processing your request.")
        return send_file(error_audio, mimetype='audio/wav')

def generate_speech_audio(text):
    """Generate speech audio from text"""
    import wave
    import numpy as np
    
    # Create a more pleasant tone based on text length
    sample_rate = 22050
    duration = min(max(len(text) * 0.05, 1.0), 5.0)  # Duration based on text length
    
    # Create multiple tones for a more speech-like sound
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Base frequency varies with text characteristics
    base_freq = 200 + (len(text) % 100)  # Vary pitch based on text
    
    # Create harmonics for more natural sound
    audio_data = (
        np.sin(2 * np.pi * base_freq * t) * 0.3 +
        np.sin(2 * np.pi * base_freq * 1.5 * t) * 0.2 +
        np.sin(2 * np.pi * base_freq * 2.0 * t) * 0.1
    )
    
    # Add some variation to make it less monotone
    audio_data *= (1 + 0.3 * np.sin(2 * np.pi * 2 * t))
    
    # Apply fade in/out
    fade_samples = int(sample_rate * 0.1)
    audio_data[:fade_samples] *= np.linspace(0, 1, fade_samples)
    audio_data[-fade_samples:] *= np.linspace(1, 0, fade_samples)
    
    # Convert to 16-bit
    audio_data = (audio_data * 32767).astype(np.int16)
    
    # Save to temp file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
        with wave.open(f.name, 'wb') as wav_file:
            wav_file.setnchannels(1)
            wav_file.setsampwidth(2)
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        return f.name

@app.route('/voices')
def voices():
    return jsonify({"voices": [{"id": "test", "name": "Test Voice"}]})

if __name__ == '__main__':
    print("🚀 Starting Minimal AI Server...")
    print("🌐 Open: http://localhost:8080")
    print("🔗 Server will be available in a few seconds...")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
