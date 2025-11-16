"""Application configuration settings"""

from pydantic_settings import BaseSettings
from pydantic import Field, validator
from typing import List, Optional
import os


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""
    
    # Application Settings
    APP_NAME: str = "AI-Homework-Management-System"
    APP_VERSION: str = "1.0.0"
    ENVIRONMENT: str = "development"
    DEBUG: bool = True
    SECRET_KEY: str = Field(..., min_length=32)
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    
    # Database Configuration
    DATABASE_URL: str = Field(..., description="PostgreSQL database URL")
    DATABASE_POOL_SIZE: int = 20
    DATABASE_MAX_OVERFLOW: int = 10
    
    # Redis Configuration
    REDIS_URL: str = "redis://localhost:6379/0"
    CELERY_BROKER_URL: str = "redis://localhost:6379/1"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/2"
    
    # JWT Authentication
    JWT_SECRET_KEY: str = Field(..., min_length=32)
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    # ML Model Configuration
    MODEL_BASE_PATH: str = "./data/models"
    LLAMA_MODEL_NAME: str = "meta-llama/Llama-3.2-3B"
    DEVICE: str = "cuda"
    MAX_LENGTH: int = 2048
    TEMPERATURE: float = 0.7
    TOP_P: float = 0.9
    TOP_K: int = 50
    
    # HuggingFace Configuration
    HUGGINGFACE_TOKEN: Optional[str] = None
    
    # Question Generation Settings
    MIN_QUESTIONS_PER_HOMEWORK: int = 5
    MAX_QUESTIONS_PER_HOMEWORK: int = 15
    MCQ_OPTIONS_COUNT: int = 4
    HOMEWORK_PER_SUBJECT_PER_WEEK: int = 2
    
    # Grading Configuration
    AUTO_GRADE_THRESHOLD: float = 0.85
    SIMILARITY_THRESHOLD: float = 0.75
    
    # Performance Analytics
    PERFORMANCE_CALCULATION_INTERVAL: str = "daily"
    REPORT_GENERATION_DAY: int = 1
    
    # Email Configuration
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: Optional[str] = None
    SMTP_PASSWORD: Optional[str] = None
    EMAIL_FROM: str = "noreply@homework-system.com"
    
    # File Upload
    MAX_UPLOAD_SIZE_MB: int = 10
    ALLOWED_EXTENSIONS: List[str] = [".txt", ".pdf", ".docx"]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "./logs/app.log"
    
    # CORS Settings
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    CORS_ALLOW_CREDENTIALS: bool = True
    
    @validator("CORS_ORIGINS", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("ALLOWED_EXTENSIONS", pre=True)
    def parse_allowed_extensions(cls, v):
        if isinstance(v, str):
            return [ext.strip() for ext in v.split(",")]
        return v
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Global settings instance
settings = Settings()


# Create necessary directories
def create_directories():
    """Create necessary directories for the application"""
    directories = [
        "data/raw",
        "data/processed",
        "data/models",
        "logs",
        "uploads"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)


if __name__ != "__main__":
    create_directories()

