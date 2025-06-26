#!/usr/bin/env python3
"""
Test script for the Orpheus TTS API
"""

import requests
import json
import sys
import os

def test_health_check(base_url):
    """Test the health check endpoint"""
    print("Testing health check...")
    try:
        response = requests.get(f"{base_url}/")
        print(f"Status: {response.status_code}")
        print(f"Response: {response.json()}")
        return response.status_code == 200
    except Exception as e:
        print(f"Health check failed: {e}")
        return False

def test_speech_generation(base_url, text="tara: Hello from Orpheus TTS!", output_file="test_output.wav"):
    """Test speech generation endpoint"""
    print(f"Testing speech generation with text: '{text}'")
    try:
        headers = {"Content-Type": "application/json"}
        data = {"text": text}
        
        response = requests.post(f"{base_url}/speak", headers=headers, json=data)
        
        if response.status_code == 200:
            with open(output_file, "wb") as f:
                f.write(response.content)
            print(f"✓ Speech generated successfully! Saved to {output_file}")
            print(f"File size: {len(response.content)} bytes")
            return True
        else:
            print(f"✗ Speech generation failed: {response.status_code}")
            print(f"Response: {response.text}")
            return False
    except Exception as e:
        print(f"Speech generation failed: {e}")
        return False

def test_voices_endpoint(base_url):
    """Test the voices listing endpoint"""
    print("Testing voices endpoint...")
    try:
        response = requests.get(f"{base_url}/voices")
        if response.status_code == 200:
            voices = response.json()
            print(f"✓ Available voices: {voices}")
            return True
        else:
            print(f"✗ Voices endpoint failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"Voices endpoint failed: {e}")
        return False

def main():
    # Default to local development server
    base_url = "http://localhost:8080"
    
    # Allow override via command line
    if len(sys.argv) > 1:
        base_url = sys.argv[1].rstrip('/')
    
    print(f"Testing Orpheus TTS API at: {base_url}")
    print("=" * 50)
    
    # Run tests
    tests_passed = 0
    total_tests = 3
    
    if test_health_check(base_url):
        tests_passed += 1
    
    if test_voices_endpoint(base_url):
        tests_passed += 1
    
    if test_speech_generation(base_url):
        tests_passed += 1
    
    print("=" * 50)
    print(f"Tests completed: {tests_passed}/{total_tests} passed")
    
    if tests_passed == total_tests:
        print("✓ All tests passed!")
        sys.exit(0)
    else:
        print("✗ Some tests failed!")
        sys.exit(1)

if __name__ == "__main__":
    main()
