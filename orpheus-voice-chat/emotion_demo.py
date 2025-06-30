#!/usr/bin/env python3
"""
🎭 EMOTION TAG DEMO
===================
Test script to demonstrate emotion tag parsing and voice synthesis
"""

import asyncio
import tempfile
import os
from pathlib import Path

# Import our emotion TTS engine
from emotion_voice_chat import EmotionOrpheusTTS

async def demo_emotion_tags():
    """Demonstrate emotion tag functionality"""
    
    print("🎭 EMOTION TAG DEMO")
    print("=" * 40)
    
    # Initialize the TTS engine
    tts = EmotionOrpheusTTS()
    
    # Demo texts with emotion tags
    demo_texts = [
        "<happy>Hello! I'm so excited to meet you!</happy>",
        
        "<whisper>Let me tell you a secret...</whisper> <excited>This voice system is amazing!</excited>",
        
        "<sad>I'm sorry to hear that.</sad> <calm>But everything will be okay.</calm>",
        
        "<laugh>Haha, that's so funny!</laugh> <happy>I love your sense of humor!</happy>",
        
        "<angry>I can't believe this happened!</angry> <calm>But let me take a deep breath and think about it.</calm>",
        
        "<surprised>Wow! I didn't expect that!</surprised> <dramatic>This changes everything!</dramatic>",
        
        "This is regular speech without any emotion tags.",
        
        "<excited>Welcome to the future of voice synthesis!</excited> <whisper>It's like magic...</whisper>"
    ]
    
    print(f"🎯 Testing {len(demo_texts)} emotion examples...\n")
    
    for i, text in enumerate(demo_texts, 1):
        print(f"📢 Demo {i}/{len(demo_texts)}")
        print(f"📝 Text: {text}")
        
        # Parse emotion segments
        segments = tts.parse_emotion_tags(text)
        print(f"🎭 Emotions detected: {[(emotion, content[:30]+'...' if len(content) > 30 else content) for emotion, content in segments]}")
        
        # Generate audio (this will show the process)
        try:
            audio_file = await tts.synthesize_speech(text)
            if audio_file:
                print(f"✅ Audio generated: {audio_file}")
                # Clean up
                try:
                    os.unlink(audio_file)
                except:
                    pass
            else:
                print("❌ Audio generation failed")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
        
        # Small delay between demos
        await asyncio.sleep(1)
    
    print("🎉 Emotion tag demo completed!")
    print("\n💡 Tips for using emotion tags:")
    print("   • Tags can be nested or sequential")
    print("   • Mix emotions for natural conversation")
    print("   • Text without tags uses neutral voice")
    print("   • Orpheus-TTS provides the highest quality")

def test_emotion_parsing():
    """Test emotion tag parsing logic"""
    print("\n🧪 TESTING EMOTION PARSING")
    print("=" * 30)
    
    tts = EmotionOrpheusTTS()
    
    test_cases = [
        "Simple text without tags",
        "<happy>Just happy text</happy>",
        "<excited>Excited!</excited> Normal text <sad>then sad</sad>",
        "<whisper>Secret message</whisper>",
        "<laugh>Haha!</laugh> <excited>Amazing!</excited> <calm>Now calm.</calm>",
        "Start normal <angry>get angry</angry> <happy>then happy</happy> end normal"
    ]
    
    for text in test_cases:
        print(f"\n📝 Input: {text}")
        segments = tts.parse_emotion_tags(text)
        print(f"🎭 Parsed: {segments}")

if __name__ == "__main__":
    print("🎭 ORPHEUS-TTS EMOTION TAG SYSTEM")
    print("=" * 50)
    
    # Test parsing first
    test_emotion_parsing()
    
    # Then run the full demo
    print("\n" + "=" * 50)
    asyncio.run(demo_emotion_tags())
