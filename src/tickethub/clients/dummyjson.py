import httpx
from functools import lru_cache

BASE_URL = "https://dummyjson.com"


@lru_cache
def _client() -> httpx.AsyncClient:
    return httpx.AsyncClient(base_url=BASE_URL, timeout=10.0, http2=True)


async def fetch_todos() -> list[dict]:
    res = await _client().get("/todos?limit=150")
    res.raise_for_status()
    return res.json()["todos"]


async def fetch_users() -> dict[int, str]:
    res = await _client().get("/users?limit=100")
    res.raise_for_status()
    users = res.json()["users"]
    return {u["id"]: u["username"] for u in users}
