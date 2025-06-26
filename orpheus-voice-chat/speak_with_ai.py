#!/usr/bin/env python3
"""
Quick Voice Chat Test
Speak with AI personalities and hear their voices
"""

import sys
import os
import asyncio
import tempfile
import subprocess
import platform
sys.path.append('src')

async def speak_with_ai():
    """Interactive voice chat with AI personalities"""
    print("🎭 SPEAK WITH AI - VOICE CHAT TEST")
    print("=" * 50)
    
    try:
        from ultra_enhanced_tts import UltraEnhancedEdgeTTS
        
        tts = UltraEnhancedEdgeTTS()
        print(f"✅ TTS System: {tts.tts_system}")
        print()
        
        # Available personalities
        personalities = {
            "1": ("tara", "cheerful", "Hi! I'm Tara! I'm super excited to chat with you!"),
            "2": ("jessica", "confident", "Hello, I'm Jessica. I speak with confidence and clarity."),
            "3": ("zoe", "mysterious", "Zoe here... I have a mysterious and intriguing voice."),
            "4": ("alex", "friendly", "Hey there! I'm Alex, your friendly AI companion."),
            "5": ("custom", "default", "")
        }
        
        print("🎤 Choose an AI personality to speak with:")
        print("-" * 40)
        for key, (name, emotion, sample) in personalities.items():
            if name != "custom":
                print(f"{key}. {name.title()} ({emotion}) - \"{sample[:40]}...\"")
        print("5. Custom message")
        print()
        
        choice = input("Enter your choice (1-5): ").strip()
        
        if choice in personalities:
            name, emotion, default_text = personalities[choice]
            
            if choice == "5":
                text = input("Enter your message: ").strip()
                emotion = input("Enter emotion (cheerful/confident/mysterious/default): ").strip() or "default"
                name = "Custom"
            else:
                text = default_text
            
            print(f"\n🎭 {name.title()} is speaking...")
            print(f"💬 Text: \"{text}\"")
            print(f"😊 Emotion: {emotion}")
            print()
            
            # Generate speech
            try:
                result = tts.synthesize_speech(text=text, emotion=emotion)
                
                if result and os.path.exists(result):
                    file_size = os.path.getsize(result) / 1024
                    print(f"✅ Generated audio: {os.path.basename(result)} ({file_size:.1f} KB)")
                    
                    # Play the audio
                    print("🔊 Playing audio...")
                    try:
                        if platform.system() == "Windows":
                            # Use Windows built-in player
                            subprocess.run(['start', '', result], shell=True, check=True)
                        elif platform.system() == "Darwin":  # macOS
                            subprocess.run(['afplay', result], check=True)
                        else:  # Linux
                            subprocess.run(['aplay', result], check=True)
                        
                        print("🎵 Audio is playing! You should hear the AI voice now.")
                        
                        # Keep file for a moment then clean up
                        input("\nPress Enter when done listening...")
                        
                    except Exception as e:
                        print(f"⚠️  Couldn't auto-play audio: {e}")
                        print(f"💡 Manually play this file: {result}")
                        input("Press Enter to continue...")
                    
                    # Clean up
                    try:
                        os.unlink(result)
                        print("🧹 Cleaned up audio file")
                    except:
                        pass
                        
                else:
                    print("❌ Failed to generate audio")
                    
            except Exception as e:
                print(f"❌ Speech generation error: {e}")
        else:
            print("❌ Invalid choice")
        
        print("\n🎉 Voice chat test completed!")
        
        # Offer to continue
        if input("\nWould you like to try another personality? (y/n): ").lower().startswith('y'):
            await speak_with_ai()
        
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    asyncio.run(speak_with_ai())
