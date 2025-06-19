import os
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Application settings.
    """
    API_V1_STR: str = "/api"
    PROJECT_NAME: str = "AWS to Azure Migration Mapping Tool"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: list = ["http://localhost:8080", "http://localhost:3000"]
    
    # CrewAI settings
    CREWAI_VERBOSE: bool = False
    
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")


settings = Settings()
