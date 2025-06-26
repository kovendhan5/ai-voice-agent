"""
Production configuration for Orpheus Voice Chat
Optimized for Cloud Run deployment
"""

import os
from typing import Dict, Any

class Config:
    """Base configuration"""
    
    # Server Configuration
    PORT = int(os.environ.get('PORT', 8080))
    HOST = os.environ.get('HOST', '0.0.0.0')
    DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
    
    # Orpheus TTS Configuration
    ORPHEUS_MODEL_NAME = os.environ.get('ORPHEUS_MODEL_NAME', 'canopylabs/orpheus-tts-0.1-finetune-prod')
    DISABLE_TRANSFORMERS = os.environ.get('DISABLE_TRANSFORMERS', 'true').lower() == 'true'
    
    # Audio Configuration
    SAMPLE_RATE = int(os.environ.get('SAMPLE_RATE', 24000))
    AUDIO_FORMAT = os.environ.get('AUDIO_FORMAT', 'wav')
    
    # Cache Configuration
    MODEL_CACHE_DIR = os.environ.get('MODEL_CACHE_DIR', '.cache/models')
    
    # Logging
    LOG_LEVEL = os.environ.get('LOG_LEVEL', 'INFO')
    
    # Production optimizations
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max request size
    
    @classmethod
    def get_config(cls) -> Dict[str, Any]:
        """Get configuration as dictionary"""
        return {
            'port': cls.PORT,
            'host': cls.HOST,
            'debug': cls.DEBUG,
            'orpheus_model': cls.ORPHEUS_MODEL_NAME,
            'sample_rate': cls.SAMPLE_RATE,
            'audio_format': cls.AUDIO_FORMAT,
            'cache_dir': cls.MODEL_CACHE_DIR,
            'log_level': cls.LOG_LEVEL
        }

class DevelopmentConfig(Config):
    """Development configuration"""
    DEBUG = True
    PORT = 8080

class ProductionConfig(Config):
    """Production configuration"""
    DEBUG = False
    # Use environment PORT for Cloud Run
    PORT = int(os.environ.get('PORT', 8080))

# Configuration mapping
config_map = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}

def get_config(env: str = None) -> Config:
    """Get configuration based on environment"""
    if env is None:
        env = os.environ.get('FLASK_ENV', 'default')
    return config_map.get(env, DevelopmentConfig)
