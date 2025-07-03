import redis
import json

REDIS_HOST = 'localhost'
REDIS_PORT = 6379

class RedisCache:
    def __init__(self):
        self.r = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def get(self, key):
        val = self.r.get(key)
        return json.loads(val) if val else None

    def set(self, key, value, ttl=3600):
        self.r.set(key, json.dumps(value), ex=ttl)

cache_response = RedisCache()
