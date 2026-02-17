import redis
import json
import hashlib
from typing import Optional, Any
import os

class RedisCache:
    def __init__(self):
        try:
            self.redis_client = redis.Redis(
                host=os.getenv('REDIS_HOST', 'redis'),
                port=int(os.getenv('REDIS_PORT', 6379)),
                db=0,
                decode_responses=True
            )
            # Test connection
            self.redis_client.ping()
            self.enabled = True
            print("✅ Redis cache initialized successfully")
        except Exception as e:
            print(f"⚠️ Redis not available: {e}")
            print("⚠️ Running without cache")
            self.enabled = False
            self.redis_client = None
    
    def get(self, key: str) -> Optional[Any]:
        """Отримати значення з кешу"""
        if not self.enabled:
            return None
            
        try:
            value = self.redis_client.get(key)
            if value:
                return json.loads(value)
            return None
        except Exception as e:
            print(f"Redis get error: {e}")
            return None
    
    def set(self, key: str, value: Any, expire: int = 3600):
        """Зберегти в кеш (expire в секундах)"""
        if not self.enabled:
            return False
            
        try:
            self.redis_client.setex(
                key,
                expire,
                json.dumps(value)
            )
            return True
        except Exception as e:
            print(f"Redis set error: {e}")
            return False
    
    def delete(self, key: str):
        """Видалити з кешу"""
        if not self.enabled:
            return False
            
        try:
            self.redis_client.delete(key)
            return True
        except Exception as e:
            print(f"Redis delete error: {e}")
            return False
    
    def generate_key(self, prefix: str, *args) -> str:
        """Генерувати унікальний ключ"""
        combined = f"{prefix}:" + ":".join(str(arg) for arg in args)
        return hashlib.md5(combined.encode()).hexdigest()

# Глобальний екземпляр
cache = RedisCache()
