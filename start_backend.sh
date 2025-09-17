#!/bin/bash

echo "🌊 Blue Carbon Backend Startup Script"
echo "======================================"

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Backend directory not found or main.py missing"
    echo "💡 Make sure you're in the project root directory"
    exit 1
fi

echo "📁 Changing to backend directory..."
cd backend

echo "📦 Installing dependencies..."
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt

echo "⚙️  Setting up environment..."
if [ ! -f ".env" ]; then
    cp .env.example .env 2>/dev/null || echo "DATABASE_URL=sqlite:///./bluecarbon.db
SECRET_KEY=your-secret-key-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
API_V1_STR=/api
PROJECT_NAME=Blue Carbon MRV Platform" > .env
    echo "✅ Created .env file"
fi

echo "📂 Creating directories..."
mkdir -p uploads
mkdir -p ml/models

echo "🚀 Starting backend server..."
echo "📍 Server: http://localhost:8000"
echo "📚 API Docs: http://localhost:8000/docs"
echo "🛑 Press Ctrl+C to stop"
echo "--------------------------------------"

python3 -m uvicorn main:app --reload --host 0.0.0.0 --port 8000