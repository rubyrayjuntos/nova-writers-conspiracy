"""
🌌 NOVA: The Writers' Conspiracy - Configuration Settings
The sacred configuration that awakens the cosmic atelier
"""

import os
from typing import List, Optional
from pydantic import BaseSettings, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings - the sacred configuration of the conspiracy"""
    
    # Application - the essence of NOVA
    APP_NAME: str = "🌌 NOVA: The Writers' Conspiracy"
    VERSION: str = "1.0.0"
    DEBUG: bool = False
    ENVIRONMENT: str = "development"
    APP_DESCRIPTION: str = "A cosmic atelier where storytellers conspire with AI to birth entire universes"
    
    # Security - the protective sigils
    SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # Database - the neural graveyard where memories live
    DATABASE_URL: str
    
    # Redis - the vessel of dreams and tasks
    REDIS_URL: str
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    
    @validator("CELERY_BROKER_URL", pre=True)
    def assemble_celery_broker_url(cls, v: Optional[str], values: dict) -> str:
        if v:
            return v
        return values.get("REDIS_URL", "redis://localhost:6379/0")
    
    @validator("CELERY_RESULT_BACKEND", pre=True)
    def assemble_celery_result_backend(cls, v: Optional[str], values: dict) -> str:
        if v:
            return v
        return values.get("REDIS_URL", "redis://localhost:6379/0")
    
    # CORS - the bridges between realms
    CORS_ORIGINS: List[str] = ["http://localhost:3000"]
    
    # AI Services - the divine voices of our agents
    OPENAI_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    PINECONE_INDEX_NAME: str = "nova_writers_conspiracy_index"
    SERPER_API_KEY: str
    
    # Optional AI Services - the whispered secrets
    DALLE_API_KEY: Optional[str] = None
    MIDJOURNEY_API_KEY: Optional[str] = None
    
    # File Storage - the vault of creation
    STORAGE_TYPE: str = "local"  # local or s3
    STORAGE_PATH: str = "./storage"
    
    # AWS S3 (if using S3 storage) - the cloud realm
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_REGION: str = "us-east-1"
    AWS_S3_BUCKET: Optional[str] = None
    
    # Email - the messenger of the conspiracy
    SMTP_HOST: Optional[str] = None
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@nova-writers-conspiracy.com"
    FROM_NAME: str = "🌌 NOVA: The Writers' Conspiracy"
    
    # Monitoring - the watchers in the shadows
    SENTRY_DSN: Optional[str] = None
    GOOGLE_ANALYTICS_ID: Optional[str] = None
    
    # Logging - the chronicles of creation
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "json"
    
    # Feature Flags - the sacred switches
    ENABLE_ILLUSTRATION_AGENT: bool = True
    ENABLE_EXPORT_FEATURES: bool = True
    ENABLE_VERSION_CONTROL: bool = True
    ENABLE_COLLABORATION: bool = True
    
    # Agent Configuration - the divine parameters
    MAX_AGENT_RETRIES: int = 3
    AGENT_TIMEOUT_SECONDS: int = 300
    MAX_TOKENS_PER_REQUEST: int = 4000
    
    # Vector Database - the neural graveyard configuration
    VECTOR_DIMENSION: int = 1536  # OpenAI embedding dimension
    VECTOR_METRIC: str = "cosine"
    
    # Task Queue - the workers of dreams
    CELERY_TASK_SOFT_TIME_LIMIT: int = 600  # 10 minutes
    CELERY_TASK_TIME_LIMIT: int = 900  # 15 minutes
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance - the sacred configuration
settings = Settings()


# Validate required settings - the ritual of verification
def validate_settings():
    """Validate that all required settings are present - the sacred checklist"""
    required_settings = [
        "SECRET_KEY",
        "DATABASE_URL",
        "REDIS_URL",
        "OPENAI_API_KEY",
        "PINECONE_API_KEY",
        "PINECONE_ENVIRONMENT",
        "SERPER_API_KEY",
    ]
    
    missing_settings = []
    for setting in required_settings:
        if not getattr(settings, setting, None):
            missing_settings.append(setting)
    
    if missing_settings:
        raise ValueError(f"Missing required settings: {', '.join(missing_settings)}")


# Validate settings on import - the awakening ritual
try:
    validate_settings()
except ValueError as e:
    print(f"🌌 Configuration error: {e}")
    print("Please check your .env file and ensure all required settings are present.")
    print("The cosmic atelier cannot awaken without the proper configuration.") 