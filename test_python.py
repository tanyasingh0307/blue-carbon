#!/usr/bin/env python3
"""
Test Python installation and basic functionality
"""

import sys
import subprocess

def test_python():
    """Test Python installation"""
    print("🐍 Testing Python...")
    print(f"Python version: {sys.version}")
    print(f"Python executable: {sys.executable}")
    
    if sys.version_info < (3, 7):
        print("❌ Python 3.7+ required")
        return False
    
    print("✅ Python version OK")
    return True

def test_pip():
    """Test pip installation"""
    print("\n📦 Testing pip...")
    try:
        result = subprocess.run([sys.executable, "-m", "pip", "--version"], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ pip version: {result.stdout.strip()}")
            return True
        else:
            print("❌ pip not working")
            return False
    except Exception as e:
        print(f"❌ pip error: {e}")
        return False

def test_fastapi_install():
    """Test if we can install FastAPI"""
    print("\n🚀 Testing FastAPI installation...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "fastapi", "uvicorn"], 
                      check=True, capture_output=True)
        print("✅ FastAPI installed successfully")
        return True
    except Exception as e:
        print(f"❌ FastAPI installation failed: {e}")
        return False

def main():
    print("🧪 Python Environment Test")
    print("=" * 40)
    
    tests = [
        ("Python", test_python),
        ("pip", test_pip),
        ("FastAPI", test_fastapi_install)
    ]
    
    all_passed = True
    for name, test_func in tests:
        if not test_func():
            all_passed = False
    
    print("\n" + "=" * 40)
    if all_passed:
        print("🎉 All tests passed! You can run the backend.")
        print("\nNext steps:")
        print("1. Run: python start_minimal_backend.py")
        print("2. Open: http://localhost:8000")
    else:
        print("❌ Some tests failed. Please fix the issues above.")

if __name__ == "__main__":
    main()
</parameter>