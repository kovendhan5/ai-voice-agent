#!/usr/bin/env python3
"""
🚀 SMART GITHUB PUSH HANDLER
Handles GitHub push with intelligent retry and error handling
"""

import subprocess
import time
import sys
import os

def run_git_command(cmd, timeout=300):
    """Run git command with timeout"""
    try:
        print(f"🔧 Running: {cmd}")
        result = subprocess.run(
            cmd, 
            shell=True, 
            capture_output=True, 
            text=True, 
            timeout=timeout,
            cwd=r"k:\full stack\AI\voice model"
        )
        return result.stdout, result.stderr, result.returncode
    except subprocess.TimeoutExpired:
        return "", "Timeout expired", 1
    except Exception as e:
        return "", str(e), 1

def check_github_connectivity():
    """Check if GitHub is reachable"""
    print("🌐 Testing GitHub connectivity...")
    stdout, stderr, code = run_git_command("git ls-remote origin", 30)
    if code == 0:
        print("✅ GitHub is reachable")
        return True
    else:
        print(f"❌ GitHub connectivity issue: {stderr}")
        return False

def smart_push():
    """Smart push with multiple strategies"""
    print("🚀 SMART GITHUB PUSH")
    print("=" * 40)
    
    # Check connectivity first
    if not check_github_connectivity():
        print("⚠️ Cannot reach GitHub. Check your internet connection.")
        return False
    
    # Strategy 1: Normal push
    print("\n📤 Strategy 1: Normal push...")
    stdout, stderr, code = run_git_command("git push origin main", 180)
    
    if code == 0:
        print("✅ SUCCESS! Normal push completed")
        print(stdout)
        return True
    else:
        print(f"❌ Normal push failed: {stderr}")
    
    # Strategy 2: Push with verbose output
    print("\n📤 Strategy 2: Verbose push...")
    stdout, stderr, code = run_git_command("git push origin main --verbose", 180)
    
    if code == 0:
        print("✅ SUCCESS! Verbose push completed")
        print(stdout)
        return True
    else:
        print(f"❌ Verbose push failed: {stderr}")
    
    # Strategy 3: Force push (if safe)
    print("\n📤 Strategy 3: Checking if force push is safe...")
    stdout, stderr, code = run_git_command("git status --porcelain", 10)
    
    if not stdout.strip():  # Working tree is clean
        print("Working tree is clean, attempting force push...")
        stdout, stderr, code = run_git_command("git push origin main --force", 180)
        
        if code == 0:
            print("✅ SUCCESS! Force push completed")
            print(stdout)
            return True
        else:
            print(f"❌ Force push failed: {stderr}")
    
    return False

def main():
    """Main function"""
    print("🎯 GITHUB DEPLOYMENT HANDLER")
    print("=" * 50)
    
    # Check current status
    print("📋 Current repository status:")
    stdout, stderr, code = run_git_command("git status", 10)
    print(stdout)
    
    # Attempt smart push
    success = smart_push()
    
    if success:
        print("\n🎉 DEPLOYMENT SUCCESSFUL!")
        print("✅ Your Orpheus-TTS voice chat system is now on GitHub")
        print("🔗 Repository: https://github.com/kovendhan5/ai-voice-agent")
        
        # Final verification
        print("\n📊 Final status:")
        stdout, stderr, code = run_git_command("git status", 10)
        print(stdout)
        
    else:
        print("\n⚠️ AUTOMATED PUSH FAILED")
        print("🔧 Manual solutions:")
        print("1. Try GitHub Desktop application")
        print("2. Check your GitHub authentication")
        print("3. Verify internet connection")
        print("4. Try: git push origin main --force")
        
    print("\n" + "=" * 50)
    print("🎯 PUSH HANDLER COMPLETE")

if __name__ == "__main__":
    main()
