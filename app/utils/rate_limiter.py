from slowapi import Limiter
from slowapi.util import get_remote_address
from app.redis_client import get_redis

limiter = Limiter(
    key_func=get_remote_address,
    storage_uri="memory://"
)