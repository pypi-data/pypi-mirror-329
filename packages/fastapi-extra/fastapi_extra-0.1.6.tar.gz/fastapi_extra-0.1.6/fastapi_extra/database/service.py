__author__ = "ziyan.yin"
__date__ = "2025-01-12"

from typing import Any, Generic, Self, TypeVar

from fastapi_extra.database.model import SQLModel
from fastapi_extra.database.session import DefaultSession
from fastapi_extra.dependency import AbstractDependency

Model = TypeVar("Model", bound=SQLModel)


class ModelService(AbstractDependency, Generic[Model], annotated=False):
    __slot__ = ("session", )
    __model__: SQLModel
    
    @classmethod
    def __class_getitem__(cls, item: type[SQLModel]) -> Self:
        if not issubclass(item, SQLModel):
            raise TypeError(f"type[SQLModel] expected, got {item}")
        if not (table_arg := item.model_config.get("table", None)):
            raise AttributeError(f"True expected for argument {item.__name__}.model_config.table, got {table_arg}")
        cls.__model__ = item
        return cls

    def __init__(self, session: DefaultSession):
        self.session = session

    async def get(self, ident: int | str, **kwargs: Any) -> Model | None:
        return await self.session.get(self.__model__, ident, **kwargs)

    async def create(self, model: Model) -> Model:
        return await self.session.add(model)
    
    async def create_model(self, **kwargs: Any) -> Model:
        model = self.__model__.model_validate(kwargs)
        return self.create(model)
    
    async def delete(self, model: Model) -> Model:
        return await self.session.delete(model)
