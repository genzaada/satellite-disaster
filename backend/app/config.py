"""Backend application configuration module."""

import os
from pydantic import BaseModel


class Settings(BaseModel):
    """Application settings schema."""
    APP_NAME: str = os.getenv(
        "APP_NAME",
        "Satellite-Based Multi-Hazard Disaster Early Warning System"
    )
    APP_VERSION: str = os.getenv("APP_VERSION", "0.1.0-alpha")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    CORS_ORIGINS: list[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
    ]


settings = Settings()
