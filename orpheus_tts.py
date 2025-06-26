"""
Mock implementation of Orpheus TTS for testing purposes.
This simulates the behavior of the actual orpheus_tts package.
"""

import wave
import numpy as np
import io
import time


class OrpheusModel:
    """Mock Orpheus TTS model for testing"""
    
    def __init__(self, model_name="canopylabs/orpheus-tts-0.1-finetune-prod"):
        self.model_name = model_name
        print(f"Mock: Loading Orpheus model {model_name}")
        # Simulate model loading time
        time.sleep(2)
        print("Mock: Model loaded successfully!")
    
    def generate_speech(self, prompt="Hello world", voice="tara"):
        """
        Generate mock speech audio data
        Returns audio chunks as bytes
        """
        print(f"Mock: Generating speech for prompt: '{prompt}' with voice: '{voice}'")
        
        # Simulate processing time
        time.sleep(1)
        
        # Generate a simple sine wave as mock audio
        sample_rate = 22050
        duration = 2.0  # 2 seconds
        frequency = 440  # A4 note
        
        # Generate sine wave
        t = np.linspace(0, duration, int(sample_rate * duration), False)
        audio_data = np.sin(2 * np.pi * frequency * t) * 0.3
        
        # Add some variation based on voice
        if voice == "alex":
            audio_data = audio_data * 0.8  # Quieter
        elif voice == "sarah":
            audio_data = audio_data * 1.2  # Louder
            
        # Convert to 16-bit PCM
        audio_data = (audio_data * 32767).astype(np.int16)
        
        # Create WAV file in memory
        wav_buffer = io.BytesIO()
        with wave.open(wav_buffer, 'wb') as wav_file:
            wav_file.setnchannels(1)  # Mono
            wav_file.setsampwidth(2)  # 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(audio_data.tobytes())
        
        # Return as chunks (simulating streaming)
        wav_buffer.seek(0)
        chunk_size = 1024
        chunks = []
        while True:
            chunk = wav_buffer.read(chunk_size)
            if not chunk:
                break
            chunks.append(chunk)
        
        print(f"Mock: Generated {len(chunks)} audio chunks")
        return chunks
