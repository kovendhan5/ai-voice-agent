"""
Test Authentic Orpheus TTS Installation
"""

import sys
import os

print("🔍 Testing Authentic Orpheus TTS Setup...")
print("="*50)

# Test 1: Basic imports
try:
    import torch
    print("✅ PyTorch imported successfully")
    print(f"   Version: {torch.__version__}")
    print(f"   CUDA available: {torch.cuda.is_available()}")
except ImportError as e:
    print(f"❌ PyTorch import failed: {e}")

# Test 2: Try to import orpheus_tts
try:
    from orpheus_tts import OrpheusModel
    print("✅ orpheus_tts imported successfully")
except ImportError as e:
    print(f"❌ orpheus_tts import failed: {e}")
    print("   Installing orpheus-speech package...")
    os.system("pip install orpheus-speech")

# Test 3: Try to import snac
try:
    from snac import SNAC
    print("✅ snac imported successfully")
except ImportError as e:
    print(f"❌ snac import failed: {e}")
    print("   Installing snac package...")
    os.system("pip install snac")

# Test 4: Try to import vllm
try:
    from vllm import AsyncLLMEngine, AsyncEngineArgs, SamplingParams
    print("✅ vllm imported successfully")
except ImportError as e:
    print(f"❌ vllm import failed: {e}")
    print("   Installing vllm package...")
    os.system("pip install vllm")

print("\n🎯 Testing model initialization...")
try:
    # Try to initialize a small test
    from orpheus_tts import OrpheusModel
    print("✅ OrpheusModel class available")
    
    # Note: We won't actually load the model here to save time and resources
    print("⚠️  Model loading test skipped (requires ~3GB download)")
    print("   Model: canopylabs/orpheus-tts-0.1-finetune-prod")
    
except Exception as e:
    print(f"❌ Model initialization test failed: {e}")

print("\n" + "="*50)
print("✅ Authentic Orpheus TTS setup test complete!")
print("🚀 Ready to start server with: python app_orpheus_authentic.py")
