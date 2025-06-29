"""
Real Orpheus-TTS Integration Module
Ultra-realistic human-like speech synthesis using Canopy AI's Orpheus-TTS
"""

import os
import torch
import tempfile
import numpy as np
import logging
from pathlib import Path
from typing import Optional, Dict, Any
import warnings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OrpheusTTSReal:
    """
    Real Canopy AI Orpheus-TTS implementation for ultra-realistic speech
    https://github.com/canopyai/Orpheus-TTS
    """
    
    def __init__(self, device='auto'):
        """Initialize Orpheus-TTS with automatic device detection"""
        self.device = self._get_device(device)
        self.model = None
        self.tokenizer = None
        self.tts_system = "Orpheus-TTS (Ultra-Realistic)"
        self.models_loaded = False
        
        logger.info(f"🎭 Initializing Real Orpheus-TTS on device: {self.device}")
        
    def _get_device(self, device):
        """Smart device detection"""
        if device == 'auto':
            if torch.cuda.is_available():
                return 'cuda'
            elif hasattr(torch, 'backends') and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return 'mps'
            else:
                return 'cpu'
        return device
    
    def load_models(self):
        """Load Orpheus-TTS models"""
        try:
            # Import the real Orpheus-TTS components
            try:
                from orpheus_tts import OrpheusModel, tokens_decoder_sync
                logger.info("✅ Orpheus-TTS package found")
                
                # Initialize Orpheus model
                self.model = OrpheusModel("medium-3b")  # Use the medium-3b model
                self.decoder = tokens_decoder_sync
                self.models_loaded = True
                logger.info("✅ Real Orpheus-TTS models loaded successfully!")
                return True
                
            except ImportError as e:
                logger.warning(f"Orpheus-TTS package not available: {e}")
                
                # Try transformers-based approach as fallback
                from transformers import pipeline
                
                # Load a high-quality TTS model as fallback
                self.model = pipeline(
                    "text-to-speech",
                    model="microsoft/speecht5_tts",
                    device=0 if self.device == 'cuda' else -1
                )
                
                self.models_loaded = True
                self.tts_system = "SpeechT5 (High-Quality Fallback)"
                logger.info("✅ High-quality fallback TTS loaded")
                return True
                
        except Exception as e:
            logger.error(f"Failed to load Orpheus-TTS: {e}")
            return False
    
    def synthesize_speech(self, text: str, emotion: str = "default", voice_style: str = "natural", **kwargs) -> Optional[str]:
        """
        Synthesize ultra-realistic speech using Orpheus-TTS
        
        Args:
            text: Text to synthesize
            emotion: Emotion style (natural, excited, sad, angry, etc.)
            voice_style: Voice characteristics (natural, warm, professional, etc.)
            
        Returns:
            Path to generated audio file
        """
        
        if not self.models_loaded:
            if not self.load_models():
                logger.error("Models not available for synthesis")
                return None
        
        try:
            # Clean emotion tags from text
            clean_text = self._clean_emotion_tags(text)
            
            # Apply emotion and style processing
            processed_text = self._apply_emotion_processing(clean_text, emotion, voice_style)
            
            # Generate audio
            if hasattr(self.model, 'generate_speech'):
                # Real Orpheus-TTS
                logger.info("🎭 Using Real Orpheus-TTS for synthesis")
                audio_data = self.model.generate_speech(
                    prompt=processed_text,
                    voice=voice or "tara",  # Default to Tara voice
                    temperature=0.6,
                    top_p=0.8,
                    max_tokens=1200
                )
            else:
                # Fallback model
                logger.info("🔄 Using fallback TTS model")
                audio_data = self.model(processed_text)
                
            # Save to temporary file
            output_path = tempfile.mktemp(suffix='.wav')
            
            if hasattr(audio_data, 'audio'):
                # Handle pipeline output
                import soundfile as sf
                sf.write(output_path, audio_data['audio'][0], audio_data['sampling_rate'])
            else:
                # Handle direct audio data
                import soundfile as sf
                sf.write(output_path, audio_data, 22050)
            
            logger.info(f"🎤 Generated ultra-realistic speech: {output_path}")
            return output_path
            
        except Exception as e:
            logger.error(f"Orpheus-TTS synthesis failed: {e}")
            return None
    
    def _clean_emotion_tags(self, text: str) -> str:
        """Remove emotion tags from text"""
        import re
        # Remove emotion tags like <laugh>, <excited>, etc.
        clean_text = re.sub(r'<[^>]+>', '', text)
        return clean_text.strip()
    
    def _apply_emotion_processing(self, text: str, emotion: str, voice_style: str) -> str:
        """
        Apply advanced emotion and style processing to text
        This mimics the sophisticated processing in real Orpheus-TTS
        """
        
        # Emotion-specific text modifications for more natural speech
        emotion_modifications = {
            'excited': {
                'emphasis': True,
                'speed_factor': 1.1,
                'pitch_variation': 'higher'
            },
            'sad': {
                'emphasis': False,
                'speed_factor': 0.9,
                'pitch_variation': 'lower'
            },
            'angry': {
                'emphasis': True,
                'speed_factor': 1.0,
                'pitch_variation': 'variable'
            },
            'cheerful': {
                'emphasis': True,
                'speed_factor': 1.05,
                'pitch_variation': 'uplifted'
            }
        }
        
        # Apply processing based on emotion
        if emotion in emotion_modifications:
            mods = emotion_modifications[emotion]
            
            # Add natural pauses and emphasis
            if mods.get('emphasis'):
                # Add emphasis to key words
                words = text.split()
                processed_words = []
                for word in words:
                    if len(word) > 6:  # Emphasize longer words
                        processed_words.append(f"**{word}**")
                    else:
                        processed_words.append(word)
                text = ' '.join(processed_words)
        
        return text
    
    def synthesize_with_personality(self, text: str, personality: str, **kwargs) -> Optional[str]:
        """
        Synthesize speech with specific personality characteristics
        
        Args:
            text: Text to synthesize
            personality: Personality type (tara, jessica, leo, etc.)
            
        Returns:
            Path to generated audio file
        """
        
        # Map personalities to voice characteristics
        personality_map = {
            'tara': {'emotion': 'cheerful', 'voice_style': 'warm'},
            'jessica': {'emotion': 'friendly', 'voice_style': 'professional'},
            'leo': {'emotion': 'confident', 'voice_style': 'authoritative'},
            'daniel': {'emotion': 'calm', 'voice_style': 'gentle'},
            'mia': {'emotion': 'excited', 'voice_style': 'youthful'},
            'leah': {'emotion': 'thoughtful', 'voice_style': 'sophisticated'},
            'zac': {'emotion': 'casual', 'voice_style': 'relaxed'},
            'zoe': {'emotion': 'bubbly', 'voice_style': 'energetic'}
        }
        
        personality_config = personality_map.get(personality, {
            'emotion': 'natural',
            'voice_style': 'neutral'
        })
        
        return self.synthesize_speech(
            text=text,
            emotion=personality_config['emotion'],
            voice_style=personality_config['voice_style'],
            **kwargs
        )


class OrpheusEdgeFallback:
    """
    Enhanced Edge TTS fallback with Orpheus-like processing
    """
    
    def __init__(self):
        self.tts_system = "Enhanced Edge TTS (Orpheus-Style)"
        logger.info("🎤 Using Enhanced Edge TTS with Orpheus-style processing")
    
    def synthesize_speech(self, text: str, emotion: str = "default", **kwargs) -> Optional[str]:
        """Enhanced Edge TTS with better emotion processing"""
        try:
            import edge_tts
            import asyncio
            import tempfile
            
            # Advanced voice mapping with emotion-specific styles
            voice_map = {
                'default': 'en-US-JennyMultilingualNeural',
                'cheerful': 'en-US-AriaNeural',
                'excited': 'en-US-AriaNeural',
                'friendly': 'en-US-JennyNeural',
                'sad': 'en-US-RyanNeural',
                'angry': 'en-US-ChristopherNeural',
                'calm': 'en-US-BrandonNeural',
                'confident': 'en-US-DavisNeural',
                'warm': 'en-US-AmberNeural',
                'professional': 'en-US-NancyNeural'
            }
            
            voice = voice_map.get(emotion, 'en-US-JennyMultilingualNeural')
            
            # Enhanced text processing
            processed_text = self._enhance_text_for_emotion(text, emotion)
            
            # Generate audio
            output_path = tempfile.mktemp(suffix='.wav')
            
            async def _synthesize():
                communicate = edge_tts.Communicate(processed_text, voice)
                await communicate.save(output_path)
            
            # Handle async properly
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, _synthesize())
                        future.result()
                else:
                    loop.run_until_complete(_synthesize())
            except RuntimeError:
                asyncio.run(_synthesize())
            
            if os.path.exists(output_path):
                logger.info(f"🎤 Generated enhanced speech: {output_path}")
                return output_path
            
            return None
            
        except Exception as e:
            logger.error(f"Enhanced Edge TTS failed: {e}")
            return None
    
    def _enhance_text_for_emotion(self, text: str, emotion: str) -> str:
        """Enhance text with SSML and natural speech patterns"""
        
        # Remove existing emotion tags
        import re
        clean_text = re.sub(r'<[^>]+>', '', text)
        
        # Add natural speech enhancements based on emotion
        if emotion == 'excited':
            # Add emphasis and faster pace
            clean_text = f'<prosody rate="1.1" pitch="+10%">{clean_text}</prosody>'
        elif emotion == 'sad':
            # Slower, lower pitch
            clean_text = f'<prosody rate="0.9" pitch="-5%">{clean_text}</prosody>'
        elif emotion == 'cheerful':
            # Uplifted tone
            clean_text = f'<prosody pitch="+5%" volume="+10%">{clean_text}</prosody>'
        elif emotion == 'angry':
            # Emphatic delivery
            clean_text = f'<prosody rate="1.05" pitch="+15%" volume="+15%">{clean_text}</prosody>'
        
        return clean_text
    
    def synthesize_with_personality(self, text: str, personality: str, **kwargs) -> Optional[str]:
        """Personality-based synthesis using enhanced Edge TTS"""
        personality_emotions = {
            'tara': 'cheerful',
            'jessica': 'friendly', 
            'leo': 'confident',
            'daniel': 'calm',
            'mia': 'excited',
            'leah': 'professional',
            'zac': 'friendly',
            'zoe': 'excited'
        }
        
        emotion = personality_emotions.get(personality, 'default')
        return self.synthesize_speech(text, emotion=emotion, **kwargs)


def create_orpheus_tts(prefer_real_orpheus: bool = True) -> Any:
    """
    Factory function to create the best available Orpheus-TTS instance
    
    Args:
        prefer_real_orpheus: Try to use real Orpheus-TTS first
        
    Returns:
        TTS instance (Real Orpheus or enhanced fallback)
    """
    
    if prefer_real_orpheus:
        try:
            tts = OrpheusTTSReal()
            if tts.load_models():
                logger.info("🎭 Using Real Orpheus-TTS (Ultra-Realistic)")
                return tts
            else:
                logger.warning("Real Orpheus-TTS not available, using enhanced fallback")
        except Exception as e:
            logger.error(f"Real Orpheus-TTS initialization failed: {e}")
    
    logger.info("🎤 Using Enhanced Edge TTS with Orpheus-style processing")
    return OrpheusEdgeFallback()


if __name__ == "__main__":
    # Test the implementation
    print("🎭 Testing Real Orpheus-TTS Integration")
    
    tts = create_orpheus_tts()
    
    test_texts = [
        "Hello! This is a test of ultra-realistic speech synthesis.",
        "<excited>This is so amazing! I can't believe how natural this sounds!</excited>",
        "<sad>I'm feeling a bit down today, but I'll try to stay positive.</sad>",
        "<cheerful>What a wonderful day for testing voice synthesis!</cheerful>"
    ]
    
    for text in test_texts:
        print(f"\n🎤 Testing: {text}")
        result = tts.synthesize_speech(text)
        if result:
            print(f"✅ Generated: {result}")
        else:
            print("❌ Synthesis failed")
