__author__ = "ziyan.yin"
__date__ = "2025-01-05"


from typing import Annotated, AsyncGenerator, Generator

from fastapi.params import Depends
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlmodel import Session as _Session
from sqlmodel.ext.asyncio.session import AsyncSession

from fastapi_extra.database.engine import DEFAULT_ENGINE, Engine


class SessionMaker(Depends):
    __slots__ = ("engine", )
    
    def __init__(self, engine: Engine):
        super().__init__()
        self.engine = engine
        self.dependency = self

    def __call__(self) -> Generator[_Session, None, None]:
        with _Session(self.engine) as session:
            yield session


class AsyncSessionMaker(SessionMaker):
    
    def __init__(self, engine: Engine):
        super().__init__(engine)
        self.async_engine: AsyncEngine = AsyncEngine(self.engine)
    
    async def __call__(self) -> AsyncGenerator[AsyncSession, None]:
        async with AsyncSession(self.async_engine) as session:
            yield session
            

DefaultSession = Annotated[AsyncSession, AsyncSessionMaker(DEFAULT_ENGINE)]
