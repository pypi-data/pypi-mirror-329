from __future__ import annotations

from inspect import isclass

import pydantic
from pydantic import BaseModel
from typing_extensions import TypeGuard


def is_pydantic_basemodel(type_: object) -> TypeGuard[type[BaseModel]]:
    """Check if a type is a Pydantic BaseModel."""
    return isclass(type_) and issubclass(type_, BaseModel)


def is_pydantic_basemodel_instance(v: object) -> TypeGuard[BaseModel]:
    return isinstance(v, BaseModel)


def is_pydantic_v1() -> bool:
    """
    True if pydantic is v1, else False
    """
    try:
        return int(pydantic.__version__.split(".")[0]) == 1
    except ImportError:
        return True
