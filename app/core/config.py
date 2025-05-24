from pydantic import BaseSettings, AnyHttpUrl
from typing import List


class Settings(BaseSettings):
    # App metadata
    app_name: str = "Vote Compass"
    version: str = "0.1.0"
    debug: bool = False

    # Core URLs
    database_url: str
    redis_url: str

    # CORS
    cors_origins: List[AnyHttpUrl] = ["http://localhost:3000"]

    # Security
    secret_key: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True


# Instantiate once and import elsewhere
settings = Settings()
