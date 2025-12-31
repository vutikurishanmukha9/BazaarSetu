"""
BazaarSetu Backend - Configuration Module
"""

from pydantic_settings import BaseSettings
from functools import lru_cache
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Application
    app_name: str = "BazaarSetu API"
    debug: bool = False
    version: str = "1.0.0"
    
    # Database
    database_url: str = "postgresql+asyncpg://localhost:5432/bazaarsetu"
    
    # Security
    secret_key: str = "your-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # External APIs
    data_gov_api_key: Optional[str] = None
    enam_api_key: Optional[str] = None
    data_gov_base_url: str = "https://api.data.gov.in/resource"
    
    # Redis
    redis_url: str = "redis://localhost:6379/0"
    
    # Firebase
    firebase_credentials_path: Optional[str] = None
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()
