"""
Database configuration and session management
SQLAlchemy setup with better error handling
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from core.config import settings

# Ensure database directory exists
db_dir = os.path.dirname(settings.DATABASE_URL.replace('sqlite:///', ''))
if db_dir and not os.path.exists(db_dir):
    os.makedirs(db_dir, exist_ok=True)

# Create SQLAlchemy engine
try:
    engine = create_engine(
        settings.DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
        echo=False  # Set to True for SQL debugging
    )
except Exception as e:
    print(f"❌ Database engine creation failed: {e}")
    # Fallback to simple SQLite
    engine = create_engine("sqlite:///./bluecarbon.db", connect_args={"check_same_thread": False})

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()

def get_db():
    """Dependency to get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()