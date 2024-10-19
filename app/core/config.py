from pydantic_settings import BaseSettings
import os

class Settings(BaseSettings):
    STAGE: str = os.getenv("STAGE", "development")
    
    # Redis configuration for database
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0 if STAGE == "production" else 1
    
    # Redis configuration for task broker
    REDIS_BROKER_HOST: str = "localhost"
    REDIS_BROKER_PORT: int = 6379
    REDIS_BROKER_DB: int = 2

    # Other settings...

    class Config:
        env_file = ".env"

settings = Settings()
