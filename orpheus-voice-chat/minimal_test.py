#!/usr/bin/env python3
"""
Minimal test of voice synthesis components
"""

print("🎭 MINIMAL VOICE SYNTHESIS TEST")
print("=" * 40)

# Test 1: Basic imports
print("\n1️⃣ Testing basic imports...")
try:
    import torch
    print(f"✅ PyTorch {torch.__version__}")
except Exception as e:
    print(f"❌ PyTorch: {e}")

try:
    import numpy as np
    print(f"✅ NumPy {np.__version__}")
except Exception as e:
    print(f"❌ NumPy: {e}")

# Test 2: MeloTTS
print("\n2️⃣ Testing MeloTTS...")
try:
    import melo
    print("✅ MeloTTS available")
    
    # Try to create a simple TTS instance
    from melo.api import TTS
    print("✅ MeloTTS API accessible")
    
except Exception as e:
    print(f"❌ MeloTTS: {e}")

# Test 3: Edge TTS fallback
print("\n3️⃣ Testing Edge TTS...")
try:
    import edge_tts
    print("✅ Edge TTS available")
except Exception as e:
    print(f"❌ Edge TTS: {e}")

# Test 4: OpenVoice
print("\n4️⃣ Testing OpenVoice...")
try:
    import openvoice
    print("✅ OpenVoice package found")
    
    try:
        from openvoice.api import BaseSpeakerTTS
        print("✅ OpenVoice API accessible")
    except Exception as e:
        print(f"⚠️  OpenVoice API issue: {e}")
        
except Exception as e:
    print(f"❌ OpenVoice: {e}")

print("\n" + "=" * 40)
print("📊 SUMMARY:")
print("This test helps identify which voice synthesis options are available.")
print("The system will automatically use the best available option.")
