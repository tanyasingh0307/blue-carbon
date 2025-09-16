#!/usr/bin/env python3
"""
Backend startup script with error handling and diagnostics
"""

import sys
import os
import subprocess
from pathlib import Path

def check_python_version():
    """Check if Python version is compatible"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {sys.version}")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_backend_directory():
    """Check if backend directory exists"""
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    required_files = ["main.py", "requirements.txt"]
    for file in required_files:
        if not (backend_dir / file).exists():
            print(f"❌ Required file missing: backend/{file}")
            return False
    
    print("✅ Backend directory structure is valid")
    return True

def install_dependencies():
    """Install Python dependencies"""
    print("📦 Installing dependencies...")
    try:
        subprocess.run([
            sys.executable, "-m", "pip", "install", "-r", "backend/requirements.txt"
        ], check=True, capture_output=True, text=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install dependencies: {e}")
        print(f"Error output: {e.stderr}")
        return False

def create_env_file():
    """Create .env file if it doesn't exist"""
    env_file = Path("backend/.env")
    env_example = Path("backend/.env.example")
    
    if not env_file.exists() and env_example.exists():
        print("📝 Creating .env file from .env.example...")
        env_file.write_text(env_example.read_text())
        print("✅ .env file created")
    elif env_file.exists():
        print("✅ .env file already exists")
    else:
        print("⚠️ No .env file found, using default settings")

def start_backend():
    """Start the backend server"""
    print("🚀 Starting backend server...")
    try:
        os.chdir("backend")
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ], check=True)
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to start backend: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Backend server stopped")
        return True

def main():
    """Main function to run all checks and start backend"""
    print("🌊 Blue Carbon MRV Platform - Backend Startup")
    print("=" * 50)
    
    # Run all checks
    checks = [
        ("Python Version", check_python_version),
        ("Backend Directory", check_backend_directory),
    ]
    
    for check_name, check_func in checks:
        print(f"\n🔍 Checking {check_name}...")
        if not check_func():
            print(f"\n❌ {check_name} check failed. Exiting.")
            sys.exit(1)
    
    # Install dependencies
    print(f"\n📦 Installing Dependencies...")
    if not install_dependencies():
        print("\n❌ Dependency installation failed. Exiting.")
        sys.exit(1)
    
    # Create env file
    print(f"\n⚙️ Setting up Configuration...")
    create_env_file()
    
    # Start backend
    print(f"\n🚀 Starting Backend Server...")
    print("Backend will be available at: http://localhost:8000")
    print("API documentation at: http://localhost:8000/docs")
    print("Press Ctrl+C to stop the server")
    print("=" * 50)
    
    start_backend()

if __name__ == "__main__":
    main()