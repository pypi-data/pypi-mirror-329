__author__ = "ziyan.yin"
__date__ = "2024-12-26"


from typing import Literal

from pydantic import AnyUrl, BaseModel, Field
from sqlalchemy import Engine, NullPool
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.util import _concurrency_py3k
from sqlmodel import Session, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_extra.dependency import AbstractWidget
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


_settings = DefaultDatabaseSettings()  # type: ignore
_loaded_engines: list[Engine] = []


class DB(AbstractWidget):
    default_config = _settings.datasource
    default_options = {}
    
    def __init__(self):
        self._engine = None
    
    @property
    def engine(self) -> Engine:
        if not self._engine:
            self._engine = create_engine(
                url=str(self.default_config.url),
                **self.default_config.model_dump(exclude_defaults=True, exclude={"url", "options"}), 
                **self.default_config.options,
                **self.default_options
            )
            _loaded_engines.append(self._engine)
        return self._engine

    @property
    def session(self) -> Session:
        return Session(self.engine)


class AsyncDB(DB):
    
    @property
    def engine(self) -> AsyncEngine:
        return AsyncEngine(super().engine)

    @property
    def session(self) -> AsyncSession:
        return AsyncSession(self.engine)
        

if _settings.mode == "test":
    DB.default_options = {"poolclass": NullPool}


async def dispose() -> None:
    for engine in _loaded_engines:
        await _concurrency_py3k.greenlet_spawn(engine.dispose)
