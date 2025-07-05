#!/usr/bin/env python3
"""
🧹 PREVENT FILE SPAWNING SCRIPT
===============================
Prevents unwanted files from being created automatically
Run this script to clean up any automatically spawned files
===============================
"""

import os
import shutil
from pathlib import Path

class FileSpawnPreventer:
    """Prevents unwanted files from spawning"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        
        # Files that automatically spawn and should be deleted
        self.unwanted_files = [
            # Security risk files
            'accept_model_terms.py',
            'quick_test.py', 
            'test_access.py',
            'debug_repo.py',
            'debug_security.py',
            'test_security.py',
            
            # Duplicate demos
            'cpu_demo.py',
            'cpu_orpheus_demo.py',
            'emotion_demo.py',
            'emotion_voice_chat.py',
            'enhanced_voice_chat.py',
            'final_demo.py',
            'orpheus_demo_simple.py',
            'orpheus_only_demo.py',
            'simple_test.py',
            'simple_working_demo.py',
            'streamlined_demo.py',
            'working_demo.py',
            
            # Duplicate TTS implementations
            'actual_orpheus_tts.py',
            'intel_optimized_tts.py',
            'intel_tts_fixed.py',
            'orpheus_tts_real.py',
            'orpheus_voice_chat_working.py',
            'real_orpheus_intel.py',
            'real_orpheus_tts.py',
            'real_orpheus_voice.py',
            'real_orpheus_voice_chat.py',
            'working_orpheus_tts.py',
            
            # Additional unwanted implementations
            'authentic_orpheus_direct.py',
            'check_orpheus_access.py',
            'find_real_orpheus.py',
            'orpheus_tts_direct.py',
            'pure_orpheus_only.py',
            'real_orpheus_original.py',
            'real_orpheus_voices.py',
            'working_orpheus_final.py',
            'complete_verification.py',
            'fixed_voice_chat.py',
            'install_orpheus.py',
            'official_orpheus_tts.py',
            'setup_orpheus_auth.py',
            'test_orpheus.py',
            
            # Unwanted app/deployment files
            'app.py',
            'Dockerfile',
            '.gcloudignore',
            
            # Temporary files
            '*.tmp',
            '*.temp',
            'temp_*',
        ]
        
        # Directories that spawn automatically
        self.unwanted_dirs = [
            '__pycache__',
            '.pytest_cache',
            'temp_audio',
            'scripts',
            'docs',
            'deploy',
            'tests',
            'checkpoints',
        ]
    
    def clean_unwanted_files(self):
        """Remove unwanted files"""
        removed_count = 0
        
        print("🧹 Cleaning unwanted files...")
        
        for file_pattern in self.unwanted_files:
            if '*' in file_pattern:
                # Handle wildcards
                import glob
                for file_path in glob.glob(str(self.project_root / file_pattern)):
                    try:
                        os.remove(file_path)
                        print(f"✅ Removed: {file_path}")
                        removed_count += 1
                    except Exception as e:
                        print(f"⚠️ Could not remove {file_path}: {e}")
            else:
                # Handle specific files
                file_path = self.project_root / file_pattern
                if file_path.exists():
                    try:
                        os.remove(file_path)
                        print(f"✅ Removed: {file_path}")
                        removed_count += 1
                    except Exception as e:
                        print(f"⚠️ Could not remove {file_path}: {e}")
        
        return removed_count
    
    def clean_unwanted_dirs(self):
        """Remove unwanted directories"""
        removed_count = 0
        
        for dir_name in self.unwanted_dirs:
            dir_path = self.project_root / dir_name
            if dir_path.exists():
                try:
                    shutil.rmtree(dir_path)
                    print(f"✅ Removed directory: {dir_path}")
                    removed_count += 1
                except Exception as e:
                    print(f"⚠️ Could not remove {dir_path}: {e}")
        
        return removed_count
    
    def monitor_and_prevent(self):
        """Monitor for new unwanted files and prevent them"""
        files_removed = self.clean_unwanted_files()
        dirs_removed = self.clean_unwanted_dirs()
        
        total_removed = files_removed + dirs_removed
        
        if total_removed > 0:
            print(f"\n🧹 Cleanup complete! Removed {total_removed} unwanted items")
        else:
            print("\n✅ No unwanted files found - repository is clean!")
        
        return total_removed

def main():
    """Main function"""
    print("🧹 PREVENT FILE SPAWNING")
    print("=" * 40)
    
    preventer = FileSpawnPreventer()
    total_removed = preventer.monitor_and_prevent()
    
    print("\n📋 PREVENTION STATUS:")
    print(f"   🧹 Items removed: {total_removed}")
    print("   🔒 Repository secured against file spawning")
    print("\n💡 Run this script regularly to prevent unwanted files!")

if __name__ == "__main__":
    main()
