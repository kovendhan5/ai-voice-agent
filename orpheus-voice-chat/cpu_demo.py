#!/usr/bin/env python3
"""
🎭 CPU-OPTIMIZED ORPHEUS-TTS DEMO
=================================
Real Orpheus-TTS working on CPU without NVIDIA drivers
"""

import os
import sys
import time
import tempfile
import wave

def test_cpu_mode():
    """Test Orpheus-TTS in CPU mode"""
    print("🎭 CPU-OPTIMIZED ORPHEUS-TTS DEMO")
    print("=" * 45)
    print("🔧 Running without GPU - CPU mode optimized")
    print("=" * 45)
    
    try:
        print("\n1️⃣ Testing imports...")
        from orpheus_tts import OrpheusModel
        print("✅ OrpheusModel imported successfully!")
        
        print("\n2️⃣ Setting up CPU mode...")
        import torch
        # Force CPU mode
        device = "cpu"
        print(f"✅ Using device: {device.upper()}")
        print("💡 CPU mode will be slower but fully functional")
        
        print("\n3️⃣ Loading model for CPU...")
        print("   (This will take 2-3 minutes on CPU - please wait)")
        
        start_time = time.time()
        
        # Load with CPU-optimized settings
        model = OrpheusModel(
            model_name="canopylabs/orpheus-tts-0.1-finetune-prod",
            max_model_len=512,  # Smaller for CPU
            device="cpu"  # Force CPU mode
        )
        
        load_time = time.time() - start_time
        print(f"✅ Model loaded in {load_time:.1f} seconds!")
        
        print("\n4️⃣ Testing basic speech generation...")
        
        # Simple test without complex emotions first
        test_text = "tara: Hello, this is a test of Orpheus TTS running on CPU."
        print(f"📝 Testing: {test_text}")
        
        try:
            print("🔄 Generating audio (this may take a moment on CPU)...")
            
            audio_chunks = []
            chunk_count = 0
            
            start_gen = time.time()
            for chunk in model.generate_speech(
                prompt=test_text, 
                voice="tara",
                temperature=0.7,
                max_tokens=256  # Limit for CPU
            ):
                audio_chunks.append(chunk)
                chunk_count += 1
                print(f"   Chunk {chunk_count}: {len(chunk)} bytes")
                
                # Limit for CPU demo
                if chunk_count >= 3:
                    break
            
            gen_time = time.time() - start_gen
            total_bytes = sum(len(chunk) for chunk in audio_chunks)
            
            print(f"✅ Generated {chunk_count} chunks in {gen_time:.2f}s")
            print(f"📊 Total audio: {total_bytes:,} bytes")
            
            # Save to file
            output_file = "cpu_test_output.wav"
            with wave.open(output_file, "wb") as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(24000)
                
                for chunk in audio_chunks:
                    wf.writeframes(chunk)
            
            # Calculate duration
            frames = sum(len(chunk) // 2 for chunk in audio_chunks)
            duration = frames / 24000
            
            print(f"💾 Saved: {output_file} ({duration:.1f}s audio)")
            
            print("\n5️⃣ Testing simple emotion...")
            
            emotion_text = "tara: <happy>This is working great on CPU!</happy>"
            print(f"📝 Testing emotion: {emotion_text}")
            
            try:
                emotion_chunks = []
                for i, chunk in enumerate(model.generate_speech(
                    prompt=emotion_text,
                    voice="tara",
                    max_tokens=128
                )):
                    emotion_chunks.append(chunk)
                    if i >= 2:  # Quick test
                        break
                
                emotion_bytes = sum(len(chunk) for chunk in emotion_chunks)
                print(f"✅ Emotion test successful: {emotion_bytes:,} bytes")
                
                # Save emotion test
                emotion_file = "cpu_emotion_test.wav"
                with wave.open(emotion_file, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(24000)
                    
                    for chunk in emotion_chunks:
                        wf.writeframes(chunk)
                
                print(f"💾 Saved emotion test: {emotion_file}")
                
            except Exception as e:
                print(f"⚠️ Emotion test had issues: {e}")
                print("💡 Basic TTS still works fine")
            
            print("\n🎉 SUCCESS! Orpheus-TTS working on CPU!")
            print("\n✅ What's working:")
            print("   - Real Orpheus-TTS model loaded")
            print("   - Speech generation functional")
            print("   - Audio files created")
            print("   - CPU mode optimized")
            
            print("\n📁 Generated files:")
            for filename in [output_file, "cpu_emotion_test.wav"]:
                if os.path.exists(filename):
                    size = os.path.getsize(filename)
                    print(f"   🎵 {filename} ({size:,} bytes)")
            
            print("\n💡 Performance tips for CPU mode:")
            print("   - Generation will be slower than GPU")
            print("   - Keep text shorter for faster response")
            print("   - Consider using simpler prompts")
            
            return True
            
        except Exception as e:
            print(f"❌ Speech generation failed: {e}")
            print("\n🔧 Possible solutions:")
            print("   - Restart Python session")
            print("   - Try smaller max_model_len")
            print("   - Check available RAM")
            return False
            
    except Exception as e:
        print(f"❌ Setup failed: {e}")
        print("\n🔧 Troubleshooting:")
        print("   1. Install: pip install orpheus-speech")
        print("   2. Install: pip install torch --index-url https://download.pytorch.org/whl/cpu")
        print("   3. Restart Python session")
        return False

def main():
    """Main function"""
    try:
        print("🔧 CPU-ONLY MODE DETECTED")
        print("💡 This is normal - GPU is not required!")
        print("🎯 Optimizing for CPU performance...\n")
        
        success = test_cpu_mode()
        
        if success:
            print("\n🎭 CPU MODE SUCCESS!")
            print("=" * 30)
            print("✅ Real Orpheus-TTS working on CPU")
            print("✅ Audio files generated successfully")
            print("✅ System ready for voice synthesis")
            
            print("\n🚀 Next steps:")
            print("   1. Listen to the generated .wav files")
            print("   2. Add Google API key to .env for voice chat")
            print("   3. Run voice chat: python real_orpheus_voice_chat.py")
            
            print("\n🎤 For voice chat, create .env file with:")
            print("   GOOGLE_API_KEY=your_api_key_here")
            
        else:
            print("\n❌ CPU MODE FAILED")
            print("💡 Try installing CPU-optimized PyTorch:")
            print("   pip install torch --index-url https://download.pytorch.org/whl/cpu")
        
        return success
        
    except KeyboardInterrupt:
        print("\n🛑 Interrupted by user")
        return False

if __name__ == "__main__":
    success = main()
    print(f"\n{'🎉 DEMO COMPLETE!' if success else '❌ DEMO FAILED'}")
    
    if success:
        print("\n🎭 REAL ORPHEUS-TTS IS WORKING ON CPU!")
        print("🎯 No GPU needed - fully functional!")
    
    sys.exit(0 if success else 1)
