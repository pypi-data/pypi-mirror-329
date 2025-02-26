__author__ = "ziyan.yin"
__date__ = "2025-01-17"


from typing import Annotated, AsyncGenerator

from fastapi.params import Depends
from pydantic import BaseModel, Field, RedisDsn
from redis.asyncio import ConnectionPool, Redis

from fastapi_extra.dependency import AbstractWidget
from fastapi_extra.settings import Settings


class RedisConfig(BaseModel):
    url: RedisDsn = RedisDsn("redis://localhost:6379/0")
    max_connections: int | None = None
    connection_kwargs: dict = Field(default_factory=dict)


class DefaultRedisSettings(Settings):
    redis: RedisConfig


_settings = DefaultRedisSettings()  # type: ignore
_loaded_pools: list[ConnectionPool] = []


class RedisCli(AbstractWidget):
    default_config = _settings.redis

    
    def __init__(self):
        self._pool = None
    
    @property
    def pool(self) -> ConnectionPool:
        if not self._pool:
            self._pool = ConnectionPool.from_url(
                self.default_config.url, 
                **self.default_config.model_dump(exclude_defaults=True, exclude={"url", "connection_kwargs"}), 
                **self.default_config.connection_kwargs
            )
            _loaded_pools.append(self)
        return self._pool


async def dispose() -> None:
    for redis_pool in _loaded_pools:
        redis_pool.aclose()



async def get_redis(redis_cli: RedisCli) -> AsyncGenerator[Redis, None]:
    async with Redis(connection_pool=redis_cli.pool) as redis:
        yield redis


DefaultRedis = Annotated[Redis, Depends(get_redis)]
