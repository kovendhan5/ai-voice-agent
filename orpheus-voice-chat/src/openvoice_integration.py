"""
OpenVoice/Orpheus TTS Integration Module
Real emotional speech synthesis with authentic voice cloning
"""

import os
import torch
import tempfile
import numpy as np
import soundfile as sf
from pathlib import Path
import logging
from typing import Optional, Dict, Any
import re

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OpenVoiceOrpheusTTS:
    """
    Real OpenVoice/Orpheus TTS implementation with authentic emotional synthesis
    Based on myshell-ai/OpenVoice repository
    """
    
    # Available emotion styles from actual OpenVoice implementation
    EMOTION_STYLES = {
        'default': 'default',
        'whispering': 'whispering', 
        'cheerful': 'cheerful',
        'excited': 'cheerful',  # Map to cheerful for now
        'sad': 'sad',
        'angry': 'angry', 
        'terrified': 'terrified',
        'shouting': 'angry',  # Map to angry for intensity
        'friendly': 'friendly',
        'laugh': 'cheerful',
        'chuckle': 'cheerful',
    }
    
    def __init__(self, device='auto'):
        """Initialize OpenVoice with automatic device detection"""
        self.device = self._get_device(device)
        self.models_loaded = False
        self.base_speaker_tts = None
        self.tone_color_converter = None
        self.source_se = None
        self.checkpoints_dir = self._setup_checkpoints_dir()
        
        logger.info(f"OpenVoice initialized on device: {self.device}")
        
    def _get_device(self, device):
        """Smart device detection with fallback"""
        if device == 'auto':
            if torch.cuda.is_available():
                return 'cuda'
            elif hasattr(torch, 'backends') and hasattr(torch.backends, 'mps') and torch.backends.mps.is_available():
                return 'mps'
            else:
                return 'cpu'
        return device
    
    def _setup_checkpoints_dir(self):
        """Setup checkpoints directory structure"""
        base_dir = Path(__file__).parent.parent / 'checkpoints'
        base_dir.mkdir(exist_ok=True)
        return base_dir
    
    def _download_checkpoints(self):
        """Download OpenVoice checkpoints if not present"""
        checkpoint_urls = {
            'v1': 'https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip',
            'v2': 'https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip'
        }
        
        # Check if checkpoints exist
        v2_dir = self.checkpoints_dir / 'checkpoints_v2'
        if not v2_dir.exists():
            logger.info("Downloading OpenVoice V2 checkpoints...")
            # Implementation would download and extract checkpoints
            # For now, provide instructions
            logger.warning("""
            OpenVoice checkpoints not found. Please download manually:
            1. Download: https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip
            2. Extract to: {self.checkpoints_dir}/checkpoints_v2/
            3. Install MeloTTS: pip install git+https://github.com/myshell-ai/MeloTTS.git
            4. Download unidic: python -m unidic download
            """)
            return False
        return True
    
    def load_models(self):
        """Load OpenVoice models and checkpoints"""
        try:
            # Check for checkpoints
            if not self._download_checkpoints():
                logger.error("Checkpoints not available. Using fallback implementation.")
                return False
                
            # Import OpenVoice modules
            try:
                from openvoice import se_extractor
                from openvoice.api import BaseSpeakerTTS, ToneColorConverter
                logger.info("OpenVoice modules imported successfully")
            except ImportError as e:
                logger.error(f"OpenVoice not installed: {e}")
                return False
            
            # Setup paths
            ckpt_base = self.checkpoints_dir / 'checkpoints_v2' / 'base_speakers' / 'EN'
            ckpt_converter = self.checkpoints_dir / 'checkpoints_v2' / 'converter'
            
            if not ckpt_base.exists() or not ckpt_converter.exists():
                logger.error("Checkpoint directories not found")
                return False
            
            # Load base speaker TTS
            self.base_speaker_tts = BaseSpeakerTTS(
                str(ckpt_base / 'config.json'), 
                device=self.device
            )
            self.base_speaker_tts.load_ckpt(str(ckpt_base / 'checkpoint.pth'))
            
            # Load tone color converter  
            self.tone_color_converter = ToneColorConverter(
                str(ckpt_converter / 'config.json'), 
                device=self.device
            )
            self.tone_color_converter.load_ckpt(str(ckpt_converter / 'checkpoint.pth'))
            
            # Load source speaker embeddings
            self.source_se = torch.load(
                str(ckpt_base / 'en_style_se.pth'), 
                map_location=self.device
            )
            
            self.models_loaded = True
            logger.info("OpenVoice models loaded successfully")
            return True
            
        except Exception as e:
            logger.error(f"Failed to load OpenVoice models: {e}")
            return False
    
    def process_emotion_tags(self, text: str) -> tuple[str, str]:
        """
        Process emotion tags in text and determine appropriate style
        Returns: (cleaned_text, emotion_style)
        """
        # Extract emotion tags
        emotion_pattern = r'<(laugh|chuckle|sigh|gasp|whisper|shout|angry|sad|happy|excited|cheerful|friendly)>'
        emotions_found = re.findall(emotion_pattern, text.lower())
        
        # Clean text of emotion tags
        cleaned_text = re.sub(emotion_pattern, '', text, flags=re.IGNORECASE).strip()
        
        # Determine dominant emotion
        if emotions_found:
            primary_emotion = emotions_found[-1]  # Use last emotion found
            style = self.EMOTION_STYLES.get(primary_emotion, 'default')
        else:
            style = 'default'
            
        return cleaned_text, style
    
    def create_reference_speaker(self, text_sample: str = None) -> str:
        """Create a reference speaker audio for voice cloning"""
        if not text_sample:
            text_sample = "This audio will be used to extract the base speaker tone color embedding."
            
        # Create temporary file for reference audio
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
            
        try:
            # Generate base audio with default style
            self.base_speaker_tts.tts(
                text_sample, 
                temp_path, 
                speaker='default', 
                language='English', 
                speed=1.0
            )
            return temp_path
        except Exception as e:
            logger.error(f"Failed to create reference speaker: {e}")
            return None
    
    def synthesize_speech(self, text: str, emotion: str = 'default', 
                         reference_speaker: str = None, speed: float = 1.0) -> Optional[str]:
        """
        Synthesize speech with emotional expression using real OpenVoice
        
        Args:
            text: Text to synthesize
            emotion: Emotion style for synthesis
            reference_speaker: Path to reference speaker audio for voice cloning
            speed: Speech speed multiplier
            
        Returns:
            Path to generated audio file or None if failed
        """
        if not self.models_loaded:
            if not self.load_models():
                logger.error("Cannot synthesize speech - models not loaded")
                return None
        
        try:
            # Process emotion tags in text
            cleaned_text, detected_emotion = self.process_emotion_tags(text)
            
            # Use detected emotion or provided emotion
            final_emotion = detected_emotion if detected_emotion != 'default' else emotion
            final_style = self.EMOTION_STYLES.get(final_emotion, 'default')
            
            logger.info(f"Synthesizing: '{cleaned_text[:50]}...' with style '{final_style}'")
            
            # Create temporary files
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_src:
                src_path = temp_src.name
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_out:
                output_path = temp_out.name
            
            # Generate base audio with emotional style
            self.base_speaker_tts.tts(
                cleaned_text, 
                src_path, 
                speaker=final_style, 
                language='English', 
                speed=speed
            )
            
            # If reference speaker provided, apply voice cloning
            if reference_speaker and os.path.exists(reference_speaker):
                try:
                    from openvoice import se_extractor
                    
                    # Extract target speaker embedding
                    target_se, _ = se_extractor.get_se(
                        reference_speaker, 
                        self.tone_color_converter, 
                        vad=True
                    )
                    
                    # Apply voice conversion
                    self.tone_color_converter.convert(
                        audio_src_path=src_path,
                        src_se=self.source_se,
                        tgt_se=target_se,
                        output_path=output_path,
                        message="@OrpheusVoice"
                    )
                    
                    # Clean up intermediate file
                    if os.path.exists(src_path):
                        os.unlink(src_path)
                        
                    return output_path
                    
                except Exception as e:
                    logger.warning(f"Voice cloning failed, using base voice: {e}")
                    return src_path
            else:
                return src_path
                
        except Exception as e:
            logger.error(f"Speech synthesis failed: {e}")
            return None
    
    def synthesize_with_personality(self, text: str, personality: str, **kwargs) -> Optional[str]:
        """
        Synthesize speech with personality-specific emotional mapping
        
        Personality emotion mappings:
        - tara: cheerful, friendly
        - jessica: excited, cheerful  
        - leo: friendly, default
        - daniel: default, friendly
        - mia: cheerful, excited
        - leah: friendly, cheerful
        - zachary: default, friendly
        - zoe: excited, cheerful
        """
        personality_emotions = {
            'tara': 'cheerful',
            'jessica': 'excited', 
            'leo': 'friendly',
            'daniel': 'default',
            'mia': 'cheerful',
            'leah': 'friendly', 
            'zachary': 'default',
            'zoe': 'excited'
        }
        
        emotion = personality_emotions.get(personality.lower(), 'default')
        return self.synthesize_speech(text, emotion, **kwargs)
    
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        # Implementation to clean up temporary audio files
        pass
    
    def __del__(self):
        """Cleanup on destruction"""
        try:
            self.cleanup_temp_files()
        except:
            pass


class OpenVoiceFallback:
    """
    Fallback implementation when OpenVoice is not available
    Uses the existing Edge TTS with emotion simulation
    """
    
    def __init__(self):
        logger.warning("Using OpenVoice fallback implementation (Edge TTS)")
        self.models_loaded = True
    
    def load_models(self):
        return True
    
    def synthesize_speech(self, text: str, emotion: str = 'default', **kwargs) -> Optional[str]:
        """Fallback to Edge TTS synthesis"""
        try:
            import edge_tts
            import asyncio
            
            # Map emotions to Edge TTS voices with appropriate styles
            voice_map = {
                'default': 'en-US-JennyNeural',
                'cheerful': 'en-US-AriaNeural',
                'excited': 'en-US-AriaNeural', 
                'friendly': 'en-US-JennyNeural',
                'sad': 'en-US-JennyNeural',
                'angry': 'en-US-JennyNeural',
                'whispering': 'en-US-JennyNeural',
                'terrified': 'en-US-JennyNeural'
            }
            
            voice = voice_map.get(emotion, 'en-US-JennyNeural')
            
            # Create temporary output file
            with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
                output_path = temp_file.name
            
            async def generate_speech():
                communicate = edge_tts.Communicate(text, voice)
                await communicate.save(output_path)
            
            # Run async synthesis
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            loop.run_until_complete(generate_speech())
            loop.close()
            
            return output_path
            
        except Exception as e:
            logger.error(f"Fallback synthesis failed: {e}")
            return None
    
    def synthesize_with_personality(self, text: str, personality: str, **kwargs):
        return self.synthesize_speech(text, 'default', **kwargs)


# Factory function to create appropriate TTS instance
def create_orpheus_tts(prefer_openvoice: bool = True) -> Any:
    """
    Create OpenVoice or fallback TTS instance
    
    Args:
        prefer_openvoice: Try to use real OpenVoice first
        
    Returns:
        TTS instance (OpenVoice or fallback)
    """
    if prefer_openvoice:
        try:
            tts = OpenVoiceOrpheusTTS()
            if tts.load_models():
                logger.info("Using real OpenVoice implementation")
                return tts
            else:
                logger.warning("OpenVoice models not available, using fallback")
        except Exception as e:
            logger.error(f"OpenVoice initialization failed: {e}")
    
    logger.info("Using Edge TTS fallback implementation")
    return OpenVoiceFallback()


if __name__ == "__main__":
    # Test the implementation
    tts = create_orpheus_tts()
    
    test_texts = [
        "Hello! <laugh> This is a test of emotional speech synthesis.",
        "I'm feeling quite <sad> today, but I'll try to stay positive.",
        "<cheerful> What a wonderful day for voice synthesis!",
        "<angry> This better work correctly or I'll be upset!"
    ]
    
    for text in test_texts:
        print(f"Testing: {text}")
        result = tts.synthesize_speech(text)
        if result:
            print(f"Generated audio: {result}")
        else:
            print("Synthesis failed")
        print()
