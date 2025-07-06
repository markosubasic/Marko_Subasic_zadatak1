from functools import lru_cache
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
from pydantic import Field

load_dotenv(".env")


class Settings(BaseSettings):
    redis_url: str | None = Field(None, env="REDIS_URL")
    cache_ttl: int = 60
    jwt_secret: str = Field("change-me", env="JWT_SECRET")
    rate_limit: str = "60/minute"
    log_level: str = "INFO"
    bypass_dummy_auth: bool = Field(False, env="BYPASS_DUMMY_AUTH")


@lru_cache
def get_settings() -> Settings:
    return Settings()
