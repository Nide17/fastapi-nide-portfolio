import os
from functools import lru_cache


class Settings:
    SECRET_KEY: str = os.environ.get("SECRET_KEY", "your-secret-key-change-in-production")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return settings