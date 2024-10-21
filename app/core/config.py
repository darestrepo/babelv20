from pydantic_settings import BaseSettings
from dotenv import load_dotenv
import json
import os
from typing import Dict, Any

load_dotenv()

def get_app_secret() -> Dict[str, Any]:
    """
    Loads and returns the APP_SECRET from environment variables.
    
    Returns:
        Dict[str, Any]: The parsed APP_SECRET as a dictionary.
    """
    app_secret = os.getenv('APP_SECRET')
 
    if app_secret:
        try:
            return json.loads(app_secret)
        except json.JSONDecodeError as e:
            print(f"Error parsing APP_SECRET: {e}")
            print(f"APP_SECRET value: {app_secret}")
            return {}
    return {}

def safe_int_cast(value: Any, default: int) -> int:
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        try:
            return int(value.split('#')[0].strip())  # Remove any comments
        except ValueError:
            print(f"Warning: Could not convert '{value}' to int. Using default value {default}.")
    return default

class Settings(BaseSettings):
    APP_SECRET: str

    @property
    def app_secret_dict(self) -> Dict[str, Any]:
        return get_app_secret()

    @property
    def STAGE(self) -> str:
        return self.app_secret_dict.get('STAGE', 'local')
    
    @property
    def HOST(self) -> str:
        return self.app_secret_dict.get('HOST', '0.0.0.0')

    @property
    def PORT(self) -> int:
        return safe_int_cast(self.app_secret_dict.get('PORT'), 8400)

    @property
    def REDIS_HOST(self) -> str:
        return self.app_secret_dict.get('REDIS_HOST', 'localhost')

    @property
    def REDIS_PORT(self) -> int:
        return safe_int_cast(self.app_secret_dict.get('REDIS_PORT'), 6379)

    @property
    def REDIS_DB(self) -> int:
        return safe_int_cast(self.app_secret_dict.get('REDIS_DB'), 7)
    
    @property
    def REDIS_BROKER_HOST(self) -> str:
        return self.app_secret_dict.get('REDIS_BROKER_HOST', 'localhost')

    @property
    def REDIS_BROKER_PORT(self) -> int:
        return safe_int_cast(self.app_secret_dict.get('REDIS_BROKER_PORT'), 6379)

    @property
    def REDIS_BROKER_DB(self) -> int:
        return safe_int_cast(self.app_secret_dict.get('REDIS_BROKER_DB'), 10)

    class Config:
        env_file = ".env"

settings = Settings()
