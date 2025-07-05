#!/usr/bin/env python3
"""
🎭 INTERACTIVE ORPHEUS CHAT
===========================
Simple interactive chat using the real working Orpheus
===========================
"""

import os
import sys
from pathlib import Path

# Import the working Orpheus
sys.path.append(str(Path(__file__).parent))

def main():
    """Main interactive function"""
    print("🎭 INTERACTIVE ORPHEUS CHAT")
    print("=" * 40)
    print("🎪 Using real_working_orpheus_edge.py")
    print("🎭 Type text with emotion tags: <laugh>, <whisper>, <gasp>, etc.")
    print("🛑 Type 'quit' to exit")
    print("=" * 40)
    
    try:
        # Import the working Orpheus implementation
        from real_working_orpheus_edge import RealWorkingOrpheus
        
        # Initialize Orpheus
        orpheus = RealWorkingOrpheus()
        
        # Interactive loop
        while True:
            try:
                user_input = input("\n🎭 You: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'stop']:
                    print("👋 Goodbye from Orpheus!")
                    break
                
                if not user_input:
                    continue
                
                # Speak with Orpheus
                success = orpheus.orpheus_speak(user_input)
                
                if success:
                    print("✅ Orpheus speech completed")
                else:
                    print("❌ Speech failed")
                
            except KeyboardInterrupt:
                print("\n👋 Chat ended")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
        
    except ImportError as e:
        print(f"❌ Could not import working Orpheus: {e}")
        print("🔧 Make sure real_working_orpheus_edge.py exists and is working")
    except Exception as e:
        print(f"❌ Error starting interactive Orpheus: {e}")

if __name__ == "__main__":
    main()
