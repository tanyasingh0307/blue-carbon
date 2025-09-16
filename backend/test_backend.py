"""
Test script to verify backend dependencies and setup
"""

def test_imports():
    """Test if all required packages can be imported"""
    try:
        import fastapi
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        import uvicorn
        print("✅ Uvicorn imported successfully")
    except ImportError as e:
        print(f"❌ Uvicorn import failed: {e}")
        return False
    
    try:
        import sqlalchemy
        print("✅ SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"❌ SQLAlchemy import failed: {e}")
        return False
    
    try:
        import pydantic
        print("✅ Pydantic imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic import failed: {e}")
        return False
    
    try:
        from pydantic_settings import BaseSettings
        print("✅ Pydantic Settings imported successfully")
    except ImportError as e:
        print(f"❌ Pydantic Settings import failed: {e}")
        return False
    
    try:
        from jose import jwt
        print("✅ Python JOSE imported successfully")
    except ImportError as e:
        print(f"❌ Python JOSE import failed: {e}")
        return False
    
    try:
        from passlib.context import CryptContext
        print("✅ Passlib imported successfully")
    except ImportError as e:
        print(f"❌ Passlib import failed: {e}")
        return False
    
    return True

def test_database():
    """Test database connection"""
    try:
        from database.database import engine, Base
        from sqlalchemy import text
        
        # Test connection
        with engine.connect() as conn:
            result = conn.execute(text("SELECT 1"))
            print("✅ Database connection successful")
        
        # Create tables
        Base.metadata.create_all(bind=engine)
        print("✅ Database tables created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False

def test_config():
    """Test configuration loading"""
    try:
        from core.config import settings
        print(f"✅ Configuration loaded successfully")
        print(f"   - Database URL: {settings.DATABASE_URL}")
        print(f"   - API Base: {settings.API_V1_STR}")
        print(f"   - Upload Dir: {settings.UPLOAD_DIR}")
        return True
    except Exception as e:
        print(f"❌ Configuration test failed: {e}")
        return False

if __name__ == "__main__":
    print("🧪 Testing Backend Setup...")
    print("=" * 50)
    
    all_tests_passed = True
    
    print("\n📦 Testing Package Imports...")
    if not test_imports():
        all_tests_passed = False
    
    print("\n⚙️ Testing Configuration...")
    if not test_config():
        all_tests_passed = False
    
    print("\n🗄️ Testing Database...")
    if not test_database():
        all_tests_passed = False
    
    print("\n" + "=" * 50)
    if all_tests_passed:
        print("🎉 All tests passed! Backend should be ready to run.")
        print("\nTo start the backend, run:")
        print("cd backend && python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000")
    else:
        print("❌ Some tests failed. Please check the errors above.")