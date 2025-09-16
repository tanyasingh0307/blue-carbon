"""
Configuration settings for the Blue Carbon MRV Platform
Handles environment variables and application settings
"""

from pydantic_settings import BaseSettings
from typing import Optional
import os

class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./bluecarbon.db"
    
    # JWT Authentication
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Blockchain Configuration
    WEB3_PROVIDER_URL: str = "http://127.0.0.1:8545"
    CONTRACT_ADDRESS: Optional[str] = None
    PRIVATE_KEY: Optional[str] = None
    
    # IPFS Configuration
    IPFS_API_URL: str = "https://ipfs.infura.io:5001"
    IPFS_PROJECT_ID: Optional[str] = None
    IPFS_PROJECT_SECRET: Optional[str] = None
    
    # ML Configuration
    ML_MODEL_PATH: str = "./ml/models/"
    ENABLE_ML_PROCESSING: bool = True
    
    # File Upload
    UPLOAD_DIR: str = "./uploads"
    MAX_FILE_SIZE: int = 10485760  # 10MB
    
    # API Configuration
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "Blue Carbon MRV Platform"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()

# Ensure upload directory exists
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)