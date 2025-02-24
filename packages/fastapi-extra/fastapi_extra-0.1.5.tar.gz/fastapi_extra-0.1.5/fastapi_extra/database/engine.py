__author__ = "ziyan.yin"
__date__ = "2024-12-26"


from typing import Any, Literal

from pydantic import AnyUrl, BaseModel, Field
from sqlalchemy import Engine, NullPool
from sqlalchemy.util import _concurrency_py3k
from sqlmodel import create_engine

from fastapi_extra.settings import Settings


class DatabaseConfig(BaseModel):
    url: AnyUrl
    echo: bool = False
    echo_pool: bool = False
    isolation_level: Literal[
        "SERIALIZABLE",
        "REPEATABLE READ",
        "READ COMMITTED",
        "READ UNCOMMITTED",
        "AUTOCOMMIT",
    ] | None = None
    options: dict = Field(default_factory=dict)


class DefaultDatabaseSettings(Settings):
    datasource: DatabaseConfig
    

def load_engine(config: DatabaseConfig, **kw: Any) -> Engine:
    return create_engine(
        url=str(config.url),
        **config.model_dump(exclude_defaults=True, exclude={"url", "options"}), 
        **config.options,
        **kw
    )
    

_settings = DefaultDatabaseSettings()  # type: ignore
if _settings.mode == "test":
    DEFAULT_ENGINE: Engine = load_engine(_settings.datasource, poolclass=NullPool)
else:
    DEFAULT_ENGINE: Engine = load_engine(_settings.datasource)


async def dispose() -> None:
    await _concurrency_py3k.greenlet_spawn(DEFAULT_ENGINE.dispose)
