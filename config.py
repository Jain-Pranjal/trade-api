'''
This file uses Pydantic's BaseSettings to manage configuration settings.
USAGE:
from config import settings
# Access any environment variable
api_key = settings.GEMINI_API_KEY
'''

from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # API Keys
    GEMINI_API_KEY: str
    
    # Security
    JWT_SECRET: str = "mine-super-secret-change-in-production"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # Rate Limiting
    RATE_LIMIT: int = 5  # requests per minute
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # Application
    APP_NAME: str = "Trade API"
    DEBUG: bool = True
    ENVIRONMENT: str = "development"  # development, staging, production
    
    # Database (optional - for future use)
    DATABASE_URL: Optional[str] = None
    
    # CORS
    CORS_ORIGINS: str = "*"  # Comma-separated list of allowed origins
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True

settings = Settings()





