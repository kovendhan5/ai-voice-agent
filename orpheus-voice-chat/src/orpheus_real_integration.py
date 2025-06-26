"""
Real Orpheus-TTS Integration Module
Ultra-realistic human-like speech synthesis using Canopy AI's Orpheus-TTS
"""

import os
import wave
import time
import tempfile
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import re

# Configure logging
logger = logging.getLogger(__name__)

class OrpheusRealTTS:
    """
    Real Orpheus-TTS implementation using Canopy AI's system
    Provides ultra-realistic human-like speech synthesis
    """
    
    # Available voices from Orpheus-TTS
    ORPHEUS_VOICES = {
        'tara': 'tara',      # Most conversational
        'leah': 'leah', 
        'jess': 'jess',
        'leo': 'leo',
        'dan': 'dan', 
        'mia': 'mia',
        'zac': 'zac',
        'zoe': 'zoe'
    }
    
    # Emotion tags supported by Orpheus-TTS
    EMOTION_TAGS = [
        '<laugh>', '<chuckle>', '<sigh>', '<cough>', 
        '<sniffle>', '<groan>', '<yawn>', '<gasp>'
    ]
    
    def __init__(self, model_name="canopylabs/orpheus-tts-0.1-finetune-prod"):
        """Initialize Orpheus-TTS with the production model"""
        self.model = None
        self.model_name = model_name
        self.tts_system = "Orpheus-TTS (Ultra-Realistic)"
        self.models_loaded = False
        
        logger.info(f"Initializing Orpheus-TTS: {model_name}")
        
    def load_models(self):
        """Load the Orpheus-TTS model"""
        try:
            from orpheus_tts import OrpheusModel
            
            logger.info("Loading Orpheus-TTS model...")
            self.model = OrpheusModel(
                model_name=self.model_name,
                max_model_len=2048
            )
            
            self.models_loaded = True
            logger.info("✅ Orpheus-TTS model loaded successfully!")
            return True
            
        except ImportError as e:
            logger.error(f"Orpheus-TTS not available: {e}")
            return False
        except Exception as e:
            logger.error(f"Failed to load Orpheus-TTS: {e}")
            return False
    
    def process_emotion_tags(self, text: str) -> str:
        """
        Process emotion tags in text for Orpheus-TTS
        Orpheus-TTS uses specific emotion tags like <laugh>, <chuckle>, etc.
        """
        # Map common emotion tags to Orpheus emotion tags
        emotion_mapping = {
            '<excited>': '<laugh>',
            '<happy>': '<chuckle>',
            '<cheerful>': '<chuckle>',
            '<friendly>': '',  # Remove, as base voice is friendly
            '<sad>': '<sigh>',
            '<tired>': '<yawn>',
            '<surprised>': '<gasp>',
            '<disgusted>': '<groan>',
            '<coughing>': '<cough>',
            '<crying>': '<sniffle>'
        }
        
        # Replace mapped emotions
        processed_text = text
        for old_tag, new_tag in emotion_mapping.items():
            processed_text = processed_text.replace(old_tag, new_tag)
        
        # Remove any remaining emotion tags that aren't supported
        # Keep only the supported Orpheus emotion tags
        for tag in self.EMOTION_TAGS:
            # This tag is supported, keep it
            continue
        
        # Remove unsupported emotion tags (like <emotion>text</emotion> format)
        processed_text = re.sub(r'<(\w+)>(.*?)</\1>', r'\2', processed_text)
        
        logger.info(f"Processed emotion tags: '{text}' → '{processed_text}'")
        return processed_text
    
    def synthesize_speech(self, text: str, voice: str = "tara", emotion: str = "default", **kwargs) -> Optional[str]:
        """
        Synthesize speech using Orpheus-TTS
        Returns path to generated audio file
        """
        if not self.models_loaded:
            if not self.load_models():
                logger.error("Orpheus-TTS models not available")
                return None
        
        try:
            # Process emotion tags for Orpheus format
            processed_text = self.process_emotion_tags(text)
            
            # Map voice names
            orpheus_voice = self.ORPHEUS_VOICES.get(voice, 'tara')
            
            # Format prompt for Orpheus-TTS (it expects "name: text" format)
            prompt = f"{orpheus_voice}: {processed_text}"
            
            logger.info(f"🎭 Generating Orpheus speech: {orpheus_voice} - {processed_text[:50]}...")
            
            start_time = time.monotonic()
            
            # Generate speech using Orpheus-TTS
            syn_tokens = self.model.generate_speech(
                prompt=prompt,
                voice=orpheus_voice,
                temperature=0.8,  # For natural variation
                repetition_penalty=1.1,  # Required for stable generation
                top_p=0.9
            )
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                output_path = temp_file.name
            
            # Write audio to file with proper WAV format
            with wave.open(output_path, "wb") as wf:
                wf.setnchannels(1)  # Mono
                wf.setsampwidth(2)  # 16-bit
                wf.setframerate(24000)  # 24kHz sample rate
                
                total_frames = 0
                chunk_counter = 0
                
                # Stream audio chunks and write to file
                for audio_chunk in syn_tokens:
                    chunk_counter += 1
                    frame_count = len(audio_chunk) // (wf.getsampwidth() * wf.getnchannels())
                    total_frames += frame_count
                    wf.writeframes(audio_chunk)
                
                duration = total_frames / wf.getframerate()
            
            end_time = time.monotonic()
            generation_time = end_time - start_time
            
            logger.info(f"✅ Orpheus-TTS generated {duration:.2f}s of audio in {generation_time:.2f}s")
            logger.info(f"   Real-time factor: {duration/generation_time:.2f}x")
            
            return output_path
            
        except Exception as e:
            logger.error(f"Orpheus-TTS synthesis failed: {e}")
            return None
    
    def synthesize_with_personality(self, text: str, personality: str, **kwargs):
        """
        Synthesize speech with specific personality
        Orpheus-TTS has distinct personality voices
        """
        return self.synthesize_speech(text, voice=personality, **kwargs)

class OrpheusEdgeFallback:
    """
    Enhanced Edge TTS fallback that maintains compatibility
    """
    
    def __init__(self):
        self.tts_system = "Edge TTS (Enhanced Fallback)"
        self.models_loaded = True
        logger.info("Using enhanced Edge TTS fallback")
    
    def load_models(self):
        return True
    
    def process_emotion_tags(self, text: str) -> str:
        """Process emotion tags for Edge TTS"""
        # Remove emotion tags for Edge TTS (it doesn't support them)
        processed_text = re.sub(r'<[^>]+>', '', text)
        return processed_text.strip()
    
    def synthesize_speech(self, text: str, voice: str = "tara", emotion: str = "default", **kwargs) -> Optional[str]:
        """Enhanced Edge TTS synthesis"""
        try:
            import edge_tts
            import asyncio
            import tempfile
            
            # Process text
            clean_text = self.process_emotion_tags(text)
            
            # Enhanced voice mapping for Edge TTS
            voice_map = {
                'tara': 'en-US-AriaNeural',
                'leah': 'en-US-JennyNeural', 
                'jess': 'en-US-JaneNeural',
                'leo': 'en-US-GuyNeural',
                'dan': 'en-US-DavisNeural',
                'mia': 'en-US-AmberNeural',
                'zac': 'en-US-BrandonNeural',
                'zoe': 'en-US-AvaMultilingualNeural'
            }
            
            edge_voice = voice_map.get(voice, 'en-US-AriaNeural')
            
            # Generate output file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                output_path = temp_file.name
            
            async def generate():
                communicate = edge_tts.Communicate(clean_text, edge_voice)
                await communicate.save(output_path)
            
            # Run synthesis in new thread to avoid event loop conflicts
            import threading
            result = [None]
            exception = [None]
            
            def run_synthesis():
                try:
                    asyncio.run(generate())
                    result[0] = True
                except Exception as e:
                    exception[0] = e
            
            thread = threading.Thread(target=run_synthesis)
            thread.start()
            thread.join()
            
            if exception[0]:
                raise exception[0]
            
            if os.path.exists(output_path):
                logger.info(f"✅ Enhanced Edge TTS generated audio: {output_path}")
                return output_path
            
            return None
            
        except Exception as e:
            logger.error(f"Enhanced Edge TTS failed: {e}")
            return None
    
    def synthesize_with_personality(self, text: str, personality: str, **kwargs):
        return self.synthesize_speech(text, voice=personality, **kwargs)

def create_orpheus_tts(prefer_real_orpheus: bool = True) -> Any:
    """
    Factory function to create the best available TTS instance
    
    Args:
        prefer_real_orpheus: Try to use real Orpheus-TTS first
        
    Returns:
        TTS instance (Real Orpheus-TTS or enhanced fallback)
    """
    if prefer_real_orpheus:
        try:
            tts = OrpheusRealTTS()
            if tts.load_models():
                logger.info("🎭 Using REAL Orpheus-TTS (Ultra-Realistic)")
                return tts
            else:
                logger.warning("Real Orpheus-TTS not available, using enhanced fallback")
        except Exception as e:
            logger.error(f"Real Orpheus-TTS initialization failed: {e}")
    
    logger.info("Using enhanced Edge TTS fallback")
    return OrpheusEdgeFallback()

if __name__ == "__main__":
    # Test the real Orpheus-TTS implementation
    print("🎭 Testing Real Orpheus-TTS Integration")
    print("=" * 50)
    
    tts = create_orpheus_tts()
    
    test_texts = [
        "Hello! <laugh> This is the real Orpheus-TTS system providing ultra-realistic human speech synthesis.",
        "I'm feeling quite excited today. <chuckle> The quality of this voice is absolutely incredible!",
        "<gasp> Wow, this sounds exactly like a real human speaking naturally.",
        "Let me demonstrate some emotions: <sigh> Sometimes I feel contemplative, <laugh> but mostly I'm amazed by this technology!"
    ]
    
    for i, text in enumerate(test_texts, 1):
        print(f"\n🎤 Test {i}: {text}")
        result = tts.synthesize_speech(text, voice="tara")
        if result:
            print(f"✅ Generated: {result}")
        else:
            print("❌ Synthesis failed")
        print()
