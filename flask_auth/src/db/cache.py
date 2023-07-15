from abc import ABCMeta, abstractmethod
from typing import Any

import orjson
from redis import Redis as Reddis

from core.config import config

redis: Reddis | None = None


class BaseCacheStorage(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    def set(self, key: str, value: str) -> Any:
        pass

    @abstractmethod
    def expire(self, key: str, timeout: int = 3600) -> None:
        pass

    @abstractmethod
    def delete(self, key: str) -> None:
        pass

    @abstractmethod
    def close(self) -> None:
        pass


class Redis(BaseCacheStorage):
    def __init__(self, redis: Reddis):
        self.redis = redis

    def get(self, key: str) -> Any:
        getted = self.redis.get(key)
        if getted:
            return orjson.loads(getted)
        return None

    def set(self, key: str, value: Any) -> Any:
        return self.redis.set(key, orjson.dumps(value))

    def expire(self, key: str, timeout: int = config.cache.cache_time_default) -> None:
        self.redis.expire(key, timeout)

    def delete(self, key: str) -> None:
        self.redis.delete(key)

    def close(self) -> None:
        self.redis.close()


def get_redis() -> Reddis:
    if not redis:
        raise Exception("Redis not initialized yet.")
    return redis
