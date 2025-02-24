__author__ = "ziyan.yin"
__date__ = "2025-01-17"


from typing import Annotated, AsyncGenerator

from fastapi.params import Depends
from pydantic import BaseModel, Field, RedisDsn
from redis.asyncio import ConnectionPool, Redis

from fastapi_extra.settings import Settings


class RedisConfig(BaseModel):
    url: RedisDsn = RedisDsn("redis://localhost:6379/0")
    max_connections: int | None = None
    connection_kwargs: dict = Field(default_factory=dict)


class DefaultRedisSettings(Settings):
    redis: RedisConfig


def load_pool(config: RedisConfig) -> ConnectionPool:
    return ConnectionPool.from_url(
        config.url, 
        **config.model_dump(exclude_defaults=True, exclude={"url", "connection_kwargs"}), 
        **config.connection_kwargs
    )


_settings = DefaultRedisSettings()  # type: ignore
DEFAULT_POOL = load_pool(_settings.redis)


async def dispose() -> None:
    await DEFAULT_POOL.aclose()


class RedisMaker(Depends):
    
    def __init__(self, pool: ConnectionPool):
        super().__init__()
        self.dependency = self
        self.pool = pool
    
    async def __call__(self) -> AsyncGenerator[Redis, None]:
        async with Redis(connection_pool=self.pool) as session:
            yield session


RedisCli = Annotated[Redis, RedisMaker(DEFAULT_POOL)]
