from typing import Optional, Dict, Any, TypeVar, Type, get_args, get_origin

import requests

from InsCode.types.streaming import Stream
from src.InsCode.util import cast_to

_T = TypeVar("_T")
_TT = TypeVar("_TT")


def post(url, token, data=None,
         headers: [Optional[Dict]] = None,
         cast_to=Type[_T],
         stream_cls=Type[_TT],
         **kwargs) -> Any:
    if not headers:
        headers = {}
    if 'Authorization' not in headers:
        headers['Authorization'] = token
    headers['source'] = 'sdk'
    headers['sdk-version'] = '0.0.1'

    response = requests.post(url, json=data, headers=headers, **kwargs)
    return _process_response(response, cls=cast_to, stream_cls=stream_cls)


def _process_response(response, cls=Type[Any], stream_cls=Type[Any]) -> Any:
    if 'text/event-stream' in response.headers.get('content-type'):
        stream_cast = None
        origin = get_origin(stream_cls)
        if origin is not None and issubclass(origin, Stream):
            generic_args = get_args(stream_cls)
            stream_cast = generic_args[0] if generic_args else None
        return origin(cls=stream_cast, response=response)
    else:
        return cast_to(response.text, cls)
