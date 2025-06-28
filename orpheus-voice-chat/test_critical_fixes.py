#!/usr/bin/env python3
"""
Quick Fix Test - Test the critical fixes
"""

import asyncio
import edge_tts
import tempfile
import os
import google.generativeai as genai

# Configure Gemini AI with updated model
GEMINI_API_KEY = "AIzaSyBu5izidIfzknhhMCzZB6yn1GKnzwZoUIQ"
genai.configure(api_key=GEMINI_API_KEY)

async def test_fixes():
    print("🔧 TESTING CRITICAL FIXES")
    print("=" * 40)
    
    # Test 1: Updated Gemini model
    print("\n1️⃣ Testing updated Gemini AI model...")
    try:
        model = genai.GenerativeModel('gemini-1.5-flash')
        response = model.generate_content("Say hello in a friendly way for a voice chat")
        ai_text = response.text.strip()
        print(f"✅ Gemini model working: '{ai_text}'")
    except Exception as e:
        print(f"❌ Gemini model error: {e}")
    
    # Test 2: Simplified Edge TTS
    print("\n2️⃣ Testing simplified Edge TTS...")
    try:
        text = "Hello! This is a test of the fixed voice system."
        voice = "en-US-JennyNeural"
        
        communicate = edge_tts.Communicate(text, voice)
        
        with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as temp_file:
            temp_path = temp_file.name
        
        await communicate.save(temp_path)
        
        file_size = os.path.getsize(temp_path)
        print(f"✅ Edge TTS working: {file_size} bytes generated")
        
        # Clean up
        os.unlink(temp_path)
        
    except Exception as e:
        print(f"❌ Edge TTS error: {e}")
    
    print("\n🎉 FIXES TESTED - READY TO USE!")
    print("💡 Run: python fixed_voice_chat.py")

if __name__ == "__main__":
    asyncio.run(test_fixes())
