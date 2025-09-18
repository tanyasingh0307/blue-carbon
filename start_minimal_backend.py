#!/usr/bin/env python3
"""
Minimal backend starter - guaranteed to work
"""

import sys
import subprocess
import os
from pathlib import Path

def install_minimal_deps():
    """Install only the essential dependencies"""
    print("📦 Installing minimal dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", 
            "fastapi==0.104.1", "uvicorn==0.24.0"
        ], check=True)
        print("✅ Dependencies installed")
        return True
    except Exception as e:
        print(f"❌ Failed to install dependencies: {e}")
        return False

def start_minimal_backend():
    """Start the minimal backend"""
    print("🚀 Starting minimal backend...")
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "minimal_main:app", 
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

def main():
    print("🌊 Blue Carbon - Minimal Backend Starter")
    print("=" * 50)
    
    # Check if backend directory exists
    if not Path("backend").exists():
        print("❌ Backend directory not found")
        return
    
    # Install dependencies
    if not install_minimal_deps():
        return
    
    # Start backend
    print("\n🚀 Starting backend...")
    print("📍 Server: http://localhost:8000")
    print("📚 API Docs: http://localhost:8000/docs")
    print("🛑 Press Ctrl+C to stop")
    print("-" * 50)
    
    start_minimal_backend()

if __name__ == "__main__":
    main()
</parameter>