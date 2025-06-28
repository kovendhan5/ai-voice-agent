from flask import Flask, request, send_file, jsonify
import os
import tempfile
from orpheus_tts import OrpheusModel
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Initialize the model (this might take some time on first load)
logger.info("Loading Orpheus TTS model...")
try:
    model = OrpheusModel(model_name="canopylabs/orpheus-tts-0.1-finetune-prod")
    logger.info("Model loaded successfully!")
except Exception as e:
    logger.error(f"Failed to load model: {e}")
    model = None

@app.route("/", methods=["GET"])
def health_check():
    """Health check endpoint"""
    if model is None:
        return jsonify({"status": "error", "message": "Model not loaded"}), 500
    return jsonify({"status": "healthy", "message": "Orpheus TTS API is running"})

@app.route("/speak", methods=["POST"])
def speak():
    """Generate speech from text input"""
    try:
        if model is None:
            return jsonify({"error": "Model not loaded"}), 500
        
        # Get text from request
        data = request.get_json()
        if not data or "text" not in data:
            return jsonify({"error": "Missing 'text' field in request body"}), 400
        
        prompt = data.get("text", "tara: Hello from Orpheus!")
        voice = data.get("voice", "tara")  # Allow voice selection
        
        logger.info(f"Generating speech for: {prompt[:50]}...")
        
        # Generate speech
        audio_chunks = model.generate_speech(prompt=prompt, voice=voice)
        
        # Create temporary file to store audio
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as temp_file:
            for chunk in audio_chunks:
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        logger.info("Speech generation completed")
        
        # Return the audio file and clean up after sending
        def remove_file(response):
            try:
                os.unlink(temp_file_path)
            except Exception:
                pass
            return response
        
        return send_file(
            temp_file_path, 
            mimetype="audio/wav",
            as_attachment=True,
            download_name="speech.wav"
        )
    
    except Exception as e:
        logger.error(f"Error generating speech: {e}")
        return jsonify({"error": str(e)}), 500

@app.route("/voices", methods=["GET"])
def list_voices():
    """List available voices"""
    # This is a placeholder - update with actual available voices from Orpheus
    voices = ["tara", "alex", "sarah"]  # Update based on actual Orpheus voices
    return jsonify({"voices": voices})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port, debug=False)
