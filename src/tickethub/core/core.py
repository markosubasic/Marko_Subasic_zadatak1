import json
import asyncio

from tickethub.core.config import get_settings

try:
    import redis.asyncio as redis
except ImportError:
    redis = None


class Cache:
    def __init__(self):
        settings = get_settings()
        self._ttl = settings.cache_ttl
        self._mem: dict[str, str] = {}
        self._redis = (
            redis.from_url(settings.redis_url) if settings.redis_url and redis else None
        )

    async def get(self, key: str):
        if self._redis:
            data = await self._redis.get(key)
            return json.loads(data.decode()) if data else None
        return self._mem.get(key)

    async def set(self, key: str, value, ttl: int | None = None):
        ttl = ttl or self._ttl
        if self._redis:
            await self._redis.set(key, json.dumps(value), ex=ttl)
        else:
            self._mem[key] = value
            asyncio.get_running_loop().call_later(ttl, self._mem.pop, key, None)


cache = Cache()
