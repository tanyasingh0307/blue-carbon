#!/usr/bin/env python3
"""
Simple Backend Starter
Minimal script to start the backend with error handling
"""

import sys
import os
import subprocess
from pathlib import Path

def main():
    print("🌊 Starting Blue Carbon Backend...")
    
    # Check if we're in the right directory
    if not Path("main.py").exists():
        print("❌ main.py not found. Make sure you're in the backend directory")
        print("💡 Try: cd backend && python simple_start.py")
        return False
    
    # Check if .env exists
    if not Path(".env").exists():
        print("📝 Creating .env file...")
        env_content = """DATABASE_URL=sqlite:///./bluecarbon.db
SECRET_KEY=your-secret-key-change-in-production-12345678901234567890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api
PROJECT_NAME=Blue Carbon MRV Platform
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760
ENABLE_ML_PROCESSING=true
"""
        Path(".env").write_text(env_content)
        print("✅ Created .env file")
    
    # Create uploads directory
    Path("uploads").mkdir(exist_ok=True)
    
    try:
        print("🚀 Starting server...")
        print("📍 Server will be available at: http://localhost:8000")
        print("📚 API docs will be available at: http://localhost:8000/docs")
        print("🛑 Press Ctrl+C to stop")
        print("-" * 50)
        
        # Start with minimal options
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app",
            "--host", "127.0.0.1", 
            "--port", "8000",
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped")
    except FileNotFoundError:
        print("❌ uvicorn not found. Installing...")
        subprocess.run([sys.executable, "-m", "pip", "install", "uvicorn[standard]"])
        print("✅ Please run the script again")
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        print("\n🔧 Troubleshooting:")
        print("1. Make sure you're in the backend directory")
        print("2. Install dependencies: pip install -r requirements.txt")
        print("3. Check Python version (3.8+ required)")
        return False

if __name__ == "__main__":
    main()