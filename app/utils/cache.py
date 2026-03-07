from cachetools import TTLCache
from typing import Any, Optional

# In-memory cache: TTL = 5 minutes (300 seconds) for MVP
cache = TTLCache(maxsize=1000, ttl=300)

def get_cached_recommendations(key: str) -> Optional[Any]:
    return cache.get(key)

def set_cached_recommendations(key: str, value: Any) -> None:
    cache[key] = value