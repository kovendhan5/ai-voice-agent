"""
Minimal working Flask server for testing
"""

from flask import Flask, request, send_file, jsonify
import tempfile
import os

# Import our TTS mock
from orpheus_tts import OrpheusModel

# Create Flask app
app = Flask(__name__)

# Initialize model
print("Loading TTS model...")
model = OrpheusModel()
print("Model loaded!")

@app.route('/')
def health():
    return jsonify({"status": "healthy", "message": "Server is running!"})

@app.route('/speak', methods=['POST'])
def speak():
    try:
        data = request.get_json()
        text = data.get('text', 'tara: Hello world')
        voice = data.get('voice', 'tara')
        
        print(f"Generating speech: {text}")
        
        # Generate audio
        chunks = model.generate_speech(text, voice)
        
        # Save to temp file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as f:
            for chunk in chunks:
                f.write(chunk)
            temp_path = f.name
        
        return send_file(temp_path, mimetype='audio/wav', as_attachment=True, download_name='speech.wav')
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    print("🚀 Starting Orpheus TTS Server...")
    print("🌐 Server will be available at: http://localhost:8080")
    print("📋 Endpoints:")
    print("   GET  /       - Health check")
    print("   POST /speak  - Generate speech")
    print("🔄 Starting server...")
    
    app.run(host='0.0.0.0', port=8080, debug=True)
