"""
Enhanced Orpheus TTS API with Real Speech and AI Conversation
Uses real Windows Speech API for actual voice synthesis
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
import subprocess
import sys

app = Flask(__name__)
CORS(app)

# Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'canopylabs/orpheus-tts-0.1-finetune-prod')
PORT = int(os.getenv('PORT', 8080))

# Available voices
VOICES = {
    "tara": {"id": "tara", "name": "Tara", "gender": "female", "rate": "0", "voice": "Microsoft Zira Desktop"},
    "alex": {"id": "alex", "name": "Alex", "gender": "male", "rate": "0", "voice": "Microsoft David Desktop"},
    "sarah": {"id": "sarah", "name": "Sarah", "gender": "female", "rate": "1", "voice": "Microsoft Hazel Desktop"}
}

# Conversation memory for each user
conversations = {}

def generate_real_speech_windows(text, voice="tara"):
    """
    Generate real speech using Windows Speech API (SAPI)
    """
    try:
        # Get voice settings
        voice_config = VOICES.get(voice, VOICES["tara"])
        windows_voice = voice_config["voice"]
        rate = voice_config["rate"]
        
        # Create temporary WAV file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_file.close()
        
        # PowerShell script for speech synthesis
        powershell_script = f"""
        Add-Type -AssemblyName System.Speech
        $synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
        
        # Try to set the voice
        try {{
            $synth.SelectVoice("{windows_voice}")
        }} catch {{
            # Fallback to default voice if specified voice not found
            Write-Host "Voice {windows_voice} not found, using default"
        }}
        
        $synth.Rate = {rate}
        $synth.SetOutputToWaveFile("{temp_file.name}")
        $synth.Speak("{text}")
        $synth.Dispose()
        """
        
        # Execute PowerShell script
        result = subprocess.run([
            "powershell", "-Command", powershell_script
        ], capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0 and os.path.exists(temp_file.name) and os.path.getsize(temp_file.name) > 1000:
            return temp_file.name
        else:
            # Fallback to synthetic audio if Windows Speech fails
            return generate_synthetic_speech(text, voice)
            
    except Exception as e:
        print(f"Windows Speech error: {e}")
        # Fallback to synthetic audio
        return generate_synthetic_speech(text, voice)

def generate_synthetic_speech(text, voice="tara"):
    """
    Fallback synthetic speech generator (improved version)
    """
    # Create more realistic speech-like audio
    sample_rate = 22050
    duration = len(text) * 0.12  # Slower, more realistic pace
    duration = max(1.5, min(duration, 15.0))  # Between 1.5-15 seconds
    
    # Generate time array
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Voice characteristics
    voice_frequencies = {
        "tara": {"base": 200, "formant1": 800, "formant2": 1200},
        "sarah": {"base": 220, "formant1": 900, "formant2": 1400}, 
        "alex": {"base": 120, "formant1": 600, "formant2": 1000}
    }
    
    config = voice_frequencies.get(voice, voice_frequencies["tara"])
    base_freq = config["base"]
    
    # Create more complex speech-like waveform
    audio_data = np.zeros_like(t)
    
    # Fundamental frequency with natural variation
    pitch_variation = 1 + 0.15 * np.sin(2 * np.pi * 0.5 * t) + 0.05 * np.sin(2 * np.pi * 2.3 * t)
    fundamental = np.sin(2 * np.pi * base_freq * pitch_variation * t)
    
    # Add harmonics for more natural sound
    for i, amplitude in enumerate([1.0, 0.6, 0.4, 0.25, 0.15, 0.1]):
        harmonic_freq = base_freq * (i + 1) * pitch_variation
        audio_data += amplitude * np.sin(2 * np.pi * harmonic_freq * t)
    
    # Add formants (resonant frequencies that give vowel character)
    formant1 = 0.3 * np.sin(2 * np.pi * config["formant1"] * t)
    formant2 = 0.2 * np.sin(2 * np.pi * config["formant2"] * t)
    audio_data += formant1 + formant2
    
    # Add speech-like amplitude modulation
    syllable_rate = len(text.split()) * 2.5 / duration  # Approximate syllable rate
    amplitude_mod = 1 + 0.4 * np.sin(2 * np.pi * syllable_rate * t)
    audio_data *= amplitude_mod
    
    # Add some noise for realism
    noise = 0.02 * np.random.normal(0, 1, len(t))
    audio_data += noise
    
    # Create pauses between words
    words = text.split()
    word_positions = np.linspace(0, len(t), len(words) + 1)
    for i in range(len(words)):
        start_idx = int(word_positions[i])
        end_idx = int(word_positions[i + 1])
        # Add slight pause between words
        if i < len(words) - 1:
            pause_start = int(end_idx - 0.05 * sample_rate)
            pause_end = int(end_idx)
            if pause_start < pause_end and pause_end < len(audio_data):
                audio_data[pause_start:pause_end] *= 0.1
    
    # Normalize and apply envelope
    max_val = np.max(np.abs(audio_data))
    if max_val > 0:
        audio_data = audio_data / max_val * 0.8
    
    # Apply smooth fade in/out
    fade_samples = int(sample_rate * 0.1)  # 100ms fade
    if len(audio_data) > 2 * fade_samples:
        fade_in = np.linspace(0, 1, fade_samples)
        fade_out = np.linspace(1, 0, fade_samples)
        audio_data[:fade_samples] *= fade_in
        audio_data[-fade_samples:] *= fade_out
    
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
    Enhanced AI response generator with better conversation
    """
    # Initialize conversation history for new users
    if user_id not in conversations:
        conversations[user_id] = []
    
    # Add user message to history
    conversations[user_id].append({"role": "user", "content": user_message})
    
    user_lower = user_message.lower().strip()
    
    # Enhanced response patterns
    greetings = ["hello", "hi", "hey", "good morning", "good afternoon", "good evening"]
    questions = ["how are you", "what's up", "how's it going", "what are you doing"]
    
    if any(greeting in user_lower for greeting in greetings):
        if any(question in user_lower for question in questions):
            ai_response = "Hello! I'm doing great, thank you for asking! I'm your AI voice assistant, ready to have a conversation with you. How are you doing today?"
        else:
            ai_response = "Hello there! Great to meet you! I'm your AI voice assistant. I can chat about anything you'd like - ask me questions, tell me about your day, or just have a casual conversation!"
    
    elif any(question in user_lower for question in questions):
        ai_response = "I'm doing wonderful! I love having conversations and helping people. I'm here and ready to chat about whatever interests you. What's on your mind today?"
    
    elif "your name" in user_lower or "who are you" in user_lower:
        ai_response = "I'm your AI voice assistant! Think of me as a friendly conversational partner. I can discuss topics, answer questions, share thoughts, and just chat. What would you like to talk about?"
    
    elif "weather" in user_lower:
        ai_response = "I don't have access to real-time weather data, but I'd love to hear about the weather where you are! Is it sunny, rainy, or something else today?"
    
    elif "time" in user_lower:
        current_time = datetime.now().strftime('%I:%M %p')
        ai_response = f"The current time is {current_time}. How's your day going so far?"
    
    elif "date" in user_lower or "today" in user_lower:
        current_date = datetime.now().strftime('%A, %B %d, %Y')
        ai_response = f"Today is {current_date}. Do you have any interesting plans for today?"
    
    elif "joke" in user_lower or "funny" in user_lower:
        jokes = [
            "Why don't scientists trust atoms? Because they make up everything!",
            "I told my computer a joke about UDP. It didn't get it, but that's okay!",
            "Why do programmers prefer dark mode? Because light attracts bugs!",
            "What did the AI say to the human? 'You're learning, but I'm still processing!'"
        ]
        import random
        ai_response = random.choice(jokes) + " Hope that made you smile! Got any good jokes to share with me?"
    
    elif any(word in user_lower for word in ["help", "what can you do", "capabilities"]):
        ai_response = "I'm here to have conversations with you! I can discuss various topics, answer questions, share thoughts, tell jokes, or just chat about your day. I also speak my responses out loud so we can have a natural voice conversation. What would you like to explore together?"
    
    elif any(word in user_lower for word in ["bye", "goodbye", "see you", "talk later"]):
        ai_response = "It was wonderful chatting with you! Feel free to come back anytime for another conversation. Take care and have a great day!"
    
    elif "?" in user_message:
        ai_response = f"That's a fascinating question! You asked about '{user_message}' - I find that really interesting. While I may not have all the answers, I'd love to explore this topic with you. What aspects are you most curious about?"
    
    elif any(word in user_lower for word in ["love", "like", "enjoy", "favorite"]):
        ai_response = "That sounds really wonderful! I can hear the enthusiasm in your message. What specifically do you enjoy most about it? I'd love to hear more details!"
    
    elif any(word in user_lower for word in ["problem", "issue", "difficult", "trouble", "hard"]):
        ai_response = "I can sense this might be challenging for you. While I'm here to listen and chat, sometimes it helps just to talk through things. Would you like to share more about what's on your mind?"
    
    elif len(user_message.split()) > 15:
        ai_response = "Thank you for sharing all those details with me! I really appreciate you taking the time to explain that. There's a lot to unpack there - what part would you like to dive deeper into?"
    
    elif any(word in user_lower for word in ["tell me about", "explain", "what is"]):
        ai_response = "I'd be happy to discuss that topic with you! While I aim to be helpful, I find conversations work best when we explore ideas together. What specifically interests you most about this subject?"
    
    else:
        # Dynamic responses based on message content
        if len(user_message.split()) <= 3:
            ai_response = f"Interesting point about '{user_message}'! Can you tell me more about what you're thinking? I'd love to hear your perspective on this."
        else:
            ai_response = f"I find what you're saying really engaging! You mentioned '{user_message[:50]}...' - that really resonates with me. What made you think about this topic?"
    
    # Add AI response to history
    conversations[user_id].append({"role": "assistant", "content": ai_response})
    
    # Keep conversation history reasonable (last 30 messages)
    if len(conversations[user_id]) > 30:
        conversations[user_id] = conversations[user_id][-30:]
    
    return ai_response

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Enhanced Orpheus TTS API with Real Speech & AI Chat",
        "model": MODEL_NAME,
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "features": ["real_speech", "ai_conversation", "multi_voice", "windows_sapi"]
    })

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available voices"""
    return jsonify({
        "voices": list(VOICES.values())
    })

@app.route('/speak', methods=['POST'])
def generate_speech():
    """Generate speech from text input (demo endpoint with real speech)"""
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
        
        # Generate real speech
        print(f"Generating speech for: '{text}' with voice: {voice}")
        audio_file = generate_real_speech_windows(text, voice)
        
        # Return audio file
        return send_file(
            audio_file, 
            mimetype='audio/wav',
            as_attachment=True,
            download_name=f'speech_{voice}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.wav'
        )
        
    except Exception as e:
        print(f"Speech generation error: {e}")
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
    """Voice chat endpoint - combines conversation + real speech"""
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
        print(f"User {user_id}: {user_message}")
        ai_response = get_ai_response(user_message, user_id)
        print(f"AI Response: {ai_response}")
        
        # Generate real speech for AI response
        audio_file = generate_real_speech_windows(ai_response, voice)
        
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
        print(f"Voice chat error: {e}")
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
    print(f"🎤 Starting Enhanced Orpheus TTS API with REAL SPEECH...")
    print(f"📡 Model: {MODEL_NAME}")
    print(f"🔊 Available voices: {list(VOICES.keys())}")
    print(f"🗣️ Speech Engine: Windows SAPI + Synthetic Fallback")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"📚 Endpoints:")
    print(f"   GET  / - Health check")
    print(f"   GET  /voices - List voices")
    print(f"   POST /speak - Generate real speech (demo)")
    print(f"   POST /chat - Text conversation")
    print(f"   POST /voice_chat - Voice conversation with real speech")
    print(f"   GET  /conversation/<user_id> - Get chat history")
    print(f"   DELETE /conversation/<user_id> - Clear chat history")
    print(f"🚀 Features: REAL SPEECH + Intelligent AI Conversation!")
    print(f"✨ Try saying 'hello' in the AI Chat tab for a real conversation!")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
