from pydantic_settings import BaseSettings
from typing import Optional, List
import os


class Settings(BaseSettings):
    # API Keys
    OPENROUTER_API_KEY: str
    PINECONE_API_KEY: str
    PINECONE_ENVIRONMENT: str
    HUGGINGFACE_API_KEY: str

    # Database
    DATABASE_URL: str

    # Redis
    REDIS_URL: str

    # Celery
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str

    # App
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_PREFIX: str = "/api/v1"
    PROJECT_NAME: str = "AI Research Agent"
    VERSION: str = "1.0.0"

    # CORS
    FRONTEND_URL: str = "http://localhost:3000"
    # ALLOWED_ORIGINS: List[str] = ["http://localhost:3000", "http://127.0.0.1:3000"]

    ALLOWED_ORIGINS: str = "http://localhost:3000,http://127.0.0.1:3000"

    @property
    def allowed_origins_list(self) -> List[str]:
        """Convert the comma-separated string to a list of origins."""
        return [
            origin.strip()
            for origin in self.ALLOWED_ORIGINS.split(",")
            if origin.strip()
        ]

    class Config:
        env_file = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))), ".env"
        )
        case_sensitive = True


settings = Settings()
