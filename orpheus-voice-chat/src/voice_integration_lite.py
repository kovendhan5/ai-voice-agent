"""
Lightweight OpenVoice Integration Module
Loads dependencies only when needed to avoid import issues
"""

import os
import tempfile
from pathlib import Path
import logging
from typing import Optional, Dict, Any
import re

# Configure logging
logger = logging.getLogger(__name__)

class OpenVoiceFallback:
    """
    Lightweight fallback implementation using Edge TTS
    Loads dependencies only when needed
    """
    
    # Available emotion styles
    EMOTION_STYLES = {
        'default': 'default',
        'whispering': 'whispering', 
        'cheerful': 'cheerful',
        'excited': 'excited',
        'sad': 'sad',
        'angry': 'angry', 
        'terrified': 'terrified',
        'shouting': 'shouting',
        'friendly': 'friendly',
        'laugh': 'cheerful',
        'chuckle': 'cheerful',
    }
    
    def __init__(self):
        logger.info("Using OpenVoice fallback implementation (Edge TTS)")
        self.models_loaded = True
        self._edge_tts = None
        self._asyncio = None
    
    def _lazy_import_edge_tts(self):
        """Import edge_tts only when needed"""
        if self._edge_tts is None:
            try:
                import edge_tts
                import asyncio
                self._edge_tts = edge_tts
                self._asyncio = asyncio
                logger.info("Edge TTS loaded successfully")
            except ImportError as e:
                logger.error(f"Failed to import Edge TTS: {e}")
                raise
        return self._edge_tts, self._asyncio
    
    def load_models(self):
        """Models are always 'loaded' for fallback"""
        return True
    
    def process_emotion_tags(self, text: str) -> tuple[str, str]:
        """
        Process emotion tags in text and determine appropriate style
        Returns: (cleaned_text, emotion_style)
        """
        # Extract emotion tags using regex
        emotion_pattern = r'<(\w+)>(.*?)</\1>'
        emotions_found = re.findall(emotion_pattern, text, re.IGNORECASE)
        
        # Clean text by removing emotion tags
        cleaned_text = re.sub(emotion_pattern, r'\2', text, flags=re.IGNORECASE)
        
        # Determine primary emotion
        if emotions_found:
            primary_emotion = emotions_found[0][0].lower()
            emotion_style = self.EMOTION_STYLES.get(primary_emotion, 'default')
            logger.info(f"Detected emotion: {primary_emotion} → {emotion_style}")
        else:
            emotion_style = 'default'
        
        return cleaned_text, emotion_style
    
    def synthesize_speech(self, text: str, emotion: str = 'default', **kwargs) -> Optional[str]:
        """Fallback to Edge TTS synthesis"""
        try:
            edge_tts, asyncio = self._lazy_import_edge_tts()
            
            # Map emotions to Edge TTS voices with appropriate styles
            voice_map = {
                'default': 'en-US-AriaNeural',
                'cheerful': 'en-US-AriaNeural',
                'excited': 'en-US-JennyNeural', 
                'sad': 'en-US-GuyNeural',
                'angry': 'en-US-ChristopherNeural',
                'friendly': 'en-US-AriaNeural',
                'whispering': 'en-US-AriaNeural',
                'terrified': 'en-US-GuyNeural',
                'shouting': 'en-US-ChristopherNeural'
            }
            
            voice = voice_map.get(emotion, 'en-US-AriaNeural')
            
            # Generate speech using Edge TTS
            communicate = edge_tts.Communicate(text, voice)
            
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                tmp_path = tmp_file.name
            
            # Run the async synthesis
            async def synthesize():
                await communicate.save(tmp_path)
            
            # Use existing event loop or create new one
            try:
                loop = asyncio.get_event_loop()
                if loop.is_running():
                    # If loop is running, we need to use a different approach
                    import concurrent.futures
                    with concurrent.futures.ThreadPoolExecutor() as executor:
                        future = executor.submit(asyncio.run, synthesize())
                        future.result()
                else:
                    loop.run_until_complete(synthesize())
            except RuntimeError:
                # Create new event loop
                asyncio.run(synthesize())
            
            logger.info(f"Generated speech with emotion '{emotion}' using voice '{voice}'")
            return tmp_path
            
        except Exception as e:
            logger.error(f"Edge TTS synthesis failed: {e}")
            return None

def get_openvoice_tts():
    """
    Factory function to get the appropriate TTS implementation
    Returns OpenVoice if available, otherwise returns fallback
    """
    try:
        # Try to import OpenVoice (lazy import)
        import openvoice
        from openvoice.api import BaseSpeakerTTS, ToneColorConverter
        
        # If we get here, OpenVoice is available
        logger.info("OpenVoice available - using full implementation")
        # Would return OpenVoiceOrpheusTTS() here when ready
        # For now, return fallback until fully tested
        return OpenVoiceFallback()
        
    except ImportError:
        logger.info("OpenVoice not available - using Edge TTS fallback")
        return OpenVoiceFallback()
