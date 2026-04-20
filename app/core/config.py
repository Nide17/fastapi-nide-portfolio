import os
from functools import lru_cache


class Settings:
    SECRET_KEY: str = os.environ.get(
        "SECRET_KEY", "secret_nide_portfolio_key")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    PASSWORD_RESET_TOKEN_EXPIRE_HOURS: int = 1
    MAIL_TEST_MODE: bool = os.environ.get(
        "MAIL_TEST_MODE", "true").lower() == "true"
    MAIL_HOST: str = os.environ.get("MAIL_HOST", "")
    MAIL_PORT: int = int(os.environ.get("MAIL_PORT", "587"))
    MAIL_USER: str = os.environ.get("MAIL_USER", "")
    MAIL_PASS: str = os.environ.get("MAIL_PASS", "")
    MAIL_FROM: str = os.environ.get("MAIL_FROM", "")
    MAIL_FROM_NAME: str = os.environ.get("MAIL_FROM_NAME", "")


settings = Settings()


@lru_cache()
def get_settings() -> Settings:
    return settings
