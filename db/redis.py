import json
from typing import Optional

from loguru import logger

import settings
from redis import Redis, from_url


class RedisProvider:
    def __init__(self, conf):
        self.redis: Optional[Redis] = None
        self.conf = conf  # "redis://redis:6379/"

    def init(self):
        self.redis = from_url(self.conf)

    def keys(self, pattern: str = "*"):
        return self.redis.keys(pattern)

    def set(self, key, value):
        return self.redis.set(key, json.dumps(value))

    def get(self, key):
        if not self.redis.exists(key):
            return None
        return json.loads(self.redis.get(key))

    def close(self):
        self.redis.close()

    def is_connected(self) -> bool:
        try:
            self.redis.ping()
            return True
        except Exception as ex:
            logger.error(ex)
            return False


redis = RedisProvider(settings.redis_url)
