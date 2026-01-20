"""
API Configuration

Settings for the FastAPI gateway using Pydantic Settings.
"""

from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Settings
    api_title: str = "3DM-API"
    api_description: str = "Unified REST API for Blender and FreeCAD remote control"
    api_version: str = "1.0.0"
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    
    # Blender Socket Server
    blender_host: str = "127.0.0.1"
    blender_port: int = 9876
    blender_timeout: float = 30.0
    
    # FreeCAD Socket Server
    freecad_host: str = "127.0.0.1"
    freecad_port: int = 9877
    freecad_timeout: float = 30.0
    
    # Connection Settings
    connection_pool_size: int = 5
    connection_retry_attempts: int = 3
    connection_retry_delay: float = 1.0
    
    # CORS Settings
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]
    
    # Logging
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"
        env_prefix = "TDM_"


# Global settings instance
settings = Settings()
