#!/usr/bin/env python3
"""
OpenVoice Setup Script
Downloads and configures OpenVoice checkpoints and dependencies
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_file(url, destination):
    """Download file with progress indication"""
    try:
        logger.info(f"Downloading: {url}")
        urllib.request.urlretrieve(url, destination)
        logger.info(f"Downloaded: {destination}")
        return True
    except Exception as e:
        logger.error(f"Download failed: {e}")
        return False

def extract_zip(zip_path, extract_to):
    """Extract zip file"""
    try:
        logger.info(f"Extracting: {zip_path}")
        with zipfile.ZipFile(zip_path, 'r') as zip_ref:
            zip_ref.extractall(extract_to)
        logger.info(f"Extracted to: {extract_to}")
        return True
    except Exception as e:
        logger.error(f"Extraction failed: {e}")
        return False

def install_openvoice():
    """Install OpenVoice from GitHub"""
    try:
        logger.info("Installing OpenVoice from GitHub...")
        cmd = [sys.executable, '-m', 'pip', 'install', 'git+https://github.com/myshell-ai/OpenVoice.git']
        subprocess.run(cmd, check=True)
        logger.info("OpenVoice installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"OpenVoice installation failed: {e}")
        return False

def install_melotts():
    """Install MeloTTS"""
    try:
        logger.info("Installing MeloTTS...")
        cmd = [sys.executable, '-m', 'pip', 'install', 'git+https://github.com/myshell-ai/MeloTTS.git']
        subprocess.run(cmd, check=True)
        logger.info("MeloTTS installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"MeloTTS installation failed: {e}")
        return False

def download_unidic():
    """Download unidic for Japanese support"""
    try:
        logger.info("Downloading unidic...")
        cmd = [sys.executable, '-m', 'unidic', 'download']
        subprocess.run(cmd, check=True)
        logger.info("Unidic downloaded successfully")
        return True
    except subprocess.CalledProcessError as e:
        logger.warning(f"Unidic download failed (optional): {e}")
        return False

def setup_openvoice_checkpoints():
    """Download and setup OpenVoice checkpoints"""
    
    # Get project root directory
    project_root = Path(__file__).parent.parent
    checkpoints_dir = project_root / 'checkpoints'
    checkpoints_dir.mkdir(exist_ok=True)
    
    # OpenVoice V2 checkpoints (preferred)
    v2_url = 'https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip'
    v2_zip = checkpoints_dir / 'checkpoints_v2.zip'
    v2_dir = checkpoints_dir / 'checkpoints_v2'
    
    # OpenVoice V1 checkpoints (fallback)
    v1_url = 'https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_1226.zip'
    v1_zip = checkpoints_dir / 'checkpoints_v1.zip'
    v1_dir = checkpoints_dir / 'checkpoints'
    
    success = False
    
    # Try V2 first
    if not v2_dir.exists():
        logger.info("Setting up OpenVoice V2 checkpoints...")
        if download_file(v2_url, v2_zip):
            if extract_zip(v2_zip, checkpoints_dir):
                success = True
                # Clean up zip file
                v2_zip.unlink()
            else:
                logger.error("Failed to extract V2 checkpoints")
        else:
            logger.error("Failed to download V2 checkpoints")
    else:
        logger.info("OpenVoice V2 checkpoints already exist")
        success = True
    
    # Try V1 as fallback
    if not success and not v1_dir.exists():
        logger.info("Trying OpenVoice V1 checkpoints as fallback...")
        if download_file(v1_url, v1_zip):
            if extract_zip(v1_zip, checkpoints_dir):
                success = True
                # Clean up zip file
                v1_zip.unlink()
            else:
                logger.error("Failed to extract V1 checkpoints")
        else:
            logger.error("Failed to download V1 checkpoints")
    
    return success

def verify_installation():
    """Verify OpenVoice installation"""
    try:
        import torch
        logger.info(f"PyTorch version: {torch.__version__}")
        logger.info(f"CUDA available: {torch.cuda.is_available()}")
        
        # Try importing OpenVoice
        try:
            from openvoice.api import BaseSpeakerTTS, ToneColorConverter
            from openvoice import se_extractor
            logger.info("OpenVoice modules imported successfully")
            return True
        except ImportError as e:
            logger.error(f"OpenVoice import failed: {e}")
            return False
            
    except ImportError as e:
        logger.error(f"PyTorch not available: {e}")
        return False

def main():
    """Main setup function"""
    logger.info("Starting OpenVoice setup...")
    
    success = True
    
    # Install OpenVoice
    if not install_openvoice():
        success = False
    
    # Install MeloTTS  
    if not install_melotts():
        success = False
    
    # Download unidic (optional)
    download_unidic()
    
    # Setup checkpoints
    if not setup_openvoice_checkpoints():
        logger.error("Failed to setup checkpoints")
        success = False
    
    # Verify installation
    if not verify_installation():
        logger.error("Installation verification failed")
        success = False
    
    if success:
        logger.info("✅ OpenVoice setup completed successfully!")
        logger.info("You can now use the real OpenVoice/Orpheus TTS system.")
    else:
        logger.error("❌ OpenVoice setup failed. Will use Edge TTS fallback.")
        logger.info("Manual setup instructions:")
        logger.info("1. pip install git+https://github.com/myshell-ai/OpenVoice.git")
        logger.info("2. pip install git+https://github.com/myshell-ai/MeloTTS.git")
        logger.info("3. Download checkpoints from:")
        logger.info("   https://myshell-public-repo-host.s3.amazonaws.com/openvoice/checkpoints_v2_0417.zip")
        logger.info("4. Extract to: ./checkpoints/checkpoints_v2/")
    
    return success

if __name__ == "__main__":
    main()
