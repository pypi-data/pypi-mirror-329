__author__ = "ziyan.yin"
__date__ = "2025-01-05"


from abc import ABCMeta
from typing import Annotated, Any, Self

from fastapi.params import Depends


class AnnotationMetaClass(ABCMeta):
    
    def __new__(
        mcs,
        name: str,
        bases: tuple[type, ...],
        attrs: dict,
        annotated: bool = True
    ):
        new_cls = super().__new__(mcs, name, bases, attrs)
        if annotated:
            return Annotated[new_cls, Depends(new_cls)]
        return new_cls


class AbstractDependency(metaclass=AnnotationMetaClass, annotated=False):
    __slot__ = ()


class AbstractWidget(AbstractDependency, annotated=False):
    __slot__ = ()
    __instance__: Any = None
    
    def __new__(cls, *args, **kwargs) -> Self:
        if cls.__instance__ is None:
            cls.__instance__ = super().__new__(cls)
        return cls.__instance__
