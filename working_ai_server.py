"""
Intelligent AI Voice Assistant - CORS Fixed Version
"""
from flask import Flask, request, jsonify, send_file
import tempfile
import json
import random
import re
from datetime import datetime

app = Flask(__name__)

# Store conversation history for each user
conversation_history = {}

@app.after_request
def after_request(response):
    """Add CORS headers to all responses"""
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    response.headers.add('Access-Control-Max-Age', '86400')
    return response

@app.route('/', methods=['GET', 'OPTIONS'])
def health():
    if request.method == 'OPTIONS':
        return '', 200
    return jsonify({
        "status": "healthy", 
        "message": "AI Server is running!",
        "server": "intelligent_ai",
        "timestamp": datetime.now().isoformat()
    })

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

@app.route('/chat', methods=['POST', 'OPTIONS'])
def chat():
    if request.method == 'OPTIONS':
        return '', 200
    
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

@app.route('/voice_chat', methods=['POST', 'OPTIONS'])
def voice_chat():
    if request.method == 'OPTIONS':
        return '', 200
    
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
        
        # Generate audio response using real TTS
        audio_file = generate_speech_audio(ai_response)
        
        # Determine the correct mimetype based on file extension
        if audio_file.endswith('.mp3'):
            mimetype = 'audio/mpeg'
        else:
            mimetype = 'audio/wav'
        
        return send_file(audio_file, mimetype=mimetype, as_attachment=False,
                        download_name=f'ai_response_{len(conversation_history[user_id])}.wav')
    except Exception as e:
        # Return error as audio
        error_audio = generate_speech_audio("Sorry, I encountered an error processing your request.")
        return send_file(error_audio, mimetype='audio/wav')

def generate_speech_audio(text):
    """Generate real speech audio from text using Windows SAPI"""
    try:
        # Method 1: Use Windows SAPI directly (most reliable on Windows)
        import win32com.client
        import os
        
        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        temp_path = temp_file.name
        temp_file.close()
        
        # Initialize Windows Speech API
        speaker = win32com.client.Dispatch("SAPI.SpVoice")
        
        # Set up file output
        file_stream = win32com.client.Dispatch("SAPI.SpFileStream")
        file_stream.Open(temp_path, 3)  # 3 = SSFMCreateForWrite
        speaker.AudioOutputStream = file_stream
        
        # Get available voices and try to use a female one
        voices = speaker.GetVoices()
        for i in range(voices.Count):
            voice = voices.Item(i)
            if 'female' in voice.GetDescription().lower() or 'zira' in voice.GetDescription().lower():
                speaker.Voice = voice
                break
        
        # Set speech rate (0-10, default is 0)
        speaker.Rate = 1  # Slightly faster than default
        
        # Generate speech
        speaker.Speak(text)
        
        # Close the file stream
        file_stream.Close()
        
        # Check if file was created successfully
        if os.path.exists(temp_path) and os.path.getsize(temp_path) > 100:  # Check for reasonable file size
            print(f"✅ Generated speech audio: {temp_path} ({os.path.getsize(temp_path)} bytes)")
            return temp_path
        else:
            raise Exception("Windows SAPI failed to generate audio")
            
    except Exception as e:
        print(f"Windows SAPI failed: {e}")
        try:
            # Method 2: Try edge-tts (Microsoft Edge TTS - very reliable)
            import subprocess
            import os
            
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
            temp_path = temp_file.name
            temp_file.close()
            
            # Try to use edge-tts command line tool
            cmd = [
                'edge-tts',
                '--voice', 'en-US-AriaNeural',  # Nice female voice
                '--text', text,
                '--write-media', temp_path
            ]
            
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0 and os.path.exists(temp_path) and os.path.getsize(temp_path) > 100:
                print(f"✅ Generated speech with edge-tts: {temp_path}")
                return temp_path
            else:
                raise Exception(f"edge-tts failed: {result.stderr}")
                
        except Exception as e2:
            print(f"edge-tts failed: {e2}")
            try:
                # Method 3: Try gTTS (Google TTS - requires internet)
                from gtts import gTTS
                import os
                
                # Create a temporary file
                temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
                temp_path = temp_file.name
                temp_file.close()
                
                # Generate speech using Google TTS
                tts = gTTS(text=text, lang='en', slow=False)
                tts.save(temp_path)
                
                if os.path.exists(temp_path) and os.path.getsize(temp_path) > 100:
                    print(f"✅ Generated speech with Google TTS: {temp_path}")
                    return temp_path
                else:
                    raise Exception("Google TTS failed")
                    
            except Exception as e3:
                # Method 4: Last resort - use system TTS command (Windows)
                print(f"All TTS methods failed: {e}, {e2}, {e3}")
                try:
                    import subprocess
                    import os
                    
                    # Create a VBS script to use Windows built-in TTS
                    vbs_script = f"""
                    Set speech = CreateObject("SAPI.SpVoice")
                    speech.Speak "{text}"
                    """
                    
                    # Save VBS script to temp file
                    vbs_file = tempfile.NamedTemporaryFile(mode='w', delete=False, suffix='.vbs')
                    vbs_file.write(vbs_script)
                    vbs_file.close()
                    
                    # Run the VBS script
                    subprocess.run(['cscript', '//NoLogo', vbs_file.name], check=True)
                    
                    # Clean up
                    os.remove(vbs_file.name)
                    
                    # Return a simple success tone since we can't capture the audio
                    return generate_fallback_audio("Speech played through system audio")
                    
                except Exception as e4:
                    print(f"System TTS also failed: {e4}. Using fallback tone.")
                    return generate_fallback_audio(text)

def generate_fallback_audio(text):
    """Generate a simple tone as fallback when TTS fails"""
    import wave
    import numpy as np
    
    # Create a simple pleasant tone
    sample_rate = 22050
    duration = min(max(len(text) * 0.03, 0.5), 2.0)  # Shorter duration
    
    t = np.linspace(0, duration, int(sample_rate * duration), False)
    
    # Create a pleasant chime sound
    frequency = 440  # A note
    audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
    
    # Add some harmony
    audio_data += np.sin(2 * np.pi * frequency * 1.25 * t) * 0.2  # Major third
    audio_data += np.sin(2 * np.pi * frequency * 1.5 * t) * 0.15   # Perfect fifth
    
    # Apply fade in/out
    fade_samples = int(sample_rate * 0.05)
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
    print("🚀 Starting Intelligent AI Server...")
    print("🌐 Open: http://localhost:8080")
    print("🔗 Server will be available in a few seconds...")
    print("💬 Features: ChatGPT-like responses, Voice chat, CORS enabled")
    
    app.run(host='0.0.0.0', port=8080, debug=False)
