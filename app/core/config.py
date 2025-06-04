import os
from typing import List, Any
from urllib.parse import urlparse

def _get_list(env_var: str, default: List[str]) -> List[str]:
    val = os.getenv(env_var)
    return val.split(",") if val else default

class Settings:
    # App metadata
    app_name: str = "Vote Compass"
    version: str = "0.1.0"
    debug: bool = os.getenv("DEBUG", "false").lower() in ("1", "true", "yes")

    # Required service URLs (fall back to sensible defaults for local Docker)
    database_url: str = os.getenv(
        "DATABASE_URL",
        "postgresql+psycopg2://compass:compass@db:5432/vote_compass"
    )
    redis_url: str = os.getenv(
        "REDIS_URL",
        "redis://redis:6379/0"
    )

    # CORS origins
    cors_origins: List[str] = _get_list(
        "CORS_ORIGINS",
        ["http://localhost:3000"]
    )

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "super-secret-key")


# Single global settings object
settings = Settings()
