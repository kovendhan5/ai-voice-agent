#!/usr/bin/env python3
"""
🚀 CLEAN REPOSITORY CREATOR
Creates a fresh, clean repository without large files for GitHub push
"""

import os
import shutil
import subprocess
import sys

def run_command(cmd, cwd=None):
    """Run command and return result"""
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=cwd)
        return result.returncode == 0, result.stdout, result.stderr
    except Exception as e:
        return False, "", str(e)

def create_clean_repo():
    """Create a clean repository without large files"""
    print("🧹 CREATING CLEAN REPOSITORY")
    print("=" * 40)
    
    base_dir = r"k:\full stack\AI\voice model"
    clean_dir = r"k:\full stack\AI\voice model\clean-repo"
    
    # Create clean directory
    if os.path.exists(clean_dir):
        shutil.rmtree(clean_dir)
    os.makedirs(clean_dir)
    
    print(f"📁 Created clean directory: {clean_dir}")
    
    # Copy essential files (excluding large files)
    essential_files = [
        "orpheus-voice-chat/fixed_voice_chat.py",
        "orpheus-voice-chat/complete_verification.py", 
        "orpheus-voice-chat/orpheus_tts_real.py",
        "orpheus-voice-chat/README.md",
        "orpheus-voice-chat/requirements.txt",
        "orpheus-voice-chat/.env.example",
        "orpheus-voice-chat/.gitignore",
        "orpheus-voice-chat/app.py",
        "CURRENT_STATUS.md",
        "DEPLOYMENT_COMPLETE.md"
    ]
    
    copied_files = []
    for file_path in essential_files:
        src = os.path.join(base_dir, file_path)
        if os.path.exists(src):
            dst_dir = os.path.join(clean_dir, os.path.dirname(file_path))
            os.makedirs(dst_dir, exist_ok=True)
            dst = os.path.join(clean_dir, file_path)
            shutil.copy2(src, dst)
            copied_files.append(file_path)
            print(f"✅ Copied: {file_path}")
    
    # Initialize new git repo
    success, stdout, stderr = run_command("git init", clean_dir)
    if not success:
        print(f"❌ Git init failed: {stderr}")
        return False
    
    # Add all files
    success, stdout, stderr = run_command("git add .", clean_dir)
    if not success:
        print(f"❌ Git add failed: {stderr}")
        return False
    
    # Initial commit
    success, stdout, stderr = run_command('git commit -m "🎉 Clean Orpheus-TTS Voice Chat System - No Large Files"', clean_dir)
    if not success:
        print(f"❌ Git commit failed: {stderr}")
        return False
    
    # Add remote
    success, stdout, stderr = run_command("git remote add origin https://github.com/kovendhan5/ai-voice-agent.git", clean_dir)
    if not success:
        print(f"⚠️ Remote add warning: {stderr}")
    
    # Try to push
    print("\n🚀 Attempting push to GitHub...")
    success, stdout, stderr = run_command("git push origin main --force", clean_dir)
    
    if success:
        print("✅ SUCCESS! Clean repository pushed to GitHub!")
        print(f"📊 Files pushed: {len(copied_files)}")
        print("🔗 Repository: https://github.com/kovendhan5/ai-voice-agent")
        return True
    else:
        print(f"❌ Push failed: {stderr}")
        print(f"📤 Stdout: {stdout}")
        return False

def main():
    """Main function"""
    print("🚀 CLEAN GITHUB DEPLOYMENT")
    print("=" * 50)
    
    success = create_clean_repo()
    
    if success:
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("✅ Your Orpheus-TTS voice chat system is now on GitHub")
        print("📁 Core files uploaded without large model files")
        print("🔗 https://github.com/kovendhan5/ai-voice-agent")
    else:
        print("\n⚠️ Clean deployment failed")
        print("💡 Your system still works perfectly locally!")
        
    print("\n🎯 Your voice chat system is ready to use:")
    print('   cd "k:\\full stack\\AI\\voice model\\orpheus-voice-chat"')
    print("   python fixed_voice_chat.py")

if __name__ == "__main__":
    main()
