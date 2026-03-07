from upstash_redis import Redis
import os

_redis: Redis | None = None

def get_redis() -> Redis:
    global _redis
    if _redis is None:
        url = os.getenv("UPSTASH_REDIS_REST_URL")
        token = os.getenv("UPSTASH_REDIS_REST_TOKEN")
        if not url or not token:
            raise ValueError("Missing Upstash Redis credentials")
        _redis = Redis(url=url, token=token)
    return _redis