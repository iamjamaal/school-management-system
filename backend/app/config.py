from pydantic_settings import BaseSettings
from typing import List
import os
import logging


class Settings(BaseSettings):
    # Application
    APP_NAME: str = "School Management System"
    DEBUG: bool = True
    VERSION: str = "1.0.0"
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "app.log"
    
    # Database
    DATABASE_URL: str = "postgresql://postgres:Jamal%403709@localhost:5432/school_db"
    
    # Security
    SECRET_KEY: str = "wGplUMK3Ed-YcJ9v4V1O5qf6-s0ZnJD3CurxJzBCuws"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS
    ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]
    
    # File Upload
    MAX_FILE_SIZE: int = 5242880  # 5MB
    UPLOAD_DIR: str = "./uploads"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings()

# Create upload directory if it doesn't exist
os.makedirs(settings.UPLOAD_DIR, exist_ok=True)

# Configure logging
logging.basicConfig(
    level=getattr(logging, settings.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(settings.LOG_FILE),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)