from typing import Optional, List
import json
import logging

logger = logging.getLogger(__name__)

def get_cached_recommendations(key: str) -> Optional[List[dict]]:
    try:
        from app.redis_client import get_redis
        redis = get_redis()
        value = redis.get(key)
        if value:
            return json.loads(value)
    except Exception as e:
        logger.warning(f"Cache read failed (skipping cache): {e}")
    return None

def set_cached_recommendations(key: str, value: List[dict], ttl: int = 300) -> None:
    try:
        from app.redis_client import get_redis
        redis = get_redis()
        redis.set(key, json.dumps(value), ex=ttl)
    except Exception as e:
        logger.warning(f"Cache write failed (skipping cache): {e}")