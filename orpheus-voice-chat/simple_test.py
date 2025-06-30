#!/usr/bin/env python3
"""
🎭 SIMPLE ORPHEUS-TTS TEST
==========================
Basic test to verify Orpheus-TTS is working
"""

def main():
    print("🎭 SIMPLE ORPHEUS-TTS TEST")
    print("=" * 40)
    
    try:
        print("1️⃣ Testing import...")
        from orpheus_tts import OrpheusModel
        print("✅ OrpheusModel imported successfully!")
        
        print("\n2️⃣ Testing PyTorch...")
        import torch
        cuda_available = torch.cuda.is_available()
        print(f"✅ PyTorch loaded - CUDA: {cuda_available}")
        
        print("\n3️⃣ Loading Orpheus model...")
        model = OrpheusModel(
            model_name="canopylabs/orpheus-tts-0.1-finetune-prod"
        )
        print("✅ Model loaded successfully!")
        
        print("\n4️⃣ Testing simple generation...")
        prompt = "tara: Hello, this is a test!"
        
        print(f"📝 Prompt: {prompt}")
        print("🔄 Generating audio...")
        
        # Generate just a few chunks for testing
        chunk_count = 0
        total_bytes = 0
        
        for audio_chunk in model.generate_speech(prompt=prompt, voice="tara"):
            chunk_count += 1
            total_bytes += len(audio_chunk)
            print(f"   Generated chunk {chunk_count}: {len(audio_chunk)} bytes")
            
            # Stop after a few chunks for quick test
            if chunk_count >= 3:
                break
        
        print(f"✅ SUCCESS! Generated {chunk_count} chunks ({total_bytes:,} total bytes)")
        print("\n🎉 REAL ORPHEUS-TTS IS WORKING!")
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("\n🔧 Troubleshooting:")
        print("   - Ensure you have a CUDA-compatible GPU")
        print("   - Check available GPU memory")
        print("   - Try restarting if models are cached")
        return False

if __name__ == "__main__":
    success = main()
    
    if success:
        print("\n🎤 Ready for emotion features!")
        print("   - Emotion tags: <happy>, <laugh>, <whisper>, etc.")
        print("   - Multiple voices: tara, leah, jess, leo, dan, mia, zac, zoe") 
        print("   - Voice chat: python real_orpheus_voice_chat.py")
    
    exit(0 if success else 1)
