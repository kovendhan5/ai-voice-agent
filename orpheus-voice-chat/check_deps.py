#!/usr/bin/env python3
"""Simple test to check OpenVoice availability"""

print("🔍 Checking OpenVoice Dependencies...")

try:
    import openvoice
    print("✅ OpenVoice package available")
    
    try:
        from openvoice import se_extractor
        from openvoice.api import BaseSpeakerTTS, ToneColorConverter
        print("✅ OpenVoice API modules available")
    except ImportError as e:
        print(f"❌ OpenVoice API modules not available: {e}")
        
except ImportError as e:
    print(f"❌ OpenVoice package not available: {e}")

# Test MeloTTS
try:
    import melo
    print("✅ MeloTTS available")
except ImportError as e:
    print(f"❌ MeloTTS not available: {e}")

# Test other dependencies
try:
    import torch
    print(f"✅ PyTorch {torch.__version__}")
except ImportError:
    print("❌ PyTorch not available")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except ImportError:
    print("❌ NumPy not available")

print("\n🔧 Status Summary:")
print("Dependencies installed, checking if OpenVoice package needs manual installation...")
