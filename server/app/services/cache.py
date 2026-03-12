
import redis
import json
from typing import Any, Optional
from app.core.config import settings

class CacheService:
    def __init__(self):
        self.redis_client = redis.from_url(
            settings.REDIS_URL,
            decode_responses=True
        )
    
    def get(self, key: str) -> Optional[Any]:
        value = self.redis_client.get(key)
        if value:
            return json.loads(value)
        return None
    
    def set(self, key: str, value: Any, expiry: int = 3600):
        self.redis_client.setex(
            key,
            expiry,
            json.dumps(value)
        )
    
    def delete(self, key: str):
        self.redis_client.delete(key)
    
    def exists(self, key: str) -> bool:
        return self.redis_client.exists(key) > 0

cache_service = CacheService()