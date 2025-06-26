# OpenVoice/Orpheus TTS Integration

## Overview

This project now includes **real OpenVoice/Orpheus TTS** integration for authentic emotional speech synthesis. The system automatically detects whether OpenVoice is available and falls back to Edge TTS when needed.

## Features

### ✅ Real OpenVoice Integration
- **Authentic emotional synthesis** with human-like expressions
- **Realistic laughter, sighs, and emotional expressions**
- **Advanced voice cloning capabilities**
- **Low-latency real-time generation**

### ✅ Emotion Styles Available
The real OpenVoice system supports these emotion styles:
- `default` - Natural conversation tone
- `whispering` - Soft, intimate speech
- `cheerful` - Happy, upbeat expression
- `terrified` - Fearful, scared expression
- `angry` - Intense, upset expression
- `sad` - Melancholic, sorrowful tone
- `friendly` - Warm, welcoming expression

### ✅ Emotion Tag Processing
The system automatically processes emotion tags in AI responses:
```
"Hello! <laugh> This is so exciting! <cheerful> How are you doing?"
```

These tags are converted to actual emotional expressions in the generated speech.

## Installation

### Quick Setup (Windows)
```bash
# Run the automated installation script
scripts\install_openvoice.bat
```

### Manual Setup

1. **Install OpenVoice Dependencies**
```bash
pip install torch torchaudio librosa soundfile numpy scipy
pip install matplotlib Pillow inflect phonemizer Unidecode
pip install cn2an pypinyin jieba langid-py gradio
```

2. **Install OpenVoice**
```bash
pip install git+https://github.com/myshell-ai/OpenVoice.git
```

3. **Install MeloTTS (for multi-lingual support)**
```bash
pip install git+https://github.com/myshell-ai/MeloTTS.git
python -m unidic download
```

4. **Download Checkpoints**
```bash
python scripts/setup_openvoice.py
```

Or manually download from:
- [OpenVoice V2 Checkpoints](https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip)
- Extract to `./checkpoints/checkpoints_v2/`

## Usage

### Automatic System Selection
The system automatically chooses the best available TTS:

```python
# Initialize with automatic detection
from openvoice_integration import create_orpheus_tts

tts = create_orpheus_tts(prefer_openvoice=True)
audio_path = tts.synthesize_speech(
    text="Hello! <laugh> This is amazing!",
    emotion="cheerful"
)
```

### System Status
Check which TTS system is active:
```bash
curl http://localhost:5000/system-status
```

Response:
```json
{
  "tts_system": "openvoice",
  "openvoice_available": true,
  "models_loaded": true,
  "system_info": {
    "real_orpheus": true,
    "edge_tts_fallback": false,
    "emotion_synthesis": "authentic",
    "available_emotions": ["default", "whispering", "cheerful", "terrified", "angry", "sad", "friendly"]
  }
}
```

## Architecture

### TTS System Hierarchy
1. **Primary**: Real OpenVoice/Orpheus TTS
   - Authentic emotional synthesis
   - Human-like expressions
   - Advanced voice cloning

2. **Fallback**: Edge TTS
   - Basic emotion simulation
   - Reliable cloud-based synthesis
   - Good quality but limited emotions

3. **Emergency**: pyttsx3
   - Local system TTS
   - Basic functionality only

### Emotion Processing Pipeline
1. **Text Analysis**: Detect emotion tags in AI responses
2. **Emotion Mapping**: Map tags to OpenVoice emotion styles
3. **Speech Synthesis**: Generate audio with authentic emotions
4. **Voice Cloning**: Apply personality-specific voice characteristics

## Personality-Emotion Mapping

Each AI personality has specific emotional tendencies:

| Personality | Primary Emotion | Style |
|-------------|----------------|-------|
| Tara | Cheerful | Warm, empathetic |
| Jessica | Excited | Bubbly, energetic |
| Leo | Friendly | Thoughtful, wise |
| Daniel | Default | Casual, relatable |
| Mia | Cheerful | Creative, artistic |
| Leah | Friendly | Gentle, caring |
| Zachary | Default | Tech-savvy, modern |
| Zoe | Excited | Witty, sophisticated |

## Advanced Features

### Voice Cloning
```python
# Use reference speaker for voice cloning
audio_path = tts.synthesize_speech(
    text="Clone my voice!",
    reference_speaker="path/to/reference.wav"
)
```

### Multi-Language Support
OpenVoice supports multiple languages:
- English (American, British, Indian, Australian)
- Spanish
- French
- Chinese
- Japanese
- Korean

### Custom Emotions
Add custom emotion processing:
```python
# In openvoice_integration.py
EMOTION_STYLES = {
    'excited': 'cheerful',
    'nervous': 'whispering',
    'confident': 'default',
    # Add more mappings
}
```

## Cloud Deployment

### Google Cloud Run
The system is optimized for cloud deployment:

1. **Dockerfile** includes OpenVoice dependencies
2. **Fallback system** ensures reliability
3. **Resource optimization** for cloud constraints

### Environment Variables
```bash
# Optional: Force fallback to Edge TTS
FORCE_EDGE_TTS=true

# Optional: OpenVoice model path
OPENVOICE_CHECKPOINTS=/app/checkpoints
```

## Troubleshooting

### OpenVoice Not Loading
```
⚠️ Using Edge TTS fallback (OpenVoice models not available)
```

**Solutions:**
1. Run `scripts/setup_openvoice.py`
2. Download checkpoints manually
3. Check CUDA/PyTorch installation
4. Verify checkpoint file paths

### Memory Issues
```
CUDA out of memory
```

**Solutions:**
1. Use CPU mode: `device='cpu'`
2. Reduce batch size
3. Clear audio cache regularly

### Audio Quality Issues
```
Audio generation failed
```

**Solutions:**
1. Check text length (max ~200 characters)
2. Verify emotion tags are valid
3. Test with simple text first
4. Check available disk space

## Performance Metrics

### OpenVoice vs Edge TTS

| Feature | OpenVoice | Edge TTS |
|---------|-----------|----------|
| Emotion Quality | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ |
| Generation Speed | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Voice Cloning | ⭐⭐⭐⭐⭐ | ❌ |
| Resource Usage | ⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| Offline Support | ⭐⭐⭐⭐⭐ | ❌ |
| Multi-Language | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ |

## Development

### Adding New Emotions
1. Update `EMOTION_STYLES` mapping
2. Test with OpenVoice base speakers
3. Add fallback for Edge TTS
4. Update documentation

### Custom Voice Training
1. Prepare reference audio samples
2. Extract speaker embeddings
3. Fine-tune tone color converter
4. Integrate with personality system

## Future Enhancements

- [ ] Real-time voice conversion
- [ ] Custom emotion training
- [ ] Multi-speaker conversations
- [ ] Advanced prosody control
- [ ] GPU optimization for cloud
- [ ] WebRTC integration
- [ ] Voice activity detection

## Credits

Based on:
- [OpenVoice](https://github.com/myshell-ai/OpenVoice) - MIT License
- [MeloTTS](https://github.com/myshell-ai/MeloTTS) - Multi-lingual TTS
- [Microsoft Edge TTS](https://github.com/rany2/edge-tts) - Fallback system
