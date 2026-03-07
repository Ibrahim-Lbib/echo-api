from typing import Optional, List
import json
from app.redis_client import get_redis

def get_cached_recommendations(key: str) -> Optional[List[dict]]:
    redis = get_redis()
    value = redis.get(key)
    if value:
        return json.loads(value)
    return None

def set_cached_recommendations(key: str, value: List[dict], ttl: int = 300) -> None:
    redis = get_redis()
    redis.set(key, json.dumps(value), ex=ttl)