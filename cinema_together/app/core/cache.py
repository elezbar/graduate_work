import orjson

from abc import ABCMeta, abstractmethod
from redis import ConnectionError, RedisError
from redis.asyncio import Redis as Reddis
from typing import Any

from core.backoff import backoff_function

redis: Reddis | None = None


class BaseCacheStorage(metaclass=ABCMeta):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    async def get(self, key: str) -> str | None:
        pass

    @abstractmethod
    async def set(self, key: str, value: str) -> Any:
        pass

    @abstractmethod
    async def expire(self, key: str, timeout: int = 3600) -> None:
        pass

    @abstractmethod
    async def delete(self, key: str) -> None:
        pass

    @abstractmethod
    async def close(self) -> None:
        pass


class Redis(BaseCacheStorage):
    def __init__(self, redis: Reddis):
        self.redis = redis

    @backoff_function(RedisError, ConnectionError)
    async def get(self, key: str) -> Any:
        getted = await self.redis.get(key)
        if getted:
            return orjson.loads(getted)
        return None

    @backoff_function(RedisError, ConnectionError)
    async def set(self, key: str, value: Any) -> Any:
        return await self.redis.set(key, orjson.dumps(value))

    async def expire(self, key: str, timeout: int = 3600) -> None:
        await self.redis.expire(key, timeout)

    async def delete(self, key: str) -> None:
        await self.redis.delete(key)

    async def close(self) -> None:
        await self.redis.close()


def get_redis() -> Reddis:
    if not redis:
        raise Exception("Redis not initialized yet.")
    return redis
