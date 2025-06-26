"""
Quick Test - Check if we can start a simple Orpheus server
"""

from flask import Flask, jsonify
from flask_cors import CORS
import sys
import os

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return """
    <html>
    <head>
        <title>🎭 Authentic Orpheus TTS Test</title>
        <style>
            body { font-family: Arial; margin: 40px; background: linear-gradient(135deg, #667eea, #764ba2); color: white; }
            .container { max-width: 800px; margin: 0 auto; text-align: center; }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎭 Authentic Orpheus TTS Test Server</h1>
            <h2>✅ Server is running!</h2>
            <p>This confirms the Flask server can start successfully.</p>
            <p>Next step: Install Orpheus TTS packages and load the real model.</p>
        </div>
    </body>
    </html>
    """

@app.route('/test-imports')
def test_imports():
    results = {}
    
    # Test each import
    try:
        import torch
        results['torch'] = f"✅ Success - Version: {torch.__version__}"
    except ImportError as e:
        results['torch'] = f"❌ Failed: {e}"
    
    try:
        from orpheus_tts import OrpheusModel
        results['orpheus_tts'] = "✅ Success - OrpheusModel available"
    except ImportError as e:
        results['orpheus_tts'] = f"❌ Failed: {e}"
    
    try:
        from snac import SNAC
        results['snac'] = "✅ Success - SNAC available"
    except ImportError as e:
        results['snac'] = f"❌ Failed: {e}"
    
    try:
        from vllm import AsyncLLMEngine
        results['vllm'] = "✅ Success - vLLM available"
    except ImportError as e:
        results['vllm'] = f"❌ Failed: {e}"
    
    return jsonify({
        'test_results': results,
        'status': 'complete',
        'python_version': sys.version
    })

if __name__ == '__main__':
    print("🎯 Starting Orpheus TTS Test Server...")
    print("🌐 Access at: http://localhost:8080")
    print("🔍 Test imports at: http://localhost:8080/test-imports")
    app.run(host='0.0.0.0', port=8080, debug=True)
