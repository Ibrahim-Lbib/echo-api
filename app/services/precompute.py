from app.services.engine import get_recommendations
from app.redis_client import get_redis
import json

def precompute_popular_recommendations(limit=10):
    recs = get_recommendations(user_id=None, limit=limit)  # Anonymous/top
    redis = get_redis()
    redis.set("popular_recs", json.dumps(recs), ex=3600)  # 1 hour
    print("Precomputed popular recommendations")