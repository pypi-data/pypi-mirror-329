import json
from typing import Type, Any, Dict

from pydantic import TypeAdapter


def cast_to(data: str | Dict, cls: Type[Any]):
    _data = data
    if isinstance(data, str):
        _data = json.loads(data)
    instance = TypeAdapter(cls).validate_python(_data)
    return instance
