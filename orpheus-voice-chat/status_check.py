#!/usr/bin/env python3
"""
Simple system status check for Orpheus Voice Chat
"""

import sys
import os

def check_basic_python():
    """Check basic Python functionality"""
    print("🐍 Python version:", sys.version.split()[0])
    return True

def check_core_dependencies():
    """Check if core dependencies are available"""
    deps = {
        'torch': False,
        'numpy': False, 
        'soundfile': False,
        'melo': False,
        'edge_tts': False,
    }
    
    for dep in deps:
        try:
            __import__(dep)
            deps[dep] = True
            print(f"✅ {dep}")
        except ImportError:
            print(f"❌ {dep}")
    
    return deps

def check_openvoice():
    """Check OpenVoice availability"""
    try:
        import openvoice
        print("✅ OpenVoice package available")
        return True
    except ImportError:
        print("⚠️  OpenVoice not available (will use fallback)")
        return False

def check_checkpoints():
    """Check if OpenVoice checkpoints are available"""
    checkpoint_path = os.path.join("checkpoints", "checkpoints_v2")
    if os.path.exists(checkpoint_path):
        print(f"✅ OpenVoice checkpoints found: {checkpoint_path}")
        return True
    else:
        print(f"❌ OpenVoice checkpoints not found: {checkpoint_path}")
        return False

def main():
    print("🎭 ORPHEUS VOICE CHAT - SYSTEM STATUS CHECK")
    print("=" * 50)
    
    # Basic checks
    print("\n📋 Basic System Check:")
    check_basic_python()
    
    print("\n📦 Dependencies:")
    deps = check_core_dependencies()
    
    print("\n🎤 Voice Systems:")
    openvoice_available = check_openvoice()
    checkpoints_available = check_checkpoints()
    
    print("\n" + "=" * 50)
    print("📊 SYSTEM STATUS:")
    
    # Determine system status
    if openvoice_available and checkpoints_available:
        print("🎉 FULL OPENVOICE SYSTEM READY")
        print("   • Authentic emotional synthesis available")
        print("   • Voice cloning capabilities enabled")
        status = "full"
    elif deps.get('edge_tts', False):
        print("✅ FALLBACK SYSTEM READY") 
        print("   • Edge TTS emotional synthesis available")
        print("   • Basic voice capabilities enabled")
        status = "fallback"
    else:
        print("⚠️  LIMITED SYSTEM")
        print("   • Some dependencies missing")
        print("   • May have reduced functionality")
        status = "limited"
    
    print(f"\n🔧 Current Mode: {status.upper()}")
    
    if status == "fallback":
        print("\n💡 To enable full OpenVoice:")
        print("   1. Install OpenVoice package")
        print("   2. Ensure checkpoints are properly extracted")
        
    return status in ["full", "fallback"]

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
