from pydantic import BaseSettings

class Settings(BaseSettings):
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    REDIS_HOST: str = "redis"
    REDIS_PORT: int = 11

    class Config:
        env_file = ".env"

settings = Settings()