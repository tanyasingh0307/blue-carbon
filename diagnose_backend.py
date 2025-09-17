#!/usr/bin/env python3
"""
Backend Diagnostic and Fix Script
Identifies and resolves common backend startup issues
"""

import sys
import os
import subprocess
import platform
from pathlib import Path

def print_header(title):
    print(f"\n{'='*60}")
    print(f"🔍 {title}")
    print('='*60)

def print_success(message):
    print(f"✅ {message}")

def print_error(message):
    print(f"❌ {message}")

def print_warning(message):
    print(f"⚠️  {message}")

def print_info(message):
    print(f"ℹ️  {message}")

def check_python_version():
    """Check Python version compatibility"""
    print_header("Python Version Check")
    
    version = sys.version_info
    print_info(f"Python version: {version.major}.{version.minor}.{version.micro}")
    
    if version.major < 3:
        print_error("Python 3 is required")
        return False
    elif version.minor < 8:
        print_error("Python 3.8 or higher is required")
        return False
    else:
        print_success(f"Python {version.major}.{version.minor} is compatible")
        return True

def check_directory_structure():
    """Check if backend directory structure exists"""
    print_header("Directory Structure Check")
    
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print_error("Backend directory not found")
        return False
    
    required_files = [
        "backend/main.py",
        "backend/requirements.txt",
        "backend/core/config.py",
        "backend/routers/__init__.py",
        "backend/models/__init__.py",
        "backend/schemas/__init__.py",
        "backend/services/__init__.py",
        "backend/database/__init__.py"
    ]
    
    missing_files = []
    for file_path in required_files:
        if not Path(file_path).exists():
            missing_files.append(file_path)
    
    if missing_files:
        print_error("Missing required files:")
        for file in missing_files:
            print(f"  - {file}")
        return False
    else:
        print_success("All required files present")
        return True

def install_dependencies():
    """Install Python dependencies"""
    print_header("Installing Dependencies")
    
    try:
        # Change to backend directory
        os.chdir("backend")
        
        # Upgrade pip first
        print_info("Upgrading pip...")
        subprocess.run([sys.executable, "-m", "pip", "install", "--upgrade", "pip"], 
                      check=True, capture_output=True, text=True)
        
        # Install requirements
        print_info("Installing requirements...")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"], 
                               capture_output=True, text=True)
        
        if result.returncode == 0:
            print_success("Dependencies installed successfully")
            return True
        else:
            print_error("Failed to install dependencies:")
            print(result.stderr)
            return False
            
    except subprocess.CalledProcessError as e:
        print_error(f"Installation failed: {e}")
        return False
    except Exception as e:
        print_error(f"Unexpected error: {e}")
        return False
    finally:
        # Change back to root directory
        os.chdir("..")

def test_imports():
    """Test if critical imports work"""
    print_header("Testing Critical Imports")
    
    imports_to_test = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("sqlalchemy", "SQLAlchemy"),
        ("pydantic", "Pydantic"),
        ("jose", "Python JOSE"),
        ("passlib", "Passlib")
    ]
    
    failed_imports = []
    
    for module, name in imports_to_test:
        try:
            __import__(module)
            print_success(f"{name} imported successfully")
        except ImportError as e:
            print_error(f"{name} import failed: {e}")
            failed_imports.append(module)
    
    return len(failed_imports) == 0

def create_env_file():
    """Create .env file if it doesn't exist"""
    print_header("Environment Configuration")
    
    env_path = Path("backend/.env")
    env_example_path = Path("backend/.env.example")
    
    if env_path.exists():
        print_success(".env file already exists")
        return True
    
    if env_example_path.exists():
        # Copy from example
        env_content = env_example_path.read_text()
        env_path.write_text(env_content)
        print_success("Created .env file from .env.example")
        return True
    else:
        # Create basic .env file
        basic_env = """# Backend Environment Variables
DATABASE_URL=sqlite:///./bluecarbon.db
SECRET_KEY=your-secret-key-change-in-production-12345678901234567890
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API Configuration
API_V1_STR=/api
PROJECT_NAME=Blue Carbon MRV Platform

# File Upload
UPLOAD_DIR=./uploads
MAX_FILE_SIZE=10485760

# ML Configuration
ENABLE_ML_PROCESSING=true
"""
        env_path.write_text(basic_env)
        print_success("Created basic .env file")
        return True

def create_missing_directories():
    """Create missing directories"""
    print_header("Creating Missing Directories")
    
    directories = [
        "backend/uploads",
        "backend/ml/models"
    ]
    
    for dir_path in directories:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        print_success(f"Created directory: {dir_path}")

def test_database_connection():
    """Test database connection"""
    print_header("Testing Database Connection")
    
    try:
        # Change to backend directory
        original_dir = os.getcwd()
        os.chdir("backend")
        
        # Add backend to Python path
        sys.path.insert(0, os.getcwd())
        
        from database.database import engine, Base
        from sqlalchemy import text
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print_success("Database connection successful")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print_success("Database tables created")
        
        return True
        
    except Exception as e:
        print_error(f"Database test failed: {e}")
        return False
    finally:
        os.chdir(original_dir)
        if os.getcwd() in sys.path:
            sys.path.remove(os.getcwd())

def fix_import_issues():
    """Fix common import issues"""
    print_header("Fixing Import Issues")
    
    # Create __init__.py files if missing
    init_files = [
        "backend/__init__.py",
        "backend/core/__init__.py",
        "backend/routers/__init__.py",
        "backend/models/__init__.py",
        "backend/schemas/__init__.py",
        "backend/services/__init__.py",
        "backend/database/__init__.py"
    ]
    
    for init_file in init_files:
        init_path = Path(init_file)
        if not init_path.exists():
            init_path.parent.mkdir(parents=True, exist_ok=True)
            init_path.write_text("# Package initialization\n")
            print_success(f"Created {init_file}")

def start_backend():
    """Attempt to start the backend"""
    print_header("Starting Backend Server")
    
    try:
        os.chdir("backend")
        print_info("Starting server at http://localhost:8000")
        print_info("API docs will be available at http://localhost:8000/docs")
        print_info("Press Ctrl+C to stop the server")
        print("-" * 60)
        
        # Start the server
        subprocess.run([
            sys.executable, "-m", "uvicorn", "main:app", 
            "--reload", "--host", "0.0.0.0", "--port", "8000"
        ])
        
    except KeyboardInterrupt:
        print_info("\nServer stopped by user")
    except Exception as e:
        print_error(f"Failed to start server: {e}")
        return False
    finally:
        os.chdir("..")

def main():
    """Main diagnostic and fix function"""
    print("🌊 Blue Carbon MRV Platform - Backend Diagnostic Tool")
    print("This tool will diagnose and fix common backend issues")
    
    # Run all checks and fixes
    checks = [
        ("Python Version", check_python_version),
        ("Directory Structure", check_directory_structure),
        ("Environment File", create_env_file),
        ("Missing Directories", create_missing_directories),
        ("Import Issues", fix_import_issues),
        ("Dependencies", install_dependencies),
        ("Import Test", test_imports),
        ("Database Connection", test_database_connection)
    ]
    
    failed_checks = []
    
    for check_name, check_func in checks:
        try:
            if not check_func():
                failed_checks.append(check_name)
        except Exception as e:
            print_error(f"Error in {check_name}: {e}")
            failed_checks.append(check_name)
    
    # Summary
    print_header("Diagnostic Summary")
    
    if failed_checks:
        print_error("The following checks failed:")
        for check in failed_checks:
            print(f"  - {check}")
        print_warning("Please fix these issues before starting the backend")
        return False
    else:
        print_success("All checks passed! Backend should be ready to start")
        
        # Ask if user wants to start the server
        try:
            response = input("\nWould you like to start the backend server now? (y/n): ").lower().strip()
            if response in ['y', 'yes']:
                start_backend()
        except KeyboardInterrupt:
            print_info("\nExiting...")
        
        return True

if __name__ == "__main__":
    main()