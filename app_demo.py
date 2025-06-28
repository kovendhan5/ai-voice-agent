"""
Orpheus TTS API - Lightweight text-to-speech API
Designed for deployment on GCP Cloud Run
"""
from flask import Flask, request, jsonify, send_file
import os
import tempfile
import wave
import numpy as np
from datetime import datetime

app = Flask(__name__)

# Configuration
MODEL_NAME = os.getenv('MODEL_NAME', 'canopylabs/orpheus-tts-0.1-finetune-prod')
PORT = int(os.getenv('PORT', 8080))

# Available voices
VOICES = {
    "tara": {"id": "tara", "name": "Tara", "gender": "female"},
    "alex": {"id": "alex", "name": "Alex", "gender": "male"},
    "sarah": {"id": "sarah", "name": "Sarah", "gender": "female"}
}

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

@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        "status": "healthy",
        "service": "Orpheus TTS API",
        "model": MODEL_NAME,
        "timestamp": datetime.now().isoformat(),
        "version": "0.1.0"
    })

@app.route('/voices', methods=['GET'])
def list_voices():
    """List available voices"""
    return jsonify({
        "voices": list(VOICES.values())
    })

@app.route('/speak', methods=['POST'])
def generate_speech():
    """Generate speech from text input"""
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

@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "Endpoint not found"}), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500

if __name__ == '__main__':
    print(f"🎤 Starting Orpheus TTS API...")
    print(f"📡 Model: {MODEL_NAME}")
    print(f"🔊 Available voices: {list(VOICES.keys())}")
    print(f"🌐 Server: http://localhost:{PORT}")
    print(f"📚 Endpoints:")
    print(f"   GET  / - Health check")
    print(f"   GET  /voices - List voices")
    print(f"   POST /speak - Generate speech")
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
