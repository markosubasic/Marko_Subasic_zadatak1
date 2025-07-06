from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    cache_ttl: int = 60  # sekunde
    debug: bool = False


@lru_cache
def get_settings() -> Settings:
    return Settings()
