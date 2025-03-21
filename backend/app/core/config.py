"""
Configuration settings for the application.
"""

import os
from typing import Optional
from pydantic_settings import BaseSettings
from functools import lru_cache

class Settings(BaseSettings):
    """Application settings."""
    
    # OpenAI Settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL_NAME: str = os.getenv("OPENAI_MODEL_NAME", "gpt-4o-mini")
    
    # Google Search Settings
    GOOGLE_API_KEY: str = os.getenv("GOOGLE_API_KEY", "")
    GOOGLE_CSE_ID: str = os.getenv("GOOGLE_CSE_ID", "")
    
    # News API Settings
    NEWS_API_KEY: str = os.getenv("NEWS_API_KEY", "")
    
    # API Settings
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "FactGuard"
    
    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "allow"  # Allow extra fields from .env file

@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings() 