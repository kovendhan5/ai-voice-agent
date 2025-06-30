#!/usr/bin/env python3
"""
🔧 ORPHEUS-TTS INSTALLATION SCRIPT
===================================
Automatically install and verify all dependencies
"""

import subprocess
import sys
import os

def run_command(command, description):
    """Run a command and show progress"""
    print(f"🔄 {description}...")
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ {description} completed")
            return True
        else:
            print(f"❌ {description} failed: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ {description} error: {e}")
        return False

def install_dependencies():
    """Install all required dependencies"""
    print("🔧 ORPHEUS-TTS INSTALLATION")
    print("=" * 40)
    
    # Core dependencies
    dependencies = [
        ("pip install --upgrade pip", "Upgrading pip"),
        ("pip install orpheus-speech", "Installing Orpheus-TTS"),
        ("pip install vllm", "Installing VLLM"),
        ("pip install torch torchaudio", "Installing PyTorch"),
        ("pip install transformers accelerate", "Installing Transformers"),
        ("pip install google-generativeai", "Installing Google AI"),
        ("pip install pygame soundfile", "Installing Audio libraries"),
        ("pip install speech-recognition", "Installing Speech Recognition"),
        ("pip install python-dotenv", "Installing Environment support"),
        ("pip install numpy", "Installing NumPy")
    ]
    
    success_count = 0
    for command, description in dependencies:
        if run_command(command, description):
            success_count += 1
    
    print(f"\n📊 Installation Results: {success_count}/{len(dependencies)} successful")
    
    if success_count == len(dependencies):
        print("🎉 All dependencies installed successfully!")
        return True
    else:
        print("⚠️ Some installations failed - system may still work")
        return False

def verify_installation():
    """Verify that everything is working"""
    print("\n🧪 VERIFYING INSTALLATION")
    print("=" * 30)
    
    tests = [
        ("import torch", "PyTorch"),
        ("import transformers", "Transformers"),
        ("from orpheus_tts import OrpheusModel", "Orpheus-TTS"),
        ("import google.generativeai", "Google AI"),
        ("import pygame", "Pygame"),
        ("import speech_recognition", "Speech Recognition")
    ]
    
    success_count = 0
    for test_code, test_name in tests:
        try:
            exec(test_code)
            print(f"✅ {test_name} - OK")
            success_count += 1
        except Exception as e:
            print(f"❌ {test_name} - Failed: {e}")
    
    print(f"\n📊 Verification Results: {success_count}/{len(tests)} passed")
    
    if success_count == len(tests):
        print("🎉 All components verified!")
        return True
    else:
        print("⚠️ Some components failed - check installation")
        return False

def check_gpu():
    """Check GPU availability"""
    print("\n🎮 GPU CHECK")
    print("=" * 15)
    
    try:
        import torch
        if torch.cuda.is_available():
            gpu_count = torch.cuda.device_count()
            gpu_name = torch.cuda.get_device_name(0)
            print(f"✅ CUDA available - {gpu_count} GPU(s)")
            print(f"🎮 Primary GPU: {gpu_name}")
            
            # Check memory
            memory = torch.cuda.get_device_properties(0).total_memory
            memory_gb = memory / (1024**3)
            print(f"💾 GPU Memory: {memory_gb:.1f} GB")
            
            if memory_gb >= 6:
                print("✅ Sufficient GPU memory for Orpheus-TTS")
            else:
                print("⚠️ Low GPU memory - may need CPU mode")
            
            return True
        else:
            print("❌ CUDA not available - will use CPU mode")
            print("💡 CPU mode will be slower but still functional")
            return False
    except Exception as e:
        print(f"❌ GPU check failed: {e}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    print("\n📝 ENVIRONMENT SETUP")
    print("=" * 20)
    
    env_file = ".env"
    if not os.path.exists(env_file):
        env_content = """# ORPHEUS-TTS ENVIRONMENT CONFIGURATION
# Add your Google Gemini API key below
GOOGLE_API_KEY=your_google_gemini_api_key_here

# Optional settings
MODEL_NAME=canopylabs/orpheus-tts-0.1-finetune-prod
DEFAULT_VOICE=tara
"""
        with open(env_file, 'w') as f:
            f.write(env_content)
        print(f"✅ Created {env_file}")
        print("💡 Add your Google API key to enable voice chat")
    else:
        print(f"✅ {env_file} already exists")
    
    return True

def main():
    """Main installation process"""
    print("🎭 REAL ORPHEUS-TTS SETUP")
    print("=" * 50)
    print("🎯 Setting up authentic Orpheus-TTS with emotions")
    print("=" * 50)
    
    steps = [
        ("Installing dependencies", install_dependencies),
        ("Verifying installation", verify_installation),
        ("Checking GPU", check_gpu),
        ("Setting up environment", create_env_file)
    ]
    
    results = []
    for step_name, step_func in steps:
        print(f"\n🎯 {step_name}...")
        result = step_func()
        results.append(result)
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 INSTALLATION SUMMARY")
    print("=" * 50)
    
    success_count = sum(results)
    total_steps = len(results)
    
    for i, (step_name, _) in enumerate(steps):
        status = "✅" if results[i] else "❌"
        print(f"{status} {step_name}")
    
    print(f"\n🎯 Overall: {success_count}/{total_steps} steps completed")
    
    if success_count >= 3:  # At least most steps successful
        print("\n🎉 INSTALLATION SUCCESSFUL!")
        print("\n🚀 Ready to test:")
        print("   python orpheus_only_demo.py      # Test TTS only")
        print("   python real_orpheus_voice_chat.py # Full voice chat")
        
        print("\n💡 Next steps:")
        print("   1. Get Google API key: https://makersuite.google.com/app/apikey")
        print("   2. Add to .env file: GOOGLE_API_KEY=your_key")
        print("   3. Test: python orpheus_only_demo.py")
        
        return True
    else:
        print("\n❌ INSTALLATION INCOMPLETE")
        print("💡 Check error messages above and retry")
        return False

if __name__ == "__main__":
    try:
        success = main()
        print(f"\n{'🎭 SETUP COMPLETE!' if success else '❌ SETUP FAILED'}")
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Setup interrupted by user")
        sys.exit(1)
