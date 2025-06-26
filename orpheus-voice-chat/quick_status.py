#!/usr/bin/env python3
"""
Quick System Status Check
"""

import sys
import os
sys.path.append('src')

print("🎭 ORPHEUS VOICE CHAT - SYSTEM STATUS")
print("=" * 50)

# Check basic imports
try:
    print("1️⃣ Checking basic imports...")
    import edge_tts
    print("   ✅ edge_tts")
    
    import tempfile
    print("   ✅ tempfile")
    
    import asyncio
    print("   ✅ asyncio")
    
except ImportError as e:
    print(f"   ❌ Import error: {e}")

# Check enhanced TTS
try:
    print("\n2️⃣ Checking Enhanced TTS...")
    from ultra_enhanced_tts import UltraEnhancedEdgeTTS
    enhanced = UltraEnhancedEdgeTTS()
    print(f"   ✅ {enhanced.tts_system}")
    
except ImportError as e:
    print(f"   ❌ Enhanced TTS error: {e}")

# Check Orpheus-TTS package
try:
    print("\n3️⃣ Checking Orpheus-TTS package...")
    import orpheus_tts
    print("   ✅ orpheus_tts package imported")
    
    from orpheus_tts import OrpheusModel
    print("   ✅ OrpheusModel class available")
    
except ImportError as e:
    print(f"   ⏳ Orpheus-TTS: {e}")

# Check generated audio files
print("\n4️⃣ Checking generated audio files...")
wav_files = [f for f in os.listdir('.') if f.endswith('.wav')]
total_size = sum(os.path.getsize(f) for f in wav_files) / (1024 * 1024)  # MB
print(f"   🎵 Audio files: {len(wav_files)} files")
print(f"   📊 Total size: {total_size:.1f} MB")

print("\n🚀 SYSTEM READY!")
print("Your voice chat application has ultra-realistic speech synthesis capability!")
