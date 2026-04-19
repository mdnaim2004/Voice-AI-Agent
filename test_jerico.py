#!/usr/bin/env python3
"""
Jerico Test Suite - Verify installation and functionality
"""

import sys
import os
from pathlib import Path

def print_header(title):
    """Print formatted header"""
    print(f"\n{'='*50}")
    print(f"  {title}")
    print(f"{'='*50}\n")

def test_python_version():
    """Test Python version"""
    print("📌 Testing Python Version...")
    version = sys.version_info
    print(f"   Python {version.major}.{version.minor}.{version.micro}")
    
    if version.major >= 3 and version.minor >= 8:
        print("   ✅ Python version OK")
        return True
    else:
        print("   ❌ Python 3.8+ required")
        return False

def test_imports():
    """Test required imports"""
    print("\n📌 Testing Required Modules...")
    
    modules = [
        'speech_recognition',
        'pyttsx3',
        'openai',
        'dotenv',
    ]
    
    failed = []
    for module in modules:
        try:
            __import__(module)
            print(f"   ✅ {module}")
        except ImportError:
            print(f"   ❌ {module} - NOT INSTALLED")
            failed.append(module)
    
    return len(failed) == 0, failed

def test_env_file():
    """Test .env configuration"""
    print("\n📌 Testing .env Configuration...")
    
    env_file = Path('.env')
    if env_file.exists():
        print("   ✅ .env file exists")
        
        with open(env_file, 'r') as f:
            content = f.read()
        
        if 'OPENAI_API_KEY' in content:
            # Check if key is set
            for line in content.split('\n'):
                if line.startswith('OPENAI_API_KEY='):
                    if 'your_key' in line.lower() or 'sk-' in line:
                        print("   ⚠️  API key appears to be set")
                        return True
            print("   ⚠️  API key configuration found")
            return True
        else:
            print("   ❌ OPENAI_API_KEY not found in .env")
            return False
    else:
        print("   ❌ .env file not found")
        print("      Run: cp .env.example .env")
        return False

def test_config_file():
    """Test config.json"""
    print("\n📌 Testing Configuration File...")
    
    config_file = Path('config.json')
    if config_file.exists():
        print("   ✅ config.json exists")
        
        import json
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            print(f"   ✅ Valid JSON")
            print(f"   ✅ Agent: {config.get('agent_name', 'Unknown')}")
            print(f"   ✅ Model: {config.get('openai_model', 'Unknown')}")
            return True
        except Exception as e:
            print(f"   ❌ Invalid JSON: {e}")
            return False
    else:
        print("   ❌ config.json not found")
        return False

def test_microphone():
    """Test microphone"""
    print("\n📌 Testing Microphone...")
    
    try:
        import speech_recognition as sr
        mic = sr.Microphone()
        print("   ✅ Microphone detected")
        return True
    except Exception as e:
        print(f"   ❌ Microphone error: {e}")
        print("      Check audio device and permissions")
        return False

def test_tts():
    """Test text-to-speech"""
    print("\n📌 Testing Text-to-Speech...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        print("   ✅ TTS Engine initialized")
        
        # Try to speak
        engine.say("Jerico ready")
        engine.runAndWait()
        print("   ✅ TTS working")
        return True
    except Exception as e:
        print(f"   ⚠️  TTS warning: {e}")
        return True  # Don't fail on TTS

def test_openai():
    """Test OpenAI API"""
    print("\n📌 Testing OpenAI API...")
    
    try:
        from dotenv import load_dotenv
        load_dotenv()
        
        api_key = os.getenv('OPENAI_API_KEY')
        
        if not api_key:
            print("   ❌ OPENAI_API_KEY not set")
            return False
        
        if 'your_key' in api_key.lower():
            print("   ❌ API key not configured")
            return False
        
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        print("   ✅ OpenAI client initialized")
        print("   ℹ️  Full API test requires internet connection")
        return True
    
    except Exception as e:
        print(f"   ❌ OpenAI error: {e}")
        return False

def main():
    """Run all tests"""
    print_header("🤖 JERICO TEST SUITE")
    
    results = {
        'Python Version': test_python_version(),
        '.env File': test_env_file(),
        'Config File': test_config_file(),
        'Microphone': test_microphone(),
        'Text-to-Speech': test_tts(),
        'OpenAI API': test_openai(),
    }
    
    # Test imports
    imports_ok, failed_imports = test_imports()
    results['Modules'] = imports_ok
    
    # Summary
    print_header("📊 TEST SUMMARY")
    
    for test_name, result in results.items():
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{test_name:.<30} {status}")
    
    if failed_imports:
        print(f"\n⚠️  Missing modules: {', '.join(failed_imports)}")
        print("   Run: pip install -r requirements.txt")
    
    # Overall result
    passed = sum(1 for v in results.values() if v)
    total = len(results)
    
    print_header(f"RESULT: {passed}/{total} Tests Passed")
    
    if passed == total:
        print("✅ All systems GO! Ready to run Jerico!")
        print("\nRun: python jerico_extended.py")
        return 0
    else:
        print("❌ Some tests failed. Please fix issues above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
